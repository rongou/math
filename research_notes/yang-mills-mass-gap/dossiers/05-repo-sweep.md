# Dossier 05: Repository sweep for a Yang–Mills mass-gap program (beyond family 215)

Written 2026-10-09 for the `yang-mills-mass-gap` workflow. Scope: the whole OpenAI math release at
`/home/rou/src/math` (719 manuscripts in 372 families, plus the Lean library). Family 215 (the O(3)/O(4)/O(n)
sigma-model papers) is covered by other dossiers. It appears here only where its *techniques* or *Lean
artifacts* are relevant to the sweep.

**Epistemic labels used throughout.**
- **[SRC]**: the source states or proves this. I give file:line or a theorem label.
- **[STD]**: standard expert knowledge, not taken from the repo.
- **[MINE]**: my own analysis or speculation. Treat it as a hypothesis.
- **[UNVERIFIED]**: an unformalized claim from an AI-generated manuscript. The repo itself warns that
  such claims "could have issues" (`README.md`), and it has already withdrawn three papers.

Unless stated otherwise, none of the repository papers named below has been independently refereed. "Proved"
in a section heading means "claimed proved by the manuscript".

---

## 0. Executive summary

1. **Nothing in the repository constructs, or even treats, a quantum gauge theory in d ≥ 3.** A full-text
   grep of all 8,007 TeX files under `preprints/*/build` for "Yang–Mills" finds only 9 lines in 5
   papers. All are background citations or the BFSS model (§2.4). There is no lattice gauge theory, no Wilson
   loop expectation, no plaquette action, and no Bałaban gauge-RG content. Bałaban's gauge papers are
   cited exactly once, in a history paragraph of the O(3) paper
   (`The-canonical-massive-continuum-limit-…/build/sections/history.tex:80-83`).
2. **The transferable material is methodological** and sits in a small cluster of families. It is listed
   here in descending relevance:
   - (a) the **reflection-positivity → positive transfer operator → "purity bootstrap" finite-box gap
     criterion**, which appears independently in the sharp O(4) paper (215) and the Haldane-gap paper (268);
   - (b) the **exact block-RG and conditional-averaging machinery with a reflection-positive radial
     transfer space**, from 218 (weakly interacting Ising universality) and 216 (BKT);
   - (c) the **gauge-invariant Hilbert space and Gauss-law handling for SU(N) matrix quantum mechanics** in
     270 (BFSS). This is relevant to the small-volume/Hamiltonian corner of YM, and it is the only
     repository work with a nonabelian gauge group acting on a quantum Hilbert space;
   - (d) the **axiomatic and modular-theory machinery** of 282 (4D scale ⇒ local conformal Ward identities)
     and 280 (VOAs ⇒ conformal nets);
   - (e) the **gap ⇒ area-law/PEPS** results of 265 and the **dimension-uniform Poincaré/spectral-gap**
     results of 227. These are useful consequences or structural analogues, not inputs.
3. **The Lean formalization of family 215 covers only the 20-page all-temperature O(n) decay theorem.**
   The statement is 60 lines (`lean/ComparatorChallenges/ClassicalON.lean`) and the proof is 117 files and
   12,907 lines. It uses only the axioms `propext`, `Quot.sound` and `Classical.choice`. The O(3) continuum
   limit, the O(4) gap papers, OS reconstruction and the 4-point function are **not** formalized
   (`lean/docs/215.md`). Neither are 216, 225, 232, 233, 265, 268, 270 or 282.
4. **Formal QFT infrastructure is essentially absent.** The repo's Lean code, the pinned Mathlib
   `d13f23b7` (2026-09-24) and Lean `v4.34.1` together contain: finite-volume Gibbs measures on products of
   spheres (ad hoc, in ClassicalON); Haar measure on SU(N)/U(N) (Mathlib's `Measure.haarMeasure`, used in
   BFSS); test functions, Schwartz space and tempered distributions (Mathlib); unbounded self-adjoint
   operators via `LinearPMap` (Mathlib); quasi-local C*-algebras, states and KMS states (built ad hoc in the
   Heisenberg challenge); and conformal nets with von Neumann algebras (built ad hoc in the VertexAlgebraNet
   challenge). There is **no** reflection positivity in the OS sense, no OS reconstruction, no Wightman
   axioms, no transfer-operator theory, no Bochner–Minlos theorem, no Schwartz kernel theorem (Mathlib lists it only as a future goal,
   `Analysis/Distribution/Distribution.lean:78-81`), no Stone theorem for unbounded generators,
   no lattice gauge fields, and no Peter–Weyl theorem. Mathlib does have covariant derivatives on vector
   bundles but no principal bundles or curvature.
5. **The error-rate signal is real and recent.** On 2026-10-07 the repo withdrew 3 papers. All three
   descend from one sign error in a stabilization-trace argument (the Hodge chain). It also revised 14 others
   (13 with mathematical repairs or clarified hypotheses; 1 citation-only), 4 of them in the
   lattice-model or probability area (families 232 and 233). In the
   lattice-model families, those revisions repaired exactly the multiscale, boundary-attachment and
   crossing arguments that a YM program would borrow. Unformalized 100+ page analytic papers should be
   treated as **strong heuristics with unknown defect density**, not as citable lemmas (§4).

---

## 1. Method of the sweep

- I extracted all 372 family headers from `CONTENTS.md` (9,142 lines). I also ran keyword scans over (i)
  `CONTENTS.md` abstracts and (ii) all 8,007 TeX files under `preprints/*/build` (135 MB). The scans covered
  gauge-related terms (gauge, connection, holonomy, Wilson loop, plaquette, Yang–Mills, instanton, Uhlenbeck),
  axiomatic QFT (Osterwalder, Schrader, Wightman, Schwinger function, reflection positivity, chessboard),
  spectral and transfer terms (transfer operator or matrix, spectral gap, mass gap), RG and constructive terms
  (renormalization group, block spin, multiscale, cluster or polymer expansion, Bałaban, Brydges, Gawędzki,
  Kupiainen, Glimm–Jaffe), stochastic methods (stochastic quantization, Langevin, regularity structures,
  paracontrolled), Haar, Peter–Weyl, Casimir, Gauss law and confinement. Helper scripts are in
  `research_notes/yang-mills-mass-gap/work/05-sweep/scripts/`.
- Then I read the introductions (and, where needed, the method sections) of the most relevant papers from
  TeX sources: 268, 265, 270 (both papers), 282, 216 (BKT universality), 218 (bulk Ising universality),
  232 (two-arc Lipschitz GFF), 271 (Heisenberg ferromagnet), 215 (O(4) sharp and exact; O(n) decay), and
  365.
- For Lean, I read `lean/README.md`, `lean/lakefile.lean`, `lean/lake-manifest.json`,
  `lean/lean-toolchain`, `lean/formalization.yaml` (1,783 lines, 200 `comparator_config` main-result
  entries), all 242 `lean/docs/*.md` filenames (and the relevant ones in full), and the relevant
  `ComparatorChallenges/*.lean`. I scanned all 122,458 `.lean` files under `lean/OAI` (1.8 GB). I also tallied
  `permitted_axioms` across all 416 comparator `.json` configs. To check Mathlib coverage I read (without
  building) a local Mathlib checkout at
  `/tmp/family112-build-validation.xWSfhA/project/lean/.lake/packages/mathlib`. I verified that it is
  exactly the pinned commit `d13f23b723b8a846827a245b89c10fc7d3f11612`, dated 2026-09-24.

