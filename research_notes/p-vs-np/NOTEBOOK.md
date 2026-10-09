# P vs NP roadmap — working notebook

Running notes for the question "what would it take to resolve P vs NP?", using the
OpenAI math release (commit `fd4aeeb`) as reference material. Newest entries at the
bottom of each section.

## Layout of this directory

- `NOTEBOOK.md` — this file: facts established, open questions, decisions.
- `comparator/` — independent Comparator re-checks of the release's complexity
  results (`run_comparator.sh`, per-target logs, `summary.tsv`). Builds run in an
  isolated `git archive` snapshot under `/tmp` (path in `snapshot_root.txt`); the
  repository itself is never modified.
- Workflow outputs (repo audit, literature dossiers) will be saved here as they land.

## Coordination

- A parallel session (`math-4a`) is working in `research_notes/p_vs_np_2026_10_09/`.
  Its focus: family 112 (depth-3) — Comparator build validation (PASS, axioms exactly
  `propext, Classical.choice, Quot.sound`), static semantic audit of the restriction
  lemma (no defects found), small exact experiments on the restriction lemma and a
  parity obstruction for a gate-fan-in substitution. Read-only from this side; do not
  write there. Not re-running DepthThree here because of it.

## Repository facts (verified 2026-10-09)

- 719 manuscripts / 372 families; 40 families under "Theoretical computer science",
  6 under "Mathematical logic". LaTeX source for every preprint under
  `preprints/<dir>/build/`.
- Lean: `lean/ComparatorChallenges/<Name>.lean` holds the trusted statement (ends in
  `sorry`), the `.json` names the solution module and permitted axioms; scope notes in
  `lean/docs/<NNN>.md`. 200 challenges listed in `formalization.yaml` `main_results`,
  but several formalized complexity results (PermanentCubic, DepthFive, MatchingPSD,
  WitnessedChoice, WeisfeilerLeman, FormulaHitting) have sorry-free solution trees and
  are absent from `main_results` — catalogue lags the code.
- No `.lake` in the repo; toolchain `leanprover/lean4:v4.34.1` is installed;
  `comparator`, `landrun`, `lean4export` are on PATH.

### P-vs-NP-relevant results and formal status

Lines = size of the sorry-free solution directory (grep for `sorry`, no `axiom` decls).

| Family | Claim | Lean solution | Lines |
|---|---|---|---|
| 102 | Unique Games Conjecture (+ Max-Cut, VC, Min-UnCut, DFVS) | `OAI/Computability/UniqueGames` | ~187K |
| 103 | L = RL = BPL | `OAI/Computability/Logspace` | ~43K |
| 108 | dc and border-dc of perm_m ≥ m³/(5529600e) for m ≥ 1408 | `OAI/Algebra/Determinantal` | ~21K |
| 112 | language in P needing 2^{ω(√n)} depth-3 OR-AND-OR gates | `OAI/Computability/DepthThree` | ~25K |
| 135 | IMM needs n^{√n/400} homogeneous depth-5 gates (char 0), upper n^{√n+4} | `OAI/Algebra/DepthFive` | ~23K |
| 243 | CPT+C does not capture P; witnessed symmetric choice strictly stronger | `OAI/ModelTheory/Choiceless`, `OAI/Computability/WitnessedChoice` | ~18K + ~26K |
| 126 | exponential psd rank / SDP lifts of perfect matching | `OAI/Combinatorics/MatchingPSD` | — |
| 116 | poly-time hitting sets for noncommutative formulas | `OAI/Algebra/FormulaHitting`, `OAI/Computability/RationalHitting` | ~6K + ~15K |

Statement-level observations from reading the Comparator files:

- **112** is only "beyond every constant A in 2^{A√n}" — no fixed n^{1/2+ε} exponent,
  nowhere near Valiant's 2^{n/log log n} depth-3 threshold.
- **108** is polynomial (cubic). The general `SmoothInitialForm` theorem bounds dc by
  (r−1)(d−1)/(4e) — linear in each of degree-of-initial-form and number of variables,
  so the method looks intrinsically capped at polynomial bounds. VP ≠ VNP needs
  superpolynomial.
- **135** is n^{Θ(√n)} for IMM, which is in VP — sharp at exactly the depth-reduction
  ("chasm") threshold, so by construction it cannot cross it.
- **103**'s statement uses a custom finite transition-table machine with a coin tape
  and a polynomial clock; fidelity of that model to standard BPL is being checked by
  the audit workflow.

## Work in flight

