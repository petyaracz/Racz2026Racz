# two axes over four adjective-only word lists (clinical anchor, pejorative
# colloquial anchor, neutral/positive colloquial anchor, target words). Every
# list being adjectives retires the noun-vs-adjective POS confound structurally
# instead of needing a separate control test to check for it (see README).
#
# 1. register axis: clinical-anchor centroid -> (pejorative + neutral/positive)
#    colloquial centroid. A word's projection says whether its current usage
#    pattern in this corpus reads closer to clinical nomenclature or to
#    everyday affect language -- a synchronic reading, not literally "drift
#    over time" (hunembed is a single static corpus snapshot, see README).
#
# 2. valence axis: pejorative-colloquial-anchor centroid -> neutral/positive-
#    colloquial-anchor centroid, orthogonalised against the register axis.
#    This turns "is a colloquial-leaning target word being used pejoratively
#    or just described neutrally/positively" into a second, independent
#    number instead of a discussion-section judgment call. "Pejorative" here
#    means "scores like generic negative-affect vocabulary" -- see the
#    limitations note in word_list.txt and README before treating this as a
#    validated slur/insult detector specifically.

import numpy as np
import pandas as pd

import pipeline

DAT_DIR = pipeline.DAT_DIR
AXIS_SCORES_TSV = f"{DAT_DIR}/axis_scores.tsv"

CLINICAL = "Clinical anchor"
PEJORATIVE = "Pejorative colloquial anchor"
NEUTRAL_POSITIVE = "Neutral/positive colloquial anchor"
TARGET = "Target words"

RNG_SEED = 1337
N_BOOTSTRAP = 2000


def load_embeddings(path=pipeline.WORD_LIST_EMBEDDINGS_TSV):
    df = pd.read_csv(path, sep="\t")
    dim_cols = [c for c in df.columns if c.startswith("dim_")]
    df = df[df[dim_cols[0]].notna()].reset_index(drop=True)
    return df, dim_cols


def cosine_distance(vectors, ref):
    # 1 - cosine similarity, vectorised over rows of `vectors` against one `ref` vector
    num = vectors @ ref
    denom = np.linalg.norm(vectors, axis=1) * np.linalg.norm(ref)
    return 1 - num / denom


def compute_axis(a_vecs, b_vecs):
    # axis runs from a's centroid to b's centroid; positive score = b-ward
    a_centroid = a_vecs.mean(axis=0)
    b_centroid = b_vecs.mean(axis=0)
    axis = b_centroid - a_centroid
    axis_unit = axis / np.linalg.norm(axis)
    midpoint = (a_centroid + b_centroid) / 2
    return a_centroid, b_centroid, axis_unit, midpoint


def orthogonalize(axis_unit, against_unit):
    # Gram-Schmidt: remove the component of axis_unit that overlaps with
    # against_unit, so the two axes measure independent things
    component = axis_unit - (axis_unit @ against_unit) * against_unit
    return component / np.linalg.norm(component)


def project(vectors, axis_unit, origin):
    return (vectors - origin) @ axis_unit


def bootstrap_scores(word_vecs, clinical_vecs, colloquial_vecs, positive_vecs, negative_vecs,
                      n_bootstrap=N_BOOTSTRAP, seed=RNG_SEED):
    # resample every anchor pool with replacement and recompute both axes each
    # time, to see how much a word's score depends on exactly which anchor
    # words were used. the valence axis is re-orthogonalised against the
    # resampled register axis on every draw, not just computed once, so its
    # uncertainty reflects both axes moving together.
    rng = np.random.default_rng(seed)
    n_words = word_vecs.shape[0]
    n_clin, n_coll = clinical_vecs.shape[0], colloquial_vecs.shape[0]
    n_pos, n_neg = positive_vecs.shape[0], negative_vecs.shape[0]
    register_draws = np.empty((n_bootstrap, n_words))
    valence_draws = np.empty((n_bootstrap, n_words))

    for b in range(n_bootstrap):
        clin_sample = clinical_vecs[rng.integers(0, n_clin, n_clin)]
        coll_sample = colloquial_vecs[rng.integers(0, n_coll, n_coll)]
        pos_sample = positive_vecs[rng.integers(0, n_pos, n_pos)]
        neg_sample = negative_vecs[rng.integers(0, n_neg, n_neg)]

        _, _, register_unit, midpoint = compute_axis(clin_sample, coll_sample)
        _, _, valence_raw_unit, _ = compute_axis(neg_sample, pos_sample)
        valence_unit = orthogonalize(valence_raw_unit, register_unit)

        register_draws[b] = project(word_vecs, register_unit, midpoint)
        valence_draws[b] = project(word_vecs, valence_unit, midpoint)

    return (register_draws.mean(axis=0), register_draws.std(axis=0),
            valence_draws.mean(axis=0), valence_draws.std(axis=0))