**Negative result, stated precisely [SRC, grep].** The case-insensitive regex `Yang.{0,4}Mills` over every
TeX file in `preprints/*/build` matches only these 9 lines:
- `Positive-eigenvalues-of-the-relative-SU-2-BFSS-Hamiltonian-…/…tex:59, 212, 862, 869`. This is BFSS as a
  dimensional reduction of 10D SYM, plus Lüscher's bosonic YM Hamiltonian estimates cited at :212.
- `Determination-of-a-metric-and-a-unitary-connection-…/sections/01-introduction.tex:86, 99`. This is a
  citation, plus the remark that the theorem "imposes no Yang–Mills equation".
- One line each in the class-VII (bibliography), elasticity and Griffiths-positivity (introduction) papers.

The regex `Wilson loop|plaquette|holonom` matches many papers, but every hit is "holonomy" in geometry or
topology, or "Wilson" as in Kenneth Wilson (RG). None concerns lattice gauge theory.

---

## 2. Families relevant to a YM program, by topic

For each family I give what is claimed, the technique, and the plausible use. Page counts come from
`pdfinfo`.

### 2.1 Reflection positivity, OS reconstruction, transfer operators

**2.1.1 Family 215 (context only).** The sharp O(4) paper builds the OS Hilbert space from reflection
positivity on the periodic lattice state (`Sharp-mass-bounds-…/build/sections/introduction.tex:65-79`) and
defines the **full** mass gap as `-log ‖T_β|_{Ω^⊥}‖` (`:65-81`). The exact-O(4) paper uses the same
definition (`Exact-mass-asymptotics-…/build/sections/01-introduction.tex:26-48`). [SRC] These are the only
repository papers besides the O(3) continuum paper and the O(3) pole paper that use OS language for a
*field theory*.

**2.1.2 The purity-bootstrap finite-box gap criterion.** This is the most portable tool in the repo.
- It appears in **Sharp O(4), Prop. "Finite-volume criterion"** (`…/sections/finite-volume.tex:105-125`).
  Let K_w be the positive trace-class transfer operator on circumference w, and Z(n,w) = Tr K_w^n. Define
  p(n,w) = 2 log Z(n,w) − log Z(2n,w), q(n,w) = 2 log Z(n,w) − log Z(n,2w), and
  Δ_β(n) = 4 log Z(n,n) − log Z(2n,2n) = 2p(n,n) + q(2n,n). If Δ_β(n) ≤ 2^{-10} for some even n, then
  λ_2/λ_1 ≤ e^{-(log 2)/n} on all circumferences 2^k n. Every local limit then has full gap ≥ (log 2)/n.
  The test **cancels any free-energy term proportional to the volume**, which is why it survives
  renormalization (`introduction.tex:267-273`). [SRC, UNVERIFIED]
- It reappears independently in **268, the periodic spin-one Haldane gap, Prop. "Uniform gap from two
  initial purities"** (`The-periodic-spin-one-Haldane-gap-…/build/bootstrap.tex:123-124`). The paper uses a
  spatial transfer operator built from an Aizenman–Nachtergaele ordered bond expansion
  (`introduction.tex:144-170`). Spatial purity S(n,b) = Z_{2n}(b)/Z_n(b)^2 and thermal purity
  T(n,b) = Z_n(2b)/Z_n(b)^2 improve quadratically under squaring (Lemma "Squaring probabilities"). Exact
  cancellation identities (`bootstrap.tex:66-80`) couple the two, so both defects decay doubly
  exponentially. The gap follows from purity of the Gibbs distribution. The stated main theorem
  (`introduction.tex:37-53`): the ground state is unique for even L ≥ 60, γ_L > (4/105) log(80/79) for even
  L ≥ 60, and Δ_1 ≥ log 20/784 > 0. The finite initializations come from **rigorous interval-arithmetic
  certificates**. The paper ships with a reproducibility harness (`verification/verify.py`, which I
  inspected but did not run). The author notes that **positivity of the spatial transfer is not
  required** for the criterion (`introduction.tex:167-170`). [SRC, UNVERIFIED]
- **Use in a YM program [MINE].** This criterion is the right shape for the "finite-box decay ⇒
  infinite-volume gap" step that the O(3) architecture uses (scratch note, step 4). In d = 4 with Wilson
  action, OS positivity holds for reflections through lattice hyperplanes [STD: Osterwalder–Seiler 1978].
  So the transfer operator T is positive, and the time-doubling purity p behaves as in 2D. The
  dimension-dependent parts are the **spatial-doubling identity** (in 4D one must double three spatial
  directions, so Δ_β gets the analogous 4D combination) and the **gauge sector**: on a lattice with a Gauss
  constraint the physical transfer operator acts on gauge-invariant functions of the spatial links. Neither
  part looks fatal. The squaring lemma (`bootstrap.tex:24-47`) is pure probability. What the criterion does
  **not** supply is the small initial defect on a box of bounded *physical* size. In YM that defect is
  precisely the a priori weak-coupling decay estimate, the crux identified in the scratch notes. Expected
  status: a reusable *reduction*, not progress on the crux.

**2.1.3 Reflection positivity as a spectral tool in 2D height and Ising models (232, 218, 225).**
- **232, two-arc Lipschitz heights → GFF** (64 pp; revised 2026-10-06). Reflection through rows of sites
  gives a "positive normal transfer operator". Its spectral representation writes the gradient covariance
  as a mixture of Cauchy kernels in normal frequency. A rotation-averaging argument then pins the small-p
  density to c_*/|p|^2 (`The-Gaussian-free-field-limit-of-integer-Lipschitz-heights-with-two-arc-…/build/
  sections/01-introduction.tex:182-200`). Positive transfer powers allow analytic continuation of
  translations, adapting Duminil-Copin–Kozlowski–Lammers–Manolescu (`:199-212`). [SRC, UNVERIFIED]
- **218, conformal universality of bulk Ising correlations under weak interactions** (53 pp). Reflection
  positivity places the limiting "soft weights" in a **radial Hilbert space**, whose low spectrum contains
  the spin line (dimension 1/8) and the energy line (dimension 1). A charge identity cancels dimension 2,
  leaving O((s/R)^3), and "this extra power is decisive" for contraction of irrelevant directions
  (`Conformal-universality-of-bulk-Ising-correlations-…/build/sections/introduction.tex:119-129`). [SRC,
  UNVERIFIED]
- **Use [MINE].** These show reflection positivity used as a *quantitative spectral engine*: a radial or
  dilatation transfer operator whose spectrum gives scaling dimensions, combined with symmetry-based
  cancellation of marginal directions. A YM analogue would be a *radial-quantization transfer operator*
  around a point in the continuum or near-continuum theory. That is far from current needs, and it depends
  on conformality (true at the UV fixed point of YM, which is free). Relevance: moderate-to-low. It is
  conceptually suggestive for controlling irrelevant operators near the Gaussian UV fixed point.

**2.1.4 The Heisenberg ferromagnet (271)** notes that reflection positivity *fails* to give the needed
ferromagnetic Duhamel infrared bound (`Spontaneous-magnetization-…/build/source/sections/00-introduction.tex:
103-106`). It proceeds by loop representations and stable polynomials. Not relevant to YM. It is a
reminder that RP gives infrared bounds only in favorable sign structures. [SRC]

### 2.2 Spectral gaps for Hamiltonians (quantum many-body)