- Comparator re-check of 17 targets (background, started 19:18 UTC):
  LogspaceEquality, ChoicelessPolynomialTime, PermanentCubic, SmoothInitialForm,
  DepthFive, MatchingPSD, MatchingAffineLift, WitnessedChoice, WeisfeilerLeman,
  TwoWayDeterminization, OneWayLiveness, OneTapeSpace, RationalHitting,
  FormulaHitting, UniqueGamesTheorem, PerfectCompleteness, IndependentSets.
- Workflow `pvsnp-repo-audit` (wf_aac2df9e-9d4): 12 deep-readers over the release's
  complexity families, each with an adversarial skeptic, then a synthesis.
- Workflow `pvsnp-literature-dossiers` (wf_39acdb3d-baf): 14 web-verified dossiers
  (barriers, programs, expert views, formal statement of P vs NP), each fact-checked,
  then a completeness critic.

## Open questions to settle

- Does L = BPL come with a seed-O(log n) PRG for ROBPs (black-box) or only a white-box
  algorithm? Only the former would have hardness-vs-randomness consequences.
- Is the UGC reduction's blow-up consistent with Arora–Barak–Steurer's 2^{n^ε}
  algorithm (it must be polynomial of degree growing with 1/ε, or ETH breaks)?
- Is 109 (integer multiplication below n log n on multitape TMs) in tension with the
  network-coding-conjecture lower bound (Afshani–Freksen–Kamma–Larsen 2019)?
- Exact logical relation between "no logic captures P" and P ≠ NP — it implies
  P ≠ NP, so ruling out candidate logics is progress toward a statement *stronger*
  than P ≠ NP, not a stepping stone toward it. Confirm via the dossier.

## Findings log

- 19:26 UTC — **LogspaceEquality (L = RL = BPL): Comparator PASS** in an isolated
  snapshot (build 183 s, check 121 s).
- 19:29 UTC — **ChoicelessPolynomialTime (CPT+C ≠ P): Comparator PASS** (build 135 s,
  check 67 s).
