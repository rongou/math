# Coprime theta conversion and a descent obstruction

October 9, 2026. Baseline: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

**Result:** the coprime fourth-moment kernel converts exactly into a
**divisor-weighted cubic-theta kernel**. Unfolding the divisor weight produces
the repo's cubic twisting factor, but a direct Cauchy–Schwarz reduction loses
one power of the original column length and falls outside the proved scale
range. Even an optimistically granted weighted version of the completed
estimate would miss P4. This is a quantified obstruction to a particular
reuse of the method, not a proof that every theta approach fails.

A further calculation identifies an artificial diagonal of size
\(D^{4+o(1)}\) introduced by unrestricting the converted kernel. It is **not**
a lower bound for the whole energy and **not** a disproof of P4. It explains
why a signed, correctly centered calculation is necessary.

The exact arithmetic deductions use the Gauss identities in [R11]. The new
weighted automorphic reflection and the required dispersion estimate are
**not established**. In particular, neither P4 nor RH is proved.

## 1 The coprime diagnostic sector

Use the notation of `fourth_moment.md`. Restrict the original four columns to
be pairwise coprime, and put

\[
 v=n_1n_2,\qquad w=n_3n_4,\qquad X=D^2.
\]

Then \(v,w\) are squarefree and coprime, with \(Nv,Nw\asymp_W X\). Conversely,
every factorization of such \(v,w\) into two squarefree columns on each side
has all four columns pairwise coprime. Define

\[
 V_D(v)=\sum_{ef=v}W(Ne/D)W(Nf/D).
\]

In this sector the original product-column coefficient is
\(B_v=\mu(v)\nu(v)V_D(v)\). The restriction is only a diagnostic: controlling
this sector does not control the whole fourth moment, and cancellations
between different gcd sectors cannot be ruled out in advance.

The row character \(\chi_v\overline{\chi_w}\) has primitive conductor \(vw\).
There is no balanced-prime mask in this particular sector. With the
unnormalized Gauss sum \(\tau_{vw}(\chi_v\overline{\chi_w})\), the exact
Poisson term is

\[
\begin{aligned}
 \mathcal R_{\rm cop}(D,H)
 ={}&H\sum_{\substack{v,w\ {m sf}\\(v,w)=1}}
 \frac{\mu(v)\mu(w)\nu(v)\overline{\nu(w)}V_D(v)\overline{V_D(w)}}{Nv\,Nw}
 \tau_{vw}(\chi_v\overline{\chi_w})\\
 &\quad\times\sum_{k\ne0}\overline{\chi_v(k)}\chi_w(k)
           \widehat\Phi(HNk/(Nv\,Nw)).
\end{aligned}
 \tag{1}
\]

For large \(D\) the unit product column is absent, so this is entirely
nonprincipal. The norm congruence \(Nv\equiv Nw\pmod{36}\) can also be
imposed, by the radial unit symmetry already proved.

## 2 Exact conversion to cubic theta coefficients

Write, for squarefree good \(n\),

\[
 \alpha(n)=n/\sqrt{Nn},\quad
 a(n)=\overline{\alpha(n)}\gamma_2(n),\quad
 G(n)=\overline{\chi_n(4)}\gamma_3(n).
\]

All three have modulus one. Let \(\mathcal R(v,w)\in\{1,-1\}\) be the
fixed-ray reciprocity sign in [R11, `eq:recip`]. CRT and reciprocity give

\[
 \frac{\tau_{vw}(\chi_v\overline{\chi_w})}{\sqrt{Nv\,Nw}}
   =\chi_v(w)\overline{\chi_w(v)}\gamma_1(v)\gamma_{-1}(w)
   =\mathcal R(v,w)\gamma_1(v)\gamma_{-1}(w).
\]

The two Gauss conversion identities are

\[
 \mu(v)\gamma_1(v)=G(v)\overline{a(v)},\qquad
 \mu(w)\gamma_{-1}(w)=\chi_w(-1)G(w)^{-1}a(w).
\]

The first follows from `eq:convert1` and \(|a(v)|=1\); the second is
`eq:convert2`. Hence

\[
 \boxed{
 \mu(v)\mu(w)
 \frac{\tau_{vw}(\chi_v\overline{\chi_w})}{\sqrt{Nv\,Nw}}
 =K(v,w)\overline{a(v)}a(w)
 }
 \tag{2}
\]

where the exact phase is

\[
 K(v,w)=\mathcal R(v,w)\chi_w(-1)G(v)G(w)^{-1}.
\]

On the fixed ray group, [R11, `eq:quotient`] identifies this phase with
\(G(vw^{-1})\). Here the inverse is in that finite group, not an assertion
that \(v/w\) is an integral ideal. No phase has been discarded.

