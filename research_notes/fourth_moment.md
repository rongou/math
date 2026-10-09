# Fourth moment expansion and the remaining estimate

October 9, 2026. Baseline: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

**Outcome:** the fourth moment now has an exact conductor-and-mask Poisson
formula, a positive grouped diagonal, and a unit-symmetry reduction. Elementary
completion yields \(O(D^{5+\varepsilon})\) at the proposed scale
\(H=D^{4/3}\), not the desired \(O(D^{10/3+\varepsilon})\). The missing
power saving is explicit. P4 and RH remain unproved.

The derivations below use finite character identities, lattice Poisson
summation, and elementary counting. They do **not** assume the repo's claimed
\(7/8\) theorem. The additive normalization agrees with [R11,
`lem:poisson`] and [R7, `sec:arithmetic`]. Reference keys are in `references.md`.
No novelty claim is made for these elementary reductions.

## 1 Setup and smoothing

Let \(K=\mathbb Q(\sqrt{-3})\), \(\mathcal O=\mathbb Z[\omega]\),
\(\omega^2+\omega+1=0\). Ideals are represented by their primary generators;
all column ideals exclude the fixed prime set \(S\), including primes above
2 and 3. Put

\[
 a_{\mathfrak n}=\mu_K(\mathfrak n)\nu(\mathfrak n)W(N\mathfrak n/D),
 \qquad A_u(D)=\sum_{\mathfrak n}a_{\mathfrak n}\chi_{\mathfrak n}(u).
\]

Here \(W\) is fixed, smooth, and compactly supported in \((0,\infty)\), and
\(\chi_{\mathfrak n}(u)=(u/n)_6\) retains its zero extension.
Choose a fixed nonnegative radial Schwartz profile \(\Phi\) with
\(\Phi(t)\ge1\) for \(0\le t\le1\). Define

\[
 \mathcal E_{4,\Phi}(D,H)
  =\sum_{u\in\mathcal O}|A_u(D)|^4\Phi(Nu/H).
\]

The desired sharp nonzero-row moment is bounded above by this quantity. The
included zero row contributes exactly \(|a_{(1)}|^4\Phi(0)\), since
\(\chi_{(1)}(0)=1\) and every nonunit column vanishes at 0. For all
sufficiently large \(D\), compact support of \(W\) gives \(a_{(1)}=0\).
Bounded smaller scales can be absorbed into constants. Keeping this convention
explicit avoids an erroneous extra main term.

## 2 Every shared prime pattern

For a quadruple of squarefree columns, let \(\mathfrak g_T\) be the product
of primes occurring in exactly the columns indexed by the nonempty subset
\(T\subset\{1,2,3,4\}\). These 15 ideals are squarefree and pairwise
coprime, and

\[
 \mathfrak n_j=\prod_{T\ni j}\mathfrak g_T.
\]

Columns 1 and 2 are unconjugated; 3 and 4 are conjugated. The local character
exponent is \(e_T=|T\cap\{1,2\}|-|T\cap\{3,4\}|\).

| \(T\) | \(e_T\) | Local Möbius sign | Fourier type |
| --- | --- | --- | --- |
| 1 | 1 | −1 | Sextic Gauss |
| 2 | 1 | −1 | Sextic Gauss |
| 3 | −1 | −1 | Gauss sum of inverse sextic character |
| 4 | −1 | −1 | Gauss sum of inverse sextic character |
| 12 | 2 | +1 | Cubic Gauss |
| 13 | 0 | +1 | Coprimality mask |
| 14 | 0 | +1 | Coprimality mask |
| 23 | 0 | +1 | Coprimality mask |
| 24 | 0 | +1 | Coprimality mask |
| 34 | −2 | +1 | Gauss sum of inverse cubic character |
| 123 | 1 | −1 | Sextic Gauss |
| 124 | 1 | −1 | Sextic Gauss |
| 134 | −1 | −1 | Gauss sum of inverse sextic character |
| 234 | −1 | −1 | Gauss sum of inverse sextic character |
| 1234 | 0 | +1 | Coprimality mask |

Let

\[
 \mathfrak c=\prod_{e_T\ne0}\mathfrak g_T,\qquad
 \mathfrak b=\prod_{e_T=0}\mathfrak g_T,\qquad
 \mathfrak Q=\mathfrak b\mathfrak c.
\]

The primitive character modulo \(\mathfrak c\) is

\[
 \chi(u)=\prod_{\mathfrak p\mid\mathfrak c}
           \chi_{\mathfrak p}(u)^{e_{\mathfrak p}}.
\]

