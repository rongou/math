# Literature scope: partition-function defect and full transfer gap

**Audit date:** October 9, 2026. **Type:** bounded primary-source literature check, not a proof audit or a priority assessment. The parent has completed the finite-volume argument; it is not reproduced here.

## 1. Conclusion at this stopping point

**Whether the exact defect criterion was already known is not determined. No independent external exact match was located in the primary-source passages verified in this check.** This is not a finding of novelty, and does not warrant “new,” “first,” or “previously unknown.”

The target is the following particular combination of input and conclusion:

\[
D_d(n)=2^d\log Z(n,\ldots,n)-\log Z(2n,\ldots,2n),
\]

with **ordinary, untwisted periodic partition functions**, a sufficiently small defect at **one starting size**, and a **full transfer-gap lower bound uniform along the dyadic cubes**. For the Wilson application, “full” means the physical gauge-invariant transfer space, not a selected glueball, parity, or electric-flux channel.

Positive Wilson transfer matrices, reflection/chessboard inequalities, and several kinds of finite-size criterion have authoritative precedents. The verified results below do **not** identify the exact displayed criterion: they either provide its operator framework, use twisted partition functions, control specified correlations, or impose frustration-free Hamiltonian hypotheses. These distinctions, rather than a discovery claim, are the useful outcome of this check.

## 2. Repository provenance and division of work

- The local *Sharp mass bounds for the two-dimensional O(4) model* (September 23, 2026), **Section 2, Proposition 2.2, printed/PDF p. 11**, is the literal two-dimensional instance. Its statement uses the square defect, even `n >= 4`, threshold `2^-10`, and a uniform bound on the full transfer ratio at circumferences `2^k n`. Source: `preprints/Sharp-mass-bounds-for-the-two-dimensional-O4-model-September-23-2026/build/sections/finite-volume.tex`, labels `eq:Delta` and `prop:criterion`; statement also checked in the accompanying `paper.pdf`. This is local provenance, **not independent external literature evidence**, and its dimension-two constant is not imported into dimension four here.
- The Family215 scope document, `lean/docs/215.md`, explicitly excludes the infinite-volume limit and the separate O(4) spectral-gap claim from the described formalization. Do not cite that family label as certification of the present full-gap criterion.
- The concrete SU(2) transfer interface and overlapping source verification belong to [su2_transfer_interface.md](su2_transfer_interface.md), especially its **Primary bibliography and source audit**, Sections 6–7, and scope caveats. Per the user's handoff, its verified LNWW92 and OS78 locators are imported below and explicitly distinguished from passages independently read in this literature pass. None of its operator proofs or small-beta calculations is duplicated.

## 3. Transfer-matrix and reflection-positivity references

Page locators refer to the stated version. PDF pages are **one-based**. A journal's complete page range is bibliographic metadata, not a claim to have checked every page.

### [L76/L77] Original positive Wilson transfer construction — directly inspected

**M. Lüscher, *Construction of a selfadjoint, strictly positive transfer matrix for Euclidean lattice gauge theories*. Communications in Mathematical Physics 54 (1977), 283–292; original preprint DESY 76/54 (1976).**