def build_axis_scores(out_path=AXIS_SCORES_TSV):
    df, dim_cols = load_embeddings()
    vectors = df[dim_cols].to_numpy()

    is_clinical = (df["word_type"] == CLINICAL).to_numpy()
    is_positive = (df["word_type"] == NEUTRAL_POSITIVE).to_numpy()
    is_negative = (df["word_type"] == PEJORATIVE).to_numpy()
    is_colloquial = is_positive | is_negative
    clinical_vecs = vectors[is_clinical]
    colloquial_vecs = vectors[is_colloquial]
    positive_vecs = vectors[is_positive]
    negative_vecs = vectors[is_negative]
    print(f"build_axis_scores: clinical anchor n={clinical_vecs.shape[0]}, "
          f"colloquial anchor n={colloquial_vecs.shape[0]} "
          f"(positive={positive_vecs.shape[0]}, negative={negative_vecs.shape[0]})")

    _, _, register_unit, midpoint = compute_axis(clinical_vecs, colloquial_vecs)
    _, _, valence_raw_unit, _ = compute_axis(negative_vecs, positive_vecs)
    valence_unit = orthogonalize(valence_raw_unit, register_unit)
    # same origin (the clinical/colloquial midpoint) for both axes, so the two
    # scores form one coherent 2D coordinate system rather than two separate ones
    origin = midpoint

    result = df[["word_type", "word_subtype", "word", "dual_category", "lemma_freq", "freq_bin"]].copy()
    result["dist_to_clinical"] = cosine_distance(vectors, clinical_vecs.mean(axis=0))
    result["dist_to_colloquial"] = cosine_distance(vectors, colloquial_vecs.mean(axis=0))
    result["axis_score"] = project(vectors, register_unit, origin)
    result["valence_score"] = project(vectors, valence_unit, origin)

    reg_mean, reg_std, val_mean, val_std = bootstrap_scores(
        vectors, clinical_vecs, colloquial_vecs, positive_vecs, negative_vecs
    )
    result["axis_score_bootstrap_mean"] = reg_mean
    result["axis_score_bootstrap_std"] = reg_std
    result["valence_score_bootstrap_mean"] = val_mean
    result["valence_score_bootstrap_std"] = val_std

    result = result.sort_values("axis_score").reset_index(drop=True)
    result.to_csv(out_path, sep="\t", index=False)
    print(f"build_axis_scores: wrote {out_path} ({len(result)} words)")

    # sanity check: anchors should land near their own pole by construction --
    # this doesn't validate the target words, just confirms the axes aren't broken
    clin_check = result.loc[result["word_type"] == CLINICAL, "axis_score"]
    coll_check = result.loc[result["word_type"].isin([PEJORATIVE, NEUTRAL_POSITIVE]), "axis_score"]
    pos_check = result.loc[result["word_type"] == NEUTRAL_POSITIVE, "valence_score"]
    neg_check = result.loc[result["word_type"] == PEJORATIVE, "valence_score"]
    print(f"build_axis_scores: clinical anchor axis_score range "
          f"[{clin_check.min():.3f}, {clin_check.max():.3f}]")
    print(f"build_axis_scores: colloquial anchor axis_score range "
          f"[{coll_check.min():.3f}, {coll_check.max():.3f}]")
    print(f"build_axis_scores: positive-core valence_score range "
          f"[{pos_check.min():.3f}, {pos_check.max():.3f}]")
    print(f"build_axis_scores: negative-core valence_score range "
          f"[{neg_check.min():.3f}, {neg_check.max():.3f}]")

    return result


if __name__ == "__main__":
    build_axis_scores()
