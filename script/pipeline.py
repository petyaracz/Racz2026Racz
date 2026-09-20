# pipeline: dat/word_list.txt -> word_list.tsv -> word_list_freq.tsv -> word_list_embeddings.tsv.gz
# step 1 reshapes the anchor/target word lists into a tidy word_type/word_subtype/word tsv
# step 2 joins that tsv against the webcorpus frequency parquet
# step 3 attaches a 600-d word2vec vector to each word

import gzip
import os
import subprocess

import duckdb
import pandas as pd

DAT_DIR = "/Users/raczpetya/Documents/R/joska/dat"
WORD_LIST_TXT = f"{DAT_DIR}/word_list.txt"
WORD_LIST_TSV = f"{DAT_DIR}/word_list.tsv"
FREQ_PARQUET = "/Users/raczpetya/Github/Webcorpus2FrequencyList/frequencies.parquet"
WORD_LIST_FREQ_TSV = f"{DAT_DIR}/word_list_freq.tsv"

EMBEDDINGS_TGZ = "/Users/raczpetya/Documents/corpora/hunembed/hunembed0.0.tgz"
EMBEDDINGS_MEMBER = "word2vec-mnsz2-webcorp_600_w10_n5_i1_m10.w2v"
EMBEDDINGS_MATCHED_RAW = f"{DAT_DIR}/matched_embeddings_raw.txt"
WORD_LIST_EMBEDDINGS_TSV = f"{DAT_DIR}/word_list_embeddings.tsv.gz"

# (word_type, [(subtype_clean, line_number_of_words_in_word_list_txt), ...])
# hardcoded because word_list.txt mixes header lines, word lists, and free-text notes
# ("Excluded on purpose", "Flag for later") that aren't part of the word_type/subtype/word
# structure -- those notes record why words were left out, not more words to add
SECTIONS = [
    ("Clinical anchor", [
        ("Course, prognosis, mechanism", 6),
        ("Diagnostic and procedural descriptors", 9),
    ]),
    ("Pejorative colloquial anchor", [
        ("Core", 16),
    ]),
    ("Neutral/positive colloquial anchor", [
        ("Core", 21),
    ]),
    ("Target words", [
        ("Depression", 28),
        ("Trauma", 31),
        ("Panic and phobia", 34),
        ("Hysteria, mania, paranoia", 37),
        ("Neurosis and compulsion", 40),
        ("Neurodevelopmental", 43),
        ("Psychotic spectrum", 46),
        ("Addiction and dependency", 49),
        ("Mood disorder", 52),
        ("Contemporary loanwords", 55),
        ("Insanity and madness", 58),
    ]),
]


def build_word_list_tsv(src_path=WORD_LIST_TXT, out_path=WORD_LIST_TSV, sections=SECTIONS):
    with open(src_path, encoding="utf-8") as f:
        lines = f.readlines()

    def line(n):
        # 1-indexed line lookup, stripped of trailing newline
        return lines[n - 1].rstrip("\n")

    rows = []
    for word_type, subtypes in sections:
        for subtype, ln in subtypes:
            words_raw = line(ln).split(",")
            seen = set()
            for w in words_raw:
                w = w.strip()
                if not w or w in seen:
                    continue
                seen.add(w)
                # a trailing "*" in the source marks a word the corpus shows as
                # genuinely dual-category (noun/adjective split under ~2.5:1) --
                # stripped here and carried as its own column instead, so it
                # survives the frequency/embedding joins and reaches the charts
                dual_category = w.endswith("*")
                if dual_category:
                    w = w[:-1]
                rows.append((word_type, subtype, w, dual_category))

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("word_type\tword_subtype\tword\tdual_category\n")
        for word_type, subtype, w, dual_category in rows:
            f.write(f"{word_type}\t{subtype}\t{w}\t{dual_category}\n")

    print(f"build_word_list_tsv: wrote {len(rows)} rows to {out_path}")
    return out_path