- L = BPL proof strategy (read from `sections/introduction.tex`): white-box. Builds the
  time-layered configuration graph, approximates p₀ = (I−S)⁻¹e through a hierarchy of
  "correction + copy" stages (I−D = (I+E)(I−C)), estimates entries with a randomized
  estimator that uses only O(log n) random bits (fingerprints, conditional averaging
  via Shalom's property (T) mixing bounds, a shared catalytic bit vector), then
  enumerates all 2^{O(log n)} environments and takes the median. **No PRG / hitting
  set for ROBPs is produced**, so no hardness-vs-randomness consequence follows (the
  Cheng–Hoza implication runs hitting sets ⇒ L = BPL, not back).
- The repo already contains a **formal, Comparator-vetted statement of P = NP**:
  `lean/ComparatorChallenges/BinPackingGap.lean` defines `InP`, `ClassP`, `ClassNP`
  (polynomial-time finite-alphabet `Turing.FinTM2` deciders / verifiers on
  `List Bool`, NP certificates framed by `pairBits` with a unary length prefix) and
  `PEqualsNP : Prop := ClassP = ClassNP`. Its trusted theorem `main_results`
  includes `(∃ c, Nonempty (AbsoluteAdditiveAlgorithm c)) ↔ PEqualsNP`: P = NP iff bin
  packing has a polynomial-time algorithm within an additive constant. The solution
  `OAI.Computability.BinPacking.Main` also proves `inP_to_inNP` (P ⊆ NP) via TM2
  composition (`MachineSequential.composeBits`). So "resolve P vs NP" has a ready
  formal target: `OAI.BinPackingGap.PEqualsNP` or its negation.
- UGC formal statement (`UniqueGamesTheorem.lean`): for each fixed ε, δ ∈ (0, ½) there
  is a reduction from binary 3SAT to translation UG over F₂^s, computed by one
  `TM2ComputableInPolyTime` machine whose polynomial is chosen *after* ε, δ. This
  leaves room for the degree to grow with 1/ε, as Arora–Barak–Steurer requires.
  Still to check: whether the paper's blow-up actually does.
- Formal target drafted: `formal_target/PNeNP.lean` (imports only Mathlib). Same
  conventions as the trusted KMedian file (self-delimiting `encodeNat` = unary
  bit-length, separator, binary digits; finite-alphabet `TM2ComputableInPolyTime`).
  Encoding sanity lemmas proved (`encodePair_injective`, axioms `propext`,
  `Quot.sound`); only `P_ne_NP` / `P_eq_NP` remain as `sorry`. Type-checks against the
  pinned Mathlib in ~6 s. Note for auditing: `haltList` demands that a machine halt
  with every non-output stack empty and its internal state reset to `initialState` —
  harmless normalization, but any formal solution must build that cleanup (the repo
  does, in `MachineCanonicalOutput`).
- **Ceiling of the cubic permanent method (family 108)** — elementary, from the
  paper's own bound bdc(G) ≥ (r−1)(d−1)/(4e) for G = per_m ∘ Φ with smooth projective
  zero set. If d > m², the linear part of Φ has a kernel vector v ≠ 0, so G is
  invariant under translation by v; for the lowest homogeneous part (degree r ≥ 2) this
  gives G(v) = G(0) = 0 and ∇G(v) = ∇G(0) = 0, a nonzero singular zero, contradicting
  smoothness. Hence d ≤ m², and r ≤ deg per_m = m. So the method can never certify
  more than (m−1)(m²−1)/(4e) < m³/(4e): cubic is its ceiling, up to the constant.
  More generally, for any family in N variables of degree D it caps at ≈ N·D, which is
  polynomial for every VNP family — so it cannot separate VP from VNP. Same shape as
  the Mignon–Ressayre Hessian ceiling (≤ number of variables), one degree factor
  higher. The paper says its *result* "remains a fixed polynomial bound"
  (`sections/introduction.tex:105-108`) but never states a ceiling for its *method*;
  the ceiling is our own observation (verified below).
- 109 vs network coding: Afshani–Freksen–Kamma–Larsen (2019) give Ω(n log n) Boolean
  circuit size for multiplication assuming the network coding conjecture. A multitape
  TM with time t yields circuits of size O(t log t) (Pippenger–Fischer), so
  O(n (log n)^{1−κ}) TM time only gives O(n (log n)^{2−κ}) circuits: no contradiction.
- Depth-3 (family 112), from its own intro (`00_introduction.tex:54-60`): the result
  makes log₂S₃/√n unbounded and "is weaker than a lower bound 2^{n^{1/2+ε}} for a fixed
  ε > 0" (Håstad–Jukna–Pudlák 1995, Problem 2). The Valiant depth-reduction threshold
  that would matter for general circuits (2^{ω(n/log log n)} for a function in NP)
  is an exponent of n^{1−o(1)}; the result's exponent is ω(√n), i.e. unboundedly far
  below. Technique: CNF-correlation via a clause-count-free restriction lemma (signed
  combinations of narrow CNFs), IPZ sunflower sparsification, and a language built from
  hash-and-evaluate "slices" (PSZ-style parameter fixing). `math-4a` confirmed the
  lemma and showed its fan-in generalization fails (6-bit parity).
- Second Comparator batch queued (`comparator/queue2.sh`): BinPackingGap (the trusted
  `PEqualsNP` file), KMedianThreshold, DirectedFeedback, ParityLifts, VariableWL,
  WLIdentification, TwoWayComplementation, SensitivitySeparation, GotsmanLinial,
  MatrixMultiplication. Batch 1 summary preserved as `summary_batch1.tsv`.
- UGC vs Arora–Barak–Steurer: consistent. Theorem statement
  (`The-Unique-Games-Theorem.../sections/00-introduction.tex:21-38`): "The alphabet, the
  degree of the running-time polynomial, and its constants depend only on ε, δ."
  Soundness uses parallel repetition (Dinur–Steurer projection-game bound, alphabet
  independent), with the repetition exponent fixed by the errors, so blow-up is
  n^{f(ε,δ)}, as ABS (2^{n^{poly(ε)}} algorithm) requires. Ingredients: BKS degree-two
  matrix shortcode + Khot–Minzer–Safra Grassmann expansion (external input) + a new
  nonlinear "latent" noise gadget (quadratic blocks over F₂) that fixes the
  completeness-½ obstacle. Formal statement matches (polynomial chosen after ε, δ).
- **Three different formal definitions of NP in the release.** All are reasonable, and
  none is proved equivalent to another:
  `DirectedFeedback.lean` and `BinPackingGap.lean` frame (x, w) with a *unary* length
  prefix (`1^{|x|} 0`); `KMedianThreshold.lean` uses a *binary* self-delimiting prefix
  (unary bit-length of |x|, separator, binary digits). BinPacking stores alphabet
  finiteness as `Fintype` data, the others as `Finite`. NP is robust to this, but
  proving robustness formally requires poly-time TM2 re-encoders, which the repo does
  not supply. A concrete instance of the "statement auditing" gap (cf. the earlier
  market-map report).
- L = BPL trusted statement (`ComparatorChallenges/LogspaceEquality.lean`), read
  first-hand for loopholes; none found:
  space = distinct work cells visited, summed over tapes, bounded by
  c·⌈log₂(n+2)⌉ for *all* coin sequences and all t (standard visited-cell
  convention); coins are read one-way, one bit per step (standard read-once BPL);
  halting freezes the configuration; `RL`/`BPL` require halting by a polynomial clock
  on every coin sequence, and acceptance probability is computed exactly over
  `Fin t → Bool`; input heads are confined between endmarkers. Model = multi-head
  input, multiple work tapes, finite transition table, equivalent to the textbook
  model up to constants. Formal proof: `Logspace/Equality.lean:83-108`, through
  `fixed_precision_estimator`.
- `formal_target/PNeNP.lean` now also proves **non-vacuity**: an explicit one-stack
  machine `rejectAll` (pop until empty, push `false`, reset state, halt) with a
  verified `|x| + 1` step count, giving `empty_mem_P` and `empty_mem_NP`; axioms
  `propext, Classical.choice, Quot.sound`. Remaining `sorry`: exactly `P_ne_NP` and
  `P_eq_NP`. Still worth adding: P ⊆ NP (needs a poly-time machine that strips the
  `encodePair` frame; the repo's `BinPackingGap.inP_to_inNP` shows it is doable via
  `MachineSequential.composeBits`).
- The release's complexity manuscripts state almost no open problems: of the ten
  central ones, only the permanent paper says anything "remains open" (superpolynomial
  dc / bdc of the permanent). The L = BPL conclusion never mentions generators, BPP or
  circuit lower bounds. The roadmap has to supply the programmatic framing itself.
- 19:48 UTC — MatchingAffineLift Comparator PASS (7/17 green so far).
- **Coverage gap in the release (grep over all 719 manuscripts' LaTeX):** zero
  manuscripts mention MCSP / Minimum Circuit Size, natural proofs / Razborov–Rudich,
  ACC⁰, NEXP, hardness magnification, Frege, Karchmer–Wigderson, TC⁰, algebrization,
  or range avoidance. "KRW" appears only in an ergodic-theory paper, "relativiz"
  only in set theory, "proof system" only in the PCP-for-PPAD paper. So the
  barrier-aware programs aimed squarely at P vs NP (the algorithmic method,
  meta-complexity/magnification, proof complexity, KRW/formula lower bounds, the
  TC⁰ frontier) were apparently not targeted by the evaluation; the release's
  complexity results come from problems posed as standalone open questions.
- 20:28 UTC — **Batch 1 complete: all 17 targets pass Comparator** in an isolated
  `git archive` snapshot of fd4aeeb (pinned Lean 4.34.1, Mathlib cache, default kernel,
  permitted axioms `propext, Quot.sound, Classical.choice`): LogspaceEquality,
  ChoicelessPolynomialTime, PermanentCubic, SmoothInitialForm, DepthFive, MatchingPSD,
  MatchingAffineLift, WitnessedChoice, WeisfeilerLeman, TwoWayDeterminization,
  OneWayLiveness, OneTapeSpace, RationalHitting, FormulaHitting, UniqueGamesTheorem,
  PerfectCompleteness, IndependentSets. With `math-4a`'s DepthThree PASS, every
  formalized P-vs-NP-relevant headline in the release is independently kernel-checked
  against its trusted statement. (That certifies the *encoded* statements; whether
  each encodes the intended mathematics is the statement-audit question.)
- 20:33 UTC — **BinPackingGap Comparator PASS.** Kernel-checked in the repo's own
  model: `PEqualsNP ↔ ∃ c, poly-time bin packing within +c of optimal`, plus NP-hardness
  of the +c gap for every c (items > 1/6, five per bin) and unbounded LP/IRUP gaps.
  This is a machine-verified "P vs NP ⇔ one concrete algorithmic statement" theorem;
  combined with `formal_target/PNeNP.lean`, it gives two independent formal handles on
  the problem.
- 20:58 UTC — batch 2: BinPackingGap, KMedianThreshold, DirectedFeedback all PASS.
- First audit results (pre-skeptic; may be revised):
  - **243 (CPT+C)**, relevance 2/10: Gurevich's "no logic captures P" ⇒ (via Chen–Flum
    2010: L≤ captures P iff TAUT has a p-optimal proof system) no p-optimal proof system
    ⇒ E ≠ NE (Krajíček–Pudlák 1989) ⇒ P ≠ NP. So the logic route targets a statement
    at least as strong as P ≠ NP. It also implies no poly-time canonization, which is
    an FP^NP lower bound subject to all classical barriers. Every tool in the paper
    needs automorphism-invariance at each step, which an order-simulating logic
    escapes. New technique: a support theorem independent of set rank (curl /
    totally-isotropic stabilizers for a Heisenberg-type central extension), CFI over
    F₃ on the 3D grid, and a C^M-equivalence pebble argument at width L^{7/4} via
    discrete Loomis–Whitney. Doc inconsistency: lean/docs/243.md says WSC "not
    included" yet lists its comparator.
  - **127/132/119**, relevance 2/10: Gotsman–Linial I(f) ≤ 8d√n via a short spectral
    weighted-grading proof (parity twist + Hilbert–Schmidt energy counting + binomial
    coupling); the influence method is capped near √n/d gates and "large influence"
    is a natural property (Naor–Reingold PRFs in TC⁰). 132's α is ≈ 2.00025 (≤ ≈
    2.0065), never stated in the paper; the seed function has ~10^237 inputs; the
    architecture credits "GPT-5.6-Sol" via Meiburg 2026; the fixed-exponent corollary
    is proved in Lean but is not among the comparator-certified theorems.
