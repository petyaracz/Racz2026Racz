# Handover: writing up the paper and its framing

## The one-line pitch

Do Hungarian diagnostic terms ("depresszió", "autizmus", "szkizofrénia"...)
still read as clinical language, or has everyday use pulled some of them
toward ordinary affect vocabulary, and does that show up geometrically in
word embeddings?

## What the data can support, and what it can't

**Cannot support: a claim about change over time.** hunembed is one static
embedding trained once on one corpus. There is no earlier snapshot to compare
against. Any sentence shaped like "X has drifted" or "X used to be clinical
and is now colloquial" is a claim this data does not back up, no matter how
suggestive the chart looks. Watch for this phrasing creeping into a draft --
it's the single easiest way to overclaim here.

**Can support: a synchronic register-position claim.** Given a clinical pole
and a colloquial pole built from words we're confident belong to each
register, a target word's projection onto that axis says whether its *current*
usage pattern in this corpus reads as closer to technical nomenclature or to
everyday affect language. That's the whole claim. Frame sentences as "X
currently reads closer to..." not "X has moved toward...".

This maps onto two literatures worth citing rather than re-deriving:
- **Concept creep** (Haslam 2016) -- the psychology-side framing for
  trauma/abuse/disorder vocabulary broadening into lay use. This is the
  phenomenon being tested.
