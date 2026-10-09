# Self audit of marginal boundary costs and partial cooling

**October 9, 2026.** This is a same-agent audit of the written argument and executable controls, **not independent agent review or external certification**. No novelty claim is made. The standard chessboard theorem remains a named analytic dependency; tests do not prove it or the four-dimensional measure estimates.

## Critical proof chain

1. **Normalization.** The model uses probability Haar and nonnegative Wilson energy. An event forcing total energy at least `M u` has unnormalized numerator at most `exp(-H M u)`. Omitting probability normalization or using the unshifted action without its corresponding constant would invalidate that line.
2. **Partition lower bound.** All links in the geodesic cap `rho=(8H)^(-1/2)` imply `E <= 48 V rho^2`. There are `4V` independent link variables, not `6V` independent plaquettes. Consequently `-log Z <= 4V a_H`, with `12 H rho^2 = 3/2`.
3. **Correct reflection.** The reflection goes through integer-coordinate site planes and inverts normal links whose orientation reverses. Tangential fixed-plane links remain fixed. No plaquette meets both strict halves. Conditioning on fixed-plane links produces a square of a half-integral and proves reflection positivity. This is not a bond-reflection or arbitrary-boundary positivity assertion.
4. **Imported inequality.** The event chessboard theorem is applied to geometric edge algebras on closed side-two blocks. Shared faces are allowed by the closed-half construction; they are not copied independently. The power-of-two volume restriction is explicit.
5. **Dissemination count.** A central prototype link starts at local coordinate `0` or `1` along its direction and at `1` in the other coordinates. Its six plaquettes have interiors inside its block. Reflected copies have disjoint plaquette sets even though some frozen links are shared. There are `M=V/16` blocks, giving `4V/M=64` in the star tail.
6. **Class decomposition.** Direction and the four starting-site parities give 64 classes. A class has one star per block of an explicitly shifted grid. Pulling back from an odd longitudinal block exchanges the two prototypes; the chessboard inequality permits different block events.
7. **No independence shortcut.** Within a class, joint tails are bounded by a product using chessboard. Expanding a finite product of layer-cake integrals then gives the moment bound. Across classes, Hölder costs a factor 64. The sum of all link-star energies actually equals `4E`, so an uncolored disjointness assertion would be false.
8. **Tail constants.** Choosing `theta=1/2` gives `H/128`. Rough plaquette energy is greater than `p^2/(2H)`, giving `p^2/256`. A witness can serve four links, giving `p^2/1024` in the component exponent.
9. **Minimum marginal.** `e_*,J(z) <= E_J(U)` pointwise gives its exponential moment in the actual exterior marginal. No estimate is asserted after fixing an arbitrary exterior.
10. **Overlap.** Summing retained minima is bounded by the maximum plaquette overlap times the union energy. For disjoint link sets that multiplicity is at most four, not one. This does not authorize adding independently computed replacement gains.

## Near minimum kernel

The target is the full sublevel set `E_J <= e_* + 12n/H`, not a chosen minimizer. The minimizer-cap lemma guarantees its Haar volume is at least `(24 H^(3/2))^(-n)`. Continuity of `e_*` and parameter integration give a Borel normalization; gauge transformations carry the target set onto its transformed counterpart and preserve Haar. Thus the kernel needs neither a measurable minimizer selector nor a gauge-fixing section.

This is an existence construction; no efficient general sublevel sampler or minimum solver is implemented. The one-link tests have an exact minimum and cap description and check support, volume, and covariance in that special case.

On the low-minimum class `e_* <= k p^2/(4H)`, the budget `k p^2 >= 96n` gives output rough count at most `3k/4` and scaled energy gain at least `k p^2/8`. Absorbing the density cost with `k p^2 >= 16n ell_H` leaves `exp(-k p^2/16)` for the literal output-weighted integral.

The high-minimum label is paid **only under the raw measure**, with exponent `-k p^2/512+b_H n`. This cannot be added to the positive-weight integral as if both were probabilities in the same weighted measure. Signed weights are not covered. Some individual new rough plaquettes may be created, despite the decrease in total count.

## Adaptive regions

For the actual rough-link set, a connected component of size at least `n` contains a connected `n`-link subset through the root. Each link in this subset has a rough witness, so at least `ceil(n/4)` distinct rough plaquettes touch it, including witnesses not wholly inside the subset. Sum the fixed-set estimate over at most `18^(2(n-1))` possible subsets.

No conditioning on a selected geometry occurs. No lower bound on the excess `E_J-e_*` is inferred merely from this count. Subsequent replacements change the distribution; iterating the raw-measure rarity bound on their outputs is not justified without a new density/weight analysis.

## Negative controls

- **Frustrated star:** all six affected energies sum to 6 for every central link, and `e_*=6`. Conditional removal gain is zero. A marginal cost for this exterior does not contradict its conditional rough probability of one.
- **Padded isolated defect:** a single `-I` link in an otherwise identity field has total energy 12. Enlarging the editable set does not turn this into a gain proportional to the number of edited links.
- **Overlapping edits:** the explicit two-link energies `(12,10,10,12)` refute adding two separately computed gains.
- **Flat winding holonomy:** all plaquettes and all `e_*,J` vanish, but the frozen touched graph of a wrapping strip can retain a nontrivial cycle. Energy labels are not complete frozen-holonomy labels.
- **Repeated block:** exact Z2 enumeration violates the purported chessboard bound if the same block event is counted twice as though it occupied distinct blocks.
- **Arbitrary weight:** `Q=exp(H E)` cancels Wilson suppression and gives product Haar. The high-minimum/roughness bounds are not automatically available after reweighting.

## Validation scope

The 20 tests use only Python's standard library. They exhaust the stated reflection and class geometry on `4^4` and `8^4` tori, test SU(2) quaternion identities and sublevel support, check rational budget constants, and verify exact event inequalities in a `4x4` two-dimensional Z2 gauge model. The Z2 plaquette law is justified by a GF(2) incidence-rank check; its even-parity configurations and weights are enumerated exactly.

The tests do not compute a four-dimensional SU(2) partition function, sample continuum fields, or formalize a theorem. Earlier standalone Lean files still cover only their original scalar components. The written theorem's scopes are periodic dyadic cubes, the raw Wilson measure for rarity, and the specified low-minimum class for partial cooling.