- **P ⊆ NP proved** in the formal target (subagent; independently re-verified here:
  compiles in 6.6 s, axioms `propext, Classical.choice, Quot.sound`, definitions
  byte-identical, no `sorry`/`axiom`/`native_decide`/`implemented_by`). Construction:
  the verifier `(x, w) ↦ d (x ++ w)` with certificate bound 0, and a wrapper machine
  that strips the `encodeNat |x|` header with a unit counter stack in 2(b+1) steps and
  then runs the decider unchanged. Merged into `PNeNP.lean` (589 lines). Added
  Comparator challenge pairs `ChallengePNeNP` / `ChallengePEqNP` (+ `.json`) and
  `formal_target/README.md`.
- **Permanent-method ceiling: verified and sharpened** (subagent, adversarial check;
  sharpened bound re-checked here with exact integer arithmetic, `/tmp/pvsnp-sympy/check_w.py`).
  - (a) r ≤ m and (b) d ≤ m² hold, including the smooth-initial-form variant (∂_v
    commutes with taking homogeneous parts) and the trusted Lean statement
    (`SmoothInitialForm.lean:41-46`: hypothesis `hs` fails at y = v).
  - Border/limit loophole closed: "≤ k essential variables" = rank of v ↦ ∂_v F ≤ k,
    a Zariski-closed condition (subspace variety Sub_k), so limits of affine
    restrictions of per_m have ≤ m² essential variables. Padded orbit-closure forms
    ℓ^{n−m}F are never smooth.
  - Sharper: the degree-r part of per_m(A+Y) and all its first partials vanish on
    W = {Y : first m−r+2 columns zero}, dim W = m(r−2), for every A. Checked exactly
    for m = 3, 4, 5 and all r; with one fewer zero column the point is not singular.
    Hence d ≤ m(m−r+2), and the method's cap is max_r (r−1)(m(m−r+2)−1)/(4e)
    < m(m+1)²/(16e). The paper's constant 1/(5,529,600e) sits ~3.5×10⁵ below the cap.
  - Using the paper's sharp polar count B(n, d−2) ≥ r(r−1)^{d−2} (polar.tex:196-199)
    instead of the rounded (r−1)(d−1)/(4e): the certifiable size is ≤ r(d−1), still
    cubic (≈ m³/(16e) + O(m²) numerically with the sharpened d).
  - General: for any f with N essential variables and degree D, any certificate of
    this first-polar-counting type gives at most D·N, which is polynomial for every
    VNP family. **This method cannot prove superpolynomial dc/bdc(per_m), hence
    cannot separate VBP from VNP (or the border versions), let alone VP from VNP.**
- 21:09 UTC — batch 2: ParityLifts, VariableWL, WLIdentification PASS (6/6 so far).
- 21:16 UTC — **Comparator re-check complete: 27 / 27 PASS** (`comparator/summary_all.tsv`).
  Batch 2 added BinPackingGap (the `PEqualsNP ⇔ additive-constant bin packing` theorem),
  KMedianThreshold (`PNeNP ⇒ threshold 1 + 2/e`), DirectedFeedback, ParityLifts,
  VariableWL, WLIdentification, TwoWayComplementation, SensitivitySeparation,
  GotsmanLinial, MatrixMultiplication (ω ≤ 9/4 over ℂ etc.). Isolated snapshot, pinned
  toolchain and Mathlib cache, Lean default kernel, standard three axioms.
