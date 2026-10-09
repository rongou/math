# Finite-lattice SU(2) Wilson transfer interface

**Audit date:** 2026-10-09.  **Scope:** pure SU(2), finite untwisted periodic
four-dimensional lattices, finite real `beta >= 0`, every period at least 4.
The primary convention is the **unshifted** Wilson weight
`exp[(beta/2) sum_p Tr_2 U_p]` with **probability Haar measure** on every
independent link.  No gauge fixing or division by orbit volumes is used.

This note supplies the concrete transfer-operator hypotheses for the parent's
conditional four-dimensional partition-function criterion.  It does **not**
derive that abstract criterion.  Section 9 checks its proposed elementary
small-beta antecedent, including its beta-zero limitation.  All assertions here
are finite-lattice statements; no continuum construction, limiting mass-gap
input, or extension to other gauge groups is asserted.

## 0. Interface to import

For a transverse three-torus of periods `w = (w1,w2,w3)`, let
`N = w1*w2*w3`.  The configuration space consists of its `3N` spatial links,
not its sites or its gauge orbits.  On the gauge-invariant subspace of their
product-Haar `L^2` space the operator defined below satisfies

\[
 K_{\beta,w}
   =\left.M_{\beta,w}C_{\beta,w}P_wM_{\beta,w}\right|_{\mathcal H_{\rm phys}}
   =\left.M_{\beta,w}C_{\beta,w}M_{\beta,w}\right|_{\mathcal H_{\rm phys}}.
 \tag{0.1}
\]

The verified conclusions are:

1. `P` is the orthogonal gauge-averaging projection; `C` is positive
   selfadjoint trace class; `M` is positive, bounded and boundedly invertible.
   Both `C` and `M` commute with `P`, but they need not commute with each other.
2. `K` is positive selfadjoint trace class, hence compact.  It has a strictly
   positive continuous kernel when extended by zero on the nonphysical
   subspace.  Its largest eigenvalue `lambda0 > 0` is simple, with a strictly
   positive continuous gauge-invariant eigenfunction.
3. If `beta > 0`, `K` is injective on the physical space, which is infinite
   dimensional.  Its eigenvalues can be listed with multiplicity as
   `lambda0 > lambda1 >= lambda2 >= ... > 0`, tending to zero.  If `beta = 0`,
   `K = |1><1|`; its spectrum is `{1,0}` and its excited transfer ratio is zero.
4. With **no additional constant**,

   \[
   Z_\beta(n,w_1,w_2,w_3)
        =\operatorname{Tr}_{\mathcal H_{\rm phys}}K_{\beta,w}^{\,n}.
   \tag{0.2}
   \]

   The identical statement, including positivity, holds with any of the four
   coordinates chosen as transfer direction.  Odd periods at least 5 are
   included; no even-period assumption is needed for this interface.
5. A bounded gauge-invariant observable `F` in a proper slab of `r` transfer
   steps has a slab operator `A_F` obeying

   \[
     \|A_F\|\le\|F\|_\infty\lambda_0^r,
     \qquad
     \|\lambda_0^{-r}A_F\|\le\|F\|_\infty.
   \tag{0.3}
   \]

   A time-slice observable is a multiplication operator of norm at most its
   essential supremum.  These are not claims about transfer-amputated
   operators involving `K^{-1}`.

Here and below “strictly positive” in the quadratic-form sense at `beta > 0`
means `<f,Kf> > 0` for every nonzero physical vector.  It does **not** mean
`K >= c I` for a positive `c`.  The unshifted `K` is not assumed to have norm
at most one.  Set `T = K/lambda0` only when a normalized transfer operator is
wanted, and then `Tr T^n = Z/lambda0^n`, not `Z`.

## 1. Lattice, orientation, and Wilson normalization

Let

\[
 \Lambda_L=\prod_{\mu=0}^3\mathbb Z/L_\mu\mathbb Z,
 \qquad L_\mu\ge4,
 \qquad V_4=\prod_{\mu=0}^3 L_\mu.
\]

For each positively oriented link `(x,mu)` choose one independent
`U_mu(x) in SU(2)`.  The oppositely oriented link is its inverse, not another
integration variable.  All coordinates below are read periodically.  Count
one plaquette for each `(x,mu,nu)` with `mu < nu`:

\[
 U_{\mu\nu}(x)
   =U_\mu(x)U_\nu(x+\hat\mu)
       U_\mu(x+\hat\nu)^{-1}U_\nu(x)^{-1}.
 \tag{1.1}
\]

There are `4 V4` independent links and `6 V4` such plaquettes.  With `Tr_2`
the ordinary, **unnormalized**, two-dimensional matrix trace, put

\[
 w_\beta(g)=\exp\!\left(\frac\beta2\operatorname{Tr}_2g\right),
 \qquad
 Z_\beta(L)=\int\prod_{x,\mu}dU_\mu(x)
                 \prod_{x,\mu<\nu}w_\beta(U_{\mu\nu}(x)),
 \qquad \int_{SU(2)}dg=1.
 \tag{1.2}
\]

