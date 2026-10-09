# Yang Mills research handoff

**Updated October 9, 2026.** This file is the entry point for a new agent continuing the work without the chat history. The substantive results, proofs, counterexamples, review findings, source references, and executable checks are saved in this dossier. **The continuum Yang–Mills problem remains unresolved.** The results below are locally derived research arguments, not externally certified theorems or a claim of originality. The first two passes have agent reviews; the third and fourth passes have same-agent audits. The fifth pass has bounded independent agent reviews of the integral/support and lift/repair arguments, not external expert certification. The earlier analytic moment remains an explicit input.

## Read first

1. [Dossier overview](README.md): the conditional finite-volume goal and five research passes.
2. [Exact-marginal overview](exact_marginal/README.md): the newest exact integration, nonclosure result and one-step stability theorem.
3. [Exact-marginal proof](exact_marginal/exact_marginal.tex) or [PDF](exact_marginal/exact_marginal.pdf): normalized one-link integral, sparse pattern, leading-minimum extraction, lifted local energy, retained kernel, and changed effective inventory.
4. [Independent integral/support review](exact_marginal/audits/independent_integral_review.md), [independent lift/repair review](exact_marginal/audits/independent_lift_review.md), [self-audit](exact_marginal/audit.md), and [source ledger](exact_marginal/sources.md). Independent agent review is not external expert certification or an audit of the entire fine Wilson program.
5. [Weighted-boundary proof](weighted_boundary/weighted_boundary.tex) and [overview](weighted_boundary/README.md): the earlier positive class, output domination and accepted-operator versus retained-exception distinction. That original cell class is not closed by the fifth-pass operation.
6. [Boundary-cost proof](boundary_cost/boundary_cost.tex) and [overview](boundary_cost/README.md): the original Wilson energy moment, declared as input to the exact-marginal lift.
7. [Rough-region proof](rough_region/rough_region_replacement.tex), [integration audit](rough_region/audits/integration_audit.md), and [boundary obstructions](rough_region/audits/boundary_obstructions.md): the cap/Hessian argument and arbitrary-boundary obstruction remain essential.
8. [Cutoff-bridge obligations](audits/cutoff_bridge_obligations.md): downstream RG, signed mandatory-covering and fixed-physical-size requirements, not discharged by the exact one-step marginal.

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
  The numerator is a gauge-invariant frozen-loop holonomy mismatch. Its rarity was not proved in that second pass; the third pass adds a raw marginal bound.

### Third pass

The new rarity estimates concern **raw Wilson measures on periodic cubes of side `L=2^m`, `m>=2`**, not arbitrary frozen exteriors or arbitrary weights. The proof imports the standard event chessboard inequality and derives its site-reflection/edge-algebra application directly.

- For `a_H = 3/2 + log 24 + (3/2) log(8H)` and `b_H = a_H/2 + (log 2)/64`, every fixed `J` of `n` links satisfies `E_mu exp(H E_J/128) <= exp(b_H n)`. Thus `Pr(e_*,J >= v) <= min(1, exp[-H v/128+b_H n])` in the **actual exterior marginal**. A stronger one-link bound is `Pr(e_* >= u) <= min(1, exp[-H u+64a_H])`.
- The one-link mismatch from the second pass now has the marginal bound `Pr(D >= d) <= min(1, exp[-H d/12+64a_H])`. This does not make the balanced frustrated boundary condition repairable.
- For every exterior, normalized Haar on the sublevel set `E_J <= e_* + 12n/H` is a Borel gauge-covariant replacement with density at most `(24 H^(3/2))^n`. Its volume lower bound follows from the earlier minimizer-cap lemma; no measurable minimizer selection is needed. This is an existence construction, not an efficient sampler.
- On `N_p(J) >= k` and `e_* <= k p^2/(4H)`, if `k p^2 >= 96n`, every output has at most `3k/4` rough affected plaquettes and scaled energy gain at least `k p^2/8`. Absorbing the density with `k p^2 >= 16n(log 24+1.5 log H)` gives a literal **output-weighted replacement integral** at most `exp(-k p^2/16)`. The complementary high-minimum label has **raw** probability at most `exp(-k p^2/512+b_Hn)`. These two scopes cannot be combined into a general weighted theorem.
- Without any compatibility hypothesis, `Pr(N_p(J)>=k) <= min(1, exp[-k p^2/256+b_Hn])`. For the actual rough-link component through a fixed root, `Pr(|C_p|>=n) <= min(1, 18^(2(n-1)) exp[-n(p^2/1024-b_H)])`. The proof supplies witness density `k>=n/4` and pays adaptive choice by counting fixed connected subsets.
- Several fixed retained-minimum labels admit a moment bound with explicit maximum affected-plaquette overlap. Disjoint link sets can still cost an overlap factor up to four. No additivity of independently computed replacement gains is asserted.

