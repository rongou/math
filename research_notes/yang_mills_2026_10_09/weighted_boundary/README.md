# Weighted boundary costs and accepted repairs

**Fourth research pass, October 9, 2026.** The previous pass controlled roughness in the raw Wilson measure. This pass gives a **one-region weighted comparison** for an explicit class of positive interactions, identifies the missing hypothesis for general weights, and proves a limited composition rule for successful repairs. It does not construct RG endpoint weights, a mandatory covering expansion, a cutoff comparison, or a continuum theory. No novelty claim is made.

**Exact follow-up:** the [fifth pass](../exact_marginal/README.md) now integrates a sparse set of links in pure Wilson measure exactly. It proves the original elementary-cell class fails to close, but recovers one-step repair and exceptional-label estimates by a fine-variable lift and an explicit logarithmic remainder. That operation is not repeated RG or a coarse-lattice rescaling.

Read the [proof PDF](weighted_boundary.pdf), [LaTeX source](weighted_boundary.tex), [third-pass adversarial audit](audit_third_pass.md), [weighted-proof self-audit](audit.md), and [source ledger](sources.md). All three earlier proof sources are unchanged. This is **same-agent review**, not independent certification.

## Why edit stability was not enough

Let `B` be a high-minimum boundary event with raw probability `t` in `(0,1)`. The positive weight

\[
Q=\frac{1-t}{t}\,1_B+1_{B^c}
\]

makes its weighted probability exactly `1/2`. Because `B` depends only on frozen links, **the weight does not change under any edited-link replacement**. This is an actual one-link Wilson construction using the frustrated-star boundary label, not just an abstract probability example. Continuous positive versions also exist.

Thus a bound on `Q(input)/Q(output)` pays for successful edits but cannot, by itself, pay for exceptional boundaries.

For a general positive weight, the new sufficient condition concerns the normalized **local marginal density**

\[
r_J=\frac{\mathbb E_{\mu_H}[Q\mid F_J]}{\mathbb E_{\mu_H}Q},
\]

where `F_J` is the frozen touched-link sigma algebra, involving at most `18|J|` links. If `||r_J||_r <= exp(c |J|)`, Hölder transfers the raw exceptional-label tail with exponent loss `1-1/r`. This hypothesis is explicit; it is **not** established for arbitrary RG weights.

## A class where both branches are actually proved

Keep the four-dimensional SU(2) Wilson model on periodic cubes `L=2^m`, `m>=2`, with probability Haar and `H>=1`. Admit

\[
d\nu_W=Z_W^{-1}e^{-HE+W}\,dU,\qquad W=\sum_C\phi_C,
\]

where each real, bounded, gauge-invariant potential `phi_C` depends only on links of an **elementary four-cell**, has oscillation at most `epsilon`, and the family is translation- and site-reflection-covariant, including link orientation inversions. Real potentials can have either sign; the complete Boltzmann density must be positive.

A cell does not cross both strict halves of an integer-site reflection, so reflection positivity follows directly. Each link belongs to eight cells, giving

\[
|W(x)-W(y)|\le8\epsilon |J|
\]

for a `J`-edit. Repeating the chessboard proof in the **weighted measure itself** gives

\[
\mathbb E_{\nu_W}e^{H E_J/128}
\le e^{(b_H+\epsilon/8)|J|},
\]

with `b_H` from the third pass. This also bounds the boundary-forced minimum. There is **no whole-volume factor** in the final local estimate. This structural proof is a separate route; it does not assert the local likelihood-ratio condition above for every cell weight.

### One-region repair versus exception

Set `n=|J|` and let the source have at least `k` rough affected plaquettes at threshold `p/sqrt(H)`. Split at `e_*,J = k p^2/(4H)`. For `k p^2 >= 96n`,

\[
\nu_W(N_p(J)\ge k)
\le\min\left\{1,
 e^{-kp^2/8+(\ell_H+8\epsilon)n}
 +e^{-kp^2/512+(b_H+\epsilon/8)n}\right\},
\]

where `ell_H = log 24 + (3/2) log H`.

