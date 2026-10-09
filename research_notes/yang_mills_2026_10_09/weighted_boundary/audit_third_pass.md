# Adversarial reread of the third pass

**October 9, 2026. Verdict:** no mathematical error requiring a change to the third-pass proof was found in this bounded reread. The midpoint encoding below makes its application of the imported chessboard theorem more explicit. **This is a same-agent audit, not independent review, external acceptance, or formal certification.**

Reviewed source:

```text
8bbfdee9e0be49d2cd7524ea718d2f489c34a17671ae2b41ded8b06e20498745  ../boundary_cost/boundary_cost.tex
```

## Reflection and the imported theorem

The inspected Biskup–Kotecký author manuscript, §2.2, Theorem 2.4, uses closed blocks, distinct placements, a reflection involution respecting support, and reflection positivity. The author lecture notes, §5.3, Theorem 5.8, make explicit that positivity at the designated block-boundary reflections suffices. The fourth-pass proof retains the third pass's dyadic volume restriction.

Place the link `(x,x+e_mu)` at midpoint `2x+e_mu` on a refined torus of side `2L`. Active sites have one odd coordinate; all other refined sites can be filled with deterministic dummy variables. Original side-two blocks become closed side-four blocks. Site-plane reflections preserve this pattern. Normal links are inverted when their orientation reverses, tangential fixed-plane links are left fixed, and reflections in different coordinate directions commute with these inversions. Parallel reflections at different positions need not commute and are not assumed to.

Every original plaquette lies in one closed half or in a reflecting plane. Conditional on the tangential fixed-plane variables, the two half measures are reflected copies. The integral of `f theta(f)` is therefore a positive fixed-plane integral of a squared half-integral. Shared block-face links are retained in that fixed-plane integral, not sampled independently. The abstract repeated Cauchy–Schwarz proof applies to these geometric edge algebras. This is not an assumption that all refined-lattice reflection planes, including ones not used by the blocking, are positive.

## Star dissemination and 64 classes

The two central-star prototypes have starting coordinate `0` or `1` along their direction and `1` in all transverse directions. Each star's six plaquettes has its relative interior inside the closed side-two block. Thus reflected star plaquette sets do not overlap, although some edge variables can be shared on block faces.

Classifying by link direction and four starting-site parities gives 64 classes. A grid shifted according to the class places one link in each block. Pulling back from an odd longitudinal block swaps the two prototypes. The event chessboard theorem allows the resulting different base events.

The decisive factors were checked separately:

- `V=L^4`, `M=V/16`, and `4V/M=64`.
- Cap radius `(8H)^(-1/2)` gives scaled total energy at most `6V` and log-partition lower bound `-4V a_H`.
- Disseminated star energy is at most the full total energy because its plaquette sets are disjoint.
- The uncolored sum of all link-star energies is **four times** total energy. It is not disjoint.
- Within a class the event inequality controls joint tails; layer-cake expansion supplies the moment bound. Across classes, Hölder contributes the stated factor 64.

The resulting moment coefficient `H/128`, rough-event coefficient `p^2/256`, and component coefficient `p^2/1024` follow without dropping an overlap or witness factor.

## Minimum, kernel, and counting

The minimum tail is a consequence of `e_*,J <= E_J` in the actual exterior marginal. It is not a uniform conditional tail after fixing an obstructed boundary. The exact balanced star still has zero removable excess energy.

The sublevel kernel has a positive-volume target by the minimizer-cap Hessian bound. A Borel target and parameter integral give a measurable normalization; the construction needs no measurable minimizer selector. Gauge transformations preserve both energy and Haar, so they transport the target and its normalized measure correctly.

The partial-cooling constants `96`, `16 ell_H`, `512`, and `1024 b_H` were checked against their separate energy, density, and exceptional-label steps. The positive-weight integral evaluates `Q` at the output; it is not generally the weighted source probability.

For an actual rough component, every connected `n`-link subset has at least `ceil(n/4)` witness plaquettes touching it. A witness may extend outside the subset. The bound counts fixed subsets before integrating; it never applies a conditional Gibbs law after the subset has been selected.

## Strengthened executable controls

The third-pass runner is retained. The new fourth-pass checks use a separate geometric implementation for elementary cells and refined link midpoints, plus exact noncommuting Q8 fields to verify orientation inversions and gauge covariance. Omitting normal-link inversion is detected. Weighted two-dimensional Z2 event inequalities are checked by exact finite enumeration; repeated use of the same block as distinct placements is rejected.

These computations test the stated bookkeeping, not all possible configurations or the imported theorem. Independent analytic review and any formalization beyond the earlier scalar certificates remain outstanding. All three earlier proof sources were preserved unchanged.