For SU(2), `Tr_2 g` is real, lies in `[-2,2]`, and equals `Tr_2 g^{-1}`.
Thus `w_beta` is central, invariant under inversion, and

\[
       e^{-\beta}\le w_\beta(g)\le e^{\beta}.
 \tag{1.3}
\]

This also explains why reversing a plaquette orientation does not change the
weight.  “Normalized Haar” does **not** mean that the one-plaquette weight has
been divided by its Haar integral.

For comparison, the nonnegative-action convention

\[
 S_\beta^+(U)=\beta\sum_p\left(1-\tfrac12\operatorname{Tr}_2 U_p\right)
\]

has weight `w_beta^+(g) = e^{-beta} w_beta(g)` and partition function

\[
                 Z_\beta^+(L)=e^{-6\beta V_4}Z_\beta(L).
 \tag{1.4}
\]

The transfer rescaling is recorded in Section 6.  Keeping this constant is
essential to an **exact** trace identity, even though certain volume-balanced
combinations cancel it.

As a primary normalization cross-check, [LNWW92, Section 4.2, equations
(4.4)–(4.5), printed preprint pp. 23–24] explicitly uses normalized invariant
measure and half-weight spatial boundary plaquettes.  Its sum is over both
plaquette orientations.  Our definition (1.2), rather than an implicit
translation of its coupling, fixes all factors here.

## 2. Spatial-link Hilbert space and gauge projection

Choose coordinate 0 as time and write `L = (n,w1,w2,w3)`.  Let

\[
 \Sigma_w=\prod_{i=1}^3\mathbb Z/w_i\mathbb Z,
 \quad N=|\Sigma_w|,
 \quad E=3N,
 \quad F_s=3N,
 \quad Q_w=SU(2)^{E}.
 \tag{2.1}
\]

Here `E` counts independent spatial links and `F_s` counts spatial plaquettes,
one for each site and pair `1 <= i < j <= 3`.  Write a spatial configuration
as `X = (X_i(x))`.  Define

\[
 \mathcal H_w=L^2(Q_w,dX;\mathbb C),\qquad
 dX=\prod_{x,i}dX_i(x),\qquad
 \mathcal G_w=SU(2)^{\Sigma_w}.
\]

The spatial gauge group acts by

\[
 (g\cdot X)_i(x)=g(x)X_i(x)g(x+\hat i)^{-1},
 \qquad (R(g)f)(X)=f(g^{-1}\cdot X).
 \tag{2.2}
\]

Product Haar invariance makes `R(g)` unitary.  With probability Haar on
`G_w`, set

\[
 Pf=\int_{\mathcal G_w}R(g)f\,dg,
 \qquad
 (Pf)(X)=\int_{\mathcal G_w}f(g\cdot X)\,dg,
 \qquad
 \mathcal H_{\rm phys}=P\mathcal H_w.
 \tag{2.3}
\]

The two averages agree by inversion invariance of Haar.  Invariance and
Fubini give `P^2 = P`; inversion gives `P^* = P`.  Its range is exactly the
vectors fixed by every `R(g)`.  The constant function `1` has norm one and is
physical.  This is an invariant subspace with the **original product-Haar
inner product**, not a quotient equipped with an unspecified measure.

The common center in the kernel of the gauge action and the stabilizers of
individual configurations do not create factors: an average of `1` over the
whole gauge group is exactly `1`, whether or not the action is faithful.
No gauge orbit has been counted and then divided out.

The spatial-link representation is the pure-gauge part of [L76,
Section II.A, printed p. 5, equation (10)].  The distinction between an
unprojected transfer operator and its gauge-projected version is explicit in
[LNWW92, Section 4.2, printed p. 24, equation (4.7) and its footnote].

## 3. Positive SU(2) convolution, with its trace normalization

### 3.1 A one-link calculation

Use the SU(2) irreducible characters `chi_l`, `l = 0,1,2,...`, where
`d_l = l+1`, `chi_0 = 1`, and `chi_1 = Tr_2`.  In particular

\[
 \chi_\ell(\operatorname{diag}(e^{i\theta},e^{-i\theta}))
      =\frac{\sin((\ell+1)\theta)}{\sin\theta},
 \qquad |\chi_\ell(g)|\le d_\ell.
\]

The tensor product identity
`chi_1 chi_l = chi_{l+1} + chi_{l-1}` for `l >= 1`, with
`chi_1 chi_0 = chi_1`, gives

\[
  \chi_1^r=\sum_{\ell\ge0}m_{r\ell}\chi_\ell,
  \qquad m_{r\ell}\in\mathbb Z_{\ge0},
  \qquad m_{\ell\ell}=1,
  \qquad \sum_\ell d_\ell m_{r\ell}=2^r.
 \tag{3.1}
\]

