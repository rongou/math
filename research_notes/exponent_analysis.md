# Exponent barriers and a sufficient moment theorem

The statements labeled **Derived** below are elementary consequences of
explicit hypotheses. Statements labeled **Research target** are unproved.
No claim of novelty is made for these reductions.

## 1 The original sums and the sixth power loss

Follow [R11, `sec:reduction`]. Let \(K=\mathbb Q(\sqrt{-3})\), with ring
\(\mathcal O_K\), ideal norm \(N\), and ideal Möbius function \(\mu_K\).
Fix a finite-order Hecke character \(\nu\), a finite set \(S\) of prime ideals
including those above 2 and 3 and those in its conductor, and
\(W\in C_c^\infty((0,\infty);\mathbb C)\). Write

\[
 A_u(D)=\sum_{(\mathfrak n,S)=1}
   \mu_K(\mathfrak n)\nu(\mathfrak n)
   \chi_{\mathfrak n}(u)W(N\mathfrak n/D),
 \qquad \chi_{\mathfrak n}(u)=(u/n)_6,
\]

where \(n\) is the primary generator. Rows \(u\) are nonzero Eisenstein
integers; columns are ideals. The sixth-power identity is

\[
 \chi_{\mathfrak n}(p^6)=\mathbf1_{\mathfrak p\nmid\mathfrak n},
 \qquad A_{p^6}(D)=A_1(D)+O_W(D/Y)
\]

for primes \(Y/2<N\mathfrak p\le Y\), outside \(S\). The error follows by
counting the \(O_W(D/Y)\) ideals in the support divisible by \(\mathfrak p\).
There are \(\asymp Y/\log Y\) such primes for fixed \(K,S\) and large \(Y\).
Their primary sixth powers give distinct rows with norm at most \(Y^6\).
The coprimality error cannot be discarded. [R11]

The companion claims

\[
 \sum_{0<Nu\le H}|A_u(D)|^2\ll D^{1+\varepsilon}H,
 \qquad H=D^{1+\vartheta},\quad 0<\vartheta\le1/10.
\]

**Derived.** Set \(Y=H^{1/6}\), average over these replicas, and absorb the
logarithmic prime count into the exponent loss:

\[
 |A_1(D)|^2\ll D^{1+\varepsilon}H^{5/6}+D^2H^{-1/3}.
\]

For \(H=D^h\), the two exponents for \(|A_1|\) are

\[
 a_6(h)=\max\left\{\frac12+\frac{5h}{12},\;1-\frac h6\right\}.
\]

In the stated range \(h=1+\vartheta\), the first dominates and approaches
\(11/12\) as \(\vartheta\downarrow0\). This limit means choosing a small,
fixed \(\vartheta\) for each requested exponent loss. It does not assert a
uniform estimate at \(\vartheta=0\).

### A barrier for this extraction inequality

**Derived under a hypothetical extension of the same second moment to other
scales.** The first affine function increases and the second decreases. Their
intersection is \(h=6/7\), where both equal \(6/7\). Thus

\[
 \inf_{h>0}a_6(h)=6/7>1/2.
\]

The manuscript does **not** establish its second moment at this optimizing
scale. Consequently \(6/7\) is not a new zero-free theorem. It only proves
that changing the averaging scale, while keeping this two-term inequality,
cannot reach RH. Better control of the replica error or a different extractor
would change the calculation.

For an abstract analogous \(k\)-th-power construction, the second-moment
crossover is \(k/(k+1)\). Merely increasing the order of the power makes this
particular loss worse, not better; no existence claim about such families is
being made.

## 2 A moment hierarchy that would reach the critical line

**Hypothesis at a specified scale.** For a fixed integer \(m\ge1\), suppose

\[
 \sum_{0<Nu\le H}|A_u(D)|^{2m}
       \ll_{\nu,S,W,m,\varepsilon}D^{m+\varepsilon}H,
 \qquad H=D^h.
 \tag{M}
\]

**Derived.** The inequality
\(|a+b|^{2m}\le2^{2m-1}(|a|^{2m}+|b|^{2m})\) and the same prime replicas give

\[
 |A_1(D)|\ll
 D^{1/2+\varepsilon}H^{5/(12m)}+D H^{-1/6}.
 \tag{1}
\]

Constants may depend on \(m\). For an abstract \(k\)-th-power replica system,
the exponent is

