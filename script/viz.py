# five views of the analysis, each rendered in English and Hungarian (chart
# chrome only -- the plotted words are already Hungarian in the data). the
# underlying data model is four adjective-only word lists (clinical anchor,
# pejorative colloquial anchor, neutral/positive colloquial anchor, target
# words); mds_map/axis_projection/distance_scatter collapse the two colloquial
# anchors into one display bucket since their job is the clinical-vs-colloquial
# register story, while valence_map is specifically about the pejorative/
# neutral-positive split. every list being adjective-only retired the
# noun-vs-adjective POS-control test and chart that used to live here -- see
# README for why.
# 1. mds_map          - all embedded words on one 2D map (identity: word_type)
# 2. axis_projection  - ranked "bleaching axis" score per target word, with
#                       bootstrap error bars and the anchors' own ranges as bands
# 3. distance_scatter - the same idea as (2) but as the two raw vector distances
#                       (to the clinical centroid, to the colloquial centroid)
#                       plotted against each other, rather than compressed to one axis
# 4. valence_map      - register score x valence score (orthogonalised to
#                       register), separating "bled toward neutral colloquial
#                       use" from "bled toward pejorative use". manuscript-
#                       mentioned words (md/kezirat.md) get a bold, larger label.
# 5. valence_map_pub  - print-sized rebuild of (4) for the Festschrift: anchor
#                       groups as KDE density clouds instead of scattered
#                       points, only manuscript-mentioned target words labelled,
#                       drawn at its actual intended print size so the fonts
#                       survive being reproduced in a book. See README.
#
# words the source list flags as corpus-verified dual-category (see
# dat/word_list.txt's asterisk key) get a trailing "*" on their label in every
# chart, not just a footnote -- the point of flagging them was to keep the
# caveat visible, not to file it away.

import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
from scipy.stats import gaussian_kde

KEZIRAT_MD = "/Users/raczpetya/Documents/R/joska/md/kezirat.md"

import analysis
import distance as dist_mod

VIZ_DIR = "/Users/raczpetya/Documents/R/joska/viz"

# categorical slots 1/2/3 (blue/orange/aqua) from the dataviz skill's validated
# palette: the documented set that clears the all-pairs CVD/normal-vision floors
# for exactly 3 series (the cap for a scatter/chart with no color-repeat)
COLOR_CLINICAL = "#2a78d6"
COLOR_COLLOQUIAL = "#eb6834"
COLOR_TARGET = "#1baf7a"
INK = "#17181a"
INK_MUTED = "#6f6c64"
GRID = "#dedad0"

WORD_TYPE_COLORS = {
    "Clinical anchor": COLOR_CLINICAL,
    "Colloquial anchor": COLOR_COLLOQUIAL,
    "Target words": COLOR_TARGET,
}

# the pejorative/neutral-positive split is real (word_type in the data, and
# the whole point of the valence axis) but for charts whose job is the
# clinical-vs-colloquial register story rather than the valence split (mds_map,
# axis_projection), both collapse to one "Colloquial anchor" display bucket --
# otherwise every such chart needs a 4th competing hue past the categorical
# palette's validated 3-series cap for no analytical benefit in that chart
COLLOQUIAL_TYPES = ["Pejorative colloquial anchor", "Neutral/positive colloquial anchor"]


def add_display_type(df):
    df = df.copy()
    df["display_type"] = df["word_type"].where(~df["word_type"].isin(COLLOQUIAL_TYPES), "Colloquial anchor")
    return df


def label_text(row):
    return row["word"] + ("*" if row.get("dual_category") else "")


def load_manuscript_target_words(md_path=KEZIRAT_MD, axis_scores_path=None):
    # reads the *italicised* word examples straight out of the manuscript body
    # (before the reference list) and keeps only the ones that are actual
    # target words, so the "which words does the figure need to label" list
    # stays in sync with the manuscript automatically rather than being a
    # second, hand-maintained copy that can drift out of date
    axis_scores_path = axis_scores_path or analysis.AXIS_SCORES_TSV
    with open(md_path, encoding="utf-8") as f:
        body = f.read().split("## Hivatkozások")[0]
    mentioned = set(re.findall(r"\*([a-záéíóöőúüű]+)\*", body))
    targets = set(pd.read_csv(axis_scores_path, sep="\t")
                  .loc[lambda d: d["word_type"] == "Target words", "word"])
    return mentioned & targets


