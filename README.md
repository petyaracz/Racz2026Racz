# joska

Does a diagnostic term like "depresszió" still read as clinical language, or has
it bled into everyday speech the way "depressing" has in English ("the weather
today is super depressive")? This project tests that with Hungarian word
embeddings: anchor a "clinical" pole and a "colloquial" pole in embedding space,
then see where a curated set of diagnostic terms falls between them.

Layout:

- `dat/` -- the hand-curated word list and every generated data file.
- `script/` -- the pipeline, run in order: `pipeline.py` -> `distance.py` -> `analysis.py` -> `viz.py`.
- `viz/` -- the output charts.

This is the fourth revision of the word list, and the second to change the
*shape* of the design rather than just the words in it. The first iteration
tried substance-use vocabulary against colloquial-sentiment and clinical word
lists; the categories were too neatly disjoint to say anything about
individual words drifting between registers. The second iteration fixed that
by testing the same lemma family (`depresszió`/`depressziós`/`depresszív`)
against clinical and colloquial anchors, but the clinical anchor mixed nouns
and adjectives while the colloquial anchor was 100% adjectives -- a confound a
control test confirmed was real. The third iteration retired that confound by
making every word list adjectives only. **This revision restructures the
design again: the colloquial anchor's internal positive/negative split (used
only as a secondary "valence axis" correction in the third iteration) is
promoted to two full top-level anchors.** The analysis is now built around
**four word lists** -- clinical anchor, pejorative colloquial anchor,
neutral/positive colloquial anchor, and target words -- with every target
word read directly as "closer to clinical, closer to pejorative-colloquial,
or closer to neutral/positive-colloquial," rather than as a register score
plus a bolted-on valence correction. The underlying words and math are
unchanged from the third iteration; see "Why the anchors were restructured
into four lists" below for what actually changed and why.

**Read the Limitations section below before citing anything from this
project** -- in particular, "pejorative colloquial anchor" is a name applied
to a general-negative-sentiment word list as a matter of convenience, not a
validated instrument for detecting slur-style pejoration. That gap is
consequential for this project's most interesting open question (whether
`autista`/`szkizofrén`'s colloquial use is genuinely pejorative), and is
spelled out in full below rather than left as an implicit caveat.

## The method, and its central limitation

hunembed is **one static embedding**, trained once on a fixed corpus (MNSZ2 +
webcorpus). A word's vector is already the blend of every context it appeared
in. That means this analysis **cannot show drift over time** -- there is no
earlier snapshot to compare against, so "this word used to be clinical and has
since drifted" is not a claim this data can support.

What it can support: a **synchronic** reading. Define a clinical pole and a
colloquial pole from words we're confident belong to each register, then ask
where a target word's current usage pattern sits between them. That's the
concept-creep / semantic-bleaching framing (cf. Haslam 2016 on "concept creep"
in trauma/abuse/disorder vocabulary), and the metric is the semantic-axis
projection method (cf. Kozlowski et al. 2019): project each word onto the
vector running from the clinical-anchor centroid to the colloquial-anchor
centroid.

Two corpus caveats worth keeping in mind when reading the charts:

- **Register skew.** MNSZ2 + webcorpus is general web text, not a balanced
  clinical/informal split, so a word's raw distance from the clinical pole
  isn't zero-corrected on its own -- it could look "colloquial" simply because
  clinical text is rare in the corpus overall. The anchor-pole framing (relative
  position between two poles drawn from the *same* corpus) is what makes the
  comparison meaningful; the raw distances alone would not be.
- **Corpus vintage.** hunembed's training-data cutoff relative to recent
  pop-psychology loanwords is unknown. Three exotic clinical adjectives
  (`aszimptomatikus`, `komorbid`, `prodromális`) had no embedding at all -- a
  miss here just means "too rare for this corpus," not evidence about meaning.

## The word lists (`dat/word_list.txt`)

Four word lists, three of them anchors:

- **Clinical anchor** (18 words, all adjectives) -- technical/Latinate
  diagnostic adjectives with no documented lay double meaning:
  `terápiarezisztens`, `dekompenzált`, `gyógyszerrezisztens`, `iatrogén`,
  `benignus`, `malignus`, `patológiás`, `szisztémás`, etc. Exotic on purpose --
  the more technical, the lower the risk of a colloquial double life.