**268, spin-one Haldane gap** (30 pp + 28 pp companion). See §2.1.2. The companion gives a gap for odd open
chains with endpoint field h = 3/5: gap > log(10)/392 for L ≥ 960, and Tasaki's index −1 (`CONTENTS.md`
family 268). [SRC, UNVERIFIED] **Use:** (i) the purity bootstrap; (ii) **computer-assisted rigorous
initialization** (exact integer and rational interval enclosures of matrix-exponential traces, with a
Fox–Glynn-conditioned Poisson polynomial; `introduction.tex:132-140`). In a lattice-YM program the
analogous move would be certified computation of small-volume transfer-matrix data for SU(2) at moderate β,
used to seed a bootstrap. [MINE] For YM the seeds would have to be at weak coupling on boxes of physical size
O(1), meaning lattice size ~ exp(cβ). That is computationally infeasible as β → ∞, so this route can seed only
a fixed-β (strong- or intermediate-coupling) statement, not the continuum limit.

**265, area law and PEPS for 2D gapped systems** (90 + 56 pp). Theorem "Area law"
(`A-two-dimensional-area-law-…/build/sections/00-introduction.tex:39-58`): for any finite induced
square-lattice domain Λ, a finite-range Hamiltonian with a unique ground state and global gap Δ satisfies
S(A) ≤ C(q,R,J,Δ)|∂A|. The companion proves polynomial-bond-dimension PEPS approximation on L×L. Techniques:
quasi-local positive operators annihilating the ground state, collar mutual-information bounds, and ordered
region families. [SRC, UNVERIFIED] **Use [MINE]:** low for the Clay problem itself. Lattice Hamiltonian YM
(Kogut–Susskind) has infinite-dimensional local Hilbert spaces L²(G) per link and a Gauss constraint, so the
theorem's bounded local dimension q does not apply. It would be a *consequence* of a lattice YM gap only after
truncation. Mildly relevant to tensor-network or Hamiltonian-truncation numerics for YM.

**269, Laughlin gap** (22 pp; Lean-formalized, see `lean/docs/269.md`). Fock-space inequality
H_Q² ≥ γ H_Q with γ > 1/25. Technique: algebraic, a finite-dimensional sum-of-squares structure on the
lowest Landau level. [SRC, formalized] **Use:** essentially none for YM, except as an exemplar of an
operator inequality H² ≥ γH proved and formalized. The Lean development is 1,279 files and 77,130 lines for a
22-page paper. That is a useful calibration of formalization cost (§5.4).

**271, Heisenberg ferromagnet** (Lean-formalized, see `lean/docs/271.md`). **Use:** the formal
infrastructure (quasi-local algebra, states, KMS, infinite-volume dynamics) is the closest thing in the repo
to formal algebraic QFT (§5.2). Mathematically irrelevant to YM.

**227, SK dynamics: spectral gap / Poincaré throughout high temperature** (Lean-formalized). A
dimension-free Poincaré inequality for heat-bath dynamics. [SRC, formalized] **Use [MINE]:** only as a
model of "spectral gap of a Markov generator ⇔ decay". Stochastic-quantization approaches to YM
(Chandra–Chevyrev–Hairer–Shen) would need log-Sobolev or Poincaré inequalities for Langevin dynamics on
gauge fields. The SK techniques are mean-field and do not transfer.

**261, Anderson localization** (2D pure point; d ≥ 3 a.c. spectrum at weak disorder). Not relevant to YM.

### 2.3 Renormalization group and cluster expansions

**216, XY / BKT** (6 papers; the main one is BKT universality, 169 pp). Main theorems
(`BKT-universality-…/build/sections/introduction.tex:73-120, 181-200, 226-232`): GFF limits for discrete
Gaussian heights through the roughening threshold, with the universal value β_eff(J,β_c) = 8π v_J², and
spin-field limits to imaginary GMC at low temperature. The critical-correlation paper gives
C(r) ~ A r^{-1/4}(log r)^{1/8}. Technique (`toolkit.tex:1-60`): finite-range Gaussian decompositions
(Brydges–Guadagni–Mitter, Bauerschmidt), an analytic polymer / Brydges–Yau RG framework, sine-Gordon /
Coulomb-gas flows (Dimock–Hurd, Falco), and a **"physical entry"** step that matches a microscopic
fixed-range model into the weak-activity domain of the RG maps (`introduction.tex:475-486`). [SRC,
UNVERIFIED] **Use [MINE]:** this is the repo's most developed **Brydges-style multiscale RG with
polymer/extraction norms**, which is the genre of Bałaban's YM program. Two features matter for YM:
(i) an explicit finite-range covariance decomposition with operator-norm and derivative bounds (Lemma
"Finite-range decomposition", `toolkit.tex:20-46`). An analogous decomposition for the gauge-fixed (axial or
Landau) lattice Laplacian on Lie-algebra-valued 1-forms is a standard first step in any Bałaban-type gauge
RG [STD]. (ii) The "entry" problem, i.e. getting a fixed lattice model into the RG's small-activity domain,
mirrors YM's need to pass from the Wilson action to a small-field effective action. Caveat: the XY/BKT flow
is abelian and marginal, whereas YM is nonabelian and asymptotically free. The large-field problem (gauge
orbits, Gribov copies) has no analogue in 216.

**218, Ising universality** (6 papers). See §2.1.3. RG technique: an exact conditional-averaging map on
lists of local interaction "occurrences", hard-core Mayer/tree-graph bounds (Fernández–Procacci,
Procacci–Yuhjtman), a stable-manifold construction for the thermal direction, and comparison of the
critical reference model across geometries (`introduction.tex:132-166`). The Lean formalization covers only
a finite-graph buffered likelihood-ratio comparison (`lean/docs/218.md`). [SRC] **Use [MINE]:** the
"graph of the stable manifold" construction (solve the expanding coordinate backward and the contracting
coordinates forward) is exactly how one tunes bare parameters in an RG construction. In YM it would be the
counterterm-free coupling flow (no relevant mass direction exists by gauge invariance, but the β-function
flow is marginally relevant). The cluster-expansion bounds are generic and portable.

**225, 232, 233, GFF limits** (six-vertex; Lipschitz heights; Ashkin–Teller). These are 2D integrable or
height-function techniques: transfer positivity, Bethe-ansatz-adjacent analysis, and loop-soup/GMC
identification. 232 and 233 were **both revised on 2026-10-06** for repaired crossing, boundary-attachment,
multiscale-separation and convergence arguments (`history.md`; README version notes). [SRC] **Use [MINE]:**
low. They are 2D, marginal or critical, and abelian (height = U(1)-like). They are mainly a cautionary
error-rate datum (§4).