Substitution into (1) yields

\[
\begin{aligned}
 \mathcal R_{\rm cop}(D,H)
 ={}&H\sum_{k\ne0}\sum_{\substack{v,w\ {m sf}\\(v,w)=1}}
 \frac{\nu(v)\overline{\nu(w)}V_D(v)\overline{V_D(w)}}{\sqrt{Nv\,Nw}}
 G(vw^{-1})\overline{a(v)}a(w)\\
 &\quad\times\overline{\chi_v(k)}\chi_w(k)
              \widehat\Phi(HNk/(Nv\,Nw)).
\end{aligned}
 \tag{3}
\]

This is the completed **arithmetic conversion**, not a new automorphic
reflection formula. The coefficients are related to those of the cubic theta
function by [R11, `eq:intro-theta-coefficients`]:

\[
 a(v)=3^{-5/2}\overline{\alpha(v)}\chi_v(\lambda)^2c_\theta(v),
 \qquad \lambda=1+2\omega.
\]

The Möbius signs have become structured theta phases. Taking absolute values
of \(a(v)\) would erase the arithmetic we are trying to exploit.

### Fixed ray phases do not create positivity

One may expand \(G\) in characters of the fixed ray group \(\Gamma\):

\[
 G(g)=\sum_{\eta\in\widehat\Gamma}c_\eta\eta(g),\qquad
 c_\eta=\frac1{|\Gamma|}\sum_{g\in\Gamma}G(g)\overline{\eta(g)}.
\]

The coefficients need not be nonnegative. In addition, the coprimality
restriction and the coupled Fourier profile remain. Formula (3) therefore
cannot simply be declared a sum of positive squares.

Even without those phases, dropping coprimality is not monotone. Take three
squarefree labels \(pr,qs,pq\), for four distinct primes, with coefficients
\((1,1,-2)\). The quadratic sum restricted to coprime pairs is 2, whereas
the unrestricted square is \(|1+1-2|^2=0\). This finite counterexample rules
out that shortcut; it does not model the actual Möbius coefficients.

## 3 Unfolding the divisor weight gives a concrete bilinear family

For a fixed ray character \(\xi\), put \(a_\xi(n)=a(n)\xi(n)\). A representative
weighted theta column sum is

\[
 \Theta_k(D;\xi,W)
   =\sum_{v\ {m sf}}\frac{a_\xi(v)\chi_v(k)}{\sqrt{Nv}}V_D(v).
\]

The conjugated profiles and characters arising in (3) are of the same type.
The coupled Fourier profile still requires its own justified separation;
no claim that (3) equals a single such mean square is being made.

The coefficient law [R11, `eq:crt-a`] is

\[
 a_\xi(ef)=a_\xi(e)a_\xi(f)\chi_f(e)^4\qquad((e,f)=1).
\]

Consequently the divisor weight unfolds **exactly** as

\[
\begin{aligned}
 \Theta_k
 =\sum_{e\ {m sf}}&
  \frac{a_\xi(e)\chi_e(k)W(Ne/D)}{\sqrt{Ne}}\\
 &\times\sum_{f\ {m sf}}
  \frac{a_\xi(f)\chi_f(k)\chi_f(e)^4W(Nf/D)}{\sqrt{Nf}}.
\end{aligned}
 \tag{4}
\]

There is no missing coprimality condition: \(\chi_f(e)^4=0\) when
\((e,f)\ne1\). This gives a genuine connection to the auxiliary cubic-twist
family in the repo, rather than an arbitrary-coefficient surrogate.

### What a direct Cauchy–Schwarz step costs

For each \(k\), the squared norm of the outer coefficients in (4) is
\(O_W(1)\), since \(Ne\asymp_W D\). Let
\(U_W(y)=W(y)/\sqrt y\), a fixed smooth annular profile. Cauchy–Schwarz,
followed by summing over \(0<Nk\le U\), gives

\[
 \sum_{0<Nk\le U}|\Theta_k|^2
 \ll_W D\sum_{F\asymp_W D}\mathcal E(U,D,F;\xi,U_W).
 \tag{5}
\]

There are only \(O_W(1)\) dyadic bands \(F\) in this sum, and
\(\mathcal E\) is exactly the normalized auxiliary energy in
[R11, `eq:energy`]. Indeed, its normalization is \(1/(DF)\), whereas the
squared normalized inner sum in (4) supplies \(1/D\); their ratio is
\(F\asymp D\).