def build_word_list_freq_tsv(word_list_path=WORD_LIST_TSV, parquet_path=FREQ_PARQUET, out_path=WORD_LIST_FREQ_TSV):
    con = duckdb.connect()

    query = f"""
    with words as (
        select * from read_csv('{word_list_path}', delim='\t', header=true)
    ),
    -- restrict the 37M-row parquet to lemmas we actually need before deduping
    freq_raw as (
        select distinct lemma, lemma_freq, llfpm10
        from read_parquet('{parquet_path}')
        where lemma in (select distinct word from words)
    ),
    -- a lemma can carry several (lemma_freq, llfpm10) pairs (homonyms across xpostag);
    -- keep the highest-frequency pair per lemma
    freq_best as (
        select lemma, lemma_freq, llfpm10,
               row_number() over (partition by lemma order by lemma_freq desc) as rn
        from freq_raw
    ),
    freq as (
        select lemma, lemma_freq, llfpm10 from freq_best where rn = 1
    ),
    joined as (
        select w.word_type, w.word_subtype, w.word, w.dual_category, f.lemma_freq, f.llfpm10
        from words w
        left join freq f on f.lemma = w.word
    ),
    -- ntile must only see rows with a known frequency, otherwise the unmatched
    -- rows would count as partition members and shift everyone else's bin edges
    matched as (
        select word_type, word_subtype, word, dual_category, lemma_freq, llfpm10,
               ntile(10) over (partition by word_type order by lemma_freq) as freq_bin
        from joined
        where lemma_freq is not null
    ),
    unmatched as (
        select word_type, word_subtype, word, dual_category, lemma_freq, llfpm10, null::bigint as freq_bin
        from joined
        where lemma_freq is null
    )
    select * from matched
    union all
    select * from unmatched
    order by word_type, word_subtype, word
    """

    result = con.execute(query).df()

    n_missing = result["lemma_freq"].isna().sum()
    print(f"build_word_list_freq_tsv: rows: {len(result)}, unmatched (no corpus frequency): {n_missing}")
    if n_missing:
        missing_words = result.loc[result["lemma_freq"].isna(), "word"].tolist()
        print("unmatched words:", ", ".join(missing_words))

    result.to_csv(out_path, sep="\t", index=False)
    print(f"build_word_list_freq_tsv: wrote {out_path}")
    return out_path


def _extract_raw_embeddings(target_variants, tgz_path, member, out_path):
    # streams the ~3.7GB tgz through tar+awk rather than loading the 1.9M-word,
    # 600-dim w2v file into memory; only lines whose first token is a target word
    # (or its space->underscore variant) are kept. takes several minutes.
    variants_path = out_path + ".variants"
    with open(variants_path, "w", encoding="utf-8") as f:
        for v in sorted(target_variants):
            f.write(v + "\n")

    awk_prog = (
        "BEGIN{while((getline w < wf)>0) target[w]=1} "
        "NR==1{next} "
        "($1 in target){print}"
    )
    with open(out_path, "w", encoding="utf-8") as out_f:
        tar_proc = subprocess.Popen(
            ["tar", "-xzOf", tgz_path, member], stdout=subprocess.PIPE
        )
        subprocess.run(
            ["awk", "-v", f"wf={variants_path}", awk_prog],
            stdin=tar_proc.stdout,
            stdout=out_f,
            check=True,
        )
        tar_proc.stdout.close()
        tar_proc.wait()

    os.remove(variants_path)


def build_word_list_embeddings_tsv(
    word_list_freq_path=WORD_LIST_FREQ_TSV,
    tgz_path=EMBEDDINGS_TGZ,
    member=EMBEDDINGS_MEMBER,
    raw_path=EMBEDDINGS_MATCHED_RAW,
    out_path=WORD_LIST_EMBEDDINGS_TSV,
    force_extract=False,
):
    freq_df = pd.read_csv(word_list_freq_path, sep="\t")
    words = sorted(freq_df["word"].unique())

    # word2vec phrase tokens use underscores, so a multi-word entry (none currently
    # in this word list, but kept for robustness) is looked up both ways
    variant_to_word = {}
    for w in words:
        variant_to_word[w] = w
        if " " in w:
            variant_to_word[w.replace(" ", "_")] = w

    if force_extract or not os.path.exists(raw_path):
        _extract_raw_embeddings(variant_to_word.keys(), tgz_path, member, raw_path)

    # parse the raw "token v1 v2 ... v600" lines, mapping variants back to the
    # original word and keeping only the first hit per word (space form preferred)
    embeddings = {}
    with open(raw_path, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split(" ")
            token, values = parts[0], parts[1:]
            word = variant_to_word.get(token)
            if word is None:
                continue
            if word in embeddings and " " not in token:
                continue  # space-form match already stored, don't overwrite with underscore hit
            embeddings[word] = [float(v) for v in values]

    dim = len(next(iter(embeddings.values())))
    dim_cols = [f"dim_{i}" for i in range(1, dim + 1)]
    emb_df = pd.DataFrame.from_dict(embeddings, orient="index", columns=dim_cols)
    emb_df.index.name = "word"
    emb_df = emb_df.reset_index()

    result = freq_df.merge(emb_df, on="word", how="left")

    n_missing = result[dim_cols[0]].isna().sum()
    print(f"build_word_list_embeddings_tsv: rows: {len(result)}, unmatched (no embedding): {n_missing}")
    if n_missing:
        missing_words = sorted(result.loc[result[dim_cols[0]].isna(), "word"].unique())
        print("unmatched words:", ", ".join(missing_words))

    with gzip.open(out_path, "wt", encoding="utf-8") as f:
        result.to_csv(f, sep="\t", index=False)
    print(f"build_word_list_embeddings_tsv: wrote {out_path}")
    return out_path


if __name__ == "__main__":
    build_word_list_tsv()
    build_word_list_freq_tsv()
    build_word_list_embeddings_tsv()
