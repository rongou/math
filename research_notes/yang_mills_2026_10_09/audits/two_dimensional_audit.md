# Independent audit: the two-dimensional finite-volume full-gap criterion

**Date:** October 9, 2026.  
**Initial scope:** the O(4) finite-volume criterion and its O(3) trace-section reuse only. This is not a full Family 215 audit. No renormalization, preliminary mixing, continuum-construction, Yang–Mills, or higher-dimensional theorem is certified by this 2D audit. A separately requested review of the new research manuscript, if present below, has its own scope and verdict.

## 1. Executive verdict

**The 2D criterion passes under the actual model conventions.** I found no false scalar inequality, incorrect numerical constant, missing spectral sector within the specified OS Hilbert space, or substantive square-versus-cylinder gap in the argument. The O(3) rectangular and sheared reuse also passes, **conditional on its explicitly cited upstream inputs**.

There is one minor indexing correction and several worthwhile proof clarifications:

1. **O4-FV:177–188:** explicitly restrict the half-period argument to `k >= 1`. Then `w/2 = 2^(k-1)n` is an admissible previously controlled square. At `k=0, n=4`, the half-period is 2, outside the paper's period convention; for other starting sizes it need not be a controlled earlier dyadic scale. Discarding this initial index does not change any limit or conclusion.
2. **O4-FV:194–200; O3-TR:439–457:** the full-space conclusion needs the positive one-step OS contraction, centering, density, and spectral-projection argument written explicitly. These are valid here, not new unproved model hypotheses: O4's construction is supplied in O4-PRE:1199–1235, and O3 states the two reflection-positivity properties. A complete proof is below.
3. **O3-TR:440–443:** on a finite even torus, site reflection fixes **two rows**, and one conditions on both. The singular “fixed row” is harmless shorthand if the proof is understood through finite-volume reflection positivity and passage to the limit.
4. **Do not weaken the hypotheses when reusing this proof.** Both coordinate directions must have the requisite positive-transfer trace representation; a width-uniform cylinder gap alone does not identify square-torus limits; pointwise-positive kernels need not be positive semidefinite; and a selected-sector trace does not control the full local-observable Hilbert space. Explicit counterexamples below show these distinctions are essential. They do **not** refute the two papers' stated 2D arguments.

In particular, the covariance prefactor **1** is correct, not 4, and no factor depending on slab thickness or number of observed spins is lost. The trace-comparison constants **2** (ordinary closing) and **4** (shifted closing) are also correct.

## 2. Source snapshot and anchor conventions

All line numbers are one-based in the following inspected files. An anchor such as `O4-FV:69–77` means exactly that line range in the corresponding path.

| Alias | Repository-relative file |
|---|---|
| O4-FV | `preprints/Sharp-mass-bounds-for-the-two-dimensional-O4-model-September-23-2026/build/sections/finite-volume.tex` |
| O4-INTRO | `preprints/Sharp-mass-bounds-for-the-two-dimensional-O4-model-September-23-2026/build/sections/introduction.tex` |
| O4-PRE | `preprints/Sharp-mass-bounds-for-the-two-dimensional-O4-model-September-23-2026/build/sections/preliminary.tex` |
| O3-TR | `preprints/The-canonical-massive-continuum-limit-of-the-two-dimensional-O3-model-October-4-2026/build/sections/trace.tex` |
| O3-PRE | `preprints/The-canonical-massive-continuum-limit-of-the-two-dimensional-O3-model-October-4-2026/build/sections/preliminary.tex` |
| O3-SHOOT | `preprints/The-canonical-massive-continuum-limit-of-the-two-dimensional-O3-model-October-4-2026/build/sections/shooting.tex` |
| O3-COMP | `preprints/The-canonical-massive-continuum-limit-of-the-two-dimensional-O3-model-October-4-2026/build/sections/comparison.tex` |
| O3-SETUP | `preprints/The-canonical-massive-continuum-limit-of-the-two-dimensional-O3-model-October-4-2026/build/sections/setup.tex` |

SHA-256 of the two audit targets:

```text
O4-FV  ee00fec334af6784448923f7c1df428538c13927964b8911649d8c18766aa9b5
O3-TR  847a3baefeee82e3190d62d2a7970df4cab93a81f134452cc3a3d16512e64249
```

The contextual assumptions are normalized sphere measure, finite ferromagnetic coupling, homogeneous nearest-neighbor interactions, and the stated admissible periods. O4-INTRO:4–17 supplies `beta > 0` and even periods at least four; O3-TR:124–125 explicitly allows `beta >= 0`. The O4 definition of “full” is the completion of the local half-space algebra, not an unspecified enlarged representation (O4-INTRO:65–80).

**Verdict vocabulary:** **PASS** = the statement follows under these conventions; **EXPOSITION** = valid, with a compressed justification completed below; **MINOR FIX** = an indexing/domain qualification is required but the theorem survives unchanged; **CONDITIONAL** = the implication is checked, not the upstream input theorem.

## 3. Statement-by-statement verdicts

### 3.1 O4 finite-volume section