For example, these identities follow by starting with `m_{00}=1` and
iterating `m_{r+1,l}=m_{r,l-1}+m_{r,l+1}`, taking indices below zero to vanish.
They give the actual Wilson character expansion

\[
 \begin{split}
 w_\beta(g)&=\sum_{\ell\ge0}b_\ell(\beta)\chi_\ell(g),\\
 b_\ell(\beta)&=\sum_{r\ge0}\frac{(\beta/2)^r}{r!}m_{r\ell}\ge0,\\
 \sum_{\ell\ge0}d_\ell b_\ell(\beta)&=e^\beta.
 \end{split}
 \tag{3.2}
\]

The last equality follows by substituting the dimension identity in (3.1).
It also proves absolute uniform convergence of the character expansion,
since `|chi_l| <= d_l`; thus the rearrangement of the exponential series is
justified.  If `beta > 0`,

\[
 b_\ell(\beta)\ge\frac{(\beta/2)^\ell}{\ell!}>0
 \quad\text{for every }\ell.
 \tag{3.3}
\]

At `beta = 0`, `b_0=1` and every other `b_l=0`.

Consider

\[
 (c_\beta f)(x)=\int_{SU(2)}w_\beta(xy^{-1})f(y)\,dy.
 \tag{3.4}
\]

The Peter–Weyl orthonormal basis is `sqrt(d_l) D^l_ab`, where `D^l` runs over
the irreducible unitary representations.  Centrality and Schur orthogonality
give, on each of its `d_l^2` matrix coefficients, the eigenvalue

\[
                a_\ell(\beta)=b_\ell(\beta)/d_\ell.
 \tag{3.5}
\]

Indeed, substituting `z=xy^{-1}` in (3.4) reduces the matrix integral to
`int w_beta(z) D^l(z^{-1}) dz = (b_l/d_l) I`.  Consequently

\[
 c_\beta=c_\beta^*\ge0,
 \qquad
 \operatorname{Tr}c_\beta
       =\sum_{\ell\ge0}d_\ell^2a_\ell(\beta)
       =e^\beta=w_\beta(1).
 \tag{3.6}
\]

This proves trace class, not just Hilbert–Schmidt regularity.  For `beta > 0`
all its eigenvalues are positive, so it is injective.  At zero it is the
projection onto constants.  Positivity here follows from the character
coefficients; a positive-valued integral kernel alone would not suffice.

The tensor-character method is the one used in [L76, Proposition 1(c),
printed pp. 8–9, especially equations (22)–(23)].  Equations (3.1)–(3.6) give
the complete SU(2) specialization and the trace-class estimate needed here.

### 3.2 All spatial links

Take the tensor product over the `E` links:

\[
 \begin{split}
 C&=\bigotimes_{e=1}^{E}c_\beta,\\
 (Cf)(X)&=\int_{Q_w}c(X,Y)f(Y)\,dY,\\
 c(X,Y)&=\prod_{x,i}w_\beta\bigl(X_i(x)Y_i(x)^{-1}\bigr).
 \end{split}
 \tag{3.7}
\]

It follows that `C = C^* >= 0`, `Tr C = e^{beta E}`, and `C` is injective
when `beta > 0`.  At `beta = 0`, `C = |1><1|` on the full link space.

For a simultaneous spatial gauge transformation,

\[
 (g\cdot X)_i(x)(g\cdot Y)_i(x)^{-1}
    =g(x)X_i(x)Y_i(x)^{-1}g(x)^{-1}.
\]

Centrality and a Haar change of variables therefore show `CR(g)=R(g)C`.
In particular, `CP=PC`.

## 4. Magnetic multiplication and the full-space extension

For the spatial plaquette `X_ij(x)` defined as in (1.1), put

\[
 B(X)=\prod_{x,\,1\le i<j\le3}w_\beta(X_{ij}(x)),
 \qquad m(X)=B(X)^{1/2},
 \qquad (Mf)(X)=m(X)f(X).
 \tag{4.1}
\]

Gauge invariance makes `M` commute with `P` and every `R(g)`.  Moreover,

\[
 e^{-\beta F_s/2}\le m(X)\le e^{\beta F_s/2},
 \qquad M=M^*>0,
 \qquad M^{-1}\text{ is bounded}.
 \tag{4.2}
\]

Define on the full link Hilbert space

\[
 \widetilde K=MCPM.
 \tag{4.3}
\]

Using only the commutations with `P`, not a commutation of `C` with `M`,

\[
 \widetilde K
       =(C^{1/2}PM)^*(C^{1/2}PM),
 \qquad
 \widetilde KP=P\widetilde K=\widetilde K.
 \tag{4.4}
\]

The operator `C^{1/2}` is Hilbert–Schmidt by (3.6)–(3.7).  Thus (4.4) proves
selfadjoint positivity and trace class, with

\[
 0<\operatorname{Tr}\widetilde K
      \le\|M\|^2\operatorname{Tr}C
      \le e^{\beta(F_s+E)}=e^{6\beta N}.
 \tag{4.5}
\]

