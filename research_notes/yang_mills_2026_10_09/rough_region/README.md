# Rough link replacement with boundary conditions

**Second research pass, October 9, 2026.** This follows the [finite-volume criterion](../README.md). It establishes a concrete finite-block replacement estimate under an explicit boundary condition, plus an arbitrary-boundary excess-energy estimate. It also disproves the stronger arbitrary-boundary all-small filling claim. **It does not prove the cutoff-comparison estimate, construct a continuum theory, or solve Yang–Mills.** No novelty claim is made.

Read the [proof PDF](rough_region_replacement.pdf) or its [LaTeX source](rough_region_replacement.tex).

## 1. An unrestricted replacement theorem would be false

One editable SU(2) link is incident to six plaquettes. Freeze their three-edge detours so three prefer the identity and three prefer minus the identity. These are consistent assignments to actual links, not independently assigned plaquettes.

For every choice of the editable link,

\[
E_J(U)=3(1-\tfrac12\operatorname{Tr}U)+3(1+\tfrac12\operatorname{Tr}U)=6.
\]

At least three affected plaquettes have operator curvature at least `sqrt(2)`. No interior-link replacement can make all six small while preserving this exterior. The impossibility persists on an **open, positive-measure set of boundary data**, not just the displayed central-sign example. Their probability is not shown to stay positive uniformly as the inverse coupling grows.

This is boundary frustration, **not** an asserted continuum topological obstruction. Unrestricted finite-link configuration space is connected. Continuum degree arguments require additional interpolation or regularity assumptions; the earlier dossier's degree warning must be read with that qualification.

For one link the unavoidable energy also has an explicit gauge-invariant description. Write its six staple transporters as unit quaternions `s_j`, and `B = sum s_j`. Then

\[
e_*(z)=6-|B|=\frac{\sum_{i<j}|s_i-s_j|^2}{6+|B|}.
\]

The numerator measures frozen-loop holonomy mismatch. This supplies a concrete defect quantity to retain or charge—not a proof that it is rare.

## 2. What holds for every boundary

Let `J` be a fixed set of `n` edited links, `E_J` the sum of Wilson plaquette energies over **all** affected plaquettes, and `e_*(z)` its minimum over the interior with frozen exterior `z`. For inverse coupling `H >= 1`,

\[
\Pr_H(E_J\ge e_*(z)+h\mid z)
\le\min\{1,\exp[-Hh+n(12+\log24+\tfrac32\log H)]\}.
\]

The proof uses a cap around a conditional minimizer and a uniform Hessian bound. **It bounds energy above the boundary-forced minimum, not that minimum itself.** In the frustrated example, every configuration is already a minimizer and the conditional law is Haar.

## 3. A genuine gauge-covariant removal kernel

For each fixed `J`, take all frozen links on its affected plaquettes and choose a spanning forest of that graph. Require its fundamental-cycle holonomies, expressed in the tree frames, to lie within operator distance `H^(-1/2)` of identity. This is an explicit gauge-invariant, sufficient compatibility condition; it is **not** proved typical, necessary, or implied by small local plaquette curvature.

Random root frames and independent central Haar caps then give a measurable gauge-covariant kernel that:

- leaves every link outside `J` unchanged;
- has conditional edited-link density at most `(24 H^(3/2))^n`;
- makes every affected plaquette curvature at most `4/sqrt(H)`;
- has affected energy at most `48n/H`, improving to `12n/H` for exactly flat-compatible boundary data;
- automatically obeys link-induced plaquette identities and preserves loops supported entirely in the frozen exterior.

No claim is made to preserve loops crossing `J` or an interpolated topological charge.

For `p >= 4`, call a plaquette rough when its curvature exceeds `p/sqrt(H)`. If `k` affected plaquettes are rough, the compatible-boundary probability bound is

\[
\Pr_H(\text{at least }k\text{ rough plaquettes}\mid z)
\le\min\{1,\exp[-kp^2/2+n(48+\log24+\tfrac32\log H)]\}.
\]

The same bound holds **unconditionally for the joint event** “compatible exterior and at least `k` rough affected plaquettes.” It is not a bound for all rough configurations with arbitrary exterior.

The proof also gives a positive-weight replacement integral with the same exponential bound, **without** truncation by one. Such an integral is not generally a probability. A probability statement for a reweighted model requires a separate bound on the weight's change under replacement; signed RG weights are not silently included.

## 4. Why this still does not close the cutoff argument

A density cost proportional to `n log H` must be paid from enough removable energy. Merely enclosing one bad plaquette in a large region does not supply that energy. If a region-selection argument could establish at least `n/s` rough affected plaquettes and compatibility, the explicit budget

\[
p^2\ge4s(48+\log24+\tfrac32\log H)
\]

gives decay `exp[-n p^2/(4s)]`. An elementary connected-set count then sums these **specified compatible events**. This is not a construction of the required regions.

**The next missing estimate is precise:** control incompatible boundary holonomies and the boundary-forced minimum, either by enlarging the region with controlled cost or by retaining and bounding the unavoidable defects. That must come with sufficient removable energy per edited link. It must eventually survive the additional interactions generated by exact renormalization. A conditional one-block tail does not provide any of those steps.

The [boundary audit](audits/boundary_obstructions.md) gives an additional sharp necessary condition: a frozen loop of SU(2) angle `alpha` bounding a disk of `m` plaquettes forces at least one plaquette curvature of `2 sin(alpha/(2m))` or larger. This explains both the obstruction to too-small fillings and how a larger region can distribute holonomy; it is not a general extension theorem.

## Audits and validation

- [Boundary obstructions](audits/boundary_obstructions.md): explicit star, open-set robustness, finite-area loop lower bounds, and topology qualifications.
- [Gauge-covariant kernel](audits/gauge_covariant_kernel.md): forest construction, stabilizers, Borel measurability, density, and pointwise curvature estimates.
- [Integration audit](audits/integration_audit.md): change-of-measure, minimum-energy estimate, positive-weight scope, geometry/counting qualifications.
- [Literature context](audits/literature.md): five original sources with exact access limits; no claim they provide the full missing estimate.
- [Executable checks](checks/check_replacement.py): deterministic finite-link diagnostics and negative controls, **not proofs**; [output](checks/output.txt).
- [Scalar and integration controls](checks/check_scalar_controls.py): exact positive-weight and adaptive-support counterexamples, absorption arithmetic, and quaternion minimum-energy diagnostics; [output](checks/scalar-output.txt).
- [Lean scalar scope](formal/README.md): natural-number incidence inequalities and constants only; no graph, analytic, probability, or Yang–Mills formalization.

Run from this directory:

```bash
./check.sh
pdflatex -interaction=nonstopmode -halt-on-error rough_region_replacement.tex
pdflatex -interaction=nonstopmode -halt-on-error rough_region_replacement.tex
```

The earlier finite-volume proof and published sources are preserved. Independent agent review is not external expert certification.