- **Pejorative colloquial anchor** (24 words, all adjectives) -- everyday
  negative-affect adjectives (`rossz`, `szörnyű`, `csúnya`, `unalmas`,
  `szomorú`...), standing in for "words used to put someone down." **This name
  is a simplification -- see Limitations.** Unchanged word list from the
  previous iteration's "Colloquial anchor / Negative, core" subtype, now
  promoted to a full top-level anchor.
- **Neutral/positive colloquial anchor** (25 words, all adjectives) --
  everyday positive-to-neutral affect adjectives (`jó`, `remek`, `kedves`,
  `nyugodt`...), standing in for "words used to describe something without
  insult." Unchanged word list from the previous iteration's "Colloquial
  anchor / Positive, core" subtype, now promoted to a full top-level anchor.
- **Target words** (32 words, 11 families) -- diagnostic adjectives with
  documented informal extension. Every noun and verb form from the previous
  iteration's families is gone (`depresszió`, `trauma`, `autizmus`, `pánikol`,
  `trigger`... all dropped), keeping only the adjective/participle form of
  each concept. One new family: **Insanity and madness** (`bolond`, `őrült`,
  `tébolyult`, `elmebeteg`, `dilis`, `hibbant`, `zakkant`, `flúgos`, `eszelős`,
  `habókos`, `ütődött`, `abnormális`, `beszámíthatatlan`) -- a single semantic
  field spanning clinical/legal register through literary to plain slang
  without needing a noun/adjective derivational pair to do it.

**Dual-category flag.** Some words are genuinely split between two
part-of-speech readings in actual corpus usage (Hungarian freely lets
adjectives nominalise: "an autistic person" vs "autistic behaviour"). These
are marked with a trailing `*` in `word_list.txt`, stripped and carried as a
`dual_category` column through every downstream file, and shown as a trailing
`*` on every chart label rather than filed away in a footnote. Flagged:
`traumás`, `zakkant`, `elmebeteg`, `békés`, `fóbiás`, `paranoiás`,
`megszállott`, `autista`, `addikt`, `bolond`, `idiopátiás`, `szisztémás`,
`multifaktoriális`, `malignus` -- exact corpus ratios are in `word_list.txt`'s
asterisk key. `szkizofrén` gets a stronger note there too: it's 100%
noun-tagged in the corpus despite adjectival senses existing in casual speech,
kept anyway since it's central to the pejoration question below.

99 words total, unchanged from the previous iteration -- this revision
restructures which word_type each word belongs to (see intro), not the words
or word count themselves. For the record, two things were caught and fixed by
checking actual corpus xpostag data when this word list was first assembled:
`refrakter` (intended as "treatment-refractory") turned out to be used almost
exclusively (913:1) as an unrelated industrial noun -- a false friend -- and
was replaced with the transparent compound `gyógyszerrezisztens`;
`elmezavart` appeared exactly once in the entire frequency corpus and was
dropped for lack of data.

## Step 1-3 (`script/pipeline.py`): word_list.txt -> tsv -> frequency -> embeddings

Same three-stage shape as before (reshape -> DuckDB join against
`Github/Webcorpus2FrequencyList/frequencies.parquet` -> stream-filter the
3.7GB hunembed tgz). `build_word_list_tsv` now also strips the trailing `*`
convention and emits a `dual_category` boolean column, which every later
script's queries/joins explicitly carry through rather than dropping. Note for
future edits: the tar+awk extraction is cached in
`dat/matched_embeddings_raw.txt`, keyed to whatever word list existed when it
was built -- adding new words requires `force_extract=True`, or they silently
come back with no embedding.