Its restriction to the physical subspace is `K`; its restriction to the
orthogonal complement is zero.  In particular, both traces agree for every
positive integer power.  On a nonzero physical vector `f`, when `beta > 0`,

\[
 \langle f,Kf\rangle
     =\langle Mf,CMf\rangle>0,
 \tag{4.6}
\]

because `Mf` is a nonzero physical vector and `C` is injective and positive.
There is deliberately no injectivity assertion for `tilde K` on the full
space: its nonphysical subspace is annihilated by `P`.

The explicitly gauge-averaged kernel is

\[
 \begin{split}
 k(X,Y)&=m(X)\,\mathcal E(X,Y)\,m(Y),\\
 \mathcal E(X,Y)&=\int_{\mathcal G_w}dv\,
      \prod_{x,i}w_\beta\!\left(
       X_i(x)v(x+\hat i)Y_i(x)^{-1}v(x)^{-1}\right).
 \end{split}
 \tag{4.7}
\]

To see this directly, substitute the Haar average defining `P` into `CP`
and then change `Y` by a gauge transformation.  This yields
`mathcal E(X,Y) = int c(X,v dot Y) dv` with exactly the integrand displayed.
The kernel is continuous, real and symmetric.  It is invariant under
**independent** gauge transformations of `X` and `Y`: in the integral change
`v` to `g^{-1} v h` to compare the endpoints `g dot X` and `h dot Y`.
Its bounds are

\[
       e^{-\beta(F_s+E)}\le k(X,Y)\le e^{\beta(F_s+E)}.
 \tag{4.8}
\]

In particular it maps every nonzero nonnegative physical function to a
strictly positive continuous one.  Positivity improvement (4.8) and
quadratic-form positivity (4.4) are separate statements, both now proved.

## 5. Simple leading eigenvalue, including the zero-coupling endpoint

Compact selfadjoint positivity gives an eigenvalue
`lambda0 = ||K|| > 0` and a corresponding eigenvector.  Here is a direct
simplicity argument, so no uniqueness assumption is imported from a
field-theory reconstruction theorem.

Take a nonzero real top eigenfunction `f`; real and imaginary parts allow
this choice since the kernel is real.  The modulus is still physical, and

\[
 \langle |f|,K|f|\rangle\ge\langle f,Kf\rangle
            =\lambda_0\|f\|_2^2.
 \tag{5.1}
\]

The operator-norm bound forces equality and makes `|f|` another top
eigenfunction.  In the eigenfunction equation, (4.8) makes its continuous
representative strictly positive everywhere; call its normalized version
`phi0`.  If the top eigenspace had dimension larger than one, it would
contain a nonzero real `h` orthogonal to `phi0`.  Such an `h` has positive
and negative sets of positive measure.  Strict positivity of the kernel
then gives

\[
 \langle |h|,K|h|\rangle-\langle h,Kh\rangle
   =\iint k(X,Y)\bigl(|h(X)||h(Y)|-h(X)h(Y)\bigr)\,dX\,dY>0,
 \tag{5.2}
\]

contradicting `||K|| = lambda0`.  This proves simplicity over the reals and
hence over the complex numbers.  Compactness isolates this nonzero
eigenvalue from the rest of the spectrum.

The physical Hilbert space is infinite dimensional: choose a spatial
plaquette `p`.  Its four independent links make `X_p` Haar distributed
under `dX`, by conditioning on three links and integrating the fourth.
The gauge-invariant functions `chi_l(X_p)`, `l >= 0`, are therefore an
infinite orthonormal family.  For `beta > 0`, injectivity (4.6) now implies
infinitely many positive eigenvalues tending to zero.  In particular

\[
 r_{\beta,w}:=\frac{\lambda_1}{\lambda_0}
     =\bigl\|K/\lambda_0-|\phi_0\rangle\langle\phi_0|\bigr\|
       \in(0,1)\qquad(\beta>0).
 \tag{5.3}
\]

There is no lower bound on these eigenvalues away from zero and no bounded
inverse for `K`.  Nothing in this finite-volume simplicity proof bounds
`r_{beta,w}` uniformly as widths or beta vary.

At `beta = 0`, every plaquette weight and `m` equal one, and (4.7) is the
constant kernel `1`.  Thus, **on the still infinite-dimensional physical
space**,

\[
       K_{0,w}=|1\rangle\langle1|,
       \quad\lambda_0=1,
       \quad r_{0,w}=0,
       \quad\operatorname{Tr}K_{0,w}^n=1.
 \tag{5.4}
\]

Only propagation is rank one; the definition of the physical Hilbert space
has not collapsed to a one-dimensional space.  Quadratic-form strict
positivity fails on its orthogonal complement to constants.  A logarithm
`-log(K/lambda0)` is therefore not a finite-valued Hamiltonian on that
complement at beta zero.

## 6. Exact periodic trace: temporal links, boundaries, and constants

For the requested `n >= 4`, the Hilbert–Schmidt kernel trace formula gives