def kde_cloud(ax, x, y, color, pad=0.12, gridsize=140, levels=6, alpha=0.55, zorder=1,
              bw_boost=1.6):
    # replaces a scatter of individual anchor points with a smooth density
    # cloud -- the point of an anchor is "roughly where this whole category
    # sits," not the individual words, so this is a legitimate simplification
    # rather than just a space-saving trick, and it survives being shrunk to
    # print size far better than 15-49 tiny dots would. bw_boost widens
    # scipy's default (Scott's rule) bandwidth so one or two outlier words
    # don't read as a disconnected second island -- for a simplified summary
    # shape, one smooth blob per anchor is the point, not a literal density.
    xy = np.vstack([x, y])
    kde = gaussian_kde(xy, bw_method=lambda k: k.scotts_factor() * bw_boost)
    xmin, xmax = x.min() - pad, x.max() + pad
    ymin, ymax = y.min() - pad, y.max() + pad
    xx, yy = np.mgrid[xmin:xmax:complex(gridsize), ymin:ymax:complex(gridsize)]
    zz = kde(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
    zz = zz / zz.max()
    cmap = LinearSegmentedColormap.from_list("cloud", ["#ffffff", color])
    ax.contourf(xx, yy, zz, levels=np.linspace(0.12, 1.0, levels), cmap=cmap,
                alpha=alpha, antialiased=True, zorder=zorder)
    # a faint outline at a low density threshold gives the cloud a defined
    # edge instead of fading into nothing, which reads better in print
    ax.contour(xx, yy, zz, levels=[0.12], colors=[color], linewidths=0.8,
               alpha=0.5, zorder=zorder)


def declutter_2d(fig, ax, entries, fontsize, color, weight="normal", iterations=200,
                  push_px=2.5, leader_color=None):
    # entries: list of (x_data, y_data, text). a light 2D collision-resolver:
    # place every label at its point, then repeatedly nudge overlapping pairs
    # apart in screen space (converting back to data coords each step, since
    # the axes aren't square) until nothing overlaps or the iteration budget
    # runs out. good enough for a few dozen labels on one static figure --
    # not a general-purpose replacement for a real label-placement library.
    fig.canvas.draw()
    inv = ax.transData.inverted()
    orig = [(x, y) for x, y, _ in entries]
    texts = [ax.text(x, y, s, fontsize=fontsize, color=color, fontweight=weight,
                      ha="left", va="bottom", zorder=6) for x, y, s in entries]

    for _ in range(iterations):
        renderer = fig.canvas.get_renderer()
        boxes = [t.get_window_extent(renderer=renderer) for t in texts]
        moved = False
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                if not boxes[i].overlaps(boxes[j]):
                    continue
                moved = True
                cix, ciy = boxes[i].x0 + boxes[i].width / 2, boxes[i].y0 + boxes[i].height / 2
                cjx, cjy = boxes[j].x0 + boxes[j].width / 2, boxes[j].y0 + boxes[j].height / 2
                dx, dy = cjx - cix, cjy - ciy
                dist = (dx ** 2 + dy ** 2) ** 0.5 or 1.0
                ux, uy = dx / dist, dy / dist
                pi_disp = ax.transData.transform(texts[i].get_position())
                pj_disp = ax.transData.transform(texts[j].get_position())
                texts[i].set_position(inv.transform((pi_disp[0] - ux * push_px, pi_disp[1] - uy * push_px)))
                texts[j].set_position(inv.transform((pj_disp[0] + ux * push_px, pj_disp[1] + uy * push_px)))
        if not moved:
            break

    xlo, xhi = ax.get_xlim()
    leader_threshold = 0.015 * (xhi - xlo)
    leader_color = leader_color or color
    for (x0, y0), t in zip(orig, texts):
        lx, ly = t.get_position()
        if ((lx - x0) ** 2 + (ly - y0) ** 2) ** 0.5 > leader_threshold:
            ax.plot([x0, lx], [y0, ly], color=leader_color, linewidth=0.5, alpha=0.5, zorder=5)
    return texts

# chart chrome (titles/labels/legends) translated per language; the plotted word
# tokens themselves are already Hungarian in the data and don't need translation,
# and word_subtype/word_type values used as lookup keys stay in English (the tsvs'
# language) regardless of which language a chart is rendered in
TEXT = {
    "en": {
        "word_type_label": {
            "Clinical anchor": "Clinical anchor",
            "Colloquial anchor": "Colloquial anchor",
            "Target words": "Target words",
        },
        "family_label": {
            "Depression": "Depression",
            "Trauma": "Trauma",
            "Panic and phobia": "Panic and phobia",
            "Hysteria, mania, paranoia": "Hysteria, mania, paranoia",
            "Neurosis and compulsion": "Neurosis and compulsion",
            "Neurodevelopmental": "Neurodevelopmental",
            "Psychotic spectrum": "Psychotic spectrum",
            "Addiction and dependency": "Addiction and dependency",
            "Mood disorder": "Mood disorder",
            "Contemporary loanwords": "Contemporary loanwords",
            "Insanity and madness": "Insanity and madness",
        },
        "mds_title": "Clinical anchor, colloquial anchor, and target words on one MDS map",
        "axis_title": "How far has each target word drifted toward everyday use?",
        "axis_xlabel": "<- clinical pole                          axis score                          colloquial pole ->",
        "axis_legend_clinical": "clinical anchor range",
        "axis_legend_colloquial": "colloquial anchor range",
        "dist_title": "Target words: closer to the clinic, or closer to everyday speech?",
        "dist_xlabel": "cosine distance to clinical-anchor centroid",
        "dist_ylabel": "cosine distance to colloquial-anchor centroid",
        "dist_equidistant": "equidistant",
        "dist_below": "below the line = reads more colloquial",
        "dist_above": "above the line = reads more clinical",
        "valence_title": "Two ways to leave the clinic: described neutrally, or used as an insult",
        "valence_title_pub": "Clinical to colloquial, neutral to pejorative",
        "valence_xlabel_pub": "clinical <-> colloquial",
        "valence_ylabel_pub": "pejorative <-> neutral/positive",
        "valence_xlabel": "register axis score  (<- clinical      colloquial ->)",
        "valence_ylabel": "valence axis score, orthogonalised to register  (<- negative      positive ->)",
        "valence_legend_positive": "colloquial anchor, positive",
        "valence_legend_negative": "colloquial anchor, negative",
        "valence_legend_clinical": "clinical anchor",
        "valence_legend_target": "target word",
        "valence_quadrant_pejorative": "colloquial + negative\n(pejoration-leaning)",
        "valence_quadrant_bleached": "colloquial + neutral/positive\n(neutral bleaching)",
    },
    "hu": {
        "word_type_label": {
            "Clinical anchor": "Klinikai horgony",
            "Colloquial anchor": "Köznyelvi horgony",
            "Target words": "Célszavak",
        },
        "family_label": {
            "Depression": "Depresszió",
            "Trauma": "Trauma",
            "Panic and phobia": "Pánik és fóbia",
            "Hysteria, mania, paranoia": "Hisztéria, mánia, paranoia",
            "Neurosis and compulsion": "Neurózis és kényszeresség",
            "Neurodevelopmental": "Neurofejlődési",
            "Psychotic spectrum": "Pszichotikus spektrum",
            "Addiction and dependency": "Addikció és függőség",
            "Mood disorder": "Hangulatzavar",
            "Contemporary loanwords": "Kortárs jövevényszavak",
            "Insanity and madness": "Őrület és elmezavar",
        },
        "mds_title": "Klinikai horgony, köznyelvi horgony és célszavak egy MDS-térképen",
        "axis_title": "Mennyire sodródott el az egyes célszavak jelentése a köznyelv felé?",
        "axis_xlabel": "<- klinikai pólus                          tengelyérték                          köznyelvi pólus ->",
        "axis_legend_clinical": "klinikai horgony tartománya",
        "axis_legend_colloquial": "köznyelvi horgony tartománya",
        "dist_title": "Célszavak: közelebb a klinikumhoz, vagy közelebb a köznyelvhez?",
        "dist_xlabel": "koszinusztávolság a klinikai horgony centroidjától",
        "dist_ylabel": "koszinusztávolság a köznyelvi horgony centroidjától",
        "dist_equidistant": "egyenlő távolság",
        "dist_below": "a vonal alatt = köznyelvibb hatású",
        "dist_above": "a vonal fölött = klinikaibb hatású",
        "valence_title": "Kétféleképp lehet elhagyni a klinikumot: semlegesen leírva, vagy sértésként használva",
        "valence_title_pub": "Klinikaitól a köznyelvig, semlegestől a pejoratívig",
        "valence_xlabel_pub": "klinikai <-> köznyelvi",
        "valence_ylabel_pub": "pejoratív <-> semleges/pozitív",
        "valence_xlabel": "tengelyérték  (<- klinikai      köznyelvi ->)",
        "valence_ylabel": "valenciatengely-érték, a regiszterre ortogonalizálva  (<- negatív      pozitív ->)",
        "valence_legend_positive": "köznyelvi horgony, pozitív",
        "valence_legend_negative": "köznyelvi horgony, negatív",
        "valence_legend_clinical": "klinikai horgony",
        "valence_legend_target": "célszó",
        "valence_quadrant_pejorative": "köznyelvi + negatív\n(inkább pejoratív)",
        "valence_quadrant_bleached": "köznyelvi + semleges/pozitív\n(semleges jelentéstágulás)",
    },
}

# custom diverging map for axis_score: reuses the same two hues as the scatter's
# categorical identity colors (blue=clinical, orange=colloquial) rather than the
# skill's default blue/red pair, so "which pole" reads the same way in every chart
DIVERGING_CMAP = LinearSegmentedColormap.from_list(
    "clinical_colloquial", [COLOR_CLINICAL, "#c7c2b4", COLOR_COLLOQUIAL]
)


def diverging_color(score, vmax=0.55):
    t = np.clip((score / vmax + 1) / 2, 0, 1)
    return DIVERGING_CMAP(t)


def plot_mds_map(out_path=f"{VIZ_DIR}/mds_map.png", lang="en"):
    text = TEXT[lang]
    df = add_display_type(pd.read_csv(dist_mod.MDS_COORDS_TSV, sep="\t").dropna(subset=["mds_x", "mds_y"]))

    fig, ax = plt.subplots(figsize=(15, 13), facecolor="#fcfcfb")
    ax.set_facecolor("#fcfcfb")

    for word_type, color in WORD_TYPE_COLORS.items():
        pts = df[df["display_type"] == word_type]
        ax.scatter(pts["mds_x"], pts["mds_y"], s=48, color=color, alpha=0.85,
                   linewidths=0.6, edgecolors="white", label=text["word_type_label"][word_type], zorder=3)

    for _, r in df.iterrows():
        ax.annotate(label_text(r), (r["mds_x"], r["mds_y"]), fontsize=7.2, color=INK,
                    xytext=(4, 3), textcoords="offset points", zorder=4)

    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.set_title(text["mds_title"], fontsize=14, color=INK, pad=14)
    ax.legend(loc="lower right", frameon=False, fontsize=11)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"plot_mds_map[{lang}]: wrote {out_path}")


