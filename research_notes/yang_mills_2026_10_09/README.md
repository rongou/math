# Yang Mills finite volume research dossier

**Date:** October 9, 2026. **Starting repository revision:** `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

This first research pass audits Family 215's finite-volume argument and derives a four-dimensional version applicable to the pure SU(2) Wilson lattice model. **It does not resolve the Yang–Mills Millennium problem or construct a continuum theory.** No novelty claim is made. The published preprints and existing Lean project are unchanged.

**New agent:** start with [HANDOFF.md](HANDOFF.md) for the current proof state, reading order, next task, checks, and workspace-transfer caveats.

## Second pass: rough link replacement

The [rough-region dossier](rough_region/README.md) now contains an [eight-page proof](rough_region/rough_region_replacement.pdf) and independent audits. It establishes:

1. **An obstruction:** arbitrary frozen boundary links need not permit removal of all rough affected plaquettes. An explicit one-link example remains obstructed on an open boundary-data set.
2. **An arbitrary-boundary bound:** energy above the conditional minimum has an explicit exponential tail. The boundary-forced minimum itself is not bounded.
3. **A restricted removal theorem:** a measurable gauge-covariant Haar-cap kernel removes rough plaquettes under an explicit frozen-holonomy compatibility condition, with density cost and integrated suppression quantified.

This does not construct the compatible-region selection or control incompatible boundary data. It also clarifies that continuum degree obstructions do not automatically obstruct unrestricted finite-link filling. The first-pass finite-volume proof below is unchanged.

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

**Current next analytic target:** after the [restricted replacement result](rough_region/README.md), control incompatible boundary holonomies and the boundary-forced energy minimum, or construct controlled region enlargements that yield useful compatible boundaries. This must include enough removable energy per edited link and the cost of selecting regions. Arbitrary-boundary all-small filling is already disproved; the remaining task is not to assume that obstruction away.

## Audits and their scope

- [Two-dimensional source audit](audits/two_dimensional_audit.md): checks scalar, spectral and local-limit arguments. Finds a harmless initial-index qualification in the source half-period argument and supplies missing exposition; the follow-up checks the four-dimensional proof. The new note explicitly fixes the canonical OS time translation and regularity assumptions. This does not certify upstream mixing or RG estimates.
- [SU(2) transfer interface](audits/su2_transfer_interface.md): finite-lattice structural proof and normalization checks.
- [Adversarial checks](audits/adversarial_checks.md): counterexamples to weakened assumptions and limits of the four-dimensional conclusion.
- [Cutoff-bridge obligations](audits/cutoff_bridge_obligations.md): precise source dependencies, exponents, formalization scope and the missing gauge-theory estimates.
- [Literature scope](audits/literature_scope.md): primary-source comparison; no assertion of originality.

These are independent agent reviews, not external expert certification or a full audit of Family 215.

## Reproducible checks

Run from this directory:

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

Tests support the written proof but do not replace its analytic hypotheses. No numerical partition-function or continuum mass estimate is presented.