\[
 \operatorname{Tr}_{\mathcal H_w}\widetilde K^n
   =\int\prod_{t=0}^{n-1}dX_t\,
                   \prod_{t=0}^{n-1}k(X_t,X_{t+1}),
       \qquad X_n=X_0.
 \tag{6.1}
\]

Analytically the formula already follows for `n >= 2` by applying the
Hilbert–Schmidt product trace identity to `tilde K` and `tilde K^{n-1}`.
All kernels here are continuous and bounded.  We use it only with the
nondegenerate lattice periods specified in the scope.

Insert (4.7), introducing an independent `v_t(x) in SU(2)` for each site of
each time step.  Assign the actual four-dimensional link variables by

\[
       U_i(t,x)=X_{t,i}(x),\qquad U_0(t,x)=v_t(x).
 \tag{6.2}
\]

The temporal plaquette at `(t,x)` is

\[
 U_{0i}(t,x)
     =v_t(x)X_{t+1,i}(x)v_t(x+\hat i)^{-1}X_{t,i}(x)^{-1}.
 \tag{6.3}
\]

Its inverse is exactly the argument of `w_beta` in (4.7).  Inversion
invariance of the SU(2) trace therefore gives its required plaquette
weight, not its square or its square root.  This includes the wrapping
step `t=n-1`.

The magnetic factors give

\[
 \prod_{t=0}^{n-1}m(X_t)m(X_{t+1})
       =\prod_{t=0}^{n-1}m(X_t)^2
       =\prod_{t=0}^{n-1}B(X_t).
 \tag{6.4}
\]

Every spatial plaquette receives two half contributions, including those
at the cyclic seam, and hence exactly its full Wilson weight.  The measure
in (6.1), after insertion of the `v_t` integrals, is exactly the product of
`3nN` spatial and `nN` temporal probability Haar measures.  There are
`n F_s = 3nN` spatial plaquettes and `n E = 3nN` temporal plaquettes.  Thus
(6.1) is precisely (1.2), proving

\[
 \boxed{\quad
 Z_\beta(n,w_1,w_2,w_3)
   =\operatorname{Tr}_{\mathcal H_w}\widetilde K^{\,n}
   =\operatorname{Tr}_{\mathcal H_{\rm phys}}K_{\beta,w}^{\,n}.
 \quad}
 \tag{6.5}
\]

**Gauge-volume check.** No gauge fixing was performed.  Each gauge average
in (4.7) supplied a genuine temporal-link integral with total measure one.
There is no factor involving a gauge-group volume, a stabilizer, a center,
or a number of sites.

**Temporal-gauge warning.** If `T0=MCM` denotes the unprojected operator on
`H_w`, then

\[
     Z_\beta=\operatorname{Tr}_{\mathcal H_w}(T_0^nP),
 \tag{6.6}
\]

not generally `Tr_{H_w} T0^n`.  Setting **all** temporal links to the identity
on a periodic time circle would improperly remove its closing holonomy.
In a temporal-gauge derivation one may eliminate `n-1` temporal links per
spatial site; the closing holonomy must still be integrated.  That remaining
normalized average is `P`.  Equations (6.1)–(6.5) avoid this issue entirely.
The boundary-projector formula in [LNWW92, Section 4.2, equation (4.7),
printed p. 24] is consistent with this check; our periodic identity has been
derived directly, rather than inferred from an open-boundary formula.

**Normalization check.** For the shifted weight in (1.4),

\[
 M^+=e^{-\beta F_s/2}M,\qquad C^+=e^{-\beta E}C,
 \qquad K^+=e^{-\beta(F_s+E)}K=e^{-6\beta N}K.
 \tag{6.7}
\]

Then `Tr (K^+)^n = e^{-6 beta nN} Z_beta`, as required.  More generally,
multiplying **each** plaquette weight by a positive constant `s` rescales
`K` by `s^{6N}` and `Z` by `s^{6nN}`, leaving transfer eigenvalue ratios
unchanged.  Neither normalization of the convolution alone nor division of
`K` by its top eigenvalue may be silently inserted into (6.5).

## 7. Every coordinate transfer direction

For any `mu in {0,1,2,3}`, take the other three periods as transverse widths
and repeat Sections 2–6 with their spatial links.  Coordinate relabeling
preserves the product Haar measure and permutes the six plaquette types.
Any reversed plaquette is harmless because `w_beta(g^{-1})=w_beta(g)`.
Consequently

\[
 Z_\beta(L_0,L_1,L_2,L_3)
     =\operatorname{Tr}_{\mathcal H_{\rm phys}^{(\mu)}}
                         (K_\beta^{(\mu)})^{L_\mu},
       \qquad K_\beta^{(\mu)}\ge0,
 \tag{7.1}
\]

with all of the positivity, compactness, simplicity, and slab bounds above.
This is not an identification of spectra for different transverse tori.
It is a trace representation of the same partition function in each
direction.