def plot_axis_projection(out_path=f"{VIZ_DIR}/axis_projection.png", lang="en"):
    text = TEXT[lang]
    df = pd.read_csv(analysis.AXIS_SCORES_TSV, sep="\t")
    targets = df[df["word_type"] == "Target words"].copy()
    clinical = df[df["word_type"] == "Clinical anchor"]
    colloquial = df[df["word_type"].isin(COLLOQUIAL_TYPES)]

    # keep the authored family order, but rank words within each family by score
    family_order = ["Depression", "Trauma", "Panic and phobia", "Hysteria, mania, paranoia",
                     "Neurosis and compulsion", "Neurodevelopmental", "Psychotic spectrum",
                     "Addiction and dependency", "Mood disorder", "Contemporary loanwords",
                     "Insanity and madness"]
    targets["word_subtype"] = pd.Categorical(targets["word_subtype"], categories=family_order, ordered=True)
    targets = targets.sort_values(["word_subtype", "axis_score"]).reset_index(drop=True)

    # a blank spacer row between families turns the bar list into small multiples
    rows = []
    for family in family_order:
        block = targets[targets["word_subtype"] == family]
        if block.empty:
            continue
        rows.append({"word": text["family_label"][family].upper(), "axis_score": np.nan, "is_header": True})
        for _, r in block.iterrows():
            rows.append({"word": label_text(r), "axis_score": r["axis_score"],
                         "axis_score_bootstrap_std": r["axis_score_bootstrap_std"], "is_header": False})
    plot_df = pd.DataFrame(rows)
    y = np.arange(len(plot_df))[::-1]

    fig, ax = plt.subplots(figsize=(9, 0.32 * len(plot_df) + 1.5), facecolor="#fcfcfb")
    ax.set_facecolor("#fcfcfb")

    # anchor ranges as reference bands, not individual bars -- there are 66 anchor
    # words and showing them all would swamp the 36 target words that are the point
    ax.axvspan(clinical["axis_score"].min(), clinical["axis_score"].max(),
               color=COLOR_CLINICAL, alpha=0.10, zorder=0)
    ax.axvspan(colloquial["axis_score"].min(), colloquial["axis_score"].max(),
               color=COLOR_COLLOQUIAL, alpha=0.10, zorder=0)
    ax.axvline(0, color=INK_MUTED, linewidth=1, linestyle=":", zorder=1)

    body = plot_df[~plot_df["is_header"]]
    body_y = y[~plot_df["is_header"].to_numpy()]
    colors = [diverging_color(s) for s in body["axis_score"]]
    ax.barh(body_y, body["axis_score"], height=0.62, color=colors, zorder=3,
            xerr=body["axis_score_bootstrap_std"], error_kw=dict(ecolor=INK_MUTED, elinewidth=0.8, capsize=2))

    for yi, label, is_header in zip(y, plot_df["word"], plot_df["is_header"]):
        if is_header:
            ax.text(-0.62, yi, label, fontsize=8, color=INK_MUTED, fontweight="bold",
                    va="center", ha="left")
        else:
            ax.text(0, yi + 0.34, label, fontsize=8.5, color=INK, va="bottom", ha="center")

    ax.set_xlim(-0.62, 0.58)
    ax.set_yticks([])
    ax.set_ylim(-1, len(plot_df))
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.set_xlabel(text["axis_xlabel"], fontsize=9.5, color=INK_MUTED)
    ax.set_title(text["axis_title"], fontsize=13.5, color=INK, pad=12)

    legend_handles = [
        Patch(facecolor=COLOR_CLINICAL, alpha=0.25, label=text["axis_legend_clinical"]),
        Patch(facecolor=COLOR_COLLOQUIAL, alpha=0.25, label=text["axis_legend_colloquial"]),
    ]
    ax.legend(handles=legend_handles, loc="upper center", bbox_to_anchor=(0.5, 1.0),
              ncol=2, frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"plot_axis_projection[{lang}]: wrote {out_path}")