The raw boundary-energy and component costs are therefore no longer wholly missing. What remains is an all-small compatible repair or a stable weighted/iterated defect scheme. Small or zero `e_*` is not a complete holonomy label: flat wrapping configurations can have `e_*=0` and nontrivial frozen cycles.

### Fourth pass

The third-pass proof received an adversarial same-agent reread. No mathematical error requiring a source change was found; the refined midpoint encoding and required reflection algebras are made explicit. **No independent reviewer or formal analytic certificate was obtained.**

- **General-weight obstruction:** for a high-minimum event `B` of raw probability `t`, the positive exterior-only weight `Q=((1-t)/t) 1_B+1_(B^c)` gives weighted probability `1/2` but edit ratio exactly one. The one-link example is local and gauge invariant; a continuous version also exists. Thus edit stability alone cannot control exceptional labels.
- **Sufficient general-weight condition:** `r_J=E_mu[Q|F_J]/E_mu Q` is the normalized density of the frozen touched-link marginal. If `||r_J||_r <= exp(c n)`, Hölder transfers its raw event tails with exponent `alpha=1-1/r`. Combined with an input-to-output edit ratio at most `exp(d n)`, it gives a one-region repair/exception bound in `nu_Q`. Neither hypothesis is assumed automatic for RG weights.
- **Verified extensive class:** `Q=exp(sum_C phi_C)` with bounded real gauge-invariant elementary-four-cell potentials, translation and site-reflection covariance, and `osc phi_C <= epsilon`. The law is site-reflection positive, and a `J`-edit changes `log Q` by at most `8epsilon n`. Repeating chessboard directly in this law gives `E_nu exp(H E_J/128) <= exp[(b_H+epsilon/8)n]`; no `exp(CV)` factor remains in the local estimate. This does not assert an `L^r` likelihood-ratio bound relative to raw Wilson measure.
- **One-region split in the same measure:** for `k p^2>=96n`, rough sources with `m_J<=k p^2/(4H)` have accepted output domination constant `exp[-k p^2/8+(ell_H+8epsilon)n]`, with `ell_H=log24+1.5 logH`. The high-minimum branch has probability at most `exp[-k p^2/512+(b_H+epsilon/8)n]`. The two explicit absorption budgets are stated in the proof. The squared-plaquette perturbation `gamma sum_p s(U_p)^2` is a concrete admitted example, with moment constant `b_H+3|gamma|` and sharper edit cost `24|gamma|n`.
- **Accepted repairs compose:** if `nu T_i <= c_i nu`, positivity gives `nu T_1...T_r <= product_i(c_i) nu`. Low-minimum gates must be evaluated at actual intermediate states. A specified fixed-root policy selecting the current rough component has accepted-kernel domination `c_H=exp(-d_H)/(1-324 exp(-d_H))`, where `d_H=p^2/32-ell_H-8epsilon`, under `p^2>=384` and `d_H>2 log18`; it is less than one when `d_H>log325`. This counts successive geometry changes for accepted paths only.
- **Retained exceptions do not multiply:** an identity branch on `B` has output `1_B nu`, not a small constant times `nu`. Seeing it twice still has probability `nu(B)`, not `nu(B)^2`. Joint exceptional labels in changing exteriors and full signed-covering identities remain uncontrolled. Fixed-configuration overlap moments and an accumulating bound for ungated edits are stated separately.