| Anchor | Statement or step | Verdict |
|---|---|---|
| O4-FV:4–8, 95–102 | Actual traces see all finite-cylinder sectors; area terms cancel from the test. | **PASS.** This means full, unprojected partition functions with consistent normalization. Arbitrary shape-dependent or sector-dependent normalizations are not allowed. |
| O4-FV:12–27 | Compactness, self-adjointness, positive semidefiniteness, trace class, simple largest eigenvalue. | **PASS / EXPOSITION.** The feature expansion has summable positive rank-one traces; strict positivity gives positivity improvement and a simple Perron eigenvector. See §4.1. |
| O4-FV:28–33 | Nonnegative eigenvalue list and `Z(n,w) = Tr K_w^n`. | **PASS.** The geometric period convention prevents double-counting the short-period bonds; rank one is covered by `lambda_2=0`. |
| O4-FV:35–50 | Nonnegativity of `p,q`; purity interpretation. | **PASS.** The proof for `q` uses the other coordinate transfer, not just the rectangle identity or time-transfer positivity. |
| O4-FV:55–71 | `s_n <= exp(p)-1 <= p exp(p) <= 2p` for `p <= 1/4`. | **PASS.** The largest normalized weight is `1/(1+s_n)`, and `exp(1/4)<2`. |
| O4-FV:62–76 | First excited eigenvalue bound and `p(2n,w) <= 4p(n,w)^2`. | **PASS.** `s_(2n) <= s_n^2`; the final numerical factor is bounded by `2 exp(1/2)<4`. |
| O4-FV:80–101 | Rectangle identity and the nonnegative decomposition of `Delta`. | **PASS.** Exact substitution; no asymptotic free-energy assumption. |
| O4-FV:129–133 | `q(2r,r), p(r,2r) <= Delta`; `p(2r,2r) <= 4 Delta^2`. | **PASS.** All arguments are at the stated fixed coupling. |
| O4-FV:135–143 | `q(4r,r) <= 3 Delta`; `q(4r,2r) <= 36 Delta^2`; recursion with 44, then 64. | **PASS.** The first estimate uses `Delta<=1/4`; the second uses `3 Delta<=1/4`. Both follow from the chosen threshold. |
| O4-FV:146–150 | Smallness preservation and double-exponential iteration. | **PASS.** `64 eta_*=1/16`; the printed final bound deliberately weakens the result. |
| O4-FV:152–155 | Taking the `n_k`th root gives the width-uniform gap. | **PASS.** There is no factor-of-two error. The unweakened iteration even permits the larger lower rate `(log 16)/n`. |
| O4-FV:157–166 | Bounded slab kernel and insertion norm. | **PASS / EXPOSITION.** Domination is pointwise in absolute value and works for non-self-adjoint, complex insertions. See §4.3. |
| O4-FV:167–175 | Cylinder covariance with prefactor 1 and edge separation `d`. | **PASS.** Insert `T_w^d-P_w` between the two uncentered insertion operators. The case `d=0` is valid. |
| O4-FV:178–185 | Square expectation as a trace; error at most `2 ||F||_infty s_(w/2)(w)`. | **PASS / EXPOSITION.** The unused power is trace class and the denominator is `1+s_w>=1`. See §4.4. |
| O4-FV:177–188 | Control of the half-period trace by the preceding square. | **MINOR FIX.** State `k>=1` here. No initial half-size small-box hypothesis is needed. |
| O4-FV:190–192 | Same subsequential square/cylinder limits, including products. | **PASS.** Keep coupling, observables, and their separation fixed while taking width to infinity. Each product is again a fixed local insertion. |
| O4-FV:118–124, 194–200 | Gap in every such local limit and on the full OS vacuum complement. | **PASS / EXPOSITION.** No plane-state uniqueness is needed for the first assertion. See §4.5 for contraction, density, and spectral exclusion. |
| O4-FV:203–206 | Extension to bounded measurable local observables without a slab-size prefactor. | **PASS / EXPOSITION.** Approximate inside the already obtained limiting state's finite-support marginal, preserving supremum bounds. See §4.6. |
| O4-FV:208–211 | Obtaining a small test at the desired physical scale. | **OUT OF SCOPE.** This section reduces to that problem; this audit does not prove that its proposed upstream estimates solve it. |

### 3.2 O3 trace-section reuse

| Anchor | Statement or step | Verdict |
|---|---|---|
| O3-TR:13–24 | Rectangular test and cancellation of bulk scalars. | **PASS / CONDITIONAL.** Cancellation is exact for a common area-proportional scalar. The RG assertion that the extracted scalars have this convention is an upstream input. |
| O3-TR:33–51 | Uniform reference-box proposition. | **CONDITIONAL PASS.** Its implication from the four stated inputs is correct; those inputs are not independently certified here. |
| O3-TR:55–68 | Choice of `chi`, divisibility, and the three scale inequalities. | **PASS.** Choose sufficiently small positive `upsilon`, then `upsilon/2<chi<min(1,eta/(2pi))`. Integer/dyadic rounding costs `O(1)` in `log_L m_K`. |
| O3-TR:70–87 | Reference side dominates the preliminary length; polynomial prefactors vanish against the exponential. | **CONDITIONAL PASS.** The side/length ratio grows exponentially in `K`, so the decay in that ratio dominates the microscopic-period prefactors. |
| O3-TR:89–107 | Endpoint comparison, logarithms, bulk cancellation, and `m_K^2 delta_K -> 0`. | **CONDITIONAL PASS / EXPOSITION.** Positivity and a small relative partition-function error justify taking logarithms. The exponent is `upsilon-2chi<0`. See §4.7. |
| O3-TR:112–147 | O(3) transfer hypotheses and rank-one convention. | **PASS.** Replacing `S^3` by `S^2` changes none of the feature/trace/Perron arguments. |
| O3-TR:149–192 | `p,q`, concentration lemma, and constants. | **PASS.** Same scalar proof as O4, with both coordinate transfers available. |
| O3-TR:194–205 | Two decompositions of rectangular `Delta` and rectangle identity. | **PASS.** These are exact for unequal periods. |
| O3-TR:207–259 | Rectangular doubling recursion and square width-gap conclusion. | **PASS.** Equality of the two original periods is unnecessary for the recursion. The stated square spectral consequence follows with the original time length in its denominator. |
| O3-TR:267–280 | Slab insertion norm, including `r=0`. | **PASS.** The text explicitly gives the required absolute-kernel domination argument. |
| O3-TR:282–297 | Torus/cylinder bound and interchange of directions. | **PASS.** `n` is even where `s_(n/2)` is used; all relevant residual powers are positive integers. |
| O3-TR:309–334 | Auxiliary aspects and supports, including lifted sheared supports. | **PASS.** The two auxiliary lists are precisely those used in the proof. Their evenness/minimum-size conditions are imposed in advance. |
| O3-TR:347–365 | Two one-direction comparisons and summation over subsequent doublings. | **PASS / CONDITIONAL.** The estimates are uniform over eligible bounded insertions. Identification with the named plane state uses the cited periodic-limit input. See §4.8. |
| O3-TR:367–374 | Measurable-observable identification at fixed cutoff. | **PASS.** Bounded nearest-neighbor energies give a volume-independent finite-support density bound. It need not be uniform in the cutoff. |
| O3-TR:376–395 | Shift unitary, vacuum invariance, twisted denominator, and constant 4. | **PASS.** No reflection positivity of the sheared torus is asserted or needed. See §4.9. |
| O3-TR:397–412 | Plane slab covariance with `c=log 2`. | **PASS / CONDITIONAL.** Uses the square reference test and the half-period comparison, not just the operator norm gap. |
| O3-TR:421–457 | Full OS spectrum and cutoff-independent physical lower energy scale. | **PASS / CONDITIONAL / EXPOSITION.** The spectral argument is correct; the physical conversion is exactly `a_N^(-1) log(2)/(M_0 L^N)=log(2)/M_0`. See §4.5. |
| O3-TR:440–444 | Site/link reflection positivity and positive one-step contraction. | **EXPOSITION.** In finite volume condition on both fixed rows; use the quotient/contraction argument below. No missing ferromagnetic hypothesis. |
| O3-TR:460–463 | Subsequent continuum transfer. | **OUT OF SCOPE.** A fixed-cutoff spectral estimate is not itself a continuum reconstruction theorem. |
| O3-TR:465–488 | Unimodular change of periods, shear, and eventual support lifts. | **PASS.** The determinant is 1, the area is `25M^2`, and the microscopic periods are integral. See §4.9. |