Misses: 0 words with no corpus frequency, 3 words with no embedding
(`aszimptomatikus`, `komorbid`, `prodromális` -- all clinical-anchor
candidates, too rare for the embedding model's minimum count). 96 of 99 words
carry through to the distance/MDS/axis-projection steps.

## Step 4 (`script/distance.py`): one combined distance matrix + MDS map

One cosine-distance matrix over all 96 embedded words together, then one 2D
metric MDS fit (`sklearn.manifold.MDS`, `random_state=1337`) on it ->
`dat/distance_matrix.tsv`, `dat/mds_coords.tsv`.

## Step 5 (`script/analysis.py`): register axis

The pejorative and neutral/positive colloquial anchors are pooled into one
"colloquial" group for this axis -- the register axis only cares about
clinical vs. everyday, not which flavour of everyday. For each of 2000
bootstrap draws (resampling each anchor list with replacement): compute the
clinical-anchor centroid and the pooled colloquial centroid in the raw 600-d
space, take the direction between them, and project every word onto that
axis, centred on the anchors' midpoint. Positive = reads closer to the
colloquial pole; negative = closer to the clinical pole. `dat/axis_scores.tsv`
reports the mean, the bootstrap mean/std, and the raw cosine distance to each
centroid separately.

**Sanity check:** the two anchor groups don't overlap -- clinical anchor words
score [-0.565, -0.153], pooled colloquial anchor words score [0.211, 0.560].

## Step 5b (`script/analysis.py`, valence axis): pejoration vs. neutral bleaching, measured

A colloquial-leaning target word could have got there two different ways:
described neutrally/positively in everyday speech (bleaching in the "concept
creep" sense), or used as an insult (pejoration -- a related but distinct
phenomenon).

This is what the pejorative/neutral-positive anchor split is actually for:
build a second axis from their centroids (pejorative -> neutral/positive),
then **orthogonalise it against the register axis** (Gram-Schmidt: subtract
the component of the valence direction that overlaps with the register
direction) so the two scores measure independent things, sharing one origin
(the clinical/colloquial midpoint) so they form a single 2D coordinate system.
Bootstrap resamples all four anchor pools together each draw. `dat/axis_scores.tsv`
gains `valence_score` + its bootstrap mean/std; `viz/valence_map.png` plots
register x valence for every target word, anchors shown pale for calibration
(positive anchors score [0.163, 0.494], negative anchors [-0.402, -0.133] on
this axis -- clean separation, confirming the axis works).

**Result, replicated from the previous iteration with cleaner anchors:**
`autista*` and `szkizofrén*` -- the words flagged as the likely pejoration
cases -- still do not land colloquial-and-negative. Both stay net
clinical-leaning on the register axis (`autista*` -0.16, `szkizofrén*` -0.15)
and `autista*`'s valence is, if anything, mildly *positive* (+0.13). Meanwhile
`megszállott*` (register +0.30, valence +0.14) sits cleanly in "neutral
bleaching" territory, exactly as its position on the earlier iteration's MDS
map (down among `boldog`/`békés*`) suggested it would.

**The new "Insanity and madness" family makes this a much richer test than
one word pair.** Its 13 words spread across the full register range and split
cleanly into two valence groups once they're colloquial:

| word | register | valence |
|---|---|---|
| `flúgos` | +0.17 | +0.07 |
| `habókos` | +0.30 | +0.08 |
| `dilis` | +0.30 | -0.01 |
| `bolond*` | +0.32 | -0.04 |
| `hibbant` | +0.25 | -0.05 |
| `ütődött` | +0.26 | -0.12 |
| `őrült` | +0.33 | -0.14 |
| `tébolyult` | +0.35 | -0.18 |
| `eszelős` | +0.35 | -0.24 |

`flúgos`/`habókos`/`dilis`/`bolond*` read as neutral-to-mildly-negative
everyday description; `őrült`/`tébolyult`/`eszelős` are both the most
colloquial-scoring words in the entire dataset *and* the most negative-valence
-- the clearest pejoration-leaning cluster this project has produced. Three
words sit apart from the gradient and are worth their own note: `elmebeteg*`
(register +0.05, near the clinical/colloquial midpoint, consistent with its
formal/legal register) has notably negative valence (-0.18) despite barely
being colloquial at all; `abnormális` and `zakkant*` sit slightly
clinical-of-midpoint on register, which reads as reasonable for `abnormális`
(a genuinely more formal-sounding word than the rest of the family) but was
not obviously predictable for `zakkant*` in advance.

**Read carefully before citing:** the positive/negative anchor is built from
generic affect adjectives (`jó`/`rossz`/`szomorú`/`vidám`...), the right
instrument for ordinary sentiment but not necessarily for "used as a slur
against a diagnostic identity" specifically, which is a narrower and different
kind of negativity. `autista*`/`szkizofrén*` coming back flat/positive across
two independent iterations is a more robust null result now than it was the
first time, but it still doesn't distinguish "the pejoration concern was
wrong" from "this axis isn't scoped to detect that particular mechanism."

## Why the POS-control test was retired instead of extended

The previous iteration added 6 Latinate noun/adjective pairs
(`energia`/`energikus` etc.) specifically to test whether the target words'
noun-to-adjective register shift was about clinical meaning or just about
being an adjective, and found the two groups' shifts indistinguishable (0.165
vs 0.172 mean delta). Rather than growing that control set to get a sharper
answer, this revision removes the noun/adjective distinction from the design
entirely -- every list is adjectives only, so there is no noun-vs-adjective
axis left to confound the register axis with. `CLINICAL_PAIRS`,
`CONTROL_PAIRS`, `build_pos_pairs()`, `dat/pos_pairs.tsv` and
`viz/pos_control.png` are all gone. This is a cleaner fix than a bigger
control set would have been, but it's worth being explicit that it changes the
question slightly: the previous iteration could (attempt to) say something
about *how a given diagnostic noun's meaning changes when used adjectivally*;
this iteration can only say where a diagnostic *adjective* sits, not compare
it back to its own noun form's position.