All four-dimensional probability results retain the dyadic periodic-cube restriction. The positive cell class is not proved invariant under exact RG. Signed activities are not positive base densities, and a fixed-root accepted subprobability process is not the full process with rejected sources retained.

### Fifth pass

The starting measure here is the **original pure Wilson law**, not a general fourth-pass cell perturbation. Fix removed links `D` with at most one on every original plaquette; keep `R=D^c`. This is partial marginalization at fixed lattice spacing, not yet a coarse-link or rescaling map.

- **Exact density:** with six-staple quaternion sum `B_e`, `b_e=|B_e|`, and `F(t)=2 I_1(t)/t`, `F(0)=1`, the retained density is `Z_H^-1 exp(-H E_0) product_e[exp(-6H) F(Hb_e)]`. It uses probability Haar and the original full `Z_H` exactly. Removed-variable factorization does not imply independence of the induced factors in retained variables.
- **Leading minimum and logarithmic remainder:** `m_e=6-b_e`, `r(t)=t-logF(t)`, `0<=r(t)<=1/2+log24+1.5log(1+t)`. Thus the density is `exp(-H E_D+W_D)/Z_H`, with `E_D=E_0+sum_D m_e` and `W_D=-sum_D r(Hb_e)`. The whole unsplit factor has order-`H` oscillation; only the remainder is logarithmic. The separated minimum has a cusp at `B=0`, canceled by the remainder in the smooth full density.
- **Original cell class does not close:** opposite staple-middle links at transverse positions `+1` and `-1` fit in no original elementary cell, yet the marginal log-factor has mixed response `(H/6)F'(6H)/F(6H)>0`. The obstruction also applies to decompositions asserted only almost everywhere, by Fubini and open robustness.
- **Reflection-invariant sparse pattern:** remove direction-zero links with arbitrary `x0` and even `x1,x2,x3`. It has `L^4/8` links and is invariant under all integer-site coordinate reflections. The complete marginal inherits their positivity by projection. Other fixed plaquette-disjoint removed sets still satisfy the lifted estimates, without a blanket reflection claim.
- **Retained edit closure:** for `J subset R`, `n=|J|`, let `A_D(J)` be removed stars whose full 18-edge support touches `J`, `a=|A|<=6n`, and `K=J union A`, so `|K|<=7n`. The local leading energy is `G_J=E_0,J+sum_A m_e=min_(u_A) E_K`, with all fine plaquettes touching `K` included. Its retained boundary minimum is `g_J=min_(z_J,u_A)E_K`. Consequently `E_nu exp(HG_J/128)<=exp[b_H(n+a)]`, and similarly for `g_J`.
- **Retained kernel and weighted branches:** normalized Haar on `G_J<=g_J+12n/H` has density at most `(24 H^(3/2))^n`. The cap proof fixes the removed part of a joint fine minimizer and varies only `J`, so it does not differentiate the nonsmooth minimum and pays `n`, not `n+a`, in sampling entropy. Residual edit cost is at most `a r_H`, `r_H=1/2+log24+1.5log(1+6H)`. For `k p^2>=96n`, the low-minimum accepted output is dominated by `exp[-kp^2/8+ell_H n+a r_H] nu_D`; the exceptional branch has probability at most `exp[-kp^2/512+b_H(n+a)]` in the same exact marginal.
- **Changed inventory:** the effective nonnegative labels are retained original plaquettes (energy at most 2, support 4) and removed-star minima (energy at most 6, support 18). Rough means label energy greater than `p^2/(2H)`. These are not the individual eliminated plaquettes. The effective adjacency bound is 102, witness factor 18, and component exponent `p^2/4608-7b_H`; all labels are empty only at `p^2>=12H`, not the old `4H` threshold.
- **Accepted iteration is within one marginal:** a fixed-root current-component policy with low-minimum gates has accepted output factor `exp(-d_H)/(1-10404 exp(-d_H))`, `d_H=p^2/144-ell_H-6r_H`, under `p^2>=1728` and `d_H>2log102`; it is less than one when `d_H>log10405`. This is repeated repair, not repeated integration. Retained exceptional branches still need joint control; fixed-configuration estimates include the actual lifted-plaquette overlap.

