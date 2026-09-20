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

## The current design: four word lists, not two

The analysis is built on four adjective-only word lists, not the two/three
you might expect from an earlier draft of this project:

- **Clinical anchor** -- technical/diagnostic adjectives (`terápiarezisztens`,
  `iatrogén`, `malignus`...).
- **Pejorative colloquial anchor** -- everyday negative-affect adjectives
  (`rossz`, `szomorú`, `ijesztő`...), standing in for "words used to put
  someone down."
- **Neutral/positive colloquial anchor** -- everyday positive-to-neutral
  affect adjectives (`jó`, `kedves`, `nyugodt`...), standing in for "words
  used to describe something without insult."
- **Target words** -- the diagnostic adjectives under study, 11 families
  including a purpose-built "Insanity and madness" family spanning clinical/
  legal register through literary to plain slang in one semantic field.

Two things every target word gets computed against: a **register axis**
(clinical anchor centroid -> pooled-colloquial centroid) and a **valence
axis** (pejorative-anchor centroid -> neutral/positive-anchor centroid,
orthogonalised against the register axis so the two scores are independent).
The register axis says clinical-vs-everyday; the valence axis says, among the
colloquial-leaning words, neutrally-described-vs-used-as-a-put-down.

**Read the naming carefully.** "Pejorative colloquial anchor" is this
project's name for a general-negative-sentiment word list, not a validated
slur/insult detector. See Limitations below -- this is the single caveat most
likely to matter if a reviewer pushes on the paper's central claim.

## Design history (why it looks like this)

Four revisions, each triggered by actually testing a suspicion about the
method rather than by a new idea about Hungarian:

1. **First iteration:** substance-use vocabulary vs. colloquial-sentiment vs.
   clinical word lists, authored independently. Worked, but disjoint-by-
   construction categories proved nothing about individual words drifting
   between registers.
2. **Second iteration:** the same lemma family tested across registers
   (`depresszió`/`depressziós`/`depresszív`). Better design, but the clinical
   anchor mixed nouns and adjectives while the colloquial anchor was 100%
   adjectives. A Latinate control test (`energia`/`energikus` etc.) confirmed
   this was a real confound: control pairs' noun-to-adjective shift (mean
   0.172) was indistinguishable from the clinical pairs' (mean 0.165).
3. **Third iteration:** every word list rebuilt adjectives-only, retiring the
   POS confound structurally instead of testing around it. The Latinate
   control set and its test (`CLINICAL_PAIRS`, `CONTROL_PAIRS`,
   `build_pos_pairs()`, `dat/pos_pairs.tsv`, `viz/pos_control.png`) are gone
   from the codebase entirely. The "Insanity and madness" target family was
   added here specifically to test register variation within one concept
   instead of across a noun/adjective pair.
