# Exact sparse marginals and one step stability

**Fifth research pass, October 9, 2026.** This tests the preceding estimates on an **exact marginal of the original pure SU(2) Wilson model**, rather than a separately postulated perturbation. One-link integration and its sparse extension are explicit. The old elementary-cell interaction class fails to close, but a different lifted argument gives a one-region repair and exceptional-label bound with local logarithmic costs.

Read the [proof PDF](exact_marginal.pdf), [LaTeX source](exact_marginal.tex), [integral and support review](audits/independent_integral_review.md), [lift and repair review](audits/independent_lift_review.md), [self-audit](audit.md), and [sources](sources.md). Independent **agent** review is not external expert certification. The four earlier proof sources are unchanged. **No repeated RG flow, cutoff comparison, continuum construction, mass-gap proof, or novelty claim is made.**

## Exact integration

Fix removed links `D` such that no original plaquette contains two of them. Keep the other links `z`. On each removed link, form the six frozen staple transporters and their quaternion sum `B_e`, with `b_e=|B_e|` in `[0,6]`. Then

\[
\int_{SU(2)}e^{-H E_e(u,z)}du
=e^{-6H}F(Hb_e),\qquad
F(t)=\frac{2I_1(t)}t,\quad F(0)=1.
\]

Probability Haar is used. Conditional factorization in removed variables gives the exact marginal

\[
d\nu_D(z)=Z_H^{-1}e^{-H E_0(z)}
\prod_{e\in D}[e^{-6H}F(Hb_e(z))]dz,
\]

with **the original full partition function `Z_H`**, not an unknown or restricted normalizer. `E_0` includes only plaquettes containing no removed link.

A concrete sparse pattern removes direction-zero links at arbitrary `x0` and even `x1,x2,x3`: `|D|=L^4/8`. It is plaquette-disjoint and invariant under every integer-site coordinate reflection. The complete marginal therefore inherits site-reflection positivity from the fine model. The algebraic identities and lifted bounds work for other fixed plaquette-disjoint `D` too; reflection positivity is asserted only when the removed set has the needed invariance.

## The important split and the closure obstruction

Write

\[
m_e=6-b_e,\quad r(t)=t-\log F(t),\quad
\mathcal E_D=E_0+\sum_{e\in D}m_e,\quad W_D=-\sum_{e\in D}r(Hb_e).
\]

Then `nu_D` has density `exp(-H E_D + W_D)/Z_H`, and

\[
0\le r(t)\le\tfrac12+\log24+\tfrac32\log(1+t).
\]

The entire induced log-factor has oscillation `6H-O(log H)`: **it is not a small perturbation unless its boundary minimum is retained as leading energy**. After that extraction, each remainder is only `O(log H)`, uniformly including `B=0`.

The induced interaction genuinely couples opposite staple-middle links that fit in no common original elementary four-cell. Its mixed response is nonzero, whereas any sum of original cell-supported functions has zero mixed response for that pair. Thus the previous cell class is **not closed even under one link removal**. Larger support does not destroy positivity of the complete exact marginal when reflection inheritance applies.

The split leading energy has a cusp at `B=0`, although the full exact density is smooth. The new proof never differentiates that cusp.

## One-region bound in the actual marginal

For a fixed retained edit `J`, set

- `n=|J|`;
- `A_D(J)` = removed stars whose frozen support touches `J`;
- `a=|A_D(J)| <= 6n`;
- `K=J union A_D(J)`, so `|K|<=7n`.

Keep the **complete** energy of each affected removed star. The resulting local leading energy is

\[
G_J(z)=E_{0,J}(z)+\sum_{e\in A_D(J)}m_e(z)
      =\min_{u_{A_D(J)}}E_K(u,z).
\]

For its retained boundary minimum `g_J=min_(z_J) G_J`, the original Wilson moment transfers exactly:

\[
\mathbb E_{\nu_D}e^{H G_J/128}\le e^{b_H(n+a)},\qquad
\nu_D(g_J>v)\le\min\{1,e^{-Hv/128+b_H(n+a)}\}.
\]

This is a marginal estimate, not a statement at an arbitrarily fixed exterior. It needs no new chessboard theorem on the retained graph.

The retained sublevel `G_J <= g_J+12n/H` has Haar volume at least `(24 H^(3/2))^(-n)`. To prove this, hold the removed coordinates fixed at a **joint fine minimizer** and vary only the `n` retained edited links; the original smooth Hessian bound applies. The resulting normalized sublevel kernel is Borel and gauge covariant. It is an existence construction, not a generic sampling algorithm.

Its residual log-weight cost is at most `a r_H`, where

\[
r_H=\tfrac12+\log24+\tfrac32\log(1+6H).
\]

For `k` rough **effective labels** and `k p^2>=96n`, the accepted low-minimum output satisfies

\[
\nu_D T_{J,k}\le
 e^{-kp^2/8+\ell_H n+a r_H}\nu_D,
\]

and the high-minimum label has probability at most

\[
e^{-kp^2/512+b_H(n+a)}.
\]

Both branches use the **same exact marginal**. `ell_H` and `b_H` retain their preceding definitions. The proof states the additional absorption budgets explicitly; all costs are proportional to the edited/lifted region, not the ambient volume or total number of removed links.

## The inventory has changed

The effective labels are:

1. original plaquettes containing no removed link, with energy `s(U_q)`;
2. removed-star minima `m_e`, with all 18 frozen detour links as support.

Rough means label energy greater than `p^2/(2H)`. A star label is **not an individual eliminated plaquette**, and partial repair does not restore the original fine inventory. Star values range up to six, not two; the original all-plaquette emptiness threshold cannot be reused for these labels.

Each retained link meets at most six effective supports, each of size at most 18. The proof pays the resulting adjacency bound 102 and witness factor 18 in an actual effective-component tail. A counted fixed-root accepted repair kernel also composes in this **one fixed marginal**. Repeated exceptional identity labels still cannot be multiplied as independent costs; fixed-configuration overlap bounds are stated separately.

## What remains next

This is exact partial marginalization, **not a rescaling or an iterated renormalization theorem**. A second removal generally sees coupled multi-staple interactions, even when candidate links share no original plaquette. The one-step constants and supports cannot simply be reused.

The next concrete task is to specify a second exact elimination or a true block-link map, track the support and defect-label growth, and prove a depth-uniform positive endpoint class—or exhibit precisely where the constants grow. Joint retained defects, signed mandatory coverings, all-small inventory-preserving repairs, the fixed-physical-size defect test, and continuum reconstruction remain separate obligations.

## Checks

```bash
./check.sh
pdflatex -interaction=nonstopmode -halt-on-error exact_marginal.tex
pdflatex -interaction=nonstopmode -halt-on-error exact_marginal.tex
```

The [31 standard-library tests](checks/check_exact_marginal.py) include the normalized continuous one-link integral, stable scaled quadrature, exact Q8 link algebra, complete lifted supports, and an exactly enumerated **separate two-dimensional Z2 marginal**. They also test the no-removal limit, zero-staple endpoint, changed inventory, and failure of factorization for shared removed plaquettes. [Output](checks/output.txt).

The runner also checks the original suite under `python -O` and rejects five intentionally corrupted variants in temporary files. [Mutation runner](checks/check_mutations.py), [validation output](checks/validation-output.txt).

These are diagnostics, not formal proofs or a numerical evaluation of a four-dimensional SU(2) partition function. No new Lean theorem is claimed.