The fifth-pass integral/support and lift/repair arguments receive separate bounded independent agent reviews. These do not certify the entire earlier moment proof or the continuum program. The exact one-step result does not provide uniform constants at later elimination depths.

## Exact next task

**Specify a second exact elimination or a true block-link map and track the support and constant growth.** The fifth pass performs a real first marginalization and proves one-step local repair/exception estimates despite failure of the original cell class. A later removal sees the induced multi-staple factors; sharing no original plaquette no longer guarantees conditional factorization.

A useful next deliverable should state:

1. The exact retained/coarse variables and map, the complete positive density and full normalizer, and which effective or fine inventories are retained.
2. The new dependency supports or eliminated connected components. Determine whether the leading minima and local remainders can still be bounded with depth-uniform costs; do not merely reuse the factor-seven closure or logarithmic one-step constants.
3. A proved moment/marginal estimate in that endpoint and a valid local repair kernel, differentiating a smooth lift when the leading energy is a nonsmooth minimum.
4. Reflection inheritance only for a map that respects the relevant halves, and explicit joint bounds for retained exceptional labels and changing exteriors. Signed restricted sums are never normalizers.
5. A proof, a precise support/cost growth law, or a counterexample, with tests and preserved earlier sources. A failure of uniform closure must be recorded as such rather than called an RG flow.

Controlled compatible enlargement and exact mandatory-covering constructions remain alternative routes. No step here supplies all-small, original-inventory-preserving filling or a nontrivial continuum limit.

Farther downstream, the finite-volume strategy still needs a successful test at fixed physical size along the cutoff trajectory. A common-volume-subtracted log-partition comparison on physical boxes `M` and `2M` with error `C R^4 epsilon_K` would transfer defects with error `32 C M^4 epsilon_K`. Neither this comparison nor its reference small-defect input is established for the required Yang–Mills trajectory. Nontrivial continuum observables, their short-distance identification and reconstruction remain separate obligations. No extension from SU(2) to all compact simple groups has been proved.

## Do not lose these qualifications

- Boundary-energy tails are marginal, not conditional on arbitrary frozen data. The fourth pass admits its declared positive cell weights; the fifth treats a specific exact marginal of pure Wilson measure using a lift instead. Its effective labels differ from the original removed plaquettes. Partial cooling is not original-inventory preservation.
- The exact sparse product requires at most one removed link per original plaquette. Its conditional factorization and constants do not automatically persist after another elimination. Leading minima may be nonsmooth even though the full marginal density is smooth.
- Accepted repair operators compose only with their actual gates and paid geometry. Retained exceptional identity branches do not have the small operator bound; their marginal probabilities cannot simply be multiplied.
- Arbitrary-boundary all-small removal is disproved; do not reintroduce it as an assumption supposedly obtained from a cap-volume estimate.
- Small plaquette curvature does not automatically give the specified small frozen-loop residuals. Their path lengths and geometry matter.
- The finite-link space is connected. A continuum degree obstruction needs stated interpolation, admissibility, or sector restrictions; it is not an unrestricted discrete filling obstruction.
- One bad plaquette cannot pay entropy for an arbitrarily padded region. Disjoint link sets can still share plaquette energies. Adaptive support selection needs counting or an aggregate density estimate.
- The literal positive-weight replacement integral evaluates `Q` at the **output**, and is not generally a probability or bounded by one. The fourth-pass probability/output theorem pays an explicit input-to-output ratio and separately controls boundary bias. Signed base densities remain excluded.
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
(cd boundary_cost && \
 pdflatex -interaction=nonstopmode -halt-on-error boundary_cost.tex && \
 pdflatex -interaction=nonstopmode -halt-on-error boundary_cost.tex)