\[
 a_{k,m}(h)=\max\left\{
 \frac12+\frac{(k-1)h}{2mk},\;1-\frac hk\right\}.
\]

Its algebraic optimum, **if the moment bound is available there**, is

\[
 h_{k,m}=\frac{mk}{2m+k-1},\qquad
 a_{k,m}=\frac{m+k-1}{2m+k-1}.
\]

For sextic replicas:

| \(m\) | Moment | Hypothetical scale exponent \(h\) | Consequent exponent for \(A_1\) |
| --- | --- | --- | --- |
| 1 | 2nd | \(6/7\) | \(6/7\) |
| 2 | 4th | \(4/3\) | \(7/9\) |
| 3 | 6th | \(18/11\) | \(8/11\) |
| 4 | 8th | \(24/13\) | \(9/13\) |
| 10 | 20th | \(12/5\) | \(3/5\) |
| 100 | 200th | \(120/41\) | \(21/41\) |

**Every row of this table is conditional.** The table is an exact calculation,
not numerical evidence for any moment estimate.

### A simpler sufficient target at one fixed scale

**Research target HM.** For every fixed \(m\ge1\), every
\(\varepsilon>0\), and every smooth compactly supported complex \(W\), prove

\[
 \sum_{0<Nu\le D^3}|A_u(D)|^{2m}
       \ll_{\nu,S,W,m,\varepsilon}D^{m+3+\varepsilon}.
 \tag{HM}
\]

Then (1), with replica primes of norm \(Y=D^{1/2}\), gives

\[
 |A_1(D)|\ll D^{1/2+5/(4m)+\varepsilon}+D^{1/2}.
\]

For any \(\eta>0\), choose a fixed \(m\) with \(5/(4m)<\eta/2\), then a
sufficiently small moment loss. This proves

\[
 A_1(D)\ll_{\nu,S,W,\eta}D^{1/2+\eta}.
 \tag{2}
\]

There is no need for constants uniform as \(m\to\infty\): \(m\) is fixed
before \(D\to\infty\). Conversely, computing finitely many moments or proving
a finite initial segment of HM does not establish (2).

### Why (2) would imply RH

For \(\widehat W(s)=\int_0^\infty W(y)y^s\,dy/y\), set

\[
 \mathcal M_W(s)=\int_0^\infty A_1(D)D^{-s}\,\frac{dD}{D}.
\]

The sum vanishes for sufficiently small \(D\). Estimate (2), with arbitrarily
small \(\eta\), gives locally uniform convergence of the integral in
\(\Re s>1/2\); hence it is holomorphic there. In \(\Re s>1\), absolute
convergence and termwise integration give

\[
 \mathcal M_W(s)=\frac{\widehat W(s)}{L_K^S(s,\nu)}.
\]

If \(L_K(s,\nu)\) had a zero \(\rho\) with \(\Re\rho>1/2\), choose
\(W(y)=y^{-\rho}\phi(y)\), with nonzero nonnegative
\(\phi\in C_c^\infty((1,2))\). Then
\(\widehat W(\rho)=\int\phi(y)\,dy/y>0\). The meromorphic identity theorem
extends \(L_K^S\mathcal M_W=\widehat W\) from \(\Re s>1\); evaluating at
\(\rho\ne1\) is a contradiction. Deleted Euler factors are nonzero in this
half-plane. A principal pole at 1 is not a zero and causes no problem.
This reproduces the analytic reduction in [R11] at the desired exponent.

For the trivial Hecke character,

\[
 \zeta_K(s)=\zeta(s)L(s,\chi_{-3}).
\]

In the open critical strip the second factor is holomorphic, so a zero of
\(\zeta\) to the right of \(1/2\) would be a zero of \(\zeta_K\).
The functional equation then rules out zeros to the left as well. Thus HM
for this one target, for all \(W,m,\varepsilon\), suffices for ordinary RH.
Proving HM for every \(\nu\) is a stronger goal, not a necessary definition
of ordinary RH. The internal transforms may nevertheless require estimates
for additional characters. [R11 for the factorization; C2 for the functional
equation]

**The missing theorem is HM.** Its clean formulation does not make it easier
than RH, and nothing here proves it or assigns it a success probability.

## 3 A false shortcut ruled out by positive coefficients

Could an arbitrary-coefficient large sieve supply HM? No.