Each nonzero exponent is \(\pm1\) or \(\pm2\); the corresponding local
character is nontrivial and has conductor \(\mathfrak p\). CRT therefore
gives conductor exactly \(\mathfrak c\). The original product is

\[
 \chi_{\mathfrak n_1}(u)\chi_{\mathfrak n_2}(u)
 \overline{\chi_{\mathfrak n_3}(u)\chi_{\mathfrak n_4}(u)}
 =\chi(u)\mathbf1_{(u,\mathfrak b)=1}.
 \tag{F}
\]

In particular, the five balanced patterns cannot be deleted. At a balanced
prime, the character is 1 on units but 0 on nonunits, not identically 1.
For \(\mathfrak c=(1)\), take \(\chi=1\), including at 0.

## 3 A shorter exact organization by product columns

Define the finite convolution

\[
 B_{\mathfrak v}(D)=\sum_{\mathfrak n_1\mathfrak n_2=\mathfrak v}
                    a_{\mathfrak n_1}a_{\mathfrak n_2}.
\]

Multiplicativity in the denominator, including zero extensions, gives

\[
 A_u(D)^2=\sum_{\mathfrak v}B_{\mathfrak v}(D)\chi_{\mathfrak v}(u),
\]

and hence

\[
 \mathcal E_{4,\Phi}(D,H)
 =\sum_{\mathfrak v,\mathfrak w}B_{\mathfrak v}\overline{B_{\mathfrak w}}
                       \mathcal C_\Phi(\mathfrak v,\mathfrak w;H),
 \tag{G}
\]

where \(\mathcal C_\Phi\) is the row sum of (F) against \(\Phi(Nu/H)\).
Every product column is cube-free, has norm \(\asymp_W D^2\), and has a
unique expression \(\mathfrak v=\mathfrak r\mathfrak t^2\), with
\(\mathfrak r,\mathfrak t\) squarefree and coprime. Its coefficient is

\[
 B_{\mathfrak r\mathfrak t^2}(D)
 =\mu_K(\mathfrak r)\nu(\mathfrak r\mathfrak t^2)
   \sum_{\mathfrak e\mid\mathfrak r}
     W(N(\mathfrak t\mathfrak e)/D)
     W(N(\mathfrak t\mathfrak r/\mathfrak e)/D).
 \tag{B}
\]

**Proof:** every squarefree factorization of \(\mathfrak r\mathfrak t^2\)
has the form \((\mathfrak t\mathfrak e,\mathfrak t\mathfrak r/\mathfrak e)\).
The Möbius product is \(\mu_K(\mathfrak r)\), and the character product is
\(\nu(\mathfrak r\mathfrak t^2)\). Summing gives (B).

For a product pair \((\mathfrak v,\mathfrak w)\), the same conductor/mask
split is obtained from
\(e_{\mathfrak p}=v_{\mathfrak p}(\mathfrak v)-v_{\mathfrak p}(\mathfrak w)\).
Include a prime in \(\mathfrak b\) when the valuations are equal and
positive, and in \(\mathfrak c\) when they differ. Thus
\(\mathfrak Q=\operatorname{rad}(\mathfrak v\mathfrak w)\), not generally
\(\mathfrak v\mathfrak w\).

### The grouped diagonal is nonnegative

Since the valuation differences lie in \([-2,2]\), \(\mathfrak c=(1)\)
if and only if \(\mathfrak v=\mathfrak w\). Its exact contribution is

\[
 \mathcal D_\Phi(D,H)=\sum_{\mathfrak v}|B_{\mathfrak v}|^2
       \sum_u\mathbf1_{(u,\mathfrak v)=1}\Phi(Nu/H)\ge0.
\]

The divisor bound and Cauchy–Schwarz give

\[
 \sum_{\mathfrak v}|B_{\mathfrak v}|^2
 \le \max_{N\mathfrak v\ll_W D^2}\tau_K(\mathfrak v)
          \left(\sum_{\mathfrak n}|a_{\mathfrak n}|^2\right)^2
 \ll_{S,W,\varepsilon}D^{2+\varepsilon}.
\]

Lattice counting gives \(\sum_u\Phi(Nu/H)\ll_\Phi H\) for \(H\ge1\), so

\[
 0\le\mathcal D_\Phi(D,H)\ll H D^{2+\varepsilon}.
 \tag{D}
\]

This includes all product-equality tuples, not just pairwise permutations.

## 4 Exact finite Fourier transform with masks

Use the additive character and measure

