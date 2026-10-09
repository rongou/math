# Sources and proof dependencies

**Inspected October 9, 2026.** The one-link formula is derived directly from probability Haar on `SU(2)=S^3`; the special-function reference fixes its conventional normalization. The remaining one-step bounds use the explicitly named local results from earlier passes. No continuum or RG theorem is imported, and no novelty claim is made.

## Primary Bessel definitions

NIST *Digital Library of Mathematical Functions*, modified Bessel functions:

- Equation **10.32.2**, angular integral representation. At order one, it identifies the normalized spherical integral as `2 I_1(t)/t`.
- Equation **10.25.2**, defining power series. It gives `F(t)=sum_j (t^2/4)^j/[j!(j+1)!]` and the continuous value `F(0)=1`.

The exact equation sources were fetched and inspected, not inferred from a search snippet:

```text
https://dlmf.nist.gov/10.32.E2.tex
https://dlmf.nist.gov/10.25.E2.tex
```

The remainder bound is proved by the local Haar-cap estimate; it does not use a nonuniform large-`t` asymptotic near zero staple sum.

## Local analytic inputs

- [Second-pass proof](../rough_region/rough_region_replacement.tex): the six-staple identity, robust frustrated-star example, probability-Haar cap bound, and smooth fine minimizer Hessian estimate.
- [Third-pass proof](../boundary_cost/boundary_cost.tex), Theorem 1.1: the fine Wilson exponential moment for every fixed edited set. The new marginal inherits it through a declared pointwise lifted-energy bound; no new chessboard argument on a punctured graph is assumed.
- [Fourth-pass proof](../weighted_boundary/weighted_boundary.tex): the positive-weight output domination argument, accepted subprobability composition, and counterexamples to multiplying retained-label probabilities. The elementary-cell theorem is **not** applied to the new induced interactions because its support hypotheses fail.

The prior reflection-positive fine Wilson quadratic form is used for a marginal only when the removed set is reflection invariant. Algebraic marginalization alone is not asserted to give all desired reflection properties for an arbitrary removed set.

## Independent review scope

The [integral/support audit](audits/independent_integral_review.md) and [lift/repair audit](audits/independent_lift_review.md) record the independently reviewed source state and limitations. These are agent reviews, not external expert certification and not an independent audit of the entire original fine-model program. The third-pass moment remains an explicit analytic input.

Exact finite Q8 and Z2 calculations in the tests are separate diagnostic models. They do not replace probability Haar integration in four-dimensional SU(2), certify the operator argument in Lean, or establish an iterated RG flow.