The argument proves positivity of the **one-step** operator itself, not
only of its square, and does not use reflection planes or even periods.
As a primary reflection-positivity cross-check, [OS78, Theorem 2.1,
p. 448, proof on pp. 448–449] establishes positivity for gauge-invariant
observables via its positive-cone argument.  That theorem is not used to
supply an unexamined one-step or periodic-boundary assertion here.  If the
parent additionally uses a geometric half-torus reflection identity, its
observable algebra and parity assumptions must be specified there.

## 8. Bounded gauge-invariant insertions

### 8.1 A time slice

For a bounded measurable gauge-invariant function `f(X)`, multiplication
`B_f psi = f psi` preserves the physical subspace and

\[
                     \|B_f\|\le\|f\|_\infty.
 \tag{8.1}
\]

No magnetic conjugation is necessary in this product-Haar representation.
It yields the usual insertion identity
`<f(X_0)> = Tr(B_f K^n)/Z_beta`.

### 8.2 A slab of r >= 1 steps

Consider the open slab with spatial configurations `X_0,...,X_r` and
joining links `v_0,...,v_{r-1}`.  Let `F` be bounded measurable and invariant
under gauge transformations at **all** slab vertices, including its two
boundary slices.  These act by

\[
 X_s\longmapsto g_s\cdot X_s,
 \qquad v_s(x)\longmapsto g_s(x)v_s(x)g_{s+1}(x)^{-1}.
 \tag{8.2}
\]

Write `b = ||F||_infty`; a bounded representative can be chosen without
altering the resulting operator.  Define the positive half-boundary weight

\[
 W_r(X_0,\ldots,X_r;v_0,\ldots,v_{r-1})
   =\prod_{s=0}^{r-1}
        m(X_s)c(X_s,v_s\cdot X_{s+1})m(X_{s+1}).
 \tag{8.3}
\]

Thus each interior spatial slice has its full magnetic weight and each
endpoint has its half weight.  Define a kernel and an operator by

\[
 \begin{split}
 a_F(X,Y)
   &=\int\!\left(\prod_{s=1}^{r-1}dX_s\right)
            \left(\prod_{s=0}^{r-1}dv_s\right)
       F\,W_r\big|_{X_0=X,\,X_r=Y},\\
 (A_F\psi)(X)&=\int a_F(X,Y)\psi(Y)\,dY.
 \end{split}
 \tag{8.4}
\]

Gauge changes of the integrated variables show that the kernel is invariant
under independent endpoint gauge transformations.  Accordingly its
full-space operator satisfies `PA_F=A_FP=A_F`, and it defines an operator
on the physical space.  Fubini and (4.7) give

\[
        A_1=K^r,\qquad
        |a_F(X,Y)|\le b\,k^{(r)}(X,Y)\quad\text{a.e.},
 \tag{8.5}
\]

where `k^{(r)}` is the iterated kernel of the zero extension of `K^r`.
In particular `a_F` is bounded on a probability space and defines a
Hilbert–Schmidt operator.  For a physical `psi`, its modulus is also
physical, and

\[
 |A_F\psi|\le b\,K^r|\psi|,
 \qquad
 \|A_F\psi\|_2\le b\,\|K^r\|\,\|\psi\|_2.
 \tag{8.6}
\]

This proves (0.3) for complex or real `F`, at both beta zero and positive
beta.  In normalized transfer units, `Ahat_F=lambda0^{-r}A_F` is bounded by
`b` independently of widths, beta, and the slab thickness.  Its definition
still includes the slab propagation.

If the slab is embedded in a periodic lattice with `n-r >= 1`, cutting the
remaining steps and applying the same cyclic integration proves

\[
 \langle F\rangle_{\beta,n,w}
      =\frac{\operatorname{Tr}(A_F K^{n-r})}{Z_\beta(n,w)}
      =\frac{\operatorname{Tr}(\widehat A_F T^{n-r})}
                    {\operatorname{Tr}T^n},
          \qquad T=K/\lambda_0.
 \tag{8.7}
\]

The traces are well defined: `K^{n-r}` is trace class and `A_F` is bounded.
The kernel proof can also use the Hilbert–Schmidt product trace formula.
This accommodates any proper slab after choosing a cyclic cut outside it.

**Insertion caveats.** Pointwise kernel domination is not an operator-order
inequality, and a general `A_F` need not be selfadjoint or positive.  The
bound does not justify `K^{-r/2} A_F K^{-r/2}`: inverse transfer powers are
unbounded when beta is positive and fail to exist on the kernel at beta
zero.  A general measurable full-circle insertion with no complementary
step is outside the operator trace statement (8.7); it remains a perfectly
well-defined finite-dimensional Haar integral, but trace class of its
insertion kernel is not supplied by (8.5) alone.  Charged insertions or
slabs with open color indices require a different Hilbert-space interface.

## 9. Parent's proposed elementary small-beta check

Use the shorthand `Z_beta(n^4) = Z_beta(n,n,n,n)`; this is not the fourth
power of a partition function.  The parent supplies the **conditional**
criterion involving