Thus this straightforward reduction loses a factor \(D\). Even **illegally
granting** the repo's bound \(\mathcal E\ll DF\asymp D^2\) outside its
stated range would only give \(\sum_k|\Theta_k|^2\ll D^3\), one power worse
than the desired \(D^2\) energy scale. This is not a conjectured extension
or a new bound: it diagnoses what is lost when the outer \(e\)-oscillation
is discarded.

### Why the divisor weight cannot just become a fixed twist

For an annular \(W\), \(V_D(p)=0\) for a prime product-column \(p\) once
\(W(1/D)=0\). But if two distinct primes \(p,q\) have norms in an interval
where \(W(Np/D),W(Nq/D)>0\), then \(V_D(pq)>0\).
So \(V_D\) is not completely multiplicative and cannot be absorbed into the
\(\Psi\) in [R11, `eq:T`].

It is also an arithmetic divisor weight, not a supplied fixed smooth profile
with uniform derivative bounds. A pointwise divisor bound does not provide
those derivative bounds. Unfolding it as (4) is legitimate; silently applying
ordinary theta automorphy to the weighted coefficients is not.

## 4 The exact scale hypothesis that fails

At P4, the original row scale and the product-column scale are

\[
 H=D^{4/3},\qquad X=D^2.
\]

The generic Poisson row scale is

\[
 U=X^2/H=D^{8/3},\qquad U/X=D^{2/3}>1.
\]

