# Clinical, colloquial, or neither: the Hungarian lexicon of madness in register-by-valence space

*Draft, descriptive framing. All claims are synchronic and descriptive; no
diachronic claim is made anywhere in this document, and none should be added.*

---

## Before reading: numbers and facts to verify

Values taken verbatim from `HANDOVER.md` are unmarked. Values I read off the
figures rather than from `axis_scores.tsv` are marked `[≈]` and need replacing
with exact figures. Bibliography entries are marked for verification status at
the end.

Three factual points to settle before the draft goes further:

1. **Corpus provenance.** The handover says MNSZ2 + webcorpus. The published
   description of `hunembed0.0` says word2vec, 600 dimensions, frequency
   cut-off 10, trained on the concatenation of the *Hungarian Webcorpus*
   (Halácsy et al. 2004) and the *Hungarian National Corpus* (Váradi 2002).
   Those are the first-generation resources, not Webcorpus 2.0 (Nemeskey 2020)
   or the Hungarian Gigaword Corpus (Oravecz et al. 2014). If the older
   provenance is correct, the corpus predates most contemporary informal
   Hungarian web writing by around two decades, which affects §6 substantially
   and explains the missing embeddings reported in earlier iterations. Section
   3 and §6 are written on the assumption that the older provenance is correct;
   revise if not.
2. **Attribution for `hunembed0.0` itself.** Currently cited as a resource
   without a paper. Find the citable source or cite the URL with an access date.
3. **Whether the colloquial anchor is 49 items throughout.** The handover gives
   49 for the current embeddings and 15 clinical; the valence split of those 49
   into positive and negative sub-anchors is not recorded. Report the split.

---

## Abstract

Diagnostic vocabulary and everyday vocabulary for mental states overlap
substantially in Hungarian, but the overlap is uneven: some words are at home
in a clinical report and nowhere else, some circulate freely in ordinary
speech, and some do both. We map this variation geometrically. Using a static
Hungarian word embedding, we define a clinical-to-colloquial axis from two
anchor sets of adjectives and a valence axis orthogonal to it, and we project
a set of target adjectives drawn from diagnostic and everyday vocabularies
onto the resulting plane. The resulting map is descriptive rather than
explanatory, and we offer it as such. Three features of it seem to us worth
recording. First, the Hungarian lexicon of madness (*bolond*, *őrült*,
*flúgos*, *tébolyult*, *elmebeteg* and their neighbours) spreads across
nearly the full range of the register axis, while the Latinate diagnostic
adjectives (*bipoláris*, *pszichotikus*, *toxikus*) cluster tightly at the
clinical end. Second, the colloquial end of the axis is not uniform in
valence: it contains a near-neutral cluster and a clearly negative one.
Third, two words of forensic and administrative provenance, *elmebeteg* and
*beszámíthatatlan*, sit near the midpoint of the register axis while scoring
strongly negative on valence, which we read as evidence that a two-pole axis
has no place to put a third register. We discuss what the register axis
plausibly measures, and what would be needed to establish that it measures
register at all.

**Keywords:** semantic projection, register, word embeddings, Hungarian,
psychiatric vocabulary, valence

---

## 1 Introduction

Words for mental disorder move between speech communities. A term coined in
clinical nomenclature may pass into ordinary usage, an ordinary word may be
recruited as a technical label, and a term abandoned by clinicians may persist
in law, journalism or insult. Hungarian offers an unusually dense case, because
the vocabulary of madness includes a large stock of native colloquial
adjectives (*flúgos*, *habókos*, *dilis*, *zakkant*, *hibbant*, *ütődött*)
alongside a learned Latinate stratum (*pszichotikus*, *bipoláris*,
*abnormális*) and a legal-administrative stratum (*elmebeteg*,
*beszámíthatatlan*) that overlaps with neither. The three strata refer to
roughly the same territory and differ in where they are usable.