4. **Current iteration:** the colloquial anchor's internal positive/negative
   split (previously two *subtypes* used only to build a secondary "valence
   axis" correction) was promoted to two full top-level anchors, making the
   three-way comparison (clinical / pejorative-colloquial / neutral-positive-
   colloquial) the primary structure instead of a bolt-on. This changed
   `pipeline.py`'s `SECTIONS` and `analysis.py`'s anchor filters, but not the
   underlying words, vectors, or maths -- every number in
   `dat/axis_scores.tsv` is identical to the third iteration's.

**If the paper cites the second iteration's noun/adjective finding at all,
cite it as a cautionary methods note, not a result.**

## What's actually defensible as a finding

- **Most target words stay clinical-leaning overall.** `traumás*` (-0.36) is
  the single most clinical-scoring target word; `bipoláris`, `toxikus`,
  `pszichotikus`, `szkizofrén*`, `fóbiás*` all sit deep in the clinical
  anchor's own range.
- **The insanity family shows a near-continuous register gradient within one
  concept -- lead with this.** From `abnormális`/`elmebeteg*` (near the
  clinical/colloquial midpoint) through `zakkant*` to a block of nine words
  more colloquial-scoring than any word in any other target family (`flúgos`
  +0.17 up to `eszelős` +0.35). It doesn't depend on comparing a noun to its
  own adjective, so the retired POS-control caveat doesn't touch it.
- **The valence axis splits the insanity family into a neutral cluster and a
  pejoration-leaning cluster.** `flúgos`/`habókos`/`dilis`/`bolond*` land
  colloquial and roughly neutral (valence -0.04 to +0.08); `őrült`/
  `tébolyult`/`eszelős` land colloquial *and* clearly negative (valence -0.14
  to -0.24) -- the clearest pejoration-leaning cluster the project has
  produced, and it emerged from words chosen for register spread, not for
  confirming a hypothesis.
- **`autista*` and `szkizofrén*` still do not land colloquial-and-negative,
  across two independent word-list designs now.** Current numbers: `autista*`
  register -0.16, valence +0.13 (mildly *positive*); `szkizofrén*` register
  -0.15, valence -0.11 (mildly negative, but still net clinical-leaning on
  register). This replicated cleanly through the third-to-fourth iteration
  restructuring (identical numbers, since the underlying vectors didn't
  change), which makes it a more robust null than a single run would be --
  but see Limitations point 2 before concluding anything from it.
- `traumás*` (-0.36) vs `traumatizált` (-0.01) is a striking within-family
  split worth reporting as an open question: nothing in the design predicts
  why the participle would be so much less clinical-scoring than the plain
  adjective.

## Limitations (spell these out; do not bury them)

1. **Not diachronic.** One static embedding, one corpus snapshot. No claim
   about change over time is supportable, only current relative position.
2. **"Pejorative colloquial anchor" is a proxy, not a validated instrument.**
   Built from generic negative-affect adjectives (`rossz`, `szomorú`,
   `ijesztő`), not slur-adjacent or insult-specific vocabulary. This is the
   limitation that most directly bears on the paper's most interesting
   result: `autista*`/`szkizofrén*` scoring flat/positive on this anchor is
   consistent with *either* "the pejoration concern was wrong" *or* "this
   anchor isn't scoped to detect that particular mechanism," and the data
   cannot adjudicate between those two readings. State both, favour neither.
3. **Register skew in the source corpus.** MNSZ2 + webcorpus is general web
   text, not a balanced clinical/informal split. Relative anchor-to-anchor
   position is meaningful; a raw distance number cited on its own is not.
4. **No significance or permutation test exists for either axis.** The
   bootstrap std on `axis_score`/`valence_score` reflects sensitivity to
   which anchor words got resampled, not a formal test against a null. Don't
   write "95% CI" or claim statistical significance without building that
   test first.
5. **The clinical anchor is thinner than intended.** 15 embedded words, not
   the 18 the word list specifies -- 3 exotic candidates
   (`aszimptomatikus`, `komorbid`, `prodromális`) had no embedding, likely
   too rare for the corpus rather than meaningfully absent.
6. **A number of words are corpus-verified dual-category**, not cleanly one
   part of speech (`traumás`, `autista`, `bolond`, `szisztémás`... -- full
   list and ratios in `word_list.txt`'s asterisk key). `szkizofrén` is a
   further, stronger case: 100% noun-tagged in this corpus despite adjectival
   senses existing in casual speech. Don't present the word list as cleaner
   than it is; a reviewer who checks will find these.
7. **Corpus vintage relative to current usage is unknown.** A missing or
   weak embedding is at least as likely to be a corpus-age artefact as a
   finding about a word's actual currency.

## Open decisions not yet made

- Whether it's worth building a second, narrower anchor -- slur-adjacent/
  insult vocabulary specifically -- to properly test whether `autista*`/
  `szkizofrén*`'s colloquial use is pejorative in the sense the current
  valence axis can't confirm or rule out (Limitations point 2).
- Whether `elmebeteg*`'s odd register/valence combination (near-midpoint
  register, but valence as negative as far-more-colloquial words) is worth
  chasing down or just reporting as an outlier.
- Whether a permutation-based significance test is worth building before the
  paper makes any claim stronger than "descriptively, these words pattern
  this way."
- Whether to grow the clinical anchor back toward 18 embedded words.

## Standing style notes (already in the global CLAUDE.md, restated because
they matter more in prose than in code)

British spelling, no em dashes, concise by default. Label speculation clearly,
then commit to it rather than hedging every sentence. For each argument the
paper makes, give the strongest weakness or alternative reading alongside it --
the Limitations section above is a starting list, not exhaustive.