Sources: [DESY original preprint](https://bib-pubdb1.desy.de/record/396349/files/7611148.pdf); [publisher record and DOI](https://link.springer.com/article/10.1007/BF01614090).

**Checked passages:** DESY Section II.A, printed p. 5, spatial-link Hilbert space/kernel representation; Section II.B, printed pp. 7–9, **Proposition 1**, equations **(17), (20)–(23)**; Section II.C, printed p. 11, **Proposition 2** and the physical-state discussion. Printed pp. 8–9 share PDF p. 7. The setup includes four-dimensional SU(N) Wilson theory; the gauge part is relevant to SU(2).

**Use:** cite for explicit transfer construction and the character-positivity method. Do not turn strict positivity into a spatial-volume-uniform gap, a bounded inverse, or an assertion of pure-gauge vacuum uniqueness. The companion audit makes these distinctions explicitly. These are DESY locators, **not silently converted journal page numbers**. No defect criterion is identified here.

### [LNWW92] Gauge projection and boundary normalization — companion-verified original

**M. Lüscher, R. Narayanan, P. Weisz, and U. Wolff, *The Schrödinger Functional — a Renormalizable Probe for Non-Abelian Gauge Theories*. Nuclear Physics B 384 (1992), 168–228.**

Sources: [original preprint, hep-lat/9207009v1](https://arxiv.org/pdf/hep-lat/9207009v1); [publisher DOI](https://doi.org/10.1016/0550-3213(92)90466-O).

**Verified in the companion audit:** Section **4.2**, printed preprint **pp. 23–24 / PDF pp. 24–25**, equations **(4.4)–(4.7)**: half-weight spatial boundary plaquettes, normalized invariant measure, and the physical projector in (4.7), including its footnote.

**Use:** authoritative normalization/projection reference. Its Schrödinger-functional boundary formula must not be relabeled a periodic-torus trace theorem or a finite-size gap criterion. The companion audit separately supplies the periodic identity. This pass imports its source verification; it does not independently claim to have reread these pages.

### [OS78] Original lattice gauge reflection positivity — companion-verified theorem

**K. Osterwalder and E. Seiler, *Gauge field theories on a lattice*. Annals of Physics 110 (1978), 440–471.**

Sources: [publisher article](https://www.sciencedirect.com/science/article/pii/0003491678900398); [DOI](https://doi.org/10.1016/0003-4916(78)90039-8); [companion source audit](su2_transfer_interface.md).

**Verified in the companion audit:** Section **2.1**, pp. **442–445**, especially equation **(2.9)**; Section **2.3**, **Theorem 2.1, p. 448**, with the positive-cone argument and Lemmas **2.2–2.4** on pp. **448–449**. Its discussion on **p. 450** uses a **two-unit shift**; it is not the citation being used for one-step positivity or exact periodic normalization.

This literature pass independently read the publisher abstract, not the article scan. The abstract reports physical positivity and strong-coupling infinite-volume/confinement results. The detailed locators above are delegated verification as authorized by the user. Neither that abstract nor these positivity passages establish the target defect implication.

### [MP87] Site-reflection positivity — publisher-verified bibliographic supplement

**P. Menotti and A. Pelissetto, *General proof of Osterwalder-Schrader positivity for the Wilson action*. Communications in Mathematical Physics 113 (1987), 369–373.**

Source: [publisher article / DOI 10.1007/BF01221251](https://link.springer.com/article/10.1007/BF01221251).

The **publisher abstract** explicitly extends the Osterwalder–Seiler argument to reflection planes containing sites, for the Wilson action with fermions. This is relevant to distinguishing site and link reflections, not an exact defect match. **Full text was not obtained here; no internal theorem number or narrower page attribution is asserted.**

### [DMG09] Physical trace versus selected spectral sectors — directly inspected

**Michele Della Morte and Leonardo Giusti, *Symmetries and exponential error reduction in Yang-Mills theories on the lattice*. Computer Physics Communications 180 (2009), 819–826.**

Sources: [original preprint, arXiv:0806.2601v2](https://arxiv.org/pdf/0806.2601v2); [publication metadata](https://arxiv.org/abs/0806.2601); [DOI](https://doi.org/10.1016/j.cpc.2009.03.009).

**Checked passages:** Sections **2.1–2.2**, printed preprint **pp. 3–4 / PDF pp. 4–5**, equations **(2.6)–(2.19)**, including the gauge projector and partition-function trace; Section **3**, printed **p. 6 / PDF p. 7**, equations **(3.12)–(3.13)**, separating parity-even and parity-odd spectral sums.

This paper explicitly works with **four-dimensional SU(3)** Wilson theory, not SU(2), and credits the older transfer construction. It is useful corroboration of the distinction between a complete physical trace and channel-restricted partition functions. Its numerical error-reduction method is **not** a volume-uniform full-gap theorem, and its SU(3) results are not imported as an SU(2) theorem.

## 4. Related finite-size and partition-function results

### [FILS78] Original systematic reflection/chessboard framework — directly inspected

**J. Fröhlich, R. Israel, E. H. Lieb, and B. Simon, *Phase transitions and reflection positivity. I. General theory and long range lattice models*. Communications in Mathematical Physics 62 (1978), 1–34.**

Sources: [author-hosted published paper](https://math.caltech.edu/SimonPapers/93.pdf); [DOI](https://doi.org/10.1007/BF01940327).

**Checked passages:** **Theorem 2.1, p. 5**, on preservation of reflection positivity in the specified interaction class; **Theorems 4.1–4.3, pp. 19–21**, giving abstract and rectangular-lattice chessboard estimates, with the distinction between reflections through sites and between sites.

**Related machinery, not an exact match.** These are reflection/Schwarz bounds for observables and their reflected repetitions. The displayed theorems do not state that the unmodified two-cube logarithmic defect at one scale controls the complete transfer spectrum on larger cubes. The source itself discusses earlier antecedents; “systematic framework” should not be mistaken for a claim that this paper originated all reflection arguments.

### [S80] An actual finite-volume correlation criterion — directly inspected

**Barry Simon, *Correlation inequalities and the decay of correlations in ferromagnets*. Communications in Mathematical Physics 77 (1980), 111–126.**

Source: [author-hosted published paper](https://math.caltech.edu/SimonPapers/127.pdf).

**Checked passages:** **Theorem 1.3, p. 112**, a contraction criterion for exponential decay; **Theorem 2.2, p. 116**, explicitly credited to Lieb, with a correlation computed in a restricted region; **Theorem 4.3, pp. 120–121**, equation **(4.6)**, a finite-volume procedure whose critical-temperature bounds converge.

**Related, not exact.** The finite test uses boundary sums of finite-volume **Ising correlations with free boundary conditions**, supported by ferromagnetic correlation inequalities. It is not a test of two ordinary periodic partition functions. Its stated correlation conclusion is not the requested all-sector transfer-gap statement for Wilson SU(2). The attribution to Lieb within Simon's paper is retained rather than treating every displayed result as Simon's alone.

### [TY85] Original SU(2) twist/confinement source — original identified; theorem read in [K09]

**E. T. Tomboulis and L. G. Yaffe, *Finite temperature SU(2) lattice gauge theory*. Communications in Mathematical Physics 100 (1985), 313–341.**

Source: [publisher article / DOI 10.1007/BF01206134](https://link.springer.com/article/10.1007/BF01206134).

The publisher abstract and bibliographic record were inspected. The original full text was not accessible in this pass, so **no original appendix page or equation number is claimed as verified**. Kanazawa's original extension paper [K09], Section 2.1, identifies this as the original source and explicitly restates its SU(2) inequality as **Theorem 1, equation (4), preprint p. 5**.

That inspected restatement bounds a Wilson loop using the **twisted-to-untwisted partition-function ratio on the same torus**. Its confinement conclusion is not the target full-transfer-gap conclusion. Cite Tomboulis–Yaffe as the original result, and identify Kanazawa as the source actually consulted for this formula; do not transfer Kanazawa's theorem numbering to the 1985 paper.

### [K09] Closest verified partition-function/RP analogy — directly inspected

**Takuya Kanazawa, *Generalizing the Tomboulis-Yaffe Inequality to SU(N) Lattice Gauge Theories and General Classical Spin Systems*. Annals of Physics 324 (2009), 1634–1665.**

Sources: [original preprint, arXiv:0808.3442v3](https://arxiv.org/pdf/0808.3442v3); [version/publication record](https://arxiv.org/abs/0808.3442); [DOI](https://doi.org/10.1016/j.aop.2009.04.002). Locators use **v3, April 2, 2009**, not the PDF's later auto-generated title-page date.

**Checked passages:** Section **2.1**, preprint **pp. 4–5**, equations **(2)–(4)** and **Theorem 1**; Section **3.2**, **Theorem 5, p. 17**, assumptions **(99)–(100)** and bound **(101)**; **p. 21**, equation **(135)** and accompanying decay interpretation.

**Not exact.** The inputs are twisted wall/vortex free energies. The spin theorem requires zero group average of each individual insertion, condition (100), and bounds the specified two-point function. Thus its abstract's mass-gap language must not be substituted for an all-observable, including invariant-sector, theorem. The dyadic condition concerns separation versus one torus period; it is not the requested one-scale ordinary-defect propagation through growing cubes.

### [Kn88] Original Hamiltonian finite-size criterion — original identified; precise restatement in [GM16]

**Stefan Knabe, *Energy gaps and elementary excitations for certain VBS-quantum antiferromagnets*. Journal of Statistical Physics 52 (1988), 627–638.**

Source: [publisher article / DOI 10.1007/BF01019721](https://link.springer.com/article/10.1007/BF01019721).

The publisher abstract confirms lower bounds obtained by diagonalizing a finite system. The original full text was not obtained here. **Its internal theorem numbering is not asserted.** The precise result was inspected in the primary extension [GM16], which explicitly labels its **Theorem 1 and Corollary 2, preprint p. 5**, as Knabe's result.

This establishes a genuine finite-size-gap precedent, but in the specified frustration-free spin-Hamiltonian setting, not a two-partition-function defect criterion.

### [GM16] A primary extension with explicit finite-size thresholds — directly inspected

**David Gosset and Evgeny Mozgunov, *Local gap threshold for frustration-free spin systems*. Journal of Mathematical Physics 57 (2016), 091901.**

Sources: [original preprint, arXiv:1512.00088v1](https://arxiv.org/pdf/1512.00088v1); [DOI](https://doi.org/10.1063/1.4962337).

**Checked passages:** Section **2**, preprint **p. 5**, including the finite-dimensional, translation-invariant, nearest-neighbor projector and frustration-free hypotheses; **Theorem 1 / Corollary 2** restating Knabe; **Theorem 3**, their improved criterion. The local-gap thresholds are respectively `1/(n-1)` and `6/[n(n+1)]`.

**Related, not exact.** These compare an open-subchain Hamiltonian gap with periodic-chain gaps, rather than ordinary partition functions at two cube sizes. Reflection positivity by itself does not establish the listed frustration-free projector hypotheses for the Wilson transfer Hamiltonian. No applicability reduction to that class was verified here.

### [DS87] Constructive partition-function/decay literature — scope lead, not theorem-checked

**R. L. Dobrushin and S. B. Shlosman, *Completely analytical interactions: Constructive description*. Journal of Statistical Physics 46 (1987), 983–1014.**

Source: [publisher article / DOI 10.1007/BF01011153](https://link.springer.com/article/10.1007/BF01011153).

The **publisher abstract** describes twelve equivalent types of conditions involving partition-function analyticity, correlation decay, truncated correlations, and asymptotics of `log Z`, with verification reduced to bounded-size volumes. Its stated partition-function example involves **complex perturbations and nonvanishing**, not the displayed real two-cube defect. Full text was not obtained; internal theorem/page locators and a complete exclusion of an equivalent formulation are **not verified**. This is an important limitation on any broad assertion that finite-volume partition-function criteria are absent from earlier literature.

## 5. Search boundary, evidence limits, and safe use

The bounded search combined title-led retrieval of the above works with queries including:

- `"reflection positivity" "finite-size criterion"`;
- `"partition functions" "finite-volume criterion"`;
- `"partition function" "mass gap criterion"`;
- `"log Z" "doubling" "gap"`;
- `"partition function" "dyadic" "reflection"`;
- `"finite size" "criterion" "lattice gauge"`.

Searches targeted primary-paper/author and official archive domains, including arXiv, Springer, Project Euclid, CERN/DESY, APS, ScienceDirect, and Caltech author copies. Some formula/phrase searches returned no results; others did not yield a verified match. **Neither outcome establishes absence**, especially for older scanned papers. Publisher abstracts were not promoted into full-text verification. General web summaries and online claimed Millennium solutions were not used as mathematical evidence. The delegated OS78/LNWW92 passage checks are identified explicitly above.

There was no exhaustive citation-forward search, survey of every constructive field-theory book, or complete review of all finite-size criteria. Original-text access limitations remain particularly relevant for TY85, Kn88, DS87, and MP87. The stopping point follows the user's request to finish with verified material.

**Recommended attribution:** cite Lüscher and the companion audit's OS78/LNWW92 locators for the Wilson transfer framework; FILS78 for reflection/chessboard machinery; and S80, TY85/K09, Kn88/GM16 as **related but distinct** finite-size results. Describe the exact ordinary-defect implication as the criterion proved in the parent document, with its relation to prior formulations **not determined by this bounded check**. This audit supplies no additional claim about useful weak-coupling smallness of the defect, cutoff-uniform physical masses, or a continuum Yang–Mills construction.