(cd weighted_boundary && \
 pdflatex -interaction=nonstopmode -halt-on-error weighted_boundary.tex && \
 pdflatex -interaction=nonstopmode -halt-on-error weighted_boundary.tex)
(cd exact_marginal && \
 pdflatex -interaction=nonstopmode -halt-on-error exact_marginal.tex && \
 pdflatex -interaction=nonstopmode -halt-on-error exact_marginal.tex)
```

The top-level runner includes all five passes. It was rerun successfully during this handoff on October 9, 2026. The third pass adds 20 Python tests; the fourth adds 30 and a four-mutation validation record. These include exact finite-group diagnostics, not four-dimensional SU(2) integration. The fifth adds 31 tests and five mutation controls. None of these three follow-ups adds a Lean theorem. Rerun LaTeX again if it reports changed labels. Existing per-script output and Lean mutation-check records are saved alongside the scripts. Python checks use the standard library. Standalone Lean scripts point to the installed **Lean 4.34.1** under `/home/rou/.elan/toolchains/`; on another machine adjust the compiler path and install the matching toolchain. No Mathlib download or build of the repository's large Lean project is required for these certificates.

Final main-source SHA-256 values, to distinguish reviewed revisions from later edits:

```text
22a3c353e7e1abf6a1abd1c994b7a1c38ad6d118411abfbbc058efc2970b36a4  finite_volume_criterion.tex
6f6ee90e89c6156cfd142c463dd6cb68c19c4f6c9b78705522b510673d753038  rough_region/rough_region_replacement.tex
8bbfdee9e0be49d2cd7524ea718d2f489c34a17671ae2b41ded8b06e20498745  boundary_cost/boundary_cost.tex
ae5f41176f97d21f895855b42b9ab6f448905b5b3d1ea96acbb579eb5934fd8e  weighted_boundary/weighted_boundary.tex
29c5ff27d0fe50c67612ab1af732ab0e0b29b9b8966a234ded914d2a77f2b9f2  exact_marginal/exact_marginal.tex
```

## Workspace and portability

- Current workspace: `/home/rou/src/math-nvcodex-yang-mills`. The first two passes originated in `/home/rou/src/math` at inspected base revision `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.
- The first two passes are tracked in commit `c7456ca3a` (`add yang mills research notes`). The third-, fourth- and fifth-pass artifacts and updated entry points are included with this handoff in the follow-up research commit on branch `math-nvcodex-yang-mills`. Use `git log -- research_notes/yang_mills_2026_10_09` to identify the saved revision; these files no longer require separate workspace copying.
- Published preprints and the repository Lean project were not changed. Other research directories are unrelated work; preserve them.
- Historical agents from the first two passes finished. The third and fourth passes used no subagents. The fifth pass used one independent review agent for two bounded audit scopes; its reports and final correction checks are saved in `exact_marginal/audits/`. The reviewer has finished; no background task needs recovery. No external expert review is claimed.
- These are durable technical notes, not a verbatim chat or raw scratch transcript. External papers are cited with locators and access limits, but not every original PDF is bundled. One literature audit used a PDF under `research_notes/yang-mills-mass-gap/work-06-lit/downloads-balaban/`, outside this dossier. The elementary local proofs and executable tests do not depend on that file; reopening that literature requires its cited source or retained local copy.

## Suggested restart instruction

> Read `research_notes/yang_mills_2026_10_09/HANDOFF.md`, then the exact-marginal proof and independent audits. Specify a second elimination or genuine block-link map, track the induced supports/minima/remainders and effective inventory, and prove a depth-uniform estimate or an explicit obstruction. Preserve earlier sources and save a precise result with tests in a new directory. Do not assume the original cell class closes, reuse the one-step constants without proof, conflate accepted repairs with RG steps, multiply repeated retained-label tails, or claim continuum existence.
