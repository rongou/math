# Yang Mills research handoff

**Updated October 9, 2026.** This file is the entry point for a new agent continuing the work without the chat history. The substantive results, proofs, counterexamples, review findings, source references, and executable checks are saved in this dossier. **The continuum Yang–Mills problem remains unresolved.** The results below are locally derived research arguments with agent review, not externally certified theorems or a claim of originality.

## Read first

1. [Dossier overview](README.md): the original goal and conditional finite-volume criterion.
2. [Rough-region overview](rough_region/README.md): the most recent work and the immediate remaining problem.
3. [Rough-region proof source](rough_region/rough_region_replacement.tex) or [PDF](rough_region/rough_region_replacement.pdf): precise definitions and quantifiers. This is the current analytic starting point.
4. [Integration audit](rough_region/audits/integration_audit.md), [boundary obstructions](rough_region/audits/boundary_obstructions.md), and [kernel audit](rough_region/audits/gauge_covariant_kernel.md): pitfalls and independent checks.
5. [Cutoff-bridge obligations](audits/cutoff_bridge_obligations.md): how a successful local estimate would need to connect to the larger program. Its first-pass proposed replacement target has now been partially answered by the rough-region work; do not mistake it for wholly unattempted work.

The [finite-volume proof source](finite_volume_criterion.tex), [PDF](finite_volume_criterion.pdf), and [SU(2) transfer interface](audits/su2_transfer_interface.md) supply the earlier spectral component. Both `audits/literature_scope.md` and `rough_region/audits/literature.md` record literature limitations. The two-dimensional source audit does **not** certify the full Family 215 continuum construction.

## Current mathematical state

### First pass

For exact, consistently normalized positive transfer traces in every coordinate direction,

\[
D_\beta(n)=16\log Z_\beta(n,n,n,n)-\log Z_\beta(2n,2n,2n,2n)
\]

satisfies the conditional implication

\[
D_\beta(n)\le1/2048
\implies \lambda_2(2^kn)/\lambda_1(2^kn)\le2^{-1/n}.
\]

Here `n >= 4` is even and the spatial cross-sections are **dyadic three-dimensional cubes**. The proof uses `D(2r) <= 700 D(r)^2 <= 1024 D(r)^2`. The extension to local-limit vacuum representations has explicit canonical OS translation, reflection positivity, density, and regularity assumptions. It does not imply all-state uniqueness, every rectangular-volume bound, or a result for all charged sectors.

The Wilson finite-lattice interface `K=MCPM` is derived separately, including gauge projection and the periodic closing holonomy. The only supplied direct small-defect application is a tiny known strong-coupling range `beta <= 2^-26`; it is not a weak-bare-coupling continuum trajectory. At zero coupling the transfer is rank one, illustrating why the criterion alone cannot prove nontriviality.

### Second pass

Conventions: unrestricted SU(2) link variables, product **probability Haar**, all periods at least four, and Wilson weight `exp(-H E)`, where `H >= 1` is the inverse coupling and `E=sum_p(1-Tr U_p/2)`. For a fixed editable link set `J`, `n=|J|`, include **every** plaquette touching `J` in `E_J`.

- **Unrestricted all-small filling is false.** A one-link boundary with three `+I` and three `-I` staple transports forces `E_J=6` for every interior value and at least three curvatures at least `sqrt(2)`. The impossibility persists on an open set of exterior data. This is not a claim that those data have probability bounded below uniformly in `H`.
- **Every boundary has an excess-energy bound.** With `e_*(z)=min_x E_J(x,z)`,
  `Pr(E_J >= e_*+h | z) <= min(1, exp[-H h+n(12+log 24+1.5 log H)])`.
  This does **not** bound the boundary-forced minimum.
- **Compatible boundaries permit genuine removal.** A specified frozen-graph spanning forest defines gauge-invariant fundamental-loop residuals. If every residual has operator distance at most `H^-1/2` from identity, random root frames and independent geodesic caps yield a Borel gauge-covariant replacement with density at most `(24 H^(3/2))^n`, affected curvature at most `4/sqrt(H)`, and affected energy at most `48n/H` (`12n/H` for exactly flat-compatible data). Only the edited-link law depends solely on the frozen touched edges; the full output also copies the exterior.
- **The compatible rough-event estimate** for `p >= 4`, positive integer `k`, and roughness threshold `p/sqrt(H)` is
  `Pr(#rough >= k | compatible z) <= min(1, exp[-k p^2/2+n c_H])`,
  where `c_H=48+log 24+1.5 log H`. There is also a joint-event bound including compatibility, not a bound for arbitrary exteriors.
- **A concrete one-link defect quantity:** if the six staples are unit quaternions `s_j` and `B=sum s_j`, then
  `e_*(z)=6-|B|=sum_(i<j)|s_i-s_j|^2/(6+|B|)`.
  The numerator is a gauge-invariant frozen-loop holonomy mismatch. Its rarity has not been proved.

## Exact next task

**Control incompatible boundaries and obtain enough removable energy per edited link.** Either construct a quantitatively controlled enlargement/selection of editable regions whose frozen boundaries meet a useful compatibility condition, or retain the unavoidable boundary defects with bounds sufficient for integration and summation.