Register is usually studied as a property of texts rather than of words:
corpora are divided into registers and lexical distributions compared across
the division (see Biber and Conrad 2009 for the canonical statement). The
approach we take here inverts that. Rather than partitioning the corpus, we
treat register position as a continuous property of a word and estimate it from
the word's distributional neighbourhood in a single undivided corpus. The
method is semantic projection: define an axis from two sets of anchor words
that are agreed to occupy opposite ends of some dimension, then project other
words onto it. Kozlowski, Taddy and Evans (2019) established the technique in
sociology, using it to recover dimensions of social class from historical text;
Grand et al. (2022) showed that projections of this kind recover graded human
feature judgements across many object categories, which is the strongest
available evidence that the geometry tracks something people know. An, Kwak and
Ahn (2018) generalised the construction to arbitrary antonym-derived axes, and
Hamilton et al. (2016) showed, for the sentiment case specifically, that the
lexicon induced this way varies by community.

What we do here is apply that machinery to one Hungarian semantic field and
report what it yields. We want to be explicit at the outset about what this
paper is not. It is not a test of concept creep (Haslam 2016), the hypothesis
that harm-related psychological concepts have broadened over recent decades: a
single static embedding trained on a single corpus offers no earlier snapshot
to compare against, and no arrangement of the present data can bear on
diachronic change. Nor is it a validation of the instrument, since we have no
independent human judgements of Hungarian register against which to check the
projections. It is a map, produced by a method with a published track record in
adjacent applications, of a lexical field that has not to our knowledge been
described this way before. We take the descriptive contribution to be the
contribution, and we are explicit in §6 about the several readings of the
register axis that the data cannot distinguish.

## 2 Materials

### 2.1 Target words

The target set comprises 28 [≈ verify count] Hungarian adjectives and
participial adjectives grouped into families by semantic field: depression
(*depressziós*, *depresszív*), trauma (*traumás*, *traumatizált*), panic and
phobia (*fóbiás*), hysteria and mania (*mániás*, *paranoiás*, *hisztis*),
neurosis and compulsion (*neurotikus*, *kényszeres*, *megszállott*),
neurodevelopmental (*autista*, *hiperaktív*), psychotic spectrum
(*pszichotikus*, *szkizofrén*), addiction (*függő*, *addikt*), mood disorder
(*bipoláris*), contemporary loans (*toxikus*), and madness (*abnormális*,
*zakkant*, *elmebeteg*, *beszámíthatatlan*, *flúgos*, *hibbant*, *ütődött*,
*habókos*, *dilis*, *bolond*, *őrült*, *eszelős*, *tébolyult*).

The madness family deserves comment, because it was assembled differently from
the others. Its thirteen members were chosen to span the register range as a
native speaker perceives it, from the formal-administrative *elmebeteg* to the
markedly colloquial *flúgos*. This is a selection criterion that guarantees a
spread on any instrument that works at all, and we do not present the existence
of a spread as a finding. What the selection does not determine is the ordering
within the spread or the family's position relative to the other targets, and
those are what we report.