**215 methods relevant to RG, for completeness.** The sharp O(4) paper performs an *exact* stochastic block
transformation through a normalized probability kernel (it cites Hasenfratz–Niedermayer's perfect action)
and compares complete positive densities rather than formal expansions
(`Sharp-mass-bounds-…/build/sections/introduction.tex:159-210`). Bałaban's sigma-model and gauge papers
are cited as "relevant predecessors" whose "hypotheses and conclusions do not supply the exact iterated
O(4) density estimates required here" (`:186-197`). The exact-O(4) paper uses a **U(2) = (U(1)×SU(2))/{±1}
Brownian-loop regulator** whose transfer operators decompose by particle number
(`Exact-mass-asymptotics-…/build/sections/01-introduction.tex:132-150`). [SRC, UNVERIFIED] Note [STD]: the
2D O(4) model **is** the SU(2) principal chiral model (S³ ≅ SU(2)). So family 215 already handles a
group-valued field with Haar reference measure, which is a closer YM analogue than O(3).

### 2.4 Gauge-invariant quantum mechanics: BFSS (family 270)

**Paper 1: "The unique threshold bound state of the SU(N) BFSS model"** (48 pp; 3,628 TeX lines).
- Setup (`The-unique-threshold-bound-state-…/build/manuscript/sections/01-introduction.tex:25-72`): nine
  traceless Hermitian N×N matrices X_i = x_i^A T_A, 16 real fermions per color in an irreducible Clifford
  module, and supercharges
  Q_α = p_i^A γ^i θ^A + ½ f_{ABC} x_i^B x_j^C γ^{ij} θ^A. The **physical Hilbert space is the SU(N)-invariant
  subspace** 𝓗_N = [L²(ℝ^{9(N²−1)}) ⊗ 𝓕_N]^{SU(N)} under the simultaneous adjoint action. H_N is the
  self-adjoint operator of the closed quadratic form (1/16)Σ‖Q_α Ψ‖² on the gauge-invariant smooth
  compactly supported core.
- Main theorem (`:74-81`): dim Ker H_N = 1 for every N ≥ 2. The kernel is Spin(9)-invariant and even.
  [SRC, UNVERIFIED]
- Gauge handling (`02-algebra.tex:54-61`): "Gauge invariance means equivariance of the Clifford-valued
  function", which infinitesimally gives the Gauss law p·ad(w)x = −(i/2)θᵗ ad(w) θ on gauge-invariant
  functions. The square of a charge (Prop. "Square of a charge", `02-algebra.tex:63-82`) produces the
  YM-type potential Σ|[x_i,x_j]|² plus a fermion bilinear, with a "gauge cancellation" in the cross terms.
- Technique: a Fredholm index for a BMN mass deformation (index = p(N), the partition number), a
  massless limit h → ∞ with cluster decomposition over partitions of N, graph-norm "local profile"
  estimates near each cluster, a Hardy-inequality exterior estimate, and an induction on N
  (`01-introduction.tex:171-271`).

**Paper 2: "Positive eigenvalues of the relative SU(2) BFSS Hamiltonian"** (9 pp). Theorem (`…tex:135-145`):
there are infinitely many positive eigenvalues E_j → ∞ with L² eigenvectors. Mechanism (`:147-178`): the
quartic potential V = Σ|x^a ∧ x^b|² has flat directions. Fixing u = x^a, the transverse oscillator has
frequency ∝ |u|. Restricting to Spin(9) sectors with large λ_2 (branching to the Spin(8) stabilizer)
excludes low oscillator levels, so the transverse energy confines and the sector has compact resolvent. It
cites **Lüscher's bosonic Yang–Mills Hamiltonian estimates** (`:212`) and Simon's x²y² argument. [SRC,
UNVERIFIED]

**Use in a YM program [MINE].**
- **Small-volume Hamiltonian YM.** Pure YM on a spatial torus T³ of side L, in the zero-momentum (constant
  mode) truncation, is bosonic matrix quantum mechanics with three matrices and the Gauss law [STD: Lüscher
  1983; van Baal]. The **bosonic** spectrum is discrete because the commutator potential confines, as in
  Simon's x²y² argument. The BFSS papers' technology (gauge-invariant core, closed forms, slice/orbit
  integration on SU(N)-orbits, oscillator confinement transverse to flat directions, cluster decompositions)
  is directly relevant to making the small-L (Lüscher–van Baal) regime of YM on T³ rigorous, including
  non-constant modes. That regime is *not* the Clay problem: the Clay problem is the infinite-volume
  continuum limit. But it is a necessary ingredient of any "finite physical box" step. A box of size
  O(1/Λ_QCD) is exactly the scale at which the 4D analogue of the O(3) finite-box criterion would be checked.
- **Caveat.** BFSS is supersymmetric with flat directions and continuous spectrum starting at 0. Pure
  bosonic YM QM has *no* flat-direction problem (Simon), so the hard part of BFSS (threshold states) is
  absent. The easy part (gauge-invariant operator domains, form closures, invariant cores) is reusable.
- **Formal infrastructure.** `lean/OAI/MathematicalPhysics/BFSS/` (74 files, 17,934 lines, sorry-free by
  grep) formalizes the BFSS Hilbert space, supercharges, the **SU(N)-invariant physical subspace**
  (`GaugeCore.lean:18-52`), **Haar measure on U(N)** (`SliceIntegrals.lean:168-177`), gauge-orbit averaging
  (`GaugeAverages.lean:16-60`), orbit slices and normal tubes, Rellich compactness, and fermion
  quantization. It has **no comparator challenge, no formalization.yaml entry and no `lean/docs/270.md`**,
  so it is in-progress infrastructure without a stated top-level theorem. This is the only Lean code in the
  repo with a nonabelian compact gauge group acting on a quantum Hilbert space. [SRC]

### 2.5 Axiomatic QFT: family 282 (and 280)

**282, "Scale and conformal symmetry in four-dimensional operational quantum field theory"** (112 pp;
8,578 TeX lines; not formalized). Theorem (`…/build/sections/01-introduction.tex:56-72`): suppose
Assumption "framework" holds. That is: a local unitary positive-energy theory on ℝ^{1,3} with a Poincaré-
and dilatation-invariant vacuum; a discrete, bounded-below scaling spectrum with finite multiplicities and
finite scaling support; a covariant causally commuting **bounded local net** with compatible affiliated
realizations of the fields; and a physical local stress tensor T and virial field V with compact-flux Ward
identities. Then there is a Hermitian dimension-2 scalar L with ∂·V^{(3)} = □L. The improvement
t_{μν} = T^{(4)}_{μν} + (1/3)(∂_μ∂_ν − η□)L is symmetric, conserved and traceless, and the conformal currents
have unbroken local Ward identities. The conclusion is **local**; a global conformal action on the net is
left open (`:74-81`). "In a gauge description, the construction takes place in the chosen gauge-invariant
local algebras" (`:86-87`). Technique (`:192-223`): wedge modular theory and half-sided modular inclusions
for null cuts, a two-horizon dispersion "critical-tail" test, KMS identification of cone modular groups,
extraction of a dimension-2 scalar wave via diamond modular transformations, and reconstruction of
products, domains and affiliation. [SRC, UNVERIFIED]

**Use [MINE].** Low for the mass gap itself. A massive YM theory is not scale-invariant; its UV limit is
free, and 282 concerns exactly scale-invariant theories. Possible uses: (i) as a framework check that a
constructed YM theory's UV limit (free gluons in a gauge-invariant algebra) fits an operational net
framework; (ii) the **reconstruction section** (§8 of the paper, 1,716 lines) on affiliation of
reconstructed point fields to a bounded net, and on common invariant domains, addresses a gap that also
arises when passing from OS-reconstructed Wightman fields to a Haag–Kastler net. That passage is not
required by Jaffe–Witten, who ask for Wightman/OS-level axioms. Its hypotheses are heavy and it has not been
checked.

**280, unitary VOAs ⇒ conformal nets** (47 pp; first step formalized: polynomial energy bounds, strong
locality, an irreducible conformal net; see `lean/docs/280.md`). **Use:** none for 4D YM mathematically. Its
Lean challenge (`ComparatorChallenges/VertexAlgebraNet.lean`, 830 lines) is the repo's richest *formal*
AQFT-style statement (§5.2).

### 2.6 Stochastic and PDE methods

- **No stochastic-quantization, Langevin-SPDE, regularity-structure or paracontrolled paper exists in the
  repo.** "Langevin" hits are SK spin-glass dynamics (227) and log-concave sampling (139). [SRC, grep]
- **362, global smoothness for 3D relativistic Vlasov–Maxwell** (49 pp; Lean-formalized,
  `lean/docs/362.md`: 207 files, 89,993 lines). This is classical abelian gauge-field PDE with Gauss
  constraints. **Use [MINE]:** none for quantum YM. Classical YM in 4D is globally well-posed [STD:
  Eardley–Moncrief; Klainerman–Machedon], and that is not where the difficulty lies.
- **306, purely cosmetic surgery** (144 pp). Real **instanton Floer theory**: ASD moduli, Uhlenbeck-type
  small-curvature gauges, Chern–Simons, gluing (`Purely-Cosmetic-Surgery-…/build/sections/05-stack.tex`,
  `09-analysis.tex`). Classical gauge analysis (moduli of SU(2) instantons), not QFT. **Use [MINE]:** low. It
  could inform semiclassical instanton contributions, which are irrelevant to the rigorous mass gap.
- **365, joint metric and U(2)-connection recovery from one boundary patch** (50 pp). Theorem
  (`Determination-of-a-metric-and-a-unitary-connection-…/build/sections/01-introduction.tex:39-60`): the
  zero-frequency DN form of d_A^* d_A on a trivial C² bundle determines (g, A) up to boundary-fixing
  diffeomorphism and gauge U with U|_Γ = I. **Use:** none. It is inverse problems for a *fixed* classical
  connection. Its Lean formalization covers only the scalar nonuniqueness companion (`lean/docs/365.md`).
- **364, 363, Boltzmann; 376, Navier–Stokes computation; 371, NLS blowup.** Irrelevant.

### 2.7 Everything mentioning gauge fields or connections (exhaustive list of non-trivial hits)

| Family | Paper | What "gauge" means there | YM relevance |
|---|---|---|---|
| 270 | both BFSS papers | SU(N) gauge invariance of matrix QM; Gauss law | **Medium**: small-volume Hamiltonian YM |
| 215 | O(n) decay; O(4) exact | *External* SO(3) background gauge field for a spin model (the twist response W(A)); "change of gauge" in the Bethe-ansatz section | Mechanism-level, see scratch notes |
| 306 | Cosmetic surgery | SU(2)/SO(3) instantons, Floer theory | Low (classical) |
| 365 | Connection recovery | U(2) connection, gauge equivalence | None |
| 362 | Vlasov–Maxwell | Classical Maxwell fields, Gauss constraints | None |
| 341 / 342 | Hypersymplectic / taming | gauge fixing in elliptic PDE | None |
| 044 | Hikita conjecture | quiver gauge theories (Coulomb/Higgs branches) | None |
| 042 / 260 / 264 | Class VII / Penrose / cosmic censorship | Donaldson theory cited; L² Christoffel "connection" | None |

ClassicalON's Lean code formalizes the external-gauge-field twist identity: `SpinSystem.gauge`,
`Z_gauge`, `noncommuting_gauge` (`lean/OAI/Probability/ClassicalON/FiniteVolume.lean:230-330`). This is a
*global-symmetry background field*, not a dynamical gauge field. [SRC]

---

## 3. Ranked list of reusable tools

Ranking is by expected usefulness to a rigorous 4D SU(N) program whose architecture follows the O(3)
paper (lattice a priori bound, exact RG, cross-cutoff comparison, OS reconstruction). Each claim is
[UNVERIFIED] unless marked formalized.

| Rank | Tool | Source | Formal? | What it would do for YM | Main obstacle in 4D gauge setting [MINE] |
|---|---|---|---|---|---|
| 1 | Full-gap definition via OS transfer on local observables, plus the **purity-bootstrap finite-box criterion** (volume-term cancelling) | 215 Sharp O(4) Prop. criterion (`finite-volume.tex:105-125`); 268 Prop. bootstrap (`bootstrap.tex:123`) | No | Reduces "infinite-volume full gap" to "small Δ on one box". It survives exact RG because bulk free energy cancels | Needs the 4D/gauge-invariant version of the rectangle identities. Does **not** supply the small initial defect (the crux) |
| 2 | **Exact block RG through a normalized probability kernel**; comparison of complete positive densities across cutoffs at fixed terminal kinetic coupling | 215 Sharp O(4) §§renormalization/comparison; O(3) paper | No | The template for Bałaban-type gauge RG with complete-density (not formal-expansion) control | Gauge-covariant blocking (Bałaban's axial-gauge / averaging), large-field regions, Gribov |
| 3 | **Brydges-style polymer RG with finite-range Gaussian decomposition; "physical entry" into the small-activity domain** | 216 BKT (`toolkit.tex:1-60`; `introduction.tex:475-486`) | No | Finite-range decomposition for gauge-fixed Laplacian on 1-forms; matching Wilson action into a small-field effective action | Nonabelian, asymptotically free (marginally relevant) flow, versus abelian marginal flow in BKT |
| 4 | Stable-manifold ("graph") construction tuning bare parameters; hard-core Mayer / tree-graph bounds; exact conditional-averaging maps | 218 (`introduction.tex:132-166`) | Only a finite-graph comparison (218.md) | Coupling-constant tuning along the RG trajectory; cluster-expansion estimates | Generic; must be redone with gauge-covariant locality |
| 5 | Gauge-invariant Hilbert space, invariant cores, closed forms, orbit slices, Haar averaging for SU(N) | 270 (`02-algebra.tex:54-82`); Lean `BFSS/GaugeCore.lean`, `SliceIntegrals.lean` | Partial Lean (no top theorem) | Rigorous small-volume / Hamiltonian YM on T³; Gauss law handling | Pure-YM QM is easier (no flat directions). Field theory needs infinitely many modes |
| 6 | Reflection-positive **radial/normal transfer** spectral representation; symmetry cancellation of marginal directions | 218 (`introduction.tex:119-129`); 232 (`01-introduction.tex:182-200`) | No | Control of irrelevant operators near a (free) UV fixed point; spectral representation of covariances | Relies on conformality; 4D YM UV fixed point is Gaussian with logs |
| 7 | Rigorous computer-assisted seeds (interval-arithmetic transfer traces) | 268 (`introduction.tex:132-140`; `verification/`) | Scripts, not Lean | Fixed-β lattice SU(2) certificates | Cannot reach β → ∞ boxes of physical size O(1) |
| 8 | Group-valued (SU(2) ≅ S³) sigma-model control; U(2) Brownian-loop regulator; quaternionic noncommuting rotations | 215 O(4) papers | No (only O(n) decay) | Closest repo analogue with Haar measure on a compact Lie group | 2D ⇒ 4D power counting (see scratch notes) |
| 9 | Modular-theory reconstruction of local fields, affiliation to bounded nets | 282 §8 | No | Passing from OS/Wightman fields to a net (beyond Clay requirements) | Heavy hypotheses; scale-invariant setting |
| 10 | Area law / PEPS from a global gap; dimension-free Poincaré | 265; 227 | 227 partially; 265 has partial sorry-free PEPS Lean code without comparator | Downstream consequences or numerics only | Infinite local dimension for gauge links |

**Families examined and judged irrelevant** (with reason): 211–214, 217, 219–224, 226, 228–231, 234–239
(planar maps, percolation, spin glasses, SLE and other 2D-conformal or mean-field topics without any
massive-field-theory content); 260–264, 266–267, 272–279, 281, 283–284 (GR, atomic physics, quantum
information); 285–303 (operator algebras: the techniques are von Neumann-algebraic, with no QFT model);
304–377 (topology, geometry, PDE), except as noted in §2.6–2.7.

---

## 4. Withdrawals, revisions and what they imply

**What `history.md` records [SRC].**
- **2026-10-07 withdrawals (3 papers):** "Algebraicity of Weil classes on split abelian eightfolds",
  "Algebraicity of Kuga–Satake correspondences for K3 surfaces", and "The rational Hodge conjecture for
  products of K3 surfaces". The withdrawal notices (README in each directory; each PDF is now a 1-page notice, the `build/`
  TeX trees were deleted on 2026-10-07, and the originals remain at git revision `adc7f1241`) say a **sign error** in the stabilization-trace argument gives signed double-point count
  I_new = I(f_1) − m = −2m ≠ 0 instead of 0. So the Eliashberg–Murphy cancellation hypothesis fails, and the
  two dependent papers inherit the gap. All notices add: "This withdrawal concerns the proof; it does not
  assert that the mathematical statement is false."
- **14 revised manuscripts** with proof repairs, corrected statements or clarified hypotheses: Lipschitz
  heights and Ashkin–Teller currents (4 manuscripts: repaired crossing, boundary-attachment, conditioning
  and convergence arguments); Kähler MMP and abundance (6 manuscripts); taming and hypersymplectic
  (2 manuscripts: corrected a cone-equality claim and added a strict-inclusion example); Incompressible
  Box Transport (torus-projection and common-clock estimates); and one obsolete citation in exact BSD. 13
  more manuscripts were updated only to cite revised companions. I count 27 READMEs carrying a "Version
  note". The ones in probability or lattice models are all in **families 232 and 233**. Examples:
  "repairs the boundary-attachment, landing-comparison, and multiscale separation arguments, including the
  conditional walk and hookup steps" (`Uniform-real-Lipschitz-surfaces-…-October-6-2026/README.md`); and
  "replaces excursion convergence with a signed-loop-soup/GMC argument"
  (`The-joint-scaling-limit-of-critical-Ashkin-Teller-currents-October-6-2026/README.md`).
- Formalization coverage: 300/719 ≈ 42% of top-line results (`history.md`). For the families relevant here,
  formalized top-line statements exist only for 215 (the O(n) decay theorem only), 218 (a supporting finite
  comparison only), 269, 271 and 227 (parts). The scope notes explicitly exclude the hardest claims. For
  example, 215.md excludes the infinite-volume limit and the O(4) spectral gap.

**Error-rate signals [MINE, with the data above].**
- Within one week of release, ~2.2% of manuscripts (16 of 719: 3 withdrawals plus 13 mathematical
  repairs or clarifications, excluding the citation-only fix) needed a withdrawal or a substantive revision.
  That is a lower bound on the defect rate, because it counts only defects found so far, mostly by whoever
  scrutinized the high-profile claims. The Hodge chain shows **error propagation through companion-paper
  dependencies**: one sign error invalidated three papers.
- The repaired lattice-model papers (232, 233) were repaired in exactly the steps a YM program would borrow:
  multiscale separation, boundary attachment, crossing and conditioning estimates. Those steps are the
  hardest to check by eye in 60–170-page analytic papers.
- The YM-relevant analytic papers are long and mutually dependent. Sharp O(4) (102 pp) feeds exact O(4)
  (109 pp). The O(3) continuum paper (122 pp) imports from the pole paper and the O(n) decay paper. BKT
  universality runs 169 pp. Only the 20-page O(n) decay theorem in this cluster is machine-checked.

**Implications for building on 100+ page unformalized analytic papers [MINE].**
1. Use them as **architectural blueprints and sources of lemma statements**, not as citable results. Any
   roadmap step that depends on, for example, the sharp O(4) density comparison should be labelled
   "conditional on [paper], unverified".
2. Before building on a specific lemma, (a) re-derive it independently, or (b) formalize it, or (c) seek a
   human expert check. Prioritize lemmas whose failure would invalidate the architecture, such as the
   finite-box criterion and the cross-cutoff comparison window. The finite-box criterion is a good first
   formalization target. It is short and finite-dimensional plus one limiting argument, and §5.4 estimates
   it at weeks, not years.
3. Treat **dependency chains** as multiplicative risk. The O(3) result depends on at least the O(n) decay
   paper (formalized), the pole paper (26 pp, unformalized) and the O(4)-style machinery.
4. Statements also get **narrowed** in revisions. The taming paper restricted a cone-sum equality to a
   special case. So even the *statement* of an unformalized theorem may shift, and downstream roadmaps should
   cite the version date (e.g. "October 4, 2026 edition").

---

## 5. Lean infrastructure

### 5.1 Toolchain and dependencies [SRC]

- `lean/lean-toolchain`: `leanprover/lean4:v4.34.1`.
- Mathlib pinned at `d13f23b723b8a846827a245b89c10fc7d3f11612` (`lakefile.lean`, `lake-manifest.json`). Its
  commit date is 2026-09-24 ("chore: bump toolchain to v4.34.1"), verified on a local checkout.
- Other direct dependencies: PrimeNumberTheoremAnd, StrongPNT, carleson, rellich-kondrachov, AINTLIB,
  ClassFieldTheory, schoenflies-lean, SphereEversion, TauCeti, gromov, fixed-point-theorems, AbsorptionCutoff,
  Zeta3Irrational, eleven `lana-agents/*` packages (iut, heights, belyi, etc.), leancert, LeanArchitect,
  PrimeCert, checkdecls and doc-gen4. 24 compatibility patches live in `lean/patches/` and are applied by
  custom Lake code in `lakefile.lean`. **None of these dependencies concerns QFT, statistical mechanics or
  gauge theory.**
- Library size: 122,458 `.lean` files, 1.8 GB, in a single `OAI` library. The README warns to compile only
  small portions and documents an mmap workaround. `OAI/MathematicalPhysics` holds 6,736 files and
  `OAI/Probability` 12,971.
- Verification: Comparator (`lean/ComparatorChallenges/README.md`). Each `*.json` names a challenge module (a
  statement with `sorry`), a solution module and permitted axioms. **All 416 configs permit exactly
  `propext`, `Quot.sound` and `Classical.choice`** (my tally). There are no custom axioms anywhere in
  comparator scope.

### 5.2 What is formalized for family 215 [SRC]

- Scope note (`lean/docs/215.md`): the formalized result is **only** the all-temperature exponential decay of
  the 2D classical O(n) spin two-point function for n ≥ 3. It is uniform over finite free-boundary
  square-lattice subgraphs and edge strengths in [0, β]. "The infinite-volume limit and the separate O(4)
  spectral-gap claim are not included." The O(3) continuum limit, the O(3) particle pole and the exact O(4)
  asymptotics are not formalized either.
- Statement (`lean/ComparatorChallenges/ClassicalON.lean`, **60 lines**, imports only Mathlib):
  - `Site := ℤ × ℤ`; `LatticeGraph` = a finite vertex set plus nearest-neighbor positive-direction edges
    (`:11-19`).
  - `Spin n` = the unit sphere in `EuclideanSpace ℝ (Fin n)`. `sphereProbability` is the normalized
    `Measure.toSphere` of Lebesgue measure. `referenceLaw` is the product measure (`:21-29`).
  - `interaction`, `partition`, `correlation` define the finite-volume Gibbs expectation of σ_x·σ_y
    (`:31-41`).
  - `ExponentialDecay`: ∀ n ≥ 3, ∀ β > 0, ∃ A, m > 0, ∀ G, ∀ b with 0 ≤ b_e ≤ β, ∀ x y,
    0 ≤ ⟨σ_x·σ_y⟩ ≤ A·exp(−m·|x − y|_2) (`:46-51`). `theorem main : ExponentialDecay` (`:53`).
- Config (`ClassicalON.json`): solution `OAI.Probability.ClassicalON.Main`, theorem `OAI.ClassicalON.main`,
  the three standard axioms, `enable_nanoda: false`.
- Proof size: `lean/OAI/Probability/ClassicalON/` has 117 files, 12,907 lines, ~583 kB, 757 theorems and
  lemmas, 320 definitions and structures, and **0 `sorry`/`axiom`** by grep. The largest file is
  `FiniteVolume.lean` (1,245 lines): Gibbs integrals, differentiation under the integral, rotation-invariance
  of the sphere measure, the **external gauge-field partition function `Z`, `gauge`, `Z_gauge`,
  `noncommuting_gauge`**, and the twist energies with their first through fourth variations. Other files
  formalize FKG on product measures (`FinFKG`, `ProductFKG`), Ginibre inequalities for Ising and plane
  rotators (`IsingGinibre`, `PlanarGinibre`), complex Ward identities (`ComplexWard`, `MixedWard`), the Ising
  bond expansion (`BondExpansion`), annulus crossing (`AnnulusCrossing`), coarse-graining and the final
  exponential (`CoarseExponential.connection_exponential`), and the reduction from n to 3 components
  (`BlockReduction`).
- Size ratio: 60-line statement to 12,907-line proof for a 20-page paper, about **650 Lean lines per paper
  page**.

### 5.3 Inventory of formal infrastructure relevant to YM

| Needed object | In repo Lean (`lean/OAI`) | In pinned Mathlib | Notes [SRC unless marked] |
|---|---|---|---|
| Finite-volume Gibbs measures on lattices | **Ad hoc, model-specific**: ClassicalON (sphere spins), CriticalSK, InvariantIsing, ContinuumTransition, HardSphere | No general Gibbs/DLR theory (grep "Gibbs": 2 incidental hits) | No infinite-volume Gibbs states or DLR equations. ClassicalON stays in finite volume by design |
| Haar measure on compact groups | BFSS uses `Measure.haarMeasure` on `unitary (Matrix (Fin N) (Fin N) ℂ)` (`SliceIntegrals.lean:168-177`) | Yes: `MeasureTheory/Measure/Haar/*` (existence, uniqueness, quotient, disintegration) | No Peter–Weyl, no character expansion, no heat kernel on SU(N). Mathlib has `Matrix.specialUnitaryGroup` (`LinearAlgebra/UnitaryGroup.lean`) |
| Lattice gauge fields (link variables, plaquettes, gauge transformations, Wilson action) | **None** | None | Grep for Wilson/plaquette/holonomy in `lean/OAI` finds only geometry and topology uses |
| Reflection positivity (OS sense) | **None**. Hits for "reflection_positive" are unrelated: a combinatorial tuple law (`Combinatorics/SquareDifference`) and a trace identity (`Analysis/Commutator/DihedralHaar.lean:65`) | None | |
| Transfer operators, spectral gap of transfer | **None** as theory. Spectral-gap statements exist for Markov chains (SwitchChain, SK) and for finite matrices (Laughlin) | Compact self-adjoint spectral theorem (`Analysis/InnerProductSpace/Spectrum.lean`), compact operators | No trace-class or Hilbert–Schmidt integral-operator theory for transfer kernels |
| OS reconstruction | **None** | None | |
| Wightman axioms / Haag–Kastler nets | Ad hoc: `IrreducibleConformalNetStructure` (VertexAlgebraNet challenge `:783-818`): von Neumann algebras on arcs, isotony, locality, Möbius covariance, vacuum, self-adjoint positive-energy Hamiltonian | `VonNeumannAlgebra`; GNS (`Analysis/CStarAlgebra/GelfandNaimarkSegal.lean`); standard subspaces (`Analysis/InnerProductSpace/StandardSubspace.lean`, Tomita–Takesaki preliminaries) | Only 1D (circle) conformal nets. No Minkowski nets, no Wightman distributions |
| KMS states, quasi-local algebras | Ad hoc in the Heisenberg challenge (`ComparatorChallenges/Heisenberg.lean:57-200`): quasi-local C*-algebra on ℓ², states, `IsKMS`, infinite-volume dynamics as a norm limit | C*-algebra basics, CFC | Proof: 128 files, 25,400 lines, 0 sorry |
| Schwartz space, tempered distributions | Used in 163 directories (mostly number theory and Fourier analysis); `EinsteinFour` uses 𝓢' | Yes: `Analysis/Distribution/{SchwartzSpace, TemperedDistribution, TestFunction, Distribution, Sobolev, FourierMultiplier}` | Enough to *state* Schwinger functions as tempered distributions. No nuclear theorem / kernel theorem, no Bochner–Minlos |
| Unbounded self-adjoint operators | Used (BFSS form closure; VertexAlgebraNet `resolvent`, `flow`) | `LinearPMap`, adjoint, `IsSelfAdjoint`, closedness (`Analysis/InnerProductSpace/LinearPMap.lean`) | **No unbounded spectral theorem, no Stone theorem.** VertexAlgebraNet builds the unitary flow by hand from resolvents (`:744-773`) |
| Probability on infinite products, weak convergence | Used widely | Kolmogorov extension (`MeasureTheory/Constructions/Projective*`, Ionescu-Tulcea), Prokhorov (`MeasureTheory/Measure/Prokhorov.lean`), Gaussian measures, Brownian motion, CLT | No GFF; no measures on 𝓢'(ℝ^d) |
| Connections and curvature | None | Covariant derivatives on vector bundles (`Geometry/Manifold/VectorBundle/CovariantDerivative/*`, including Levi-Civita and torsion); Lie algebra of a Lie group (`Geometry/Manifold/GroupLieAlgebra.lean`) | No principal bundles, no curvature 2-form, no gauge group of a bundle |
| Renormalization group / polymer expansions | None as reusable library. ClassicalON has an Ising bond expansion | None | |

### 5.4 Formalization gap for a YM-scale proof [MINE]

**Calibration data [SRC].** These ratios are Lean lines per paper page, and they mix proof styles.
- ClassicalON: 12,907 lines for 20 pp (~650/pp).
- Heisenberg (271): 25,400 for 54 pp (~470/pp).
- VertexAlgebra (280, first step only): 36,159 for 47 pp. The fraction of the paper covered is unknown.
- Laughlin (269): 77,130 for 22 pp (~3,500/pp; computation-heavy).
- Vlasov–Maxwell (362): 89,993 for 49 pp (~1,840/pp).
- BFSS (270): 17,934 lines with no top-level theorem yet.

A plausible range is 500–2,000 Lean lines per dense analytic page, **assuming the infrastructure
exists**.

**A YM-scale proof would need, roughly in dependency order:**

1. **Lattice gauge theory core** (none exists): links of ℤ⁴ (or a torus), G-valued link fields, gauge
   transformations, plaquette holonomies, Wilson action, Haar product measure, gauge invariance of
   expectations, Gauss law, and the gauge-invariant transfer operator on L²(G^{spatial links})^{G^{sites}}.
   Estimate: **5–15k lines**. Mostly bookkeeping on Mathlib's Haar measure. Needs Peter–Weyl and character
   expansions for strong-coupling and heat-kernel actions (Mathlib has none): **+10–30k**.
2. **Reflection positivity and OS reconstruction on the lattice:** time-reflection Θ on link
   configurations, the OS form, the null-space quotient and completion, the transfer operator T as a
   positive self-adjoint contraction, and the full-gap definition. For a finite lattice everything is
   finite-dimensional in the configuration-space variables but uses L² of a compact group. Estimate
   **5–15k**. The repo's sharp O(4) paper does the scalar-spin version in a few pages. The **purity-bootstrap
   criterion** (rank 1 above) is then perhaps **2–5k** on top. This is the cheapest, highest-value formal
   target in the whole program.
3. **Continuum OS axioms and reconstruction** (the Jaffe–Witten target): Schwinger functions as (gauge-
   invariant, e.g. smeared Wilson-loop or field-strength) tempered distributions, Euclidean invariance,
   OS positivity, symmetry, cluster property, the OS linear-growth condition, and the reconstruction
   theorem to Wightman fields, with the mass gap as a spectral condition. Mathlib has distributions but no
   OS/Wightman framework, no unbounded spectral theorem, no Stone theorem, no SNAG theorem and no
   nuclear/kernel theorem. Estimate **40–150k lines** of foundational functional analysis. This is a
   multi-person-year project independent of YM. It is reusable for any constructive QFT, including the
   O(3) continuum limit of family 215.
4. **Constructive analysis.** These are the proof-specific bulk:
   - (a) the a priori weak-coupling lattice gap (no known proof);
   - (b) Bałaban-scale gauge RG: small and large fields, axial/Landau gauge fixing on blocks, background-field
     minimizers, polymer expansions, and on the order of 10–15 Bałaban papers' worth of estimates, ~500+
     dense pages [STD; the page count is my rough estimate];
   - (c) the cross-cutoff comparison;
   - (d) continuum limit, rotation invariance (cf. the 3-4-5 / quaternion trick in the scratch notes), and
     non-triviality.
   At 500–2,000 lines per page this is **0.25M–1M+ lines**, before any of it is known to be correct.
   For comparison, the entire `OAI` library is ~122k files. Typical directories run 10⁴–10⁵ lines.
5. **Lie theory for general compact simple G:** Jaffe–Witten require every compact simple G. Mathlib has
   matrix groups SU(n) and generic Lie groups as manifolds, but no classification, no root systems tied to
   compact groups, and no uniform representation-theoretic estimates. The exceptional groups need either
   uniform arguments or case-by-case treatment.

**Net assessment [MINE].** The formal gap is dominated by item 4 (no proof exists to formalize) and item 3
(missing foundations). Items 1–2 are well within reach of the repo's demonstrated formalization throughput.
That throughput is O(10⁴–10⁵) lines per paper, apparently AI-produced, and it reached 300 formalized
top-line results in a few weeks. Items 1–2 would provide a machine-checked **lattice** framework: lattice YM,
OS positivity, the transfer operator, and the finite-box gap criterion. Every later analytic claim could
then be stated precisely and checked incrementally. A sensible first comparator challenge [MINE] would be
"for 4D SU(2) lattice YM at fixed β on a periodic box: OS positivity holds, the transfer operator is a
positive trace-class contraction, and the Sharp-O(4)-style criterion Δ_β(n) ≤ η_* ⇒ full gap ≥ c/n holds".
The statement is perhaps 150–300 lines, comparable in size to `Heisenberg.lean` (218 lines).

---

## 6. Summary of implications for a 4D YM program [MINE unless marked]

1. The repo contributes **no gauge-theory results**. Its contribution is a toolkit: (i) a volume-insensitive
   finite-box ⇒ full-gap criterion; (ii) exact-RG/density-comparison architecture (215) and Brydges-type
   polymer RG with physical entry (216, 218); (iii) gauge-invariant SU(N) Hamiltonian technology and partial
   Lean infrastructure (270); (iv) reflection-positivity spectral representations (218, 232); and
   (v) modular/net reconstruction (282).
2. The **crux** identified in the scratch notes, an a priori weak-coupling decay estimate for 4D nonabelian
   LGT with exponent within a factor of about 3/2 of asymptotic freedom, is **not addressed anywhere in the
   repo**. No family proves any gap, decay or confinement statement for a system with a local (dynamical)
   gauge symmetry.
3. The only machine-checked YM-adjacent statements are the 2D O(n) decay theorem (60-line statement,
   standard axioms), Heisenberg KMS/ordering, and Laughlin and SK spectral gaps. None involves gauge fields,
   OS reconstruction or continuum limits.
4. Treat every unformalized 100+ page analytic claim as unverified. The repo's own record has 3 withdrawals
   and 14 repairs within a week, including repairs to multiscale and boundary arguments in 2D lattice
   papers. The most leverage per unit effort comes from formalizing the lattice framework and the finite-box
   criterion first.

---

## Appendix A. Key file paths

- Family map: `/home/rou/src/math/CONTENTS.md` (family headers: grep `^\*\*NNN\. `).
- Withdrawals and revisions: `/home/rou/src/math/history.md`; READMEs with "Version note" under `preprints/`.
- Purity bootstrap: `preprints/Sharp-mass-bounds-for-the-two-dimensional-O4-model-September-23-2026/build/
  sections/finite-volume.tex:105-125`; `preprints/The-periodic-spin-one-Haldane-gap-September-24-2026/build/
  bootstrap.tex:123`.
- BFSS: `preprints/The-unique-threshold-bound-state-of-the-SU-N-BFSS-model-September-24-2026/build/manuscript/
  sections/{01-introduction,02-algebra}.tex`; `preprints/Positive-eigenvalues-of-the-relative-SU-2-BFSS-
  Hamiltonian-October-5-2026/build/positive-eigenvalues-relative-su2-bfss.tex`; Lean
  `lean/OAI/MathematicalPhysics/BFSS/`.
- 282: `preprints/Scale-and-conformal-symmetry-in-four-dimensional-operational-quantum-field-theory-
  September-26-2026/build/sections/01-introduction.tex`.
- 216 RG toolkit: `preprints/BKT-universality-for-height-and-planar-spin-fields-September-24-2026/build/
  sections/toolkit.tex`.
- 218: `preprints/Conformal-universality-of-bulk-Ising-correlations-under-weak-interactions-September-23-2026/
  build/sections/introduction.tex`.
- 232 reflection positivity: `preprints/The-Gaussian-free-field-limit-of-integer-Lipschitz-heights-with-two-arc-
  boundary-data-October-6-2026/build/sections/01-introduction.tex:127-212`.
- 265: `preprints/A-two-dimensional-area-law-from-a-global-spectral-gap-September-24-2026/build/sections/
  00-introduction.tex:39-58`.
- Lean 215: `lean/docs/215.md`, `lean/ComparatorChallenges/ClassicalON.{lean,json}`,
  `lean/OAI/Probability/ClassicalON/`.
- Lean AQFT-like: `lean/ComparatorChallenges/Heisenberg.lean`, `lean/ComparatorChallenges/VertexAlgebraNet.lean`.
- Toolchain: `lean/lean-toolchain`, `lean/lakefile.lean`, `lean/lake-manifest.json`.
- Sweep helpers (mine): `research_notes/yang-mills-mass-gap/work/05-sweep/scripts/{fam.sh,kw.sh,texgrep.sh}`,
  `research_notes/yang-mills-mass-gap/work/05-sweep/{families.txt,fam2dir.txt,revised.txt}`.
