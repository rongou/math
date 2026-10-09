# Yang Mills finite volume research dossier

**Date:** October 9, 2026. **Starting repository revision:** `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

This dossier started by auditing Family 215's finite-volume argument and deriving a four-dimensional version applicable to the pure SU(2) Wilson lattice model; four follow-ups address rough-region replacement, boundary costs, weighted comparison, and an exact sparse marginal of the Wilson model. **It does not resolve the Yang–Mills Millennium problem or construct a continuum theory.** No novelty claim is made. The published preprints and existing Lean project are unchanged.

**New agent:** start with [HANDOFF.md](HANDOFF.md) for the current proof state, reading order, next task, checks, and workspace-transfer caveats.

## Fifth pass: an exact marginal and one-step stability

The [exact-marginal dossier](exact_marginal/README.md) adds a [ten-page proof](exact_marginal/exact_marginal.pdf), bounded independent agent reviews, and 31 tests. It performs a specified operation on the **original pure Wilson measure**, not an assumed RG endpoint:

1. **Exact one-link and sparse integration:** for removed links sharing no plaquette, each star integrates to `exp(-6H) F(Hb)`, with `F(t)=2 I_1(t)/t` and `F(0)=1`. The retained density has the original full normalizer `Z_H`.
2. **A proved nonclosure and a useful split:** the induced interaction couples opposite staples and cannot be a sum of original elementary-cell interactions. Extracting the minimum `6-b` as leading energy leaves a remainder bounded by `r_H=1/2+log24+(3/2)log(1+6H)` per removed link; the unsplit factor has order-`H` oscillation.
3. **A one-step repair/exception estimate in that exact marginal:** a retained edit of `n` links lifts to at most `7n` fine links, inherits their energy moments, and admits a near-minimum retained kernel with density cost `(24 H^(3/2))^n`. Both branches are paid in the same marginal, with no ambient-volume prefactor. The effective rough inventory is explicitly different from the removed plaquette inventory.

An invariant sparse pattern retains site-reflection positivity by projection. This is exact partial marginalization, not rescaling, repeated RG closure, signed covering control, or a continuum theorem. The four earlier proof sources remain unchanged.

## Fourth pass: weighted comparison and accepted repairs

The [weighted-boundary dossier](weighted_boundary/README.md) adds a [ten-page proof](weighted_boundary/weighted_boundary.pdf), an [adversarial reread of the third pass](weighted_boundary/audit_third_pass.md), and 30 tests. It establishes:

1. **A precise missing condition for general weights:** edit stability alone does not control frozen-boundary bias. An exterior-only, positive gauge-invariant tilt provides a counterexample. A normalized local marginal-density bound is a sufficient extra hypothesis.
2. **A verified positive weighted class:** bounded translation- and site-reflection-covariant interactions on elementary four-cells retain the needed reflection positivity. Their energy-moment cost is `b_H+epsilon/8` per edited link, and their edit cost is at most `8epsilon` per edited link. The two branches of the one-region comparison are controlled in the **same** weighted measure, with no full-volume prefactor.
3. **Output domination for accepted repairs:** specified successful repairs compose with their actual intermediate-state gates. A counted fixed-root adaptive accepted kernel is also controlled. Repeated exceptional identity labels do **not** acquire independent small factors.

This supplies a one-region weighted result for a declared class, not an RG closure or signed-covering theorem. The earlier proof sources are unchanged. The review is same-agent, not independent certification.

## Third pass: marginal boundary costs and partial cooling

The [boundary-cost dossier](boundary_cost/README.md) adds a [nine-page proof](boundary_cost/boundary_cost.pdf), a self-audit, and 20 executable checks. On periodic cubes of side `L = 2^m`, `m >= 2`, in the raw SU(2) Wilson model it derives:

1. **A marginal cost for unavoidable boundary energy:** an exponential moment for every fixed affected energy `E_J`, and hence an exponential tail for its boundary-forced minimum under the actual Wilson exterior marginal.
2. **A near-minimum kernel for every boundary:** uniform sampling from `E_J <= e_* + 12|J|/H` is Borel and gauge-covariant, with an explicit Haar-density bound. On a stated low-minimum class it reduces the rough count and releases enough energy under explicit budgets; high-minimum labels have a separate raw-measure cost.
3. **A counted bound for actual rough components:** site reflection, the standard event chessboard estimate, a 64-class decomposition and explicit witness counting give exponential component-size tails without assuming forest compatibility.

This advances the raw statistical and partial-replacement steps. It does **not** make arbitrary boundaries repairable, pay exceptional labels under arbitrary weights, or establish an RG-stable comparison. The third pass is self-audited, not independently agent-reviewed. The two earlier proof sources are unchanged.

## Second pass: rough link replacement

The [rough-region dossier](rough_region/README.md) now contains an [eight-page proof](rough_region/rough_region_replacement.pdf) and independent audits. It establishes:

1. **An obstruction:** arbitrary frozen boundary links need not permit removal of all rough affected plaquettes. An explicit one-link example remains obstructed on an open boundary-data set.
2. **An arbitrary-boundary bound:** energy above the conditional minimum has an explicit exponential tail. The boundary-forced minimum itself is not bounded.
3. **A restricted removal theorem:** a measurable gauge-covariant Haar-cap kernel removes rough plaquettes under an explicit frozen-holonomy compatibility condition, with density cost and integrated suppression quantified.

That second pass does not construct compatible-region selection or control incompatible boundary data; the third pass adds the specifically scoped follow-up above. It also clarifies that continuum degree obstructions do not automatically obstruct unrestricted finite-link filling. The first-pass finite-volume proof below is unchanged.

## Main result

The human-readable proof is in [finite_volume_criterion.pdf](finite_volume_criterion.pdf), with [LaTeX source](finite_volume_criterion.tex).

For consistently normalized positive transfer traces in every coordinate direction, set

\[
D_\beta(n)=16\log Z_\beta(n,n,n,n)-\log Z_\beta(2n,2n,2n,2n).
\]

If an even `n >= 4` satisfies `D_beta(n) <= 1/2048`, the proof gives

\[
\frac{\lambda_2(2^k n)}{\lambda_1(2^k n)}\le2^{-1/n}
\quad\text{for every }k\ge0.
\]

Here the transfer cross-section is a **three-dimensional spatial cube** of side `2^k n`; the eigenvalues range over the full gauge-invariant finite-slice Hilbert space. The key recursion is

\[
D_\beta(2r)\le700D_\beta(r)^2\le1024D_\beta(r)^2.
\]

With the separately stated local-observable/reflection-positivity interface, the bound passes to every local limit along these dyadic tori, on its full **vacuum-sector local-observable Hilbert space**. It does not prove uniqueness of all Gibbs states, estimates for every rectangular cross-section, or a statement about all charged representations.

The [SU(2) interface audit](audits/su2_transfer_interface.md) derives `K = M C P M`, including the gauge projection, positive character expansion, trace class, simple leading eigenvalue, exact periodic trace and bounded slab insertions. These are mathematical derivations, not Lean-certified operator results.

### A deliberately weak consistency check

For probability Haar measure and the unshifted Wilson weight `exp[(beta/2) sum Tr U_p]`, Jensen's inequality yields `0 <= log Z_beta(n,n,n,n) <= 6 beta n^4`. Thus

\[
D_\beta(4)\le24576\beta\le3/8192<1/2048
\quad(0\le\beta\le2^{-26}).
\]

This recovers a tiny known **strong-coupling** regime. It supplies no weak-bare-coupling or continuum input. At `beta=0` the transfer is rank one, so the test itself cannot establish nontriviality. The finite-slice physical L2 space is still infinite dimensional; rank-one propagation kills its orthogonal-to-vacuum directions.

## What remains unproved

The decisive missing estimate is a successful box of **fixed physical size** along an asymptotically free trajectory:

\[
a\,n(a)\to R_0\in(0,\infty),\qquad
D_{\beta(a)}(n(a))\le1/2048
\quad\text{for all sufficiently small }a.
\]

That would give cutoff physical transfer masses bounded below by `log(2)/R0`. Nontrivial continuum fields, their required Yang–Mills short-distance behavior, reconstruction axioms and compatible convergence are still separate obligations.

The note makes a precise sufficient comparison step explicit. With `F_N(R) = log Z_betaN((R B^N)^4)` and **one common volume-proportional subtraction** at each cutoff, a bound

\[
|\widetilde F_N(R)-\widetilde F_K(R)|\le C R^4\epsilon_K
\quad(R=M,2M;\ N\ge K)
\]

implies `|D_N(M)-D_K(M)| <= 32 C M^4 epsilon_K`. A reference test and this error must both fit into the threshold. **Neither required Yang–Mills estimate is proved.** The schematic budget `4 gamma < alpha` is sufficient only for a proposed mixing-versus-comparison scheme, not a necessary condition for solving Yang–Mills.

**Current next analytic target:** specify a second exact elimination or a true block-link map after the [first exact-marginal step](exact_marginal/README.md). Track the induced supports, leading minima, remainder costs and effective inventories, and prove depth-uniform bounds or a precise obstruction. The original elementary-cell class is now shown not to close under even one removal, although the one-step estimates survive by a fine lift. Do not assume the closure factor seven repeats uniformly or that retained exceptional labels multiply independently. Signed mandatory coverings and the fixed-physical-size defect test remain downstream.

## Audits and their scope

- [Two-dimensional source audit](audits/two_dimensional_audit.md): checks scalar, spectral and local-limit arguments. Finds a harmless initial-index qualification in the source half-period argument and supplies missing exposition; the follow-up checks the four-dimensional proof. The new note explicitly fixes the canonical OS time translation and regularity assumptions. This does not certify upstream mixing or RG estimates.
- [SU(2) transfer interface](audits/su2_transfer_interface.md): finite-lattice structural proof and normalization checks.
- [Adversarial checks](audits/adversarial_checks.md): counterexamples to weakened assumptions and limits of the four-dimensional conclusion.
- [Cutoff-bridge obligations](audits/cutoff_bridge_obligations.md): precise source dependencies, exponents, formalization scope and the missing gauge-theory estimates.
- [Literature scope](audits/literature_scope.md): primary-source comparison; no assertion of originality.

The first two passes have independent agent reviews, not external expert certification or a full audit of Family 215. The [third-pass audit](boundary_cost/audit.md) and [fourth-pass audit](weighted_boundary/audit.md) are explicitly same-agent reviews; independent review remains outstanding.

## Reproducible checks

Run `./check.sh` from this directory for all five passes. The earlier individual checks remain:

```bash
python3 checks/check_finite_volume.py
python3 checks/check_su2_interface.py
./formal/check.sh
pdflatex -interaction=nonstopmode -halt-on-error finite_volume_criterion.tex
pdflatex -interaction=nonstopmode -halt-on-error finite_volume_criterion.tex
```

- [Finite-volume checks](checks/check_finite_volume.py): exact coefficient identities for all 24 coordinate orders, exact rational constant certificates, positive-spectrum and actual product-chain regression examples, and counterexamples to weaker hypotheses. Uses only Python's standard library; [captured output](checks/last_run.txt).
- [SU(2) interface diagnostics](checks/check_su2_interface.py): fixed-seed matrix checks in all four transfer directions, gauge covariance, wrapping holonomy, beta-zero rank-one propagation, and character/quadrature diagnostics; [captured output](checks/check_su2_interface_output.txt). These do not evaluate a partition function or prove the operator theorem.
- [Lean certificate and scope](formal/README.md): a standalone, axiom-free **denominator-cleared natural-number scalar induction**. It derives the intermediate bounds from explicit recurrence/local-loss assumptions. It does **not** formalize arbitrary real inputs, the spectral estimates, the transfer model, or Yang–Mills.
- [Lean compiler transcript](formal/compiler-output.txt) and [mutation tests](formal/validation-output.txt): checked with installed Lean 4.34.1 and no downloaded dependencies or changes to the repository's Lean configuration.

The [third-pass checks](boundary_cost/checks/check_boundary_cost.py) additionally exercise reflection/block geometry, sublevel support, exact scalar budgets, and an exact two-dimensional Z2 comparison model. They do not calculate four-dimensional SU(2) probabilities.

The [fourth-pass checks](weighted_boundary/checks/check_weighted_boundary.py) add exact positive-weight counterexamples, output-domination/composition controls, elementary-cell incidence and noncommuting Q8 link algebra, and weighted finite Z2 diagnostics. Four deliberately corrupted variants are rejected by the recorded mutation checks.

The [fifth-pass checks](exact_marginal/checks/check_exact_marginal.py) add the continuous normalized one-link formula, independent scaled quadrature, exact sparse-support and lift checks, and separate finite-group marginalization diagnostics. Five recorded mutation controls catch wrong normalization, omitted minima, a false closure constant and an incorrect mixed-response coefficient. The [bounded independent reviews](exact_marginal/audits/independent_integral_review.md) are not external expert certification.

Tests support the written proofs but do not replace their analytic hypotheses. No numerical partition-function or continuum mass estimate is presented.