def plot_distance_scatter(out_path=f"{VIZ_DIR}/distance_scatter.png", lang="en"):
    text = TEXT[lang]
    df = pd.read_csv(analysis.AXIS_SCORES_TSV, sep="\t")
    targets = df[df["word_type"] == "Target words"].copy()

    fig, ax = plt.subplots(figsize=(10, 10), facecolor="#fcfcfb")
    ax.set_facecolor("#fcfcfb")

    lo = min(targets["dist_to_clinical"].min(), targets["dist_to_colloquial"].min()) - 0.03
    hi = max(targets["dist_to_clinical"].max(), targets["dist_to_colloquial"].max()) + 0.03
    ax.plot([lo, hi], [lo, hi], color=INK_MUTED, linewidth=1, linestyle=":", zorder=1)
    ax.text(hi - 0.005, hi - 0.02, text["dist_equidistant"], fontsize=8, color=INK_MUTED,
            ha="right", va="top", rotation=45)

    colors = [diverging_color(s) for s in targets["axis_score"]]
    ax.scatter(targets["dist_to_clinical"], targets["dist_to_colloquial"], s=60,
               color=colors, edgecolors="white", linewidths=0.6, zorder=3)
    for _, r in targets.iterrows():
        ax.annotate(label_text(r), (r["dist_to_clinical"], r["dist_to_colloquial"]),
                    fontsize=7.5, color=INK, xytext=(4, 3), textcoords="offset points", zorder=4)

    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_xlabel(text["dist_xlabel"], fontsize=10, color=INK_MUTED)
    ax.set_ylabel(text["dist_ylabel"], fontsize=10, color=INK_MUTED)
    ax.set_title(text["dist_title"], fontsize=13.5, color=INK, pad=12)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.annotate(text["dist_below"], xy=(0.02, 0.02), xycoords="axes fraction",
                fontsize=8.5, color=COLOR_COLLOQUIAL, ha="left", va="bottom")
    ax.annotate(text["dist_above"], xy=(0.98, 0.98), xycoords="axes fraction",
                fontsize=8.5, color=COLOR_CLINICAL, ha="right", va="top")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"plot_distance_scatter[{lang}]: wrote {out_path}")