## 4. Completed proofs and the one required correction

The following are independent derivations of the compressed steps. Except for the `k>=1` qualification, they complete exposition rather than replace false claims.

### 4.1 Trace class and simple ground state

**Anchors:** O4-FV:12–33; O3-TR:112–147.

Let `nu_w` be product probability measure on the row spin space, and write

\[
 M(s)=e^{\beta V_w(s)/2},\qquad
 K_w(s,s')=M(s)\prod_{i=1}^w e^{\beta s_i\cdot s_i'}M(s').
\]

Continuity on the compact product and symmetry give a Hilbert–Schmidt, hence compact, self-adjoint operator. For `beta>=0`, expand each exponential in tensor-coordinate features. The result is a sum of positive rank-one operators

\[
 K_w=\sum_\alpha c_\alpha\,|f_\alpha\rangle\langle f_\alpha|,
 \qquad c_\alpha\ge0,
\]

where each feature includes the factor `M`. Its total trace is finite:

\[
 \sum_\alpha c_\alpha\|f_\alpha\|_2^2
 =\int K_w(s,s)\,d\nu_w(s)
 =\int e^{\beta V_w(s)+\beta w}\,d\nu_w(s)
 \le e^{2\beta w}.
\]

Tonelli applies to the nonnegative diagonal terms. Thus the rank-one series converges in trace norm, not merely in Hilbert–Schmidt norm. It is the displayed kernel operator and is positive semidefinite and trace class. This avoids the invalid inference “compact implies trace class.”

The kernel is strictly positive everywhere. A top Rayleigh vector can be replaced by its absolute value without decreasing the Rayleigh quotient. Equality at the maximum forces constant phase: a sign-changing real maximizer, or a complex maximizer with nonconstant phase, would give a strictly smaller quotient than its absolute value. Applying the kernel to a nonzero nonnegative maximizer makes it strictly positive. A second top eigenvector orthogonal to that positive eigenvector would contradict this equality condition. Hence the top eigenvalue is positive and simple. Compactness then gives `lambda_2<lambda_1`; positive semidefiniteness gives nonnegative remaining eigenvalues.

At `beta=0`, `K_w` is exactly the rank-one averaging projection; the convention `lambda_2=0` is correct. No injectivity or strictly positive lower bound on all eigenvalues is required.

Closing `n` transfer steps gives exactly the nearest-neighbor torus integral: each row's half-potentials add to one complete horizontal potential. All powers used in the criterion are trace class. The same construction works in the other coordinate direction.

### 4.2 Purity, recursion, and every numerical constant

**Anchors:** O4-FV:35–155; O3-TR:149–259.

Put `r_i=lambda_i/lambda_1`, `r_1=1`, and `s_j=sum_{i>=2} r_i^j`. Then

\[
 p(j,w)=2\log(1+s_j)-\log(1+s_{2j}),\qquad
 t_1=\frac1{1+s_j},\qquad e^{-p}=\sum_i t_i^2\le t_1.
\]

Therefore

\[
 s_j\le e^p-1\le pe^p\le2p\quad(0\le p\le1/4).
\]

Nonnegativity of all summands gives `s_(2j)<=s_j^2`, so

\[
 \begin{aligned}
 p(2j,w)
 &\le2\log(1+s_{2j})\le2s_{2j}\le2s_j^2\\
 &\le2p^2e^{2p}\le2e^{1/2}p^2<4p^2.
 \end{aligned}
\]

These arguments apply to `q` only because it too is a positive-transfer purity defect, in the other direction.

For a rectangle, direct cancellation of logarithms gives

\[
 \Delta(n,w)=2p(n,w)+q(2n,w)=2q(n,w)+p(n,2w),
\]

\[
 p(n,2w)=2p(n,w)-2q(n,w)+q(2n,w).
\]

If `Delta=Delta(n,w)<=eta_*=2^(-10)`, the two decompositions imply

\[
 p(n,2w)\le\Delta,\quad q(2n,w)\le\Delta,\quad
 p(2n,2w)\le4\Delta^2.
\]

The interchanged identity gives

\[
 q(4n,w)\le2\Delta+4\Delta^2\le3\Delta,
\]

and a spatial squaring then gives

\[
 q(4n,2w)\le4(3\Delta)^2=36\Delta^2.
\]

Thus

\[
 \Delta(2n,2w)\le(8+36)\Delta^2=44\Delta^2\le64\Delta^2.
\]

The complete threshold check is

\[
 3\eta_*=\frac3{1024}<\frac14,\qquad
 64\eta_*=\frac1{16},\qquad
 64\eta_*^2=\frac1{16384}<\eta_*.
\]

Writing `D_k=Delta(2^k n,2^k w)`, induction yields

\[
 D_k\le\frac1{64}(64D_0)^{2^k}
 \le\frac1{64}16^{-2^k}
 \le\frac1{64}2^{-2^k}.
\]

For a square, with `n_k=2^k n`,

\[
 \left(\frac{\lambda_2(n_k)}{\lambda_1(n_k)}\right)^{n_k}
 \le2p(n_k,n_k)\le D_k.
\]

Using even the printed weaker estimate gives the claimed rate `log(2)/n`. Retaining `16^(-2^k)` instead gives the stronger permissible rate `log(16)/n`. This is unused slack, not an error in the stated constant. Rank one and `D_0=0` are handled directly, without taking the logarithm of zero.

### 4.3 Slab insertions and why the covariance constant is 1

**Anchors:** O4-FV:157–175; O3-TR:267–280, 397–409.

Let `F` read a finite slab from its first to its last row, with exactly `r` transfer edges between these rows. The internal integrations have nonnegative weight, hence

\[
 |K_{w,F}(s,s')|\le\|F\|_\infty K_w^r(s,s').
\]

For `T_w=K_w/lambda_1(w)` and `A_F=K_{w,F}/lambda_1(w)^r`, this is an absolute-kernel bound, not a claim that `A_F` is positive or self-adjoint. For every `f` in the row `L^2` space,

\[
 |A_Ff|\le\|F\|_\infty T_w^r|f|,
 \qquad \|A_Ff\|_2\le\|F\|_\infty\|f\|_2.
\]

The case `r=0` is multiplication by `F`. For `r>=1`, the insertion kernel is bounded and Hilbert–Schmidt, but need not itself be trace class. The later trace formulas always multiply it by an unused positive power of `T_w`, so no unjustified trace of a bare insertion is taken.

The positive normalized ground vector defines a genuine stationary cylinder law. Explicitly its row distribution and transition kernel are

\[
 \pi_w(ds)=\Omega_w(s)^2\nu_w(ds),\qquad
 P_w^{\rm Markov}(s,ds')=
 \frac{K_w(s,s')\Omega_w(s')}{\lambda_1(w)\Omega_w(s)}\nu_w(ds').
\]

The eigenvector equation normalizes the transition, and symmetry gives stationarity. Its slab expectation is `omega_w(F)=<Omega_w,A_F Omega_w>`.

Write `P_w=|Omega_w><Omega_w|` for the Hilbert-space ground projection. For two ordered slabs with `d` edges between the last row of the first and the first row of the second,

\[
 \operatorname{Cov}_{\omega_w}(F,G)
 =\langle\Omega_w,
 A_{\overline F}(T_w^d-P_w)A_G\Omega_w\rangle.
\]

Consequently

\[
 |\operatorname{Cov}_{\omega_w}(F,G)|
 \le\|F\|_\infty\|G\|_\infty\,
 \|T_w^d-P_w\|
 \le\|F\|_\infty\|G\|_\infty e^{-md}.
\]

For `d=0`, use `T_w^0-P_w=I-P_w`, whose norm is at most one. This also covers slabs meeting at an endpoint row. There is no need to replace the insertion operators by centered operators with potentially doubled norms. That is why no extraneous factor 4 appears. Neither `r`, the spatial support size, nor the number of observed spins enters the bound.

### 4.4 Torus/cylinder comparison and the corrected square limit

**Anchors:** O4-FV:177–192; O3-TR:282–297, 410–412.

Fix a circumference and suppress `w`. For every positive integer `j`,

\[
 R_j=T^j-P\ge0,\qquad \|R_j\|_1=\operatorname{Tr}R_j=s_j.
\]

If the time period is `h` and `r<=h/2`, the unused power `h-r>=1` is trace class. Set `a_F=<Omega,A_F Omega>`. The exact difference is

\[
 \frac{\operatorname{Tr}(A_FT^{h-r})}{\operatorname{Tr}T^h}-a_F
 =\frac{\operatorname{Tr}(A_FR_{h-r})-a_Fs_h}{1+s_h}.
\]

Trace duality, `|a_F|<=||F||_infty`, and monotonicity of the nonnegative trace tails give, for even `h`,

\[
 |\mu_{h,w}(F)-\omega_w(F)|
 \le\|F\|_\infty\frac{s_{h-r}+s_h}{1+s_h}
 \le2\|F\|_\infty s_{h/2}(w).
\]

The path-integral trace identity also holds for bounded measurable insertions: for a nonzero-thickness insertion it follows by composing the two Hilbert–Schmidt kernels; for a zero-thickness multiplier one can split the unused transfer power into two Hilbert–Schmidt factors. Thus it is not an unsupported diagonal-trace assertion about an arbitrary bounded kernel.

**Precise O4 correction.** Put `w_k=2^k n` and take **`k>=1`**, with `k` eventually large enough that the fixed slab satisfies `r<=w_k/2`. Then `w_k/2=w_(k-1)` is an admissible even period at least four, and

\[
 p(w_k/2,w_k)
 =\Delta_\beta(w_k/2)-2q(w_k/2,w_k/2)
 \le\Delta_\beta(w_{k-1}).
\]

Hence

\[
 s_{w_k/2}(w_k)
 \le e^{\Delta_\beta(w_{k-1})}-1\longrightarrow0.
\]

This proves equality of every fixed continuous local expectation in square and cylinder subsequential limits. A product of any fixed finite collection of observables is another bounded local observable; its enclosing slab has fixed thickness. In particular, for each fixed separation the two-observable products needed for the covariance bound are covered.

The limit order is important: fix the coupling, observable(s), and separation, then increase `w_k`. No convergence of finite-volume eigenvectors, no uniform-in-separation interchange of limits, and no plane-state uniqueness are needed to prove the bound in **every** square subsequential limit. Existence of subsequences follows from compactness of the spin configuration space. A separately given unique periodic state identifies that state with these limits.

### 4.5 Complete passage to the full OS Hilbert space

**Anchors:** O4-FV:194–200; O4-INTRO:65–80; O4-PRE:1199–1235; O3-TR:421–457.

#### Reflection positivity and the one-step operator

On every even untwisted torus, site reflection fixes two opposite rows. Conditioning on both fixed rows separates the two reflected interiors and gives a nonnegative reflected square. Link reflection has two crossing seams; expanding the ferromagnetic crossing kernels in positive tensor features gives reflection positivity there as well. This is consistent with the standard finite-torus reflection-positivity criterion [RP1]. Both properties, and translation/reflection invariance, pass to every local weak limit for continuous local functions. The finite-support approximation in §4.6 extends them to bounded measurable local functions.

Let `theta_0` reflect `t` to `-t`, and let `tau` move the support one step forward in time. On the bounded local algebra supported in `t>=0`, define

\[
 B(F,G)=\omega((\theta_0\overline F)G).
\]

Site reflection positivity makes this a positive semidefinite sesquilinear form. Reflection and translation invariance give

\[
 B(\tau F,G)=B(F,\tau G).
\]

To check that translation descends through the null space and is bounded, set

\[
 a_j=B(\tau^jF,\tau^jF),\qquad
 0\le a_j\le\|F\|_\infty^2.
\]

Cauchy–Schwarz in `B`, together with the symmetry just proved, gives

\[
 a_j^2\le a_{j-1}a_{j+1}\qquad(j\ge1).
\]

If `a_0=0`, this forces `a_1=0`. If `a_1>a_0>0`, the successive positive ratios cannot decrease, forcing unbounded geometric growth of `a_j`, a contradiction. Thus `a_1<=a_0`. Translation therefore induces a symmetric contraction on the quotient and extends to a self-adjoint contraction `T` on its completion.

For the link reflection `theta_(1/2)(t)=1-t`,

\[
 B(F,\tau F)
 =\omega((\theta_{1/2}\overline{\tau F})\,\tau F)\ge0.
\]

Thus `0<=T<=I`, and `T Omega=Omega` for `Omega=[1]`. This verifies positivity of the **one-step** operator, rather than only its square; there is no lost factor of two in the gap.

#### Centering, positive spectral measures, and density

For a bounded local half-space function `F`, put

\[
 \psi=[F]-\omega(F)\Omega.
\]

Then `psi` is orthogonal to `Omega`, and

\[
 \langle\psi,T^j\psi\rangle
 =\operatorname{Cov}_\omega(\theta_0F,\tau^jF).
\]

The reflected support lies in `t<=0`; the translated support lies in `t>=j`. Their edge separation is at least `j`. Applying the already proved slab bound to the **uncentered** functions therefore gives

\[
 0\le\langle\psi,T^j\psi\rangle
 \le\|F\|_\infty^2\alpha^j,
\]

where `alpha=exp(-log(2)/n)` in O4 and `alpha=exp(-log(2)/(M_0 L^N))` in O3. With other origin conventions a fixed slab-offset constant is harmless; it does not change the exponential rate.

The spectral theorem for the positive contraction gives

\[
 \langle\psi,T^j\psi\rangle
 =\int_{[0,1]}t^j\,d\nu_\psi(t).
\]

If `nu_psi([b,1])>0` for any `b>alpha`, then this is at least `b^j nu_psi([b,1])`, contradicting the upper bound as `j` tends to infinity. Thus every centered local vector is annihilated by the spectral projection onto `(alpha,1]`.

The local algebra is dense by the definition of the OS Hilbert space. Applying the bounded projection `I-|Omega><Omega|` shows that its centered vectors are dense in `Omega^perp`. Spectral projections are bounded, so the same exclusion holds on **all** of that complement:

\[
 \operatorname{spec}(T|_{\Omega^\perp})\subset[0,\alpha].
\]

A prefactor depending on the chosen local vector does **not** obstruct this argument: one first proves that each individual spectral projection vanishes, then uses its boundedness and density. No uniform comparison between supremum norms of representatives and OS norms is necessary. The result also rules out additional invariant vectors in this Hilbert space; vacuum uniqueness is a conclusion here, not an extra assumption needed for spectral exclusion.

“Full” includes every sector generated by the local half-space algebra, including invariant bond observables and arbitrary finite slabs. It does not mean all nonperiodic Gibbs representations or additional superselection spaces not generated by that algebra.

Finally, at spacing `a_N=L^(-N)`, every nonzero non-vacuum transfer spectral value has physical energy at least

\[
 -a_N^{-1}\log\alpha=\frac{\log2}{M_0}.
\]

Allowing transfer spectral value zero is consistent with the stated spectral inclusion and requires no inverse for `T`. This calculation does not by itself construct a continuum Hamiltonian.

### 4.6 Bounded measurable observables: two distinct arguments

**Anchors:** O4-FV:203–206; O4-PRE:1202–1209, 1224–1235; O3-TR:367–374.

**After a limiting state is fixed:** on the original finite support of a bounded measurable `F`, continuous functions are dense in the marginal `L^2` space. Project continuous approximants onto the closed complex disk of radius `||F||_infty` to preserve that supremum bound. Reflection/translation invariance transfers the approximation to reflected/translated copies, and ordinary Cauchy–Schwarz passes products and covariances to the limit. The constant 1 survives. Moreover,

\[
 \|[H]\|_{\rm OS}^2
 =\omega((\theta_0\overline H)H)
 \le\omega(|H|^2),
\]

so the same approximation proves OS density even if the defining algebra is taken to contain all bounded measurable local functions.

**To identify finite-volume measurable expectations:** weak convergence alone is insufficient. O3 correctly supplies a stronger fixed-cutoff domination. For a finite support `S`, at most `4|S|` bonds meet `S`. With `nu_S` the product sphere measure, the conditional density obeys

\[
 \frac{d\mu_S(\cdot\mid\sigma_{S^c})}{d\nu_S}
 \le e^{2\beta\,\#\{e:e\cap S\ne\varnothing\}}
 \le e^{8\beta|S|}.
\]

The first inequality follows by bounding both the conditional Boltzmann weight and the reciprocal normalizer. Marginals inherit it, as does the local weak limit. Product-measure `L^1` approximation therefore controls the expectation error uniformly over enclosing volumes.

This approximation is at **fixed cutoff and support**; the bound may depend strongly on both. Uniformity of the eventual volume/decorrelation estimates in `N` comes from the transfer inequalities, not from incorrectly asserting a cutoff-uniform density bound. Consequently cutoff-dependent local insertions with growing microscopic supports are permitted when they obey the displayed extent conditions; no support-dependent constant enters the final transfer estimate.

### 4.7 Conditional O3 reference-box calculation

**Anchors:** O3-TR:33–108. Input statements inspected, not their proofs: O3-PRE:21–50; O3-SHOOT:160–175, 269–292; O3-COMP:62–80. O3-SETUP:459 sets the support exponent `A=64`.

The choice

\[
 \upsilon/2<\chi<\min(1,\eta/(2\pi))
\]

is possible for sufficiently small positive `upsilon`. A fixed integer multiple of rounded dyadic sizes realizes

\[
 m_K\asymp L^{(1-\chi)K}
\]

while satisfying all finitely many rational denominator, evenness, minimum-period, and divisibility requirements. Shooting gives

\[
 X(\beta_K)\le C_H K^{C_H}L^{(2-\eta/(2\pi))K}.
\]

For the finite list of aspects, the shortest reference side is comparable to `L^((2-chi)K)`. Its ratio to `X(beta_K)` is at least a fixed inverse polynomial times

\[
 L^{(\eta/(2\pi)-\chi)K}.
\]

The exponent is positive. The preliminary exponential in this ratio dominates every stated polynomial in the microscopic periods and `beta_K`.

Here is the logarithmic comparison step explicitly. Let the scalar-stripped endpoint partition functions be

\[
 Z_i^\circ=\int e^{X_i}\Xi_i\,dq,
\]

with actual endpoint densities positive. Put

\[
 a=\|X_2-X_1\|_\infty,\qquad
 b=\sum_\lambda d_\lambda e^{2s_\lambda}.
\]

The nonempty supports and `A=64>=2` imply `a,b<=D_H v delta_K`: sum the per-site activity bound over the `v` sites. The integrated comparison gives

\[
 R:=\frac1{Z_1^\circ}\int e^{X_1}|\Xi_2-\Xi_1|\,dq\le e^b-1.
\]

Positivity of the complete endpoint densities then yields

\[
 e^{-a}(1-R)\le\frac{Z_2^\circ}{Z_1^\circ}\le e^a(1+R).
\]

When `v delta_K` is small, `R<1/2`, so taking logarithms costs only `C_H v delta_K`. This step does not assume that each signed activity or each summand of the covering expansion is positive.

Applying the logarithmic bound to terminal volumes `v` and `4v` gives at most `8 C_H v delta_K` for the difference of doubling defects; the two bulk scalars cancel separately because they are area-proportional with a common coefficient for each cutoff. Finally,

\[
 m_K^2\delta_K\le C L^{(\upsilon-2\chi)K}\longrightarrow0.
\]

Choosing one sufficiently large `K_0` and setting `M_0=m_(K_0)` proves exactly the conditional reference-box statement. This calculation neither proves preliminary mixing nor validates the endpoint comparison inputs.

### 4.8 O3 rectangular telescoping and uniformity

**Anchors:** O3-TR:309–365.

Let

\[
 \delta_k=64^{-1}2^{-2^k}.
\]

The aspect `(u_1/2,u_2)` controls `s_(n/2)(w)`. The aspect `(2u_1,u_2/2)` controls the analogous spatial tail with running length `w/2` and transverse circumference `2n`. For either tail,

\[
 s\le e^{\delta_k}-1\le2\delta_k
 =\frac1{32}2^{-2^k},
\]

since `delta_k<=1/128`. Comparing `(n,w)` with `(2n,w)` through their common infinite-time cylinder costs at most four times the first tail times `||F||_infty`. Comparing `(2n,w)` with `(2n,2w)` costs at most four times the second. Thus one simultaneous doubling costs at most

\[
 \frac14\|F\|_\infty\,2^{-2^k}.
\]

The fixed support still fits all subsequent rectangles. Since

\[
 \sum_{j\ge k}2^{-2^j}\le2\,2^{-2^k},
\]

summation gives, for the unshifted comparison, even the explicit permissible bound

\[
 |\mu_{n,w}(F)-\omega(F)|
 \le\frac12\|F\|_\infty\,2^{-2^k}.
\]

The paper only claims unspecified `C,c>0`, so its bound has ample slack. Naming the limit `omega_(beta_N)` uses the separately supplied periodic-limit identification at fixed `N`. The constants just computed do not depend on `N`, `k`, or the number of observed sites.

### 4.9 Shifted closing and the tilted periods

**Anchors:** O3-TR:331–334, 376–395, 465–488.

A spatial shift acts by a unitary, positivity-preserving permutation `U_s` on row configurations. It commutes with `T_w`. Simplicity of the ground eigenvalue makes `U_s Omega_w` a scalar multiple of `Omega_w`; positivity and normalization force that scalar to be 1. Therefore the vacuum contributions to the closing traces are exactly

\[
 \operatorname{Tr}(P_wU_s)=1,\qquad
 \operatorname{Tr}(A_FP_wU_s)=\omega_w(F).
\]

For `R_j=T_w^j-P_w`, trace duality and unitarity give

\[
 |\operatorname{Tr}(R_jU_s)|\le s_j(w),\qquad
 |\operatorname{Tr}(A_FR_jU_s)|\le\|F\|_\infty s_j(w).
\]

Writing the twisted denominator as `1+epsilon`, `|epsilon|<=s_n`, gives

\[
 |\mu^{(s)}_{n,w}(F)-\omega_w(F)|
 \le\|F\|_\infty\frac{s_{n-r}+s_n}{1-s_n}
 \le4\|F\|_\infty s_{n/2}(w),
\]

provided `s_n<1/2`. This follows even from the weakened `k=0` bound:

\[
 s_n\le s_{n/2}\le e^{1/128}-1<0.008<1/2.
\]

There is no application of purity, spectral positivity, or reflection positivity to `T_w^n U_s` itself. The twisted operator need not be positive semidefinite. The actual partition integral is positive, and the comparison additionally gives an explicit denominator bounded away from zero.

The support-lift condition permits a seam outside the insertion slab. For period lattice generated by `(w,0)` and `(s,n)`, a rectangle of time extent at most `n/2` and spatial extent at most `w/2` is injective modulo that lattice: a nonzero time-period coefficient is incompatible with the first extent bound, and a remaining nonzero spatial-period coefficient is incompatible with the second. Thus the same lifted local function can be compared on the cylinder, ordinary torus, and plane.

The difference between shifted and unshifted torus expectations is at most six times `||F||_infty` times the half-period tail. Combining with §4.8 gives, for example, a common permissible volume bound with `C=1` and `c=log(2)` for both closing conditions. The text's generic constants are therefore valid uniformly in the shift.

For the tilted torus,

\[
 a=M(3,4),\quad b=M(-4,3),\qquad
 3a-4b=(25M,0),\quad a-b=(7M,M).
\]

The integer basis-change matrix has determinant `3(-1)-(-4)(1)=1`. Both bases have area `25M^2`. The time height is `M`, the spatial circumference is `25M`, and the shear is `7M` (up to the immaterial sign convention for closing). Multiplication by `L^N` makes all microscopic periods and shifts integral. Reflection changes no required size bounds. A fixed compact physical support has bounded coordinate diameters, so for all sufficiently large `k` it satisfies the two extent conditions uniformly in `N`. No further nonrectangular trace criterion is being assumed.

## 5. Active counterexample search and boundaries of valid reuse

The following counterexamples target tempting **weakenings** of the proof. They do not satisfy all hypotheses of the audited nearest-neighbor sphere models.

### 5.1 Positive kernels and simple Perron eigenvalues in one direction are insufficient

On a two-state row space let `P` be projection onto the constant vector and set

\[
 K_w=P+e^{-16/w}(I-P).
\]

Every `K_w` is trace class, positive semidefinite, has strictly positive matrix entries, and has a simple top eigenvalue 1. Nevertheless, for `Z(n,w)=Tr K_w^n`,

\[
 Z(n,w)=1+e^{-16n/w},\qquad
 \Delta(n,n)=3\log(1+e^{-16})\approx3.3760551\cdot10^{-7}<2^{-10}.
\]

The square defect is the same at every dyadic size, while `lambda_2(w)=exp(-16/w)` tends to 1. Taking initial `n=4` and `w=128` gives

\[
 e^{-16/128}\approx0.882497>
 e^{-(\log2)/4}\approx0.840896.
\]

The purported generalization of the width-gap conclusion is false. The exact missing property is the other-direction positive trace: here

\[
 q(n,n)=2\log(1+e^{-16})-\log(1+e^{-8})<0.
\]

Both audited papers establish that property for the actual model. The rectangle identities alone do not establish it.

### 5.2 A uniform cylinder gap does not identify square-torus limits

Take row states `{0,1}^w`, of cardinality `D=2^w`, and let

\[
 T_w=aI+(1-a)P_w,\qquad a=3/4,
\]

where `P_w` averages all row states. The matrix is strictly positive, positive semidefinite, and has simple top eigenvalue 1 and width-independent gap `-log a`. But

\[
 s_w(w)=(2^w-1)a^w\longrightarrow\infty.
\]

This is not merely an abstract trace obstruction. Let `F` be the indicator that the first bit agrees between two adjacent time rows, a fixed two-site observable. Its infinite-time cylinder expectation is

\[
 \omega_w(F)=\frac{1+a}{2}=\frac78.
\]

Writing `B_(s,s')=(T_w)_(s,s') 1_{s_1=s'_1}`, one has `Tr B=D a+(1-a)` and `<Omega,B Omega>=(1+a)/2`. Splitting `T_w^(w-1)` into its two eigenspaces gives exactly

\[
 \mu_{w,w}(F)
 =1-\frac{(1-a)(1-a^{w-1})}{2[1+(2^w-1)a^w]}
 \longrightarrow1.
\]

Thus even a local expectation differs in the two limits despite the uniform gap. The family is nonlocal in the spatial row and does not supply the second-direction hypotheses. The audited proof avoids this error precisely through the half-period trace-tail estimate.

### 5.3 Pointwise positivity is not positive semidefiniteness

The symmetric matrix

\[
 K=\begin{pmatrix}1&2\\2&1\end{pmatrix}
\]

has strictly positive entries and a simple positive Perron eigenvalue, but eigenvalues `3,-1`. For odd `n` its purity defect is negative:

\[
 2\log(3^n-1)-\log(3^{2n}+1)<0.
\]

It does not have the spectral or reflection-positivity properties used here. Both papers' tensor-feature proofs, and the restriction to ferromagnetic coupling, address this rather than confusing the two meanings of positivity.

### 5.4 Degenerate ground states and sector-restricted traces

If the top eigenvalue has multiplicity `g>=2`, then `t_1<=1/g`, so `p>=log g`. In particular a small full-trace test with `Delta>=2p` cannot hide a degenerate leading state. A model with a genuine extra invariant sector cannot simply pass this test by choosing one of its vacua.

However, replacing the full trace by a selected-sector trace can hide it. For `T=diag(1,1,a)`, a trace restricted to the first coordinate is identically 1 and has defect zero, while the gap on the complement of the chosen first vacuum is zero. Actual full traces and the specified local OS representation are essential.

Likewise a correlator confined to the `a`-eigenspace of `diag(1,a,b)` with `0<a<b<1` cannot detect the slower `b`-sector. The use of all local observables and density, not just the spin two-point function, is what repairs that issue here.

### 5.5 Measurability, normalization, and endpoint cases

- Weak convergence does not imply convergence of every bounded measurable expectation: `delta_(1/j)` converges weakly to `delta_0`, but the indicator of `{0}` has expectations 0 and 1. O3's fixed-support density domination and O4's post-limit marginal approximation are legitimate ways around the relevant versions of this problem.
- Multiplying every partition function by a common non-area scalar `c` changes the doubling test by `3 log c`. Only a consistently area-proportional additive contribution to `log Z` cancels. One cannot manufacture a small defect by changing the normalization arbitrarily.
- Compactness alone does not give a finite trace. The summable feature-diagonal calculation in §4.1 is a genuine necessary justification of the claimed trace-class property, not decorative wording.
- Rank-one transfer (`beta=0`), `d=0`, zero-thickness insertions, complex insertions, and arbitrarily large but finite slab/spatial supports all satisfy the stated bounds. None produced an endpoint counterexample.

## 6. Minimal changes warranted in the 2D exposition

No theorem constant needs to be weakened. If revising the preprints separately, the minimal useful changes are:

1. In O4-FV:177–188, write: “For `k>=1`, put `w=2^k n`, so `w/2=2^(k-1)n`; for each fixed local insertion take `k` sufficiently large that `r<=w/2`.” Then use the displayed half-period estimate. This is the only actual domain/index correction found.
2. Beside O4-FV:183–185 and O3-TR:282–295, include the exact normalized residual-trace formula from §4.4.
3. Beside O4-FV:194–200, cite the already present discrete OS construction and spell out centering plus bounded spectral projections. O3's longer version is correct; its one-step contraction sentence can be expanded as in §4.5.
4. In O3-TR:440–443, mention the two fixed rows of an even finite torus before taking the limit.
5. Keep the distinctions “full unprojected trace,” “both coordinate transfers,” “local OS representation,” and “fixed-cutoff approximation” explicit in any subsequent reuse.

These are recommendations in this audit only. The preprints and Lean library were not edited.

## 7. Verification record and limits of certification

- Applicable ancestor and nested `AGENTS.md` instructions were searched for; none were found for the audited paths or this report destination. Existing unrelated repository changes were left untouched.
- The two main source files were read with line numbers. Surrounding files were read only to identify conventions, the discrete OS construction, and the statements of explicitly invoked O3 inputs.
- Two authorized read-only subagents independently cross-checked (i) scalar/trace/doubling hypotheses and (ii) slab/volume/OS conclusions. Their findings were checked against the derivations above; they did not edit repository files.
- Exact rational threshold checks and an in-memory Python smoke test were run. With seed `20261009`, 10,000 finite nonnegative spectra were tested; 1,337 were in the `p<=1/4` regime. No violation of the concentration or squaring inequalities was found. The proofs above, not this numerical test, establish the inequalities.
- The one-direction and growing-multiplicity counterexamples were evaluated explicitly. At width 64, the latter's adjacent-bit square expectation is approximately `0.9999999999993284`, versus the cylinder value `0.875`.
- **[RP1]** Marek Biskup, *Reflection Positivity and Phase Transitions in Lattice Spin Models*, `arXiv:math-ph/0610025v2` (April 27, 2009), §5.1, especially Lemma 5.2, Corollary 5.4, and Lemma 5.5. The author's full text was consulted as an external cross-check of the site/bond finite-torus reflection-positivity construction. It is not a source for the audited finite-volume recursion or a certification of the preprints' upstream estimates.

**Bottom line for the completed 2D assignment:** the conditional finite-volume-to-full-OS-gap implication is sound for the specified O(4)/O(3) lattice models, with a harmless initial-index correction and completed exposition as recorded above. This does not validate the small-box inputs, a continuum construction, or the rest of Family 215.

## 8. Short follow-up: new manuscript, Sections 3–5 only

**Scope added at the user's request after completion of the 2D audit.** Source: `research_notes/yang_mills_2026_10_09/finite_volume_criterion.tex`. The following line anchors refer to SHA-256 `e51402d8a4b950c8b9eef9cfe4a3ca29b05b843e1c15f218d13f94bed887957c`, including the parent's two newly applied limit-passage fixes. Sections 1–2 were used only for hypotheses; Sections 6 onward and the gauge-theory interface are not certified here.

- **Section 3, lines 133–209 — PASS.** At each of the six preparation updates, `D_i x=y^(j)` is exactly correct. The accumulated quadratic coefficients are `4,44,188`; the unsquared bounds `delta,3delta,5delta,9delta` are legitimate at `delta<=1/2048`. Their squared weighted sum is `32+144+200+324=700`. No transverse-size monotonicity is smuggled into the argument.
- **Section 4, lines 211–229 — PASS.** `1024 epsilon_*=1/2` preserves the threshold. Telescoping with time first gives `8p_i<=delta_k`, hence the printed `delta_k/4` eigenvalue bound and root `2^(-1/n)`. The zero-defect/rank-one case is valid.
- **Section 5, lines 269–294 — PASS after the visible fixes.** The explicit `k>=1` now makes the half-period admissible and controlled. Passing continuous local products first, then using norm-preserving marginal `L^2` approximation in the limiting state, repairs the measurable-observable passage. The torus/cylinder constant 2 and covariance prefactor 1 remain correct.

### Remaining hypothesis-level correction: identify the OS time translation

**Lines 247–250 do not literally supply the identity used at 296–297.** Merely admitting *a positive contraction* in the reflected Hilbert space does not identify it with time evolution, ensure `T Omega=Omega`, or make its matrix elements reflected time correlations. Specify that this is the **canonical one-step OS translation**. Suitable minimal wording is:

> The limiting states are time-translation and reflection invariant. With the OS form `B(A,B)=omega((Theta conjugate(A))B)` on the admitted positive-time local algebra, `Omega=[1]` and `T[A]=[tau_1 A]`; this operator extends to a positive self-adjoint contraction.

Then `T Omega=Omega` and, for `v_A=[A]-omega(A)Omega`,

\[
 \langle v_A,T^s v_A\rangle
 =\operatorname{Cov}_\omega(\Theta A,\tau_s A).
\]

The positive spectral-measure and dense spectral-projection argument at 300–306 is then correct, with no additional estimate. This is an **interface-definition omission**, not a failure of the intended canonical-transfer theorem. To see why the literal weaker assumption is insufficient, an independent-spin model has `Z=1` and rank-one finite transfer operators; on its nontrivial site-reflection OS space, the arbitrary choice `T=I` is also a positive contraction but violates the asserted gap. It is excluded precisely by requiring the canonical time translation.

**Minor regularity qualification:** lines 233–234 should specify compact **metrizable** local spaces with Borel probability measures, or equivalent sequential-compactness/regularity hypotheses, for the assertions at 285–291. In the gauge-restricted version, Haar averaging preserves the required `L^2` approximation when the marginal is gauge invariant. These are standard properties of the intended compact-Lie-group setting, but should be part of the abstract interface rather than inferred from the word “compact” alone. Torus insertion formulas are understood for a support fitting the period, with `w>r`; the proof uses the stronger `r<=w/2`.

**Follow-up conclusion:** no correction to the four-direction algebra, constant 700, threshold `1/2048`, or gap rate is required. Apart from the already applied two limit-passage fixes, the remaining substantive wording correction is the explicit canonical OS-translation interface. The main manuscript was not edited by this reviewer; this remains a limited review, not a full Family 215 audit.

**Revision confirmation — October 9, 2026:** Verified manuscript SHA-256 `22a3c353e7e1abf6a1abd1c994b7a1c38ad6d118411abfbbc058efc2970b36a4`. Lines 233–259 now supply the compact-metrizable/Borel, invariance, support-fit, canonical OS-translation, and gauge-averaging hypotheses requested above. The conjugate-linear `Theta` convention and matrix-element identity are consistent. The `k>=1` and continuous-first approximation fixes remain at lines 281–303. All reported Section 3–5 issues are resolved; no further correction is required within this limited conditional review. The main manuscript was not edited.

**Final confirmation:** For the verified manuscript revision `22a3c353e7e1abf6a1abd1c994b7a1c38ad6d118411abfbbc058efc2970b36a4`, the patched canonical OS interface and compact-metrizability assumptions resolve the reported issues. No outstanding correction remains within the reviewed Sections 3–5.