A useful starting point is the explicit one-link defect above and the [frozen-loop finite-area lower bounds](rough_region/audits/boundary_obstructions.md). Test any proposed selection rule on the frustrated star, large padded regions containing only one defect, and overlapping edits before claiming a general estimate.

A successful next deliverable should state:

1. The admitted region and boundary-data class, any retained holonomy/defect labels, and which links remain frozen.
2. A bound on their statistical or integration cost—not merely a conditional bound with compatibility assumed.
3. A lower bound on removable energy compared with the number of edited links and the sampling entropy, with constants and uniformities explicit.
4. A treatment of source-dependent region choice, affected-plaquette overlap, and the number of possible geometries.
5. A proof or a counterexample, plus reproducible checks. Any extension to RG-generated interactions must state and prove its extra hypotheses separately.

The existing absorption `k >= n/s` and `p^2 >= 4s c_H` gives `exp[-n p^2/(4s)]`, but **no region-selection theorem supplies those premises yet**. The connected-set count only sums events already known to satisfy them.

Farther downstream, the finite-volume strategy still needs a successful test at fixed physical size along the cutoff trajectory. A common-volume-subtracted log-partition comparison on physical boxes `M` and `2M` with error `C R^4 epsilon_K` would transfer defects with error `32 C M^4 epsilon_K`. Neither this comparison nor its reference small-defect input is established for the required Yang–Mills trajectory. Nontrivial continuum observables, their short-distance identification and reconstruction remain separate obligations. No extension from SU(2) to all compact simple groups has been proved.

## Do not lose these qualifications

- Arbitrary-boundary removal is disproved; do not reintroduce it as an assumption supposedly obtained from a cap-volume estimate.
- Small plaquette curvature does not automatically give the specified small frozen-loop residuals. Their path lengths and geometry matter.
- The finite-link space is connected. A continuum degree obstruction needs stated interpolation, admissibility, or sector restrictions; it is not an unrestricted discrete filling obstruction.
- One bad plaquette cannot pay entropy for an arbitrarily padded region. Disjoint link sets can still share plaquette energies. Adaptive support selection needs counting or an aggregate density estimate.
- The positive-weight replacement integral evaluates `Q` at the **output**, and is not generally a probability. It has no automatic truncation by one. Reweighted probabilities need extra stability; signed RG weights are not covered by assumption.
- The replacement kernel is gauge-covariant but is not asserted to preserve reflection positivity, mixed-loop holonomies, or an interpolated topological charge.
- Lean certifies only the documented scalar arithmetic/induction; it does not formalize the analytic, spectral, gauge, or continuum results. Passing numerical tests is not a proof.
- Originality and independent expert acceptance remain undetermined. Keep theorem conclusions separate from hypotheses still to be discharged.

## Run and validate

From this dossier directory:

```bash
./check.sh

pdflatex -interaction=nonstopmode -halt-on-error finite_volume_criterion.tex
pdflatex -interaction=nonstopmode -halt-on-error finite_volume_criterion.tex
(cd rough_region && \
 pdflatex -interaction=nonstopmode -halt-on-error rough_region_replacement.tex && \
 pdflatex -interaction=nonstopmode -halt-on-error rough_region_replacement.tex)
```

The top-level runner includes both passes. It was rerun successfully during this handoff on October 9, 2026. Existing per-script output and Lean mutation-check records are saved alongside the scripts. Python checks use the standard library. Standalone Lean scripts point to the installed **Lean 4.34.1** under `/home/rou/.elan/toolchains/`; on another machine adjust the compiler path and install the matching toolchain. No Mathlib download or build of the repository's large Lean project is required for these certificates.

Final main-source SHA-256 values, to distinguish reviewed revisions from later edits:

```text
22a3c353e7e1abf6a1abd1c994b7a1c38ad6d118411abfbbc058efc2970b36a4  finite_volume_criterion.tex
6f6ee90e89c6156cfd142c463dd6cb68c19c4f6c9b78705522b510673d753038  rough_region/rough_region_replacement.tex
```

## Workspace and portability

- Repository: `/home/rou/src/math`, inspected base revision `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.
- **This dossier is local and untracked in Git at handoff.** A fresh agent in this workspace can read it. A clean clone will not contain it unless it is copied or committed; no commit or push was performed.
- Published preprints and the repository Lean project were not changed. Other research directories are unrelated work; preserve them.
- The user authorized parallel agents and a separate notes directory. All agents from these two passes have finished; no background task must be recovered.
- These are durable technical notes, not a verbatim chat or raw scratch transcript. External papers are cited with locators and access limits, but not every original PDF is bundled. One literature audit used a PDF under `research_notes/yang-mills-mass-gap/work-06-lit/downloads-balaban/`, outside this dossier. The elementary local proofs and executable tests do not depend on that file; reopening that literature requires its cited source or retained local copy.

## Suggested restart instruction

> Read `research_notes/yang_mills_2026_10_09/HANDOFF.md`, then the rough-region proof and audits. Continue the incompatible-boundary/region-selection problem specified there. Preserve the existing proofs, distinguish conditional estimates from discharged inputs, and save a precise lemma with proof or counterexample and tests in a new subdirectory. Do not assume typical compatibility, additive gains for overlapping edits, or continuum existence.