def plot_valence_map(out_path=f"{VIZ_DIR}/valence_map.png", lang="en"):
    text = TEXT[lang]
    df = pd.read_csv(analysis.AXIS_SCORES_TSV, sep="\t")
    targets = df[df["word_type"] == "Target words"].copy()
    positive = df[df["word_type"] == "Neutral/positive colloquial anchor"]
    negative = df[df["word_type"] == "Pejorative colloquial anchor"]
    clinical = df[df["word_type"] == "Clinical anchor"]

    fig, ax = plt.subplots(figsize=(11, 10), facecolor="#fcfcfb")
    ax.set_facecolor("#fcfcfb")

    # anchors plotted small and pale: calibration context, not the point of the chart
    ax.scatter(clinical["axis_score"], clinical["valence_score"], s=22, color=COLOR_CLINICAL,
               alpha=0.35, linewidths=0, zorder=2, label=text["valence_legend_clinical"])
    ax.scatter(positive["axis_score"], positive["valence_score"], s=22, color="#eda100",
               alpha=0.4, linewidths=0, zorder=2, label=text["valence_legend_positive"])
    ax.scatter(negative["axis_score"], negative["valence_score"], s=22, color="#4a3aa7",
               alpha=0.4, linewidths=0, zorder=2, label=text["valence_legend_negative"])

    ax.axhline(0, color=INK_MUTED, linewidth=1, linestyle=":", zorder=1)
    ax.axvline(0, color=INK_MUTED, linewidth=1, linestyle=":", zorder=1)

    ax.scatter(targets["axis_score"], targets["valence_score"], s=64, color=COLOR_TARGET,
               alpha=0.9, edgecolors="white", linewidths=0.7, zorder=4,
               label=text["valence_legend_target"])
    # words the manuscript actually discusses get a bolder, larger label, so
    # this detailed figure can be cross-referenced against the running text
    manuscript_words = load_manuscript_target_words()
    for _, r in targets.iterrows():
        highlighted = r["word"] in manuscript_words
        ax.annotate(label_text(r), (r["axis_score"], r["valence_score"]),
                    fontsize=9.5 if highlighted else 7.5,
                    fontweight="bold" if highlighted else "normal",
                    color=INK, xytext=(4, 3), textcoords="offset points", zorder=5)

    xlo, xhi = ax.get_xlim(); ylo, yhi = ax.get_ylim()
    ax.text(xhi - 0.01, ylo + 0.01, text["valence_quadrant_pejorative"], fontsize=9,
            color="#4a3aa7", ha="right", va="bottom", style="italic")
    ax.text(xhi - 0.01, yhi - 0.01, text["valence_quadrant_bleached"], fontsize=9,
            color="#b8860b", ha="right", va="top", style="italic")

    ax.set_xlabel(text["valence_xlabel"], fontsize=10, color=INK_MUTED)
    ax.set_ylabel(text["valence_ylabel"], fontsize=10, color=INK_MUTED)
    ax.set_title(text["valence_title"], fontsize=13.5, color=INK, pad=12)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"plot_valence_map[{lang}]: wrote {out_path}")