The word list is constrained to adjectives and participial adjectives
throughout, for both anchors and targets. An earlier iteration of this study
included nouns and their derived adjectives and compared them; a control
condition using non-clinical Latinate noun-adjective pairs (*energia*
/*energikus* and similar) found a noun-to-adjective shift on the register axis
of the same magnitude in the control as in the clinical items (0.172 against
0.165), and the largest single shift in the dataset belonged to a control pair.
We therefore removed part of speech from the design rather than report a result
we could not distinguish from a part-of-speech effect. We mention this as a
methods note and draw no substantive conclusion from it. Hungarian
adjective-to-noun conversion is pervasive enough that a fully pure adjective
list is unobtainable in any case; fourteen items whose corpus noun-to-adjective
ratio falls below roughly 2.5:1 are marked with a trailing asterisk in the
released word list and in the figures.

### 2.2 Anchors

The clinical anchor consists of 15 adjectives of epidemiological, nosological
and clinical-descriptive provenance (*patológiás*, *iatrogén*, *szubklinikai*,
*terápiarezisztens*, *kontraindikált*, *idiopátiás*, *szisztémás*, *malignus*,
*benignus*, *juvenilis*, *dekompenzált*, *posztoperatív*, *multifaktoriális*,
*neurodegeneratív*, *gyógyszerrezisztens*). Three further candidates
(*aszimptomatikus*, *komorbid*, *prodromális*) had no embedding and were
dropped, which we take as evidence about corpus coverage rather than about
those words.

The colloquial anchor consists of 49 everyday evaluative adjectives, split for
the valence axis into positive (*jó*, *kiváló*, *remek*, *kellemes*,
*csodálatos*, and so on) and negative (*rossz*, *szörnyű*, *borzasztó*,
*fájdalmas*, *undorító*, and so on) subsets.

A reviewer will note that the clinical anchor is smaller than the colloquial
one and drawn from a narrower semantic neighbourhood. We agree, and §6 sets out
what follows from the asymmetry.

## 3 Method

We use `hunembed0.0`, a word2vec model of 600 dimensions with a frequency
cut-off of 10, trained on the concatenation of the Hungarian Webcorpus
(Halácsy et al. 2004) and the Hungarian National Corpus (Váradi 2002).

The register axis is the vector running from the centroid of the clinical
anchor to the centroid of the colloquial anchor. Each target word's register
score is its projection onto this axis, normalised so that negative values lie
toward the clinical pole and positive values toward the colloquial pole. The
valence axis is the vector from the negative to the positive colloquial
sub-anchor centroid, orthogonalised against the register axis, so that a
target's valence score is its evaluative polarity net of whatever polarity the
register axis already carries.

Uncertainty is estimated by resampling the anchor sets with replacement and
recomputing both scores; the dispersion reported as error bars in the figures
is the standard deviation of the resulting distribution. This quantity measures
sensitivity to anchor choice and nothing else. It is not a confidence interval
in any formal sense, and in particular it does not capture the corpus-sampling
and training-seed variance that Antoniak and Mimno (2018) identify as the
dominant source of instability in embedding-derived similarity measures. Since
the embedding is pre-trained and fixed, that variance is inaccessible to us. We
report the anchor-sensitivity bars because they are informative about one
component of uncertainty, and we flag here that they are narrower than the true
uncertainty by an unknown margin.

We do not test any result against a null distribution. No permutation test
against random vocabulary draws has been constructed, and no claim in §4 should
be read as a claim of statistical significance.

## 4 Results

### 4.1 The register axis

Figure `axis_projection_hu.png` shows register scores by family, with the
ranges of the two anchor sets shaded. Figure `distance_scatter_hu.png` shows
the underlying quantities, cosine distance to each of the two centroids,
plotted against each other.

The Latinate diagnostic adjectives cluster at the clinical end and sit within
the clinical anchor's own range: *traumás** at -0.36, *bipoláris* at [≈ -0.30],
*toxikus* at [≈ -0.29], *pszichotikus* at [≈ -0.27], *fóbiás** at [≈ -0.21],
*mániás* at [≈ -0.22]. A second group sits between the poles without reaching
either: *szkizofrén** (-0.15), *autista** (-0.16), *neurotikus* [≈ -0.12],
*függő* [≈ -0.11], *hiperaktív* [≈ -0.10], *depressziós* [≈ -0.07],
*kényszeres* [≈ -0.07], *abnormális* [≈ -0.05].

The madness family spans from the middle of the range to beyond the colloquial
anchor's lower bound. *Abnormális*, *zakkant** and *elmebeteg** sit near the
midpoint; *beszámíthatatlan* just past it; then *flúgos* (+0.17), and a block
of eight words from *hibbant* [≈ +0.25] to *tébolyult* [≈ +0.35], with
*eszelős* at +0.35. Nine members of the family score more colloquial than any
word in any other target family.

The size of this spread is what the family was selected for, as §2.1 concedes.
The relative position of the family as a whole is not: the diagnostic families
occupy the clinical half of the axis almost without exception, and the
colloquial half of the axis is populated almost entirely by madness terms plus
three outliers (*hisztis* [≈ +0.19], *megszállott** [≈ +0.29], *paranoiás**
[≈ +0.10]).

### 4.2 The valence axis

Figure `valence_map_hu.png` plots register against orthogonalised valence. Two
observations.

The colloquial end of the register axis is not uniform in valence. Within the
madness family, *flúgos*, *habókos*, *dilis* and *bolond** fall between -0.04
and +0.08, effectively neutral, while *őrült*, *tébolyult* and *eszelős* fall
between -0.14 and -0.24. Since these two groups have nearly identical register
scores, the difference between them is not a register difference. Descriptively,
the Hungarian colloquial vocabulary of madness contains a mild and a harsh
register-equivalent series, and the distinction is visible in the geometry.

The most obvious alternative reading is frequency. *Őrült* is a common word and
*habókos* is not, and it is plausible that frequent madness terms accumulate
condemnatory contexts that rare ones do not, in which case the split is a
frequency effect wearing morphological clothing. Thirteen words cannot
adjudicate this. We record the split and flag the confound.

Second, *autista** and *szkizofrén** do not behave as pejoration cases. Their
register scores are mid-range (-0.16 and -0.15), and their valence scores are
+0.13 and -0.11 respectively: one mildly positive, the other mildly negative,
neither colloquial-and-strongly-negative. This result held across two
independent revisions of the word list, though we note that both revisions used
the same instrument and the same orthogonalisation, so the repetition is not
evidence of independence in the way a replication across instruments would be.

An important scope caveat attaches to this null. The valence anchor is built
from generic affect adjectives. It is an appropriate instrument for ordinary
positive-negative sentiment and not obviously an appropriate one for detecting
that a word is used as a slur against a diagnostic identity, which is a
narrower and structurally different kind of negativity. The flat result for
*autista** and *szkizofrén** is therefore consistent with two accounts we
cannot separate: that pejorative use is not present in this corpus, or that it
is present and the instrument is not scoped to see it.

### 4.3 The midpoint is not a register

*Elmebeteg** and *beszámíthatatlan* form a pair that the one-dimensional axis
handles badly. Both sit near the register midpoint (+0.05 and [≈ +0.07]) while
scoring clearly negative on valence (-0.18 and [≈ -0.23]), a combination that
occurs nowhere else in the target set. Both are adjacent in the MDS layout.

Our reading, offered as speculation and committed to: these are
legal-administrative rather than clinical or colloquial vocabulary.
*Beszámíthatatlan* is a term of art about criminal responsibility, and
*elmebeteg* is the term that survived in legal and journalistic usage after
clinical Hungarian abandoned it. Their negativity comes from the topical
company they keep, crime reporting and court proceedings, rather than from
evaluative use.

If this is right, it identifies a structural limitation rather than an
anomaly. A two-pole axis has one place to put a word belonging to a third
register, and that place is the middle, where it is indistinguishable from a
word genuinely intermediate between the two poles. The reading is testable by
inspecting nearest neighbours; if they are dominated by *bűncselekmény*,
*elkövető* and *kényszergyógykezelés*, the account is supported. We have not
run that check.

### 4.4 Trauma

*Traumás** is the most clinical-scoring word in the target set (-0.36), while
*traumatizált* sits essentially at the midpoint (-0.01). This is a large split
within a single lemma family and nothing in the design predicts it.

In the MDS layout, *traumás** falls among *malignus*, *benignus*, *patológiás*
and *szisztémás*. We take this as suggestive of sense conflation: *traumás* in
general Hunganian text is heavily associated with physical injury (*traumás
sérülés*, *traumatológia*), and a static embedding assigns one vector to both
senses. On this reading the word's clinical score is accurate but is a score
for the wrong sense, and the trauma family is an illustration of a general
property of the method rather than an open question about register. A nearest
neighbour check would settle it; again, we have not run it.

## 5 Discussion

### 5.1 What the axis measures

We have been calling the first dimension a register axis. There is a reading on
which that label is wrong, and we think it should be stated plainly rather than
buried in the limitations.

*Tébolyult* and *eszelős* score among the most colloquial words in the target
set. Neither is colloquial: both are literary and somewhat archaic, and neither
would appear in casual speech. What they share with the colloquial anchor is
not informality but evaluativeness. The anchor is composed of subjective
appraisal terms, while the clinical anchor is composed of referential,
non-evaluative descriptors. On this reading, the axis measures something closer
to subjectivity, in roughly the sense of the appraisal and opinion-mining
literature (Wiebe et al. 2005), and register correlates with it only because
technical writing avoids appraisal.

Register and subjectivity coincide across most of the vocabulary, which is why
the axis behaves sensibly nearly everywhere. They come apart at the literary
items, and there they come apart in the direction the subjectivity reading
predicts. We consider the subjectivity reading more likely than not, and we
note that it is diagnosable: a set of colloquial but non-evaluative items
(*cucc*, *ilyesmi*, *sima*) and formal but evaluative ones (*kiváló*,
*aggályos*, *elhanyagolható*) would separate the two accounts directly. Until
that test is run, the axis label should be read as provisional.

### 5.2 The origin has no interpretation

Most target words score negative. It would be natural to read this as most of
the vocabulary being clinical-leaning, and we think that reading is unsafe.

The clinical anchor averages 15 semantically homogeneous items and retains a
long, well-oriented mean vector. The colloquial anchor averages 49 items
spanning both valences, which partially cancel, leaving a shorter and less
coherent centroid and inflating cosine distance to it for every word in the
vocabulary. Where zero falls on the axis is therefore a function of anchor set
size and internal dispersion, not a property of the words. Statements about
which side of zero a word falls on are statements about an arbitrary point.

The remedy is a baseline: the distribution of register scores for a
frequency-matched random sample of the vocabulary, against which target scores
can be positioned. This is the same gap as the missing significance test, but
it is broader, since without the baseline even the descriptive statement is
unanchored. The relative ordering of target words, which is what §4 mostly
reports, does not depend on it.

### 5.3 What the map is for

The value of a descriptive map is that it makes subsequent questions
answerable. Three that this one raises: whether the mild and harsh colloquial
series of §4.2 are distinguished morphologically or by frequency; whether the
forensic register of §4.3 constitutes a third pole worth modelling explicitly;
and whether the axis recovers graded register judgements when checked against
human ratings, which is the question that would convert this exercise into a
validation study of the kind Grand et al. (2022) carried out for object
features. We regard the third as the most consequential and the cheapest to run.

## 6 Limitations

**The instrument is unvalidated.** No human judgements of Hungarian register
were collected, so we cannot say whether the ordering in §4.1 corresponds to
anything speakers know. This is the limitation that bounds every other claim.

**One corpus, one model, no diachrony.** All results come from a single static
embedding. If the corpus provenance is as documented, its text predates
contemporary informal Hungarian web writing by roughly two decades, which means
the colloquial pole is anchored in the informal usage of an earlier period and
recent items are poorly represented or absent. Nothing here bears on change over
time in either direction.

**Sense conflation.** A static embedding assigns one vector per word form. §4.4
gives the clearest case; *bolond*, *zakkant*, *megszállott* and *függő* all have
non-madness senses of some frequency, and their scores are correspondingly
averaged over senses in unknown proportions.

**Anchor asymmetry and size.** 15 against 49, drawn from neighbourhoods of
unequal semantic breadth. §5.2 gives the main consequence.

**Uncertainty is understated.** The reported dispersion captures anchor
resampling only, not corpus sampling or training seed (Antoniak and Mimno 2018).

**No null model.** No result has been tested against a null distribution.

**Part-of-speech purity.** Fourteen items are corpus-verified dual-category and
marked with an asterisk; the word list is "intended part of speech", not
verified part of speech.

## 7 Conclusion

We have described the position of a set of Hungarian psychiatric and everyday
adjectives on two derived dimensions of a word embedding, one running from
clinical to colloquial anchors and one carrying evaluative polarity
orthogonally to it. The Latinate diagnostic adjectives occupy the clinical end
tightly; the native madness vocabulary spreads across the whole range and
divides at its colloquial end into a near-neutral and a clearly negative
series; and two words of forensic provenance sit at a midpoint that, we argue,
represents the absence of a third pole rather than an intermediate position
between the two poles present. We have flagged, at each point, the alternative
reading we consider most serious: that the first axis measures evaluative
subjectivity rather than register, that the position of its origin is an
artefact of anchor construction, and that the valence instrument is not scoped
to the kind of negativity that pejorative use of a diagnostic label would
involve. The map is offered as a description. Whether it is a description of
register is the next question, and it is answerable with a norming study.

---

## Bibliography

Verification status: **[V]** = bibliographic details confirmed against ACL
Anthology, publisher page, or the resource's own documentation during drafting.
**[U]** = from memory, not checked, verify before submission.

**[V]** An, Jisun, Haewoon Kwak & Yong-Yeol Ahn. 2018. SemAxis: A lightweight
framework to characterize domain-specific word semantics beyond sentiment. In
*Proceedings of the 56th Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers)*, 2450–2461. Melbourne: Association for
Computational Linguistics.

**[V]** Antoniak, Maria & David Mimno. 2018. Evaluating the stability of
embedding-based word similarities. *Transactions of the Association for
Computational Linguistics* 6. 107–119. doi:10.1162/tacl_a_00008.

**[U]** Biber, Douglas & Susan Conrad. 2009. *Register, genre, and style*.
Cambridge: Cambridge University Press.

**[U]** Caliskan, Aylin, Joanna J. Bryson & Arvind Narayanan. 2017. Semantics
derived automatically from language corpora contain human-like biases.
*Science* 356(6334). 183–186. *(Cited in an earlier draft as the origin of the
target-set-versus-anchor-set design; currently uncited in this draft. Keep or
cut.)*

**[V]** Grand, Gabriel, Idan A. Blank, Francisco Pereira & Evelina Fedorenko.
2022. Semantic projection recovers rich human knowledge of multiple object
features from word embeddings. *Nature Human Behaviour* 6(7). 975–987.
doi:10.1038/s41562-022-01316-8.

**[V]** Halácsy, Péter, András Kornai, László Németh, András Rung, István Szakadát
& Viktor Trón. 2004. Creating open language resources for Hungarian. In
*Proceedings of the Fourth International Conference on Language Resources and
Evaluation (LREC'04)*. Lisbon: ELRA. *(Author list is from the LREC anthology
record and should be double-checked against the paper itself.)*

**[V]** Hamilton, William L., Kevin Clark, Jure Leskovec & Dan Jurafsky. 2016.
Inducing domain-specific sentiment lexicons from unlabeled corpora. In
*Proceedings of the 2016 Conference on Empirical Methods in Natural Language
Processing*, 595–605. Austin, TX: Association for Computational Linguistics.
doi:10.18653/v1/D16-1057.

**[V]** Haslam, Nick. 2016. Concept creep: Psychology's expanding concepts of
harm and pathology. *Psychological Inquiry* 27(1). 1–17.
doi:10.1080/1047840X.2016.1082418.

**[U]** Haslam, Nick, Brodie C. Dakin, Fabian Fabiano, Melanie J. McGrath,
Joshua Rhee, Ekaterina Vylomova, Morgan Weaving & Melissa A. Wheeler. 2020.
Harm inflation: Making sense of concept creep. *European Review of Social
Psychology* 31(1). 254–286. *(Author list and pagination uncertain. This is the
paper that concedes the original 2016 characterisation was inaccurate in
several respects, which is worth citing if §1 keeps its disclaimer about
diachrony.)*

**[V]** Kozlowski, Austin C., Matt Taddy & James A. Evans. 2019. The geometry of
culture: Analyzing the meanings of class through word embeddings. *American
Sociological Review* 84(5). 905–949. doi:10.1177/0003122419877135.

**[U]** Mikolov, Tomas, Kai Chen, Greg Corrado & Jeffrey Dean. 2013. Efficient
estimation of word representations in vector space. arXiv:1301.3781.

**[V]** Nemeskey, Dávid Márk. 2020. *Natural language processing methods for
language modeling*. Budapest: Eötvös Loránd University dissertation. *(Cite only
if the corpus turns out to be Webcorpus 2.0 after all.)*

**[V]** Oravecz, Csaba, Tamás Váradi & Bálint Sass. 2014. The Hungarian Gigaword
Corpus. In *Proceedings of the Ninth International Conference on Language
Resources and Evaluation (LREC'14)*, 1719–1723. Reykjavik: ELRA. *(Cite only if
the corpus turns out to be MNSZ2.)*

**[V]** Váradi, Tamás. 2002. The Hungarian National Corpus. In *Proceedings of
the Third International Conference on Language Resources and Evaluation
(LREC'02)*, 385–389. Las Palmas: ELRA.

**[U]** Wiebe, Janyce, Theresa Wilson & Claire Cardie. 2005. Annotating
expressions of opinions and emotions in language. *Language Resources and
Evaluation* 39(2–3). 165–210. *(Placeholder for the subjectivity literature in
§5.1. There may be a better anchor citation; check the appraisal-theory side
too, e.g. Martin & White 2005.)*

**[U]** `hunembed0.0`. Word2vec embedding for Hungarian, 600 dimensions,
frequency cut-off 10. *(No paper located. Find the citable source or cite the
distribution URL with an access date.)*

---

## Appendix A: figures

| File | Content | Status |
|---|---|---|
| `axis_projection_hu.png` | Register scores by family, anchor ranges shaded, anchor-sensitivity bars | Referenced in §4.1. Consider lightening the error bars given §3. |
| `distance_scatter_hu.png` | Cosine distance to each centroid, plotted against each other | Referenced in §4.1. Keep: it shows the low-frequency items sitting far from both poles, which the projection figure hides. |
| `valence_map_hu.png` | Register by orthogonalised valence, anchors shown | Referenced in §4.2, §4.3. This is the paper's centrepiece. |
| `mds_map_hu.png` | Two-dimensional MDS of all words | Not referenced except informally in §4.3 and §4.4 for adjacency. **Recommend cutting.** Stress for 110 points from 600 dimensions will be high enough that proximity is not interpretable, and readers will interpret it anyway. If kept, report stress and caption it as a layout aid, not a map. |

## Appendix B: work not done

Listed so that nothing in the draft implies otherwise.

1. Nearest-neighbour inspection for *traumás**, *elmebeteg**,
   *beszámíthatatlan*. Cheap, and would settle §4.3 and §4.4.
2. Frequency-matched random-vocabulary baseline for the register axis (§5.2).
3. Permutation test against a null for either axis.
4. Subjectivity-versus-register diagnostic set (§5.1).
5. Norming study against human register judgements (§5.3, §6).
6. Frequency covariate for the valence split in §4.2.

Items 1 and 2 are needed for the current draft to be accurate. Items 3 to 6 are
needed only if the claims strengthen beyond description.