- **Semantic axis projection** (Kozlowski et al. 2019, "The Geometry of
  Culture") -- the method: define a pole from two anchor word sets, project
  everything onto it. This is what `script/analysis.py` implements.

## Word-list history: two revisions, both driven by checking rather than assuming

This project has gone through three word lists. The pattern worth noticing:
each revision was triggered by actually testing a suspicion about the method,
not by a new idea about Hungarian. That's the model to keep following if the
paper's reviewers raise a similar suspicion later.

1. **First iteration:** substance-use vocabulary vs. colloquial-sentiment vs.
   clinical word lists. Worked, but the three lists were disjoint by
   construction (authored independently), so clean separation proved nothing
   about individual words drifting between registers.
2. **Second iteration:** same lemma family tested across registers
   (`depresszió`/`depressziós`/`depresszív`). Better design, but the clinical
   anchor mixed nouns and adjectives while the colloquial anchor was 100%
   adjectives. A Latinate control test (`energia`/`energikus` etc., non-
   clinical noun/adjective pairs) confirmed this was a real confound: the
   control pairs' noun-to-adjective register shift (mean 0.172) was
   indistinguishable from the clinical pairs' (mean 0.165), and the single
   largest shift in the dataset belonged to a control pair. The headline
   "adjectives bleach more than nouns" finding from that iteration could not
   be told apart from "adjectives just are more colloquial-scoring than
   nouns, full stop."
3. **Current iteration:** rather than growing the control set to get a
   sharper answer, part-of-speech was removed from the design entirely --
   every word list (clinical anchor, colloquial anchor, target words) is now
   adjectives only. The Latinate control set, `CLINICAL_PAIRS`/`CONTROL_PAIRS`,
   `build_pos_pairs()`, `dat/pos_pairs.tsv` and `viz/pos_control.png` are all
   retired. **If the paper cites the second iteration's noun/adjective
   finding at all, cite it as a cautionary methods note, not a result** --
   it's the reason this design looks the way it does, not a result. In
   return, a new "Insanity and madness" target family (13 words: `bolond`,
   `őrült`, `tébolyult`, `elmebeteg`, `dilis`, `hibbant`, `zakkant`, `flúgos`,
   `eszelős`, `habókos`, `ütődött`, `abnormális`, `beszámíthatatlan`) tests
   register variation within one semantic field instead of across a
   noun/adjective pair, and turned out to be the strongest result in the
   project so far.

## What's actually defensible as a finding

- **Most target words stay clinical-leaning overall.** `traumás*` (-0.36) is
  the single most clinical-scoring target word; `bipoláris`, `toxikus`,
  `pszichotikus`, `szkizofrén*`, `fóbiás*` all sit deep in the clinical
  anchor's own range.
- **The insanity family shows a near-continuous register gradient within one
  concept, which is a cleaner demonstration of the phenomenon than the
  cross-diagnosis comparisons ever produced.** From `abnormális`/`elmebeteg*`
  (near the clinical/colloquial midpoint) through `zakkant*` to a block of
  nine words more colloquial-scoring than any word in any other target
  family (`flúgos` +0.17 up to `eszelős` +0.35). This is the finding to lead
  with -- it doesn't depend on comparing a noun to its own adjective, so the
  retired POS-control caveat doesn't touch it.
- **The valence axis replicates cleanly across two independent word-list
  designs, and it still contradicts the original pejoration hunch.**
  `autista*` and `szkizofrén*` -- named as the likely pejoration cases back
  in the first revision of this analysis -- are *not* colloquial-and-negative
  in either version of the word list. Current numbers: `autista*` register
  -0.16, valence +0.13 (mildly *positive*); `szkizofrén*` register -0.15,
  valence -0.11 (mildly negative, but still net clinical-leaning on
  register). Neither is the colloquial-and-strongly-negative outlier
  predicted at the outset.
- **The insanity family gives the pejoration-vs-bleaching split real texture
  instead of one word pair.** `flúgos`/`habókos`/`dilis`/`bolond*` land
  colloquial and roughly neutral (valence -0.04 to +0.08); `őrült`/
  `tébolyult`/`eszelős` land colloquial *and* clearly negative (valence -0.14
  to -0.24) -- the clearest pejoration-leaning cluster the project has
  produced, and it emerged from words chosen for register spread, not for
  confirming the hypothesis.
- **Caveat that must travel with every valence-axis claim above:** the
  positive/negative anchor is built from generic affect adjectives
  (`jó`/`rossz`/`szomorú`/`vidám`...). It's the right instrument for ordinary
  sentiment, not necessarily for "used as a slur against a diagnostic
  identity" specifically, which is a narrower and different kind of
  negativity. `autista*`/`szkizofrén*` coming back flat/positive across two
  iterations is a more robust null now than it was the first time, but it
  still doesn't distinguish "the pejoration concern was wrong" from "this
  axis isn't scoped to detect that particular mechanism."
- `traumás*` (-0.36) vs `traumatizált` (-0.01) is a striking within-family
  split, worth reporting as a genuine open question rather than smoothing
  over: nothing in the design predicts why the participle would be so much
  less clinical-scoring than the plain adjective.

## Traps in the data, not visible from the charts alone

- **`elmebeteg*`'s two scores don't obviously tell the same story.** It sits
  near the clinical/colloquial midpoint on register (+0.05, consistent with
  its formal/legal register) but has clearly negative valence (-0.18),
  similar in magnitude to words far more colloquial than it. Worth a closer
  read before using it as a clean example of anything.
- **The valence anchor may not be scoped to catch diagnostic-identity
  pejoration** -- see the caveat above. Don't convert the `autista*`/
  `szkizofrén*` flat result into "pejoration isn't happening"; report it as a
  flat result with an open question about instrument scope.
- **The bootstrap std in `axis_scores.tsv` is not a confidence interval in
  the formal sense**, for either `axis_score` or `valence_score`. It only
  captures how much the score moves depending on which anchor words got
  resampled -- it says nothing about corpus sampling uncertainty more
  broadly. Don't write "95% CI" or similar; "sensitivity to anchor choice"
  is the accurate framing.
- **No significance test exists for either axis.** Nothing has been tested
  against a null (e.g. a permutation test shuffling which words are
  "target" vs a random draw from the vocabulary). If the paper wants to say
  a result is statistically significant rather than descriptively
  suggestive, that test still needs to be built.
- **Anchor sets are moderate, not large** (15 clinical, 49 colloquial with
  the current embeddings). Three exotic clinical-anchor candidates
  (`aszimptomatikus`, `komorbid`, `prodromális`) had no embedding at all --
  too rare for the corpus, not evidence about their meaning, but it does mean
  the clinical anchor is thinner than intended.
- **Register skew of the source corpus.** MNSZ2 + webcorpus is general web
  text, not a balanced clinical/informal split. Absolute distances are not
  meaningful on their own; only the relative anchor-pole framing is. This is
  already handled by the method, just don't let a stray sentence cite a raw
  distance number as if it meant something in isolation.
- **A handful of target/anchor words are corpus-verified dual-category**
  (noun/adjective split under ~2.5:1 in actual usage), marked with a trailing
  `*` throughout: `traumás`, `zakkant`, `elmebeteg`, `békés`, `fóbiás`,
  `paranoiás`, `megszállott`, `autista`, `addikt`, `bolond`, `idiopátiás`,
  `szisztémás`, `multifaktoriális`, `malignus`. This doesn't invalidate their
  inclusion (the whole word list is "intended part of speech," and Hungarian
  adjective-to-noun conversion is pervasive enough that a fully pure list
  isn't achievable), but a reviewer who checks `word_list.txt`'s asterisk key
  will find these, so don't present the word list as cleaner than it is.

## Open decisions not yet made

- Whether it's worth building a second, narrower anchor axis specifically for
  diagnostic-identity-slur-style pejoration (distinct from the general
  positive/negative anchor already in place), to properly test whether
  `autista*`/`szkizofrén*`'s colloquial use is pejorative in a way the
  current valence axis isn't scoped to catch.
- Whether `elmebeteg*`'s odd register/valence combination is worth chasing
  down (a different anchor construction? a genuine feature of legal/clinical-
  register insult words?) or just reporting as an outlier.
- Whether a permutation-based significance test is worth building before the
  paper makes any claim stronger than "descriptively, these words pattern
  this way." Still not built for either axis.
- Whether to grow the clinical anchor back toward its original size (15
  embedded words is workable but thinner than the 18 intended) by finding
  replacements for the three misses, given how rare a few of the current
  members already are.

## Standing style notes (already in the global CLAUDE.md, restated because
they matter more in prose than in code)

British spelling, no em dashes, concise by default. Label speculation clearly,
then commit to it rather than hedging every sentence. For each argument the
paper makes, give the strongest weakness or alternative reading alongside it --
the "traps" section above is a starting list, not exhaustive.