The repo's canonical energy theorem requires
\(U\le\Sigma D^{-\kappa}\), \(\kappa>0\), where \(\Sigma=X'F\).
For the bilinear reduction (5), \(X'=D\) and \(F\asymp D\), so
\(\Sigma\asymp D^2\). The hypothesis fails by a power, not an endpoint
constant. [R11, `prop:canonical`, `eq:positive-gap`]

If one instead pretends that the weighted sum could be handled as an
unweighted column of length \(X=D^2\), the same failure remains. The nominal
theta-reflected length, already for squarefree generic rows \(k\), is

\[
 U^2/X=D^{10/3},
\]

which is larger than the input column length. The formal cube cutoff becomes

\[
 H_c=(X/U)^{2/3}=D^{-4/9}<1.
\]

The actual cube-reduction proposition requires \(U\le X\) in this
unmarked setting and is not applicable. The substitution illustrates why:
the unit divisor would fall in the nominal long-divisor range and would not
shorten anything. [R11, `eq:cube-cutoff`, `lem:cube-reduction`]

The auxiliary parameter \(F\) is a real arithmetic averaging variable, not
free numerical slack. Increasing it requires an amplifier and its extraction
cost, and also changes the target \(\Sigma\); it cannot simply repair this
inequality without a new argument.

### Two bare Poisson steps do not supply descent

For fixed column exponent \(x\), row Poisson sends logarithmic scales
\(P(u,x)=(2x-u,x)\); hence \(P^2\) is the identity. There is no contraction
without the repo's separately justified enlargement and shortening step.

For a deliberately simplified length model, let
\(T(u,x)=(u,2u-x)\) be the generic theta scale. Then

\[
 TP(u,x)=(u+2(x-u),\ x+2(x-u)).
\]

If \(u<x\), both coordinates increase. At the pilot scales this model gives

\[
 (4/3,2)\longmapsto(8/3,10/3)
      \longmapsto(4,14/3)\longmapsto(16/3,6).
\]

This is an arithmetic model, **not** a claim that the changing character
families permit all these successive operations. Even that optimistic model
does not give a shrinking recursion.

## 5 Even an optimistic completed estimate would miss P4

The unweighted completed estimate in [R11, `prop:R`, with auxiliary factor 1]
has normalized energy bound

\[
 \sum_{Nk\ll U}|T_k(X)|^2\ll D^\varepsilon(U+U^2/X).
\]

**Counterfactual diagnostic only:** suppose a version of this estimate held
for the divisor-weighted sums, all coprimality and coupled-profile issues
were handled, and cube removal cost no power. A positive-energy treatment
at the natural normalization would still produce only

\[
 H(U+U^2/X)=X^2+X^3/H.
\]

At P4 this is \(D^4+D^{14/3}\), whereas the target is
\(HX=D^{10/3}\). The largest term misses by \(D^{4/3}\).
Even deleting the \(U^2/X\) term would leave \(HU=X^2=D^4\), too large.

**This does not improve our proved \(D^{5+\varepsilon}\) bound.** The
weighted completed estimate and the necessary reductions have not been
established. The calculation shows that merely extending that particular
upper-bound template would not finish P4 anyway.

## 6 The artificial diagonal that must not be hidden

A concrete large term appears if the converted coprime kernel (3) is extended
to all squarefree pairs \((v,w)\). The extension is not the original Poisson
formula at overlapping pairs: its conductor would have to change there.
Its added diagonal \(v=w\), using \(G(1)=1\), is

\[
 \mathcal A_\Delta(D,H)=
 H\sum_{v\ {m sf}}\frac{|V_D(v)|^2}{Nv}
  \sum_{k\ne0}|\chi_v(k)|^2
        \widehat\Phi\!\left(\frac{HNk}{(Nv)^2}\right).
 \tag{6}
\]

This is an **artificial diagonal of an enlarged expression**, not a newly
discovered main term of the original fourth moment.

Take a fixed nonnegative nonzero \(W\), and choose the allowed Gaussian
majorant \(\Phi(t)=e^{\pi(1-t)}\). With our self-dual measure,

\[
 \widehat\Phi(t)=e^\pi\frac2{\sqrt3}e^{-4\pi t/3}>0.
\]

For \(v=pq\), with distinct prime ideals whose norms lie in a fixed interval
of size \(\asymp D\) where \(W\) is bounded below, \(V_D(v)\gg_W1\) and
\(Nv\asymp D^2\). There are \(\gg D^2/(\log D)^2\) such different
product ideals, by the prime ideal theorem for this fixed field.

At \(H=D^{4/3}\), put \(U_v=(Nv)^2/H\asymp D^{8/3}\).
The annulus \(U_v/2<Nk\le U_v\) contains \(\gg U_v\) lattice points.
Removing multiples of \(p\) or \(q\) removes \(O(U_v/D+\sqrt{U_v/D}+1)\)
points for each prime, so \(\gg U_v\) survive. The Fourier profile is
bounded below on this annulus. Each such product column therefore contributes
at least a constant times

\[
 (H/Nv)\,|V_D(v)|^2U_v=Nv\,|V_D(v)|^2\gg D^2.
\]

Consequently

\[
 \mathcal A_\Delta(D,D^{4/3})\gg_W D^4/(\log D)^2.
\]

Conversely, Schwartz decay and the divisor coefficient square bound give
\(\mathcal A_\Delta\ll_{W,\varepsilon}D^{4+\varepsilon}\).
Thus its power scale really is 4, not the desired \(10/3\).

**Crucial limitation:** a large positive diagonal does not lower-bound a whole
energy. For example, coefficients \((1,-1)\) have diagonal mass 2 but total
square 0. Other terms can cancel (6). Nor does this calculation contradict
P4, because (6) was introduced by enlarging the converted expression.

The lesson is specific: do not discard those cancellation terms while
estimating an uncentered enlargement. To use such an enlargement, subtract
its added diagonal and account for **all** other overlapping-pair corrections
by exact identities. Subtracting a convenient term from the original fourth
moment without adding it back is not a proof.

## 7 What the next analytic input must accomplish

The useful new target is a **centered bilinear cubic-theta dispersion
estimate** for (4), with its divisor weights, in the range \(U=D^{8/3}\).
It must preserve oscillation in both factor variables and account for the
coprime restriction, rather than bounding each factor or each gcd sector
independently by a positive energy.

A viable statement would bound the signed expression (3), together with the
appropriate gcd corrections when the full fourth moment is restored, by
\(D^{10/3+\varepsilon}\). No such statement is proved here. Known
GRH-conditional cubic-Gauss dispersion estimates cannot be imported as an
unconditional input to an RH proof. [C8]

Progress from this pass is the exact conversion (2), the exact bilinear
identity (4), its quantified Cauchy loss (5), and the explicit failed descent
range and enlarged-diagonal term. None is an improved zero-free theorem.

## 8 Reproducible checks

```sh
python3 -m unittest discover -s research_notes/checks -p 'test_*.py' -v
python3 research_notes/checks/coprime_reflection.py
(cd lean && lean ../research_notes/checks/CoprimeScaleObstruction.lean)
```

- Eight local/composite cases check both single Gauss conversions, and seven
  coprime pairs check (2), with square roots cleared and exact cyclotomic
  arithmetic. Seven pairs also check the bilinear cubic coefficient law.
- Tests explicitly reject overlapping moduli and the false monotonicity and
  diagonal-lower-bound shortcuts described above.
- The scale tests distinguish the actual elementary bound from the
  **unproved hypothetical** \(D^{14/3}\) bound.
- Six additional Lean lemmas verify only the linear scale identities and
  inequalities. Their axiom reports use at most `propext`, `Quot.sound`, and
  `Classical.choice`; no new axioms or `sorry` are used.

Neither the all-prime Gauss theory nor automorphic reflection for the new
weighted sums is formalized by these small Lean files. See
`results/coprime_reflection.json` and `results/coprime_scales_lean.txt` for the
finite checks, and `results/comparator_attempt.json` for the separate
seven-eighths verification attempt.