- **Low minimum:** the sublevel kernel sends the source to at most `3k/4` rough affected plaquettes. More strongly, its accepted **output submeasure** is bounded by the first exponential times the same `nu_W`.
- **High minimum:** the second exponential pays for the retained boundary label under that same `nu_W`. No repairability is asserted on this branch.

The absorption budgets are `k p^2 >= 16n(ell_H+8 epsilon)` and `k p^2 >= 1024n(b_H+epsilon/8)`.

For probabilities alone, the direct weighted moment gives a stronger tail than this split. The added content is **control of the repair output**, usable with integrable output observables.

### Explicit example

The class includes

\[
W_\gamma=\gamma\sum_q\bigl(1-\operatorname{Tr}(U_q)/2\bigr)^2
\]

for either sign of `gamma`. One may use `epsilon=24|gamma|`, hence moment constant `b_H+3|gamma|`; direct counting improves the edit cost to `24|gamma| n`. This is a nontrivial perturbation of the continuous SU(2) Wilson action. It is **not** evidence of closure under exact RG.

## Which repeated repairs are justified

If an accepted repair kernel satisfies `nu T_i <= c_i nu`, positivity gives

\[
\nu T_1\cdots T_r\le(c_1\cdots c_r)\nu.
\]

This permits predetermined successful repairs with low-minimum gates checked on their **actual intermediate states**, even when affected plaquettes overlap. A fixed family of source-selected supports can also be summed, but its geometry count must be paid.

There is also a concrete adaptive accepted kernel: at a fixed root, select the **current** rough component and accept its repair only if its minimum is below the declared threshold. For `p^2>=384` and `d_H=p^2/32-ell_H-8epsilon > 2 log 18`, its output is dominated by

\[
c_H\nu_W,\qquad c_H=\frac{e^{-d_H}}{1-18^2e^{-d_H}}.
\]

This is less than one when `d_H>log 325` and composes as `c_H^r` for paths of `r` accepted repairs. It counts changed geometry each step without pretending the output has the original Gibbs law.

This does **not** apply to the identity branch retaining an exceptional label. Encountering the same rare event twice has probability `nu(B)`, not `nu(B)^2`. Joint exceptional labels, changing exteriors, and arbitrary adaptive histories still require separate control. The full stay-put-on-rejection process is not the accepted subprobability kernel.

The proof also extends the counted rough-component tail to the admitted weighted class, and gives an accumulating density bound for predetermined ungated sublevel edits. Neither is cost-free reuse of the original law.

## What is next

The one-region weighted obstruction is now resolved **for the declared class**, not for arbitrary weights. The next concrete task is to specify an exact coarse-graining step or complete covering-weight construction and test:

1. Is its **complete base density** positive, with the required reflection structure or a replacement marginal-density estimate?
2. Are its local edit and exceptional-label costs uniformly proportional to affected support?
3. Can joint retained defects and full inventories be controlled without multiplying repeated marginal tails or normalizing by signed restricted sums?

Elementary-cell support is not assumed to survive RG. Signed activities, mandatory covering identities, all-small inventory-preserving filling, and the fixed-physical-size defect test remain unproved.

## Checks and trust

```bash
./check.sh
pdflatex -interaction=nonstopmode -halt-on-error weighted_boundary.tex
pdflatex -interaction=nonstopmode -halt-on-error weighted_boundary.tex
```

The [30 standard-library tests](checks/check_weighted_boundary.py) cover exact rational change-of-measure identities, the exterior-tilt counterexample, accepted output domination and composition, cell geometry, exact noncommuting Q8 link algebra, and weighted chessboard diagnostics in a **different two-dimensional Z2 model**. [Captured output](checks/output.txt) and [validation record](checks/validation-output.txt). The runner also reproduces the four [mutation controls](checks/check_mutations.py) in temporary files and checks the original suite under `python -O`.

These tests do not calculate four-dimensional SU(2) probabilities or prove an analytic theorem. No new Lean result is claimed. The earlier checks and scalar certificates remain in the combined runner.