\[
 D_\beta(n)=16\log Z_\beta(n^4)-\log Z_\beta((2n)^4).
 \tag{9.1}
\]

Its implication from `D_beta(n) <= 1/2048` to the stated dyadic-cube
transfer-ratio bound `2^{-1/n}` is **not proved or assumed as an independent
Wilson fact in this note**.  The following verifies the normalization and
the proposed sufficient small-beta estimate for its antecedent.

For all four periods at least 4, each elementary plaquette uses four
separate independent link variables.  Conditioning on three of them makes
the plaquette product Haar distributed as the fourth is integrated.
Moreover

\[
       \int_{SU(2)}\operatorname{Tr}_2g\,dg=0,
 \tag{9.2}
\]

for example by the Haar-preserving change `g -> -g`.  Consequently the
Haar expectation of **each** plaquette trace, and hence of their sum, is
zero.  Plaquettes are not independent, and no such independence is used.
Jensen's inequality for the product-Haar **probability** measure and the
pointwise upper bound `Tr_2 U_p <= 2` give

\[
          0\le\log Z_\beta(L)\le 6\beta V_4
                    \qquad(\beta\ge0).
 \tag{9.3}
\]

In particular,

\[
 \begin{split}
 D_\beta(4)
    &\le16\log Z_\beta(4,4,4,4)\\
    &\le16\cdot6\cdot4^4\,\beta
      =24576\,\beta.
 \end{split}
 \tag{9.4}
\]

The first inequality uses the nonnegative logarithm of the size-8 cube;
it is not an estimate of its sign by a transfer normalization.  Exact
integer arithmetic gives

\[
 0\le\beta\le2^{-26}
 \quad\Longrightarrow\quad
 D_\beta(4)\le24576\,2^{-26}
      =\frac3{8192}<\frac4{8192}=\frac1{2048}.
 \tag{9.5}
\]

No assertion `D_beta(n) >= 0` is inferred from Jensen; that would require
additional algebra.  The deliberately crude estimate (9.5) verifies only a
tiny small-beta sufficient regime, not a sharp range or further physical
progress.

The shifted convention (1.4) gives **the same** `D`: its constant changes
(9.1) by

\[
        -16\cdot6\beta n^4+6\beta(2n)^4=0.
 \tag{9.6}
\]

Thus this particular antecedent and transfer eigenvalue ratios are
unchanged by that action constant.  The separate Jensen lower bound in
(9.3), however, is for the **unshifted** convention and must not be applied
unchanged to `Z_beta^+`.  The raw trace identity likewise always uses the
matching operator in (6.5) or (6.7).

Finally, at beta zero all partition functions equal one, so
`D_0(n)=0` for every permitted `n`, while (5.4) gives rank-one transfer
propagation and excited ratio zero.  It therefore satisfies the proposed
numerical antecedent and its ratio conclusion without any nonzero excited
transfer eigenvalue.  **The criterion alone cannot establish
nontriviality.**  Infinite-rank transfer propagation at positive beta is
instead a separate finite-lattice consequence of (3.3) and (4.6); it supplies
no assertion about a limiting theory.

## 10. Caveats and unresolved dependencies

- Under the stated finite-volume, untwisted pure-SU(2), isotropic Wilson,
  probability-Haar hypotheses, there is **no unresolved normalization,
  projection, trace-class, leading-eigenvalue, or bounded-slab issue** in
  this interface.  The proofs above are independent of numerical spectral
  experiments and of the parent's abstract criterion.
- The parent's dimension-four partition-function algebra and the
  quantitative dyadic ratio implication remain outside this audit.  So do
  verification of a useful antecedent beyond the elementary range (9.5),
  and any estimates uniform in widths or in a change of cutoff parameters.
  A simple leading eigenvalue on each finite torus by itself supplies none
  of these estimates.
- Beta zero must not be described as injective positive propagation or as
  a nontrivial excited theory.  Positivity improvement of its constant
  kernel is compatible with an infinite-dimensional nullspace.
- `beta < 0`, `beta = infinity`, periods below 4, nonperiodic or twisted
  boundary conditions, selected flux sectors, matter fields, other actions,
  and other gauge groups are not covered.  In particular the nonnegative
  character-coefficient proof relies on `beta >= 0` and on the stated
  SU(2) representation content.
- No assertion of a bounded inverse, no amputated-slab norm bound, no
  full-circle measurable-kernel trace-class assertion, and no automatic
  identification of charged sectors should be read into this result.
- There is no claim here of a continuum construction, a continuum
  nontriviality result, or a limiting mass-gap theorem.  No such input was
  used to establish the finite-lattice interface.

## Validation record

The proofs above establish the result; the following independent diagnostics
were also run on 2026-10-09 using only a temporary script outside the
repository:

- Fixed-seed SU(2) matrix calculations on a `4 x 5 x 4 x 5` torus checked all
  four coordinate decompositions, including the wrapping seam and both odd
  periods.  The `1600` link variables and `2400` plaquettes had exactly the
  stated counts.  Comparing the full unintegrated Wilson exponent with each
  sliced exponent gave absolute discrepancies below `2e-14`; the electric
  kernel argument agreed with the inverse temporal plaquette to below
  `5e-16`.  A full gauge transformation preserved the exponent to below
  `1e-14`.
- The tensor-character recurrence and direct class-Haar quadrature agreed
  for `beta = 0, 1/8, 1, 3, 10` and character labels `0,...,6`; the trace
  sum agreed with `exp(beta)` to relative error below `3e-16`.  These finite
  truncation checks are not substitutes for the convergence and positivity
  proof in Section 3.
- Rational arithmetic checked `16*6*4^4 = 24576` and
  `24576/2^26 = 3/8192 < 1/2048`.  The action-constant cancellation (9.6)
  is exact.

No partition function or spectral ratio was estimated numerically, and no
formal proof-assistant certification is claimed.

## Primary bibliography and source audit

All external sources used for mathematical context are original research
papers.  The proofs in this note fix the conventions rather than borrowing
an untracked normalization from a citation.  Page numbers below refer to
the explicitly specified version; PDF page numbers are one-based.  The
bibliography is kept **in this file** to respect the single-file write scope.

### [L76 / L77] Explicit positive transfer construction

M. Lüscher, *Construction of a selfadjoint, strictly positive transfer
matrix for Euclidean lattice gauge theories*, DESY 76/54 (1976);
**Communications in Mathematical Physics 54** (1977), 283–292.
DOI: `10.1007/BF01614090`.

- Direct primary preprint PDF:
  <https://bib-pubdb1.desy.de/record/396349/files/7611148.pdf>.
- Published article: <https://doi.org/10.1007/BF01614090>.
- **Verified locators in the DESY version:** Section II.A, printed p. 5,
  equation (10), spatial-link `L^2` kernel representation (PDF p. 5);
  Section II.B, printed pp. 7–9, equations (17), (20)–(23) and
  **Proposition 1**, especially the positive character-coefficient proof
  (PDF pp. 6–7).  Printed pp. 8–9 appear side by side on PDF p. 7 and were
  checked visually, not just by OCR.
- Scope of use: the explicit pure-gauge multiplication/convolution
  construction and its positivity method.  The paper also treats fermions;
  **its discussion is not a citation for the pure-gauge uniqueness claim
  proved in Section 5**, nor for our exact periodic gauge projection.
  We use the DESY pagination and do not silently identify it with journal
  pagination.

### [LNWW92] Normalized Haar, half boundary weights, and gauge projection

M. Lüscher, R. Narayanan, P. Weisz, and U. Wolff,
*The Schrödinger Functional — a Renormalizable Probe for Non-Abelian Gauge
Theories*, **Nuclear Physics B 384** (1992), 168–228;
`arXiv:hep-lat/9207009v1`.

- Direct primary preprint PDF:
  <https://arxiv.org/pdf/hep-lat/9207009v1>.
- Published article: <https://doi.org/10.1016/0550-3213(92)90466-O>.
- **Verified locators:** Section 4.2, printed preprint pp. 23–24
  (PDF pp. 24–25), equations **(4.4)–(4.7)**.  Equation (4.4) specifies the
  half weights on spatial boundary plaquettes; the text following (4.5)
  specifies normalized invariant measure; equation (4.7) and its footnote
  specify the physical projector.  Printed p. 24 was checked visually.
- Scope of use: those finite-lattice formulas only.  This note uses none of
  that paper's arguments or claims concerning continuum limits.

### [OS78] Gauge-invariant physical positivity

K. Osterwalder and E. Seiler, *Gauge Field Theories on a Lattice*,
**Annals of Physics 110** (1978), 440–471.
DOI: `10.1016/0003-4916(78)90039-8`.

- Direct publisher article:
  <https://www.sciencedirect.com/science/article/pii/0003491678900398>.
- DOI: <https://doi.org/10.1016/0003-4916(78)90039-8>.
- Direct scan of the primary article consulted:
  <https://archive.org/download/wikipedia-scholarly-sources-corpus/10.1016%252F0001-4575%252871%252990016-9.zip/10.1016%252F0003-4916%252878%252990039-8.pdf>.
- **Verified locators:** Section 2.1, pp. 442–445, definitions of the lattice
  gauge measure and gauge averaging, especially equation (2.9);
  Section 2.3, **Theorem 2.1, p. 448**, with Lemmas 2.2–2.4 and the
  plaquette positive-cone argument on pp. 448–449.  The theorem statement
  on printed p. 448 (PDF p. 9) was checked visually from the scan.
- Scope of use: a reflection-positivity cross-check only.  Its subsequent
  transfer discussion on p. 450 is phrased with a two-unit shift and is
  not being used to infer one-step positivity, injectivity, periodic
  normalization, or any mass-gap input in this audit.