\[
 e(z)=\exp(4\pi i\operatorname{Im}z/\sqrt3),\qquad
 d\mu(z)=\frac2{\sqrt3}\,dx\,dy.
\]

The lattice \(\mathcal O\) has covolume one for this measure and is self-dual
for the pairing \(e(zy)\). In coordinates \(z=a+b\omega\),
\(y=c+d\omega\), the exponent modulo integers is \(ad+bc-bd\), with
unimodular pairing matrix \(\begin{pmatrix}0&1\\1&-1\end{pmatrix}\).

Write \(b,c,Q=bc\) for the primary generators. Define

\[
 \tau_c(\chi)=\sum_{x\bmod c}\chi(x)e(x/c),\qquad
 r_b(k)=\sum_{\substack{x\bmod b\\(x,b)=1}}e(kx/b).
\]

For squarefree \(b\),

\[
 r_b(k)=\prod_{\mathfrak p\mid\mathfrak b}
 \begin{cases}N\mathfrak p-1,&\mathfrak p\mid(k),\\-1,&\mathfrak p\nmid(k),\end{cases}
 =\sum_{\mathfrak d\mid(\mathfrak b,(k))}
         N\mathfrak d\,\mu_K(\mathfrak b/\mathfrak d).
\]

For the product (F), its unnormalized finite Fourier transform is

\[
 \boxed{\quad
 \mathcal T_{\mathfrak v,\mathfrak w}(k)
  =\chi(b)\tau_c(\chi)\overline{\chi(k)}\,r_b(k).
 \quad}
 \tag{T}
\]

**Proof:** use CRT coordinates
\(x=b(b^{-1}\bmod c)x_c+c(c^{-1}\bmod b)x_b\). The conductor part of the
additive phase has coefficient \(kb^{-1}\) modulo \(c\), so its Gauss sum
is
\(\overline{\chi(kb^{-1})}\tau_c(\chi)
 =\chi(b)\overline{\chi(k)}\tau_c(\chi)\).
The mask part is \(r_b(kc^{-1})=r_b(k)\). This also covers nonunit \(k\):
an active prime dividing \(k\) makes its nontrivial local character sum zero.
For \(c=1\), the conventions \(\tau_1(1)=1\), \(\chi(k)=1\) give the
Ramanujan sum without an artificial zero at \(k=0\).

The global Gauss sum itself retains CRT phases:

\[
 \tau_c(\chi)
 =\prod_{\mathfrak p\mid\mathfrak c}
    \chi_{\mathfrak p}(c/p)^{e_{\mathfrak p}}
    \tau_p(\chi_{\mathfrak p}^{e_{\mathfrak p}}).
 \tag{CRT}
\]

Replacing this by the product of local Gauss sums with the phase factors
removed would be incorrect. Keeping \(\tau_c\) intact is often safer.

## 5 Exact row Poisson formula

Define the radial Fourier profile by

\[
 \widehat\Phi(|w|^2)=\int_{\mathbb C}\Phi(|z|^2)e(-zw)\,d\mu(z).
\]

Scaling and Poisson summation on the residue classes modulo \(Q\) give

\[
 \boxed{\quad
 \mathcal C_\Phi(\mathfrak v,\mathfrak w;H)
 =\frac{H\chi(b)\tau_c(\chi)}{N\mathfrak b\,N\mathfrak c}
   \sum_{k\in\mathcal O}\overline{\chi(k)}r_b(k)
       \widehat\Phi\!\left(\frac{HNk}{N\mathfrak b\,N\mathfrak c}\right).
 \quad}
 \tag{P}
\]

For clarity, Poisson on the class \(x+Q\mathcal O\) contributes
\(H/(NQ)\) times
\(e(kx/Q)\widehat\Phi(HNk/NQ)\). Summing in \(x\) produces (T).
All infinite sums converge absolutely for each fixed product pair.

Expanding the Ramanujan sum and substituting \(k=d\ell\) gives the
alternative, exactly matching the excluded-prime formula in [R11]:

\[
 \mathcal C_\Phi
 =\frac{H\tau_c(\chi)}{N\mathfrak c}
   \sum_{\mathfrak d\mid\mathfrak b}
       \frac{\mu_K(\mathfrak d)\chi(d)}{N\mathfrak d}
       \sum_{k\in\mathcal O}\overline{\chi(k)}
          \widehat\Phi\!\left(\frac{HNk}{N\mathfrak d\,N\mathfrak c}\right).
 \tag{P'}
\]

In deriving (P'), reindex the divisor in the Ramanujan sum by its complement
in \(\mathfrak b\). This is where the factor \(\chi(b)\) in (P) becomes
\(\chi(d)\) in (P').

If \(\mathfrak v\ne\mathfrak w\), the character is nonprincipal and
\(\overline{\chi(0)}=0\): the zero frequency is absent. If
\(\mathfrak v=\mathfrak w\), the zero-frequency contribution is

\[
 H\widehat\Phi(0)\prod_{\mathfrak p\mid\mathfrak v}
                              (1-(N\mathfrak p)^{-1}).
\]

The principal product pair can still have nonzero Fourier frequencies. It is
not legitimate to identify the *whole* diagonal with this density term unless
those frequencies are also controlled. Bound (D) avoids that issue.

## 6 An exact unit symmetry reduction

Let \(\epsilon=1+\omega\), a generator of the six units. Radial weights and
coprimality masks are invariant under \(u\mapsto\epsilon u\). Therefore

\[
 \mathcal C_\Phi=\chi(\epsilon)\mathcal C_\Phi,
 \qquad \chi(\epsilon)\ne1\Longrightarrow\mathcal C_\Phi=0.
\]

At a good prime,
\(\chi_{\mathfrak p}(\epsilon)
 =\epsilon^{(N\mathfrak p-1)/6}\), and \(N\mathfrak p\equiv1\pmod6\).
The map

\[
 q\longmapsto (q-1)/6\pmod6\qquad(q\equiv1\pmod6)
\]

turns multiplication into addition, since
\((1+6a)(1+6b)=1+6(a+b)+36ab\). Consequently

\[
 \chi(\epsilon)=1
 \quad\Longleftrightarrow\quad
 N\mathfrak v\equiv N\mathfrak w\pmod{36}.
 \tag{U}
\]

Thus the off-diagonal can be restricted **exactly** to these norm classes.
This is a finite congruence restriction, not a power saving by itself. In a
numerical lattice truncation, use unit-invariant truncations if exact unit
cancellation is to be preserved.

## 7 A rigorous elementary bound and its shortfall

Here is a bound that can actually be deduced without the proposed new moment
estimate. Constants depend on the fixed profiles and on the requested
\(\varepsilon\), not on the growing scales.

### A completed nonprincipal correlation

For \(c\ne1\), finite Parseval and the primitive Gauss transform imply
\(|\tau_c(\chi)|=\sqrt{N\mathfrak c}\). Indeed,
\(\sum_{k\bmod c}|\overline{\chi(k)}\tau_c|^2
 =N\mathfrak c\sum_{x\bmod c}|\chi(x)|^2\), and both character-square sums count
\(\varphi_K(\mathfrak c)\).

Lattice counting and Schwartz decay give, for every \(L>0\) and fixed
\(A>1\),

\[
 \sum_{k\ne0}(1+Nk/L)^{-A}\ll_A L.
\]

For \(L\ge1\), sum dyadic annuli. For \(L<1\), use \(Nk\ge1\) and the
convergent sum of \((Nk)^{-A}\), obtaining \(O(L^A)\), hence \(O(L)\).
Using (P') with \(L=N\mathfrak d\,N\mathfrak c/H\) yields

\[
 |\mathcal C_\Phi(\mathfrak v,\mathfrak w;H)|
 \ll_\Phi \tau_K(\mathfrak b)\sqrt{N\mathfrak c}
 \qquad(\mathfrak v\ne\mathfrak w).
 \tag{C}
\]

### Applying completion at the second moment first

For the original second moment, two distinct squarefree columns have
\(N\mathfrak c\ll_W D^2\) and \(\tau_K(\mathfrak b)\ll D^\varepsilon\).
There are \(O_W(D^2)\) column pairs. Its diagonal is \(O(HD)\), so (C)
gives

\[
 \sum_u |A_u(D)|^2\Phi(Nu/H)
       \ll HD+D^{3+\varepsilon}.
\]

Since \(|A_u(D)|\ll_W D\),

\[
 \boxed{\quad
 \mathcal E_{4,\Phi}(D,H)
  \ll HD^3+D^{5+\varepsilon},\qquad H,D\ge1.
 \quad}
 \tag{W4}
\]

The trivial bound \(O(HD^4)\) can be used when smaller. This argument works
for arbitrary uniformly bounded coefficients on the original squarefree
support. It therefore cannot establish the Möbius-specific P4 target.

At \(H=D^{4/3}\), the comparison is

| Estimate | Exponent of \(D\), ignoring \(\varepsilon\) |
| --- | --- |
| Trivial fourth moment | \(16/3\) |
| Elementary bound (W4) | \(5\) |
| Desired P4 | \(10/3\) |

The elementary estimate improves on counting by \(D^{1/3}\), but still
needs a further \(D^{5/3}\) saving to meet P4. Replica extraction from (W4)
only gives exponent \(43/36>1\) for \(A_1(D)\), worse than its trivial
bound. **It provides no improved zero-free region.**

## 8 The precise unresolved off diagonal

Let \(\mathcal R_\Phi=\mathcal E_{4,\Phi}-\mathcal D_\Phi\). Combining
(G), (P), and (U) expresses it exactly as

\[
\begin{aligned}
 \mathcal R_\Phi(D,H)
 ={}&H\sum_{\substack{\mathfrak v\ne\mathfrak w\\
                  N\mathfrak v\equiv N\mathfrak w\ (36)}}
 B_{\mathfrak v}\overline{B_{\mathfrak w}}
 \frac{\chi_{\mathfrak v,\mathfrak w}(b)
                  \tau_c(\chi_{\mathfrak v,\mathfrak w})}{N\mathfrak Q}\\
 &\quad\times\sum_{k\ne0}
 \overline{\chi_{\mathfrak v,\mathfrak w}(k)}\,r_b(k)
          \widehat\Phi(HNk/N\mathfrak Q).
\end{aligned}
 \tag{R}
\]

Conductor, mask, and character in each summand are those of its product pair.
A sufficient missing estimate is

\[
 |\mathcal R_\Phi(D,D^{4/3})|
       \ll_{\nu,S,W,\Phi,\varepsilon}D^{10/3+\varepsilon}.
 \tag{R4}
\]

**R4 has not been proved here.** The sum is real after conjugate pairs are
grouped, but its individual terms have phases. Bounding each one separately
loses precisely the cancellation we need.

Three obstacles prevent simply recycling the companion's argument:

1. The product columns have length \(D^2\), while the row range is
   \(D^{4/3}=(D^2)^{2/3}\), below the companion's stated second-moment range.
2. Coefficients (B) are divisor convolutions on cube-free support, not a
   single squarefree Möbius polynomial with one radial weight.
3. The Fourier transform contains mixed sextic/cubic Gauss factors,
   conductor-dependent CRT phases, and the balanced-prime masks. A theorem
   closing this family under theta reflection and a second Poisson step
   remains to be established.

In the generic coprime case, \(N\mathfrak Q\asymp D^4\); the dual norm
scale in (R) is \(D^{8/3}\). Treating it as a short \(D\)-scale sum would
miscount a main power.

There is also a concrete check against false progress. For coefficient 1
on prime columns with norm in \((D,2D]\), sixth-power replica rows below
\(D^{4/3}\) force a fourth moment
\(\gg D^{38/9}/(\log D)^5\), which exceeds P4's exponent \(30/9\).
This survives the exact unit projection. Any proposed proof of R4 that works
unchanged for arbitrary bounded original coefficients must therefore contain
a loss or an error. The Möbius structure in (B) must be used substantively.

## 9 Reproducible verification and its limits

Run from the repository root:

```sh
python3 -m unittest discover -s research_notes/checks -p 'test_*.py' -v
python3 research_notes/checks/fourth_moment.py
(cd lean && lean ../research_notes/checks/FourthMomentPatterns.lean)
```

Recorded in `results/fourth_moment.json` and `results/fourth_moment_lean.txt`:

- **Fourth-moment checkpoint:** 33 Python tests passed. The expanded current
  suite is listed in `README.md`.
- **355 local and 721 CRT Fourier equalities** checked using exact
  cyclotomic-polynomial arithmetic, with no floating-point comparisons.
- Split prime ideals of norms 7, 7, 13, 19, including the two different primes
  above 7, and the inert prime ideal of norm 25 are covered.
- Primitive Gauss norms, CRT phase factors, the companion's local cubic Gauss
  normalization, the core-square convolution, and the unit-norm congruence
  are checked separately.
- A complete finite fourth moment over 2,275 residue classes and seven columns
  agrees exactly with its grouped diagonal: both equal **179,509,530**.
- Lean 4.34.1 checks **six finite combinatorial/residue lemmas** from `Std`;
  `#print axioms` reports no axioms for each.

The finite complete-period example is not a short-row test of P4. The Python
checks are not formal proofs for all primes. The Lean file does not formalize
characters, Poisson summation, (W4), R4, or RH. Those boundaries matter: the
analytic deductions above are written proofs, and the new cancellation
estimate remains an open research task.