def plot_valence_map_pub(out_path=f"{VIZ_DIR}/valence_map_hu_pub.png", lang="hu"):
    # print version for the Festschrift. Designed AT its intended final printed
    # size (roughly a 13cm/5.1in-wide single-column figure) rather than at a
    # big on-screen canvas that only looks fine before it gets shrunk -- font
    # size is set in points, which are physical units relative to figsize in
    # inches, so "big figure + big font" does not survive being scaled down to
    # print size the way "print-size figure + big-for-that-size font" does.
    # Two simplifications relative to plot_valence_map: the three anchor
    # groups become density clouds instead of 15-49 individual dots, and only
    # the words the manuscript (kezirat.md) actually names get a label.
    text = TEXT[lang]
    df = pd.read_csv(analysis.AXIS_SCORES_TSV, sep="\t")
    targets = df[df["word_type"] == "Target words"].copy()
    positive = df[df["word_type"] == "Neutral/positive colloquial anchor"]
    negative = df[df["word_type"] == "Pejorative colloquial anchor"]
    clinical = df[df["word_type"] == "Clinical anchor"]
    manuscript_words = load_manuscript_target_words()

    fig, ax = plt.subplots(figsize=(6.3, 5.8), facecolor="#fcfcfb")
    ax.set_facecolor("#fcfcfb")

    kde_cloud(ax, clinical["axis_score"].to_numpy(), clinical["valence_score"].to_numpy(), COLOR_CLINICAL)
    kde_cloud(ax, positive["axis_score"].to_numpy(), positive["valence_score"].to_numpy(), "#eda100")
    kde_cloud(ax, negative["axis_score"].to_numpy(), negative["valence_score"].to_numpy(), "#4a3aa7")

    ax.axhline(0, color=INK_MUTED, linewidth=0.7, linestyle=":", zorder=2)
    ax.axvline(0, color=INK_MUTED, linewidth=0.7, linestyle=":", zorder=2)

    # every target word gets a small dot, so the overall spread stays visible
    # even for the ~5 words that don't get a label
    ax.scatter(targets["axis_score"], targets["valence_score"], s=16, color=COLOR_TARGET,
               alpha=0.85, edgecolors="white", linewidths=0.4, zorder=4)

    highlighted = targets[targets["word"].isin(manuscript_words)]
    entries = [(r["axis_score"], r["valence_score"], label_text(r)) for _, r in highlighted.iterrows()]
    declutter_2d(fig, ax, entries, fontsize=8.2, color=INK, weight="bold",
                 leader_color=INK_MUTED, push_px=3.2, iterations=300)

    ax.set_xlabel(text["valence_xlabel_pub"], fontsize=9.5, color=INK_MUTED)
    ax.set_ylabel(text["valence_ylabel_pub"], fontsize=9.5, color=INK_MUTED)
    ax.set_title(text["valence_title_pub"], fontsize=12.5, color=INK, pad=9)
    ax.tick_params(labelsize=8.5)
    for spine in ax.spines.values():
        spine.set_color(GRID)

    legend_handles = [
        Patch(facecolor=COLOR_CLINICAL, alpha=0.6, label=text["valence_legend_clinical"]),
        Patch(facecolor="#eda100", alpha=0.6, label=text["valence_legend_positive"]),
        Patch(facecolor="#4a3aa7", alpha=0.6, label=text["valence_legend_negative"]),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=COLOR_TARGET,
                   markeredgecolor="white", markersize=6, label=text["valence_legend_target"]),
    ]
    ax.legend(handles=legend_handles, loc="upper left", frameon=False, fontsize=7.8,
              handletextpad=0.5, borderaxespad=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=600, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"plot_valence_map_pub[{lang}]: wrote {out_path} "
          f"({len(entries)} of {len(targets)} target words labelled)")


if __name__ == "__main__":
    for lang, suffix in [("en", ""), ("hu", "_hu")]:
        plot_mds_map(out_path=f"{VIZ_DIR}/mds_map{suffix}.png", lang=lang)
        plot_axis_projection(out_path=f"{VIZ_DIR}/axis_projection{suffix}.png", lang=lang)
        plot_distance_scatter(out_path=f"{VIZ_DIR}/distance_scatter{suffix}.png", lang=lang)
        plot_valence_map(out_path=f"{VIZ_DIR}/valence_map{suffix}.png", lang=lang)
    plot_valence_map_pub()