**Derived counterexample to that stronger proposed inequality.** Replace
\(\mu_K(\mathfrak n)\nu(\mathfrak n)W(N\mathfrak n/D)\) by coefficient 1 on
prime ideals with \(D<N\mathfrak n\le2D\), and 0 elsewhere. The sum on every
row \(u=p^6\), \(N\mathfrak p\asymp D^{1/2}\), equals the number of column
primes, \(\asymp D/\log D\). No row prime divides a column prime in these
disjoint ranges.

There are \(\asymp D^{1/2}/\log D\) such rows below \(D^3\). Their contribution
to the \(2m\)-th moment is at least a constant times

\[
 \frac{D^{2m+1/2}}{(\log D)^{2m+1}}.
\]

The proposed coefficient-uniform upper bound would be
\(D^{m+3+\varepsilon}\). Already at \(m=3\), these exponents are
\(13/2\) and \(6+\varepsilon\), inconsistent for sufficiently small
\(\varepsilon>0\).

This **does not refute HM**, which has fixed Möbius coefficients on the full
smooth support. It shows exactly why replacing those coefficients by absolute
values or arbitrary bounded coefficients cannot prove it. The same type of
obstruction is present at the optimized fourth-moment pilot scale.

## 4 The stronger probe has its own threshold

[R7, `prop:probe-low`, `old-eq:5.11`] gives

\[
 C(s)=s-\frac{11}{16},\qquad
 |J_\eta(Z)|\ll Z^{3/16+\varepsilon}.
\]

**Derived.** In general, a direct exponent \(L\) and signal \(s+c\) meet at
\(\beta=L-c\). Here this is

\[
 \frac3{16}-\left(-\frac{11}{16}\right)=\frac78.
\]

Multiplication of both the probe and its signal by \(Z^r\) changes these to
\(L+r\) and \(c+r\), leaving the threshold \(L-c\) unchanged. With this
signal fixed, approaching \(1/2\) requires a low exponent approaching
\(-3/16\), an improvement of \(3/8\).

The current geometry has \(l_x=17/48\), \(b=1/8\), and direct exponent
\(l_x/2+b/12\). Even hypothetically deleting just the additive-Gram penalty
\(b/12=1/96\) would leave the low-side crossover at \(83/96\). That is
only a low-side calculation, not a claim that all high estimates remain valid
or that a new \(83/96\) theorem follows.

## 5 The endpoint certificate really is an exact identity

One useful finite verification is [R7, `eq:balanced-endpoint-certificate`].
For \(0\le\delta\le5/6\), \(0\le y\le1/2\), define

\[
 v=51+41y,\quad p_y=7+18y+8y^2,\quad
 j_y=185+170y+(-138+12y+96y^2)\delta,\quad
 \mathcal J=j_y/108.
\]

The manuscript's ideal endpoint value satisfies

\[
 10368\mathcal J(-E_*)
 =2j_y[1+(3+8y)\delta]-468(5/6-\delta)\delta p_y.
\]

Its certificate is

\[
\begin{aligned}
 10368v\mathcal J(-E_*)={}&
 (3+5y)\{(4v\delta-79)^2+49\}\\
 &+4y\{4v\delta[(1+3y)(15+32y)\delta+9-13y]
                  +265+3485y\}.
\end{aligned}
\]

`checks/exponent_budget.py` expands the two sides independently as rational
bivariate polynomials and checks equality of every coefficient. This is not a
floating-point fit or merely a grid check.

On the stated rectangle, \(9-13y\ge5/2\), all displayed terms are
nonnegative, and \(v\le17(3+5y)\). Moreover
\(\mathcal J=(5/6-\delta)D_x+\delta P_x\), with
\(37/18\le D_x\le3\) and \(7/9\le P_x\le2\); hence
\(0<\mathcal J\le5/2\). Therefore

\[
 -E_*\ge\frac{49}{176256\mathcal J}
       \ge\frac{49}{440640}>\frac1{10000}.
\]

The arithmetic supports this local certificate. It does not prove the analytic
row bounds feeding it. The high comparison also has to subtract
\(\Delta=C(\beta_*)-C(7/8)\), account for the \(h\Delta/4\) capacity loss,
and reserve all height and smoothing errors. Checking this polynomial is
neither a complete verification of the \(7/8\) proof nor progress by itself
from \(7/8\) to \(1/2\).