## Why the anchors were restructured into four lists

The third iteration's valence axis worked (see step 5b's results), but it was
structurally a bolt-on: the colloquial anchor was one word_type with two
subtypes, and the positive/negative split only mattered for a secondary axis
computed after the fact. This revision promotes that split to two full
top-level word lists -- clinical anchor, pejorative colloquial anchor,
neutral/positive colloquial anchor, target words -- so the three-way
comparison is the primary structure of the analysis rather than a correction
applied on top of a two-anchor design. **Nothing about the underlying words,
vectors, or maths changed**: `pipeline.py`'s `SECTIONS` and `analysis.py`'s
anchor filters were updated to read the new word_type labels, and the
register/valence axis computations are otherwise identical (verified: every
number in `dat/axis_scores.tsv` and every chart is unchanged from the third
iteration, since the same words feed the same centroids either way). This is
a data-modelling and documentation change, not a new result.

## Step 6 (`script/viz.py`): four charts

- **`viz/mds_map.png`** -- every embedded word on one labelled map, coloured
  by word_type. The pejorative and neutral/positive colloquial anchors share
  one display colour here (both are "the colloquial side" for this chart's
  purpose); `viz/valence_map.png` is where their split matters.
- **`viz/axis_projection.png`** -- target words as a ranked, bootstrap-error-
  barred bar chart, one small-multiple block per family, clinical-anchor and
  pooled-colloquial-anchor score ranges shown as background bands rather than
  as 67 individual bars.
- **`viz/distance_scatter.png`** -- the same idea as the axis chart, but as
  the two raw distances (to the clinical centroid, to the pooled colloquial
  centroid) plotted against each other with an equidistant reference line, so
  both numbers stay visible instead of being compressed into one score.
- **`viz/valence_map.png`** -- the step 5b result: register score x valence
  score for every target word, the two colloquial anchors shown as separate
  pale series for calibration, quadrant labels for "neutral bleaching" vs
  "pejoration-leaning." Words the manuscript (`md/kezirat.md`) actually
  discusses get a bolder, larger label than the rest, so this detailed
  version can be cross-referenced against the running text.

Dual-category words (see above) carry a trailing `*` on their label in every
chart. Each chart also has a Hungarian version (`*_hu.png`): titles, axis
labels, legends and family headers translated; the plotted words themselves
are untouched since they're already Hungarian in the data. Translations live
in the `TEXT` dict in `viz.py`, keyed by the same English word_type values
used elsewhere in the pipeline (`Clinical anchor`, `Pejorative colloquial
anchor`, `Neutral/positive colloquial anchor`, `Target words`).

**`viz/valence_map_hu_pub.png`** is a separate, print-oriented rebuild of the
valence map for the Festschrift manuscript, not just a resized copy of the
detailed one. Three things differ, all in service of surviving being shrunk to
book-page size and reproduced at ordinary print quality:

- The figure is drawn *at* its intended final printed size (`figsize=(6.3,
  5.8)`, roughly a 16cm-wide single figure) rather than at a large on-screen
  canvas -- font size in matplotlib is physical (points relative to figure
  inches), so a big canvas with big-looking fonts shrinks back down to
  illegibly small text, while a canvas sized for its actual print target does
  not.
- The three anchor groups (15-49 points each) become smooth KDE density
  clouds (`kde_cloud()`, `scipy.stats.gaussian_kde` with a widened bandwidth
  so one or two outlier words don't read as a disconnected second island)
  instead of scatters of individual points -- an anchor's job is "roughly
  where this whole category sits," and a cloud says that more legibly at
  small size than 49 tiny dots do.
- Only target words the manuscript actually names get a label
  (`load_manuscript_target_words()` parses `md/kezirat.md`'s `*italicised*`
  examples and intersects them with the target-word list, so the figure
  can't silently drift out of sync with the text); the rest stay as small
  unlabelled dots so the overall spread is still visible. In the current
  manuscript that's 27 of 32 target words. Labels are placed and decluttered
  by `declutter_2d()`, a small dependency-free collision resolver (nudge
  overlapping label pairs apart in screen space, iterate) with a thin leader
  line drawn back to the point wherever a label had to move more than about
  1.5% of the axis span.

### What the charts show

Most target words stay clinical-leaning: `traumás*` (-0.36, the single most
clinical-scoring target word), `bipoláris`, `toxikus`, `pszichotikus`,
`szkizofrén*` and `fóbiás*` all sit deep in the clinical anchor's own range or
past it. `traumatizált`, by contrast, sits almost exactly at the midpoint
(-0.01) -- the same divergence within one family (`trauma` -> `traumás*` /
`traumatizált`) noted in the previous iteration, now even starker.

The insanity family (see step 5b) is the strongest result in the project to
date: a single semantic field showing a near-continuous register gradient from
`abnormális`/`elmebeteg*` (clinical-legal-adjacent) through
`zakkant*`/`beszámíthatatlan` (near the midpoint) to a solid block of plain
colloquial words, nine of which are more colloquial-scoring than any word in
any other target family. That gradient exists *within one concept* (madness),
which is a cleaner demonstration of register variation than comparing across
different diagnoses ever was.

## Why this replaced the second iteration

The second iteration's headline finding -- that adjective forms of a
diagnosis score more colloquial than the noun (`depresszió` vs `depressziós`)
-- turned out to be indistinguishable from a generic part-of-speech effect
once tested against a non-clinical control. Rather than patch that with a
bigger control set, this iteration removes part-of-speech as a variable
entirely: every anchor and target word is an adjective, so there is nothing
left for a noun-vs-adjective confound to hide in. The trade-off is losing the
ability to compare a diagnosis's noun and adjective forms directly (see "Why
the POS-control test was retired" above) -- but what's gained, the insanity
family, demonstrates the actual phenomenon of interest (register variation
within one semantic field) more convincingly than the noun/adjective pairs
ever did.

## Limitations (read before citing anything from this project)

This section exists because it was asked for explicitly, and because the
individual caveats scattered through the steps above are easy to skim past
one at a time. Nothing here is new; it's a consolidated list.

1. **Not diachronic.** hunembed is one static embedding from one corpus
   snapshot. This project cannot show a word's meaning changing over time, only
   where it sits *now* relative to two chosen poles. Any "X has drifted"
   phrasing is an overclaim; "X currently reads closer to..." is what the data
   supports.
2. **"Pejorative colloquial anchor" is a proxy, not a validated instrument.**
   The anchor is built from generic negative-affect adjectives (`rossz`,
   `szomorú`, `ijesztő` -- "bad," "sad," "scary"), not slur-adjacent or
   insult-specific vocabulary. A target word scoring close to it shows
   association with general negative sentiment, which is necessary but not
   sufficient evidence for the narrower claim ("used as a slur against a
   diagnostic identity") the project's motivating question actually cares
   about. This is the single most consequential limitation for the project's
   most interesting open question: `autista`/`szkizofrén` scoring flat/positive
   on this anchor could mean the pejoration concern was wrong, or could mean
   the anchor simply isn't scoped to detect that mechanism. Both readings stay
   open; neither is proven.
3. **Register skew in the source corpus.** MNSZ2 + webcorpus is general web
   text, not a balanced clinical/informal split. A word's raw distance from
   the clinical pole isn't meaningful in isolation -- only its position
   *relative to the two anchors, drawn from the same corpus* is. Don't cite a
   raw `dist_to_clinical`/`dist_to_colloquial` number on its own.
4. **No significance or permutation test exists for either axis.** The
   bootstrap std reported alongside `axis_score` and `valence_score` measures
   sensitivity to which anchor words were resampled -- it is not a formal
   confidence interval and says nothing about corpus sampling uncertainty more
   broadly. Nothing here has been tested against a null distribution.
5. **The clinical anchor is smaller than intended.** 3 of 18 candidate
   clinical adjectives (`aszimptomatikus`, `komorbid`, `prodromális`) had no
   embedding at all -- too rare for this corpus, not evidence about their
   meaning, but it leaves 15 embedded clinical-anchor words against 49
   colloquial-anchor words.
6. **Some words are corpus-verified dual-category**, not cleanly one part of
   speech: `traumás`, `zakkant`, `elmebeteg`, `békés`, `fóbiás`, `paranoiás`,
   `megszállott`, `autista`, `addikt`, `bolond`, `idiopátiás`, `szisztémás`,
   `multifaktoriális`, `malignus` (marked `*` throughout; exact ratios in
   `word_list.txt`). `szkizofrén` is a further, stronger case: 100%
   noun-tagged in this corpus despite adjectival senses existing in casual
   speech. None of this invalidates their inclusion -- Hungarian
   adjective-to-noun conversion is pervasive enough that a fully "pure"
   adjective list isn't achievable -- but the word list is not as clean as
   "every word here is unambiguously an adjective" would suggest.
7. **Corpus vintage is unknown relative to recent usage.** Whether hunembed's
   training data predates or postdates any given word's current colloquial
   currency is not established. A missing or unexpectedly weak embedding (see
   point 5) is at least as likely to be a corpus-age artefact as a finding
   about the word's actual usage.

## Outputs

| file | rows | description |
|---|---|---|
| `dat/word_list.txt` | -- | hand-curated source: clinical anchor, pejorative colloquial anchor, neutral/positive colloquial anchor, target words |
| `dat/word_list.tsv` | 99 | word_type, word_subtype, word, dual_category |
| `dat/word_list_freq.tsv` | 99 | + lemma_freq, llfpm10, freq_bin (decile within word_type) |
| `dat/word_list_embeddings.tsv.gz` | 99 | + dim_1...dim_600 (600-d word2vec vector) |
| `dat/matched_embeddings_raw.txt` | -- | cached tar+awk extraction (regenerate with `force_extract=True` if the word list changes) |
| `dat/distance_matrix.tsv` | 96x96 | cosine-distance matrix, all embedded words |
| `dat/mds_coords.tsv` | 99 | word_list_freq.tsv + mds_x, mds_y (null where no embedding) |
| `dat/axis_scores.tsv` | 96 | dist_to_clinical/colloquial, axis_score, valence_score, both scores' bootstrap mean/std |
| `viz/mds_map.png` | -- | all words, one labelled map |
| `viz/axis_projection.png` | -- | ranked register-axis score per target word, by family |
| `viz/distance_scatter.png` | -- | distance-to-clinical vs distance-to-colloquial, per target word |
| `viz/valence_map.png` | -- | register score x valence score per target word, manuscript-mentioned words bolded |
| `viz/valence_map_hu_pub.png` | -- | print-sized rebuild for the Festschrift: anchor density clouds, only manuscript-named target words labelled |

## Decisions worth revisiting (as distinct from the limitations above)

- Whether it's worth building a second, narrower anchor -- slur-adjacent/
  insult vocabulary specifically, rather than generic negative affect -- to
  properly test whether `autista*`/`szkizofrén*`'s colloquial use is
  pejorative in the sense Limitations point 2 says the current anchor can't
  confirm or rule out.
- **`elmebeteg*`'s negative valence despite a near-midpoint register score**
  is worth a closer look -- it's the one word in the insanity family whose two
  scores don't obviously fit the same story as the rest of the gradient.
- Whether to grow the clinical anchor back toward 18 embedded words (see
  Limitations point 5) by finding replacements for the three misses.
