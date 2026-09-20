# builds one combined cosine-distance matrix over every word with an embedding
# (clinical anchor + colloquial anchor + target words together), then fits a 2D
# metric MDS on it so the whole word list can be looked at on one map.

import pandas as pd
from scipy.spatial.distance import pdist, squareform
from sklearn.manifold import MDS

import pipeline

DAT_DIR = pipeline.DAT_DIR
DISTANCE_MATRIX_TSV = f"{DAT_DIR}/distance_matrix.tsv"
MDS_COORDS_TSV = f"{DAT_DIR}/mds_coords.tsv"

DISTANCE_METRIC = "cosine"
MDS_RANDOM_STATE = 1337


def load_embeddings(path=pipeline.WORD_LIST_EMBEDDINGS_TSV):
    df = pd.read_csv(path, sep="\t")
    dim_cols = [c for c in df.columns if c.startswith("dim_")]
    # a word missing its embedding has nulls across every dim column; drop those,
    # since there's nothing to compute a distance from
    df = df[df[dim_cols[0]].notna()].reset_index(drop=True)
    return df, dim_cols


def build_label(row):
    # word alone would be unique here (no duplicate lemmas across word_type in
    # this list), but the compound label is kept for consistency and legibility
    return f"{row['word']} [{row['word_type']} / {row['word_subtype']}]"


def build_distance_matrix(out_path=DISTANCE_MATRIX_TSV):
    df, dim_cols = load_embeddings()
    vectors = df[dim_cols].to_numpy()
    dist_square = squareform(pdist(vectors, metric=DISTANCE_METRIC))
    labels = df.apply(build_label, axis=1).tolist()
    matrix = pd.DataFrame(dist_square, index=labels, columns=labels)
    matrix.to_csv(out_path, sep="\t")
    print(f"build_distance_matrix: {len(df)} words -> {out_path}")
    return matrix, df


def build_mds_coords(freq_path=pipeline.WORD_LIST_FREQ_TSV, out_path=MDS_COORDS_TSV):
    matrix, df = build_distance_matrix()
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=MDS_RANDOM_STATE,
              normalized_stress=False)
    coords = mds.fit_transform(matrix.to_numpy())

    coord_df = df[["word_type", "word_subtype", "word", "dual_category", "lemma_freq", "freq_bin"]].copy()
    coord_df["mds_x"] = coords[:, 0]
    coord_df["mds_y"] = coords[:, 1]

    # left join back onto the full frequency table so words with no embedding
    # still show up with null coordinates rather than silently disappearing
    freq_df = pd.read_csv(freq_path, sep="\t")
    id_cols = ["word_type", "word_subtype", "word", "dual_category", "lemma_freq", "freq_bin"]
    result = freq_df.merge(coord_df[id_cols + ["mds_x", "mds_y"]], on=id_cols, how="left")

    n_missing = result["mds_x"].isna().sum()
    print(f"build_mds_coords: rows: {len(result)}, without coordinates: {n_missing}")
    result.to_csv(out_path, sep="\t", index=False)
    print(f"build_mds_coords: wrote {out_path}")
    return result


if __name__ == "__main__":
    build_mds_coords()
