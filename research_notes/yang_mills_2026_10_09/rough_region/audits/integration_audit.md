# Integration and excess-energy audit

**Date:** October 9, 2026. **Verdict:** independently confirmed the principal Hessian and change-of-measure arguments. No additional substantive error found in the corrected draft's §§4, 7, and 8. The generic-positive-weight truncation by one has been removed correctly; the corrected distinction between edited-output dependence and copying the full exterior is also correct.

**Reviewed:** `rough_region_replacement.tex`, especially `lem:minimizer`, `thm:excess`, `lem:integrated`, `thm:bad`, and `cor:animals`; the constants needed from §§2, 5–6; and README §§2–4. Reviewed snapshot SHA-256: `cdd66db6eb3710692e3285fb22fc9c9d024cf330d3d7551039c38bd6806a7e7e`. This is a bounded analytic audit, not certification of a continuum or renormalization argument.

## 1. Fixed-J integrated inequality: confirmed

Write product probability Haar as `dξ dz`, where `ξ=x_J`. Suppose the jointly measurable probability kernel has edited-link density `k_z(ξ,η) ≤ M`, and

\[
 E(\xi,z)-E(\eta,z)\ge h
\]

for almost every source/kernel-output pair with source in `A`. The bound is needed only on those pairs; `h` may be negative. For the stated model `H≥1` (the measure argument only needs `H≥0`). Set

\[
 Z_Q=\int e^{-HE(x)}Q(x)\,dx\in(0,\infty),\quad
 c_{A,z}(\eta)=\int 1_{A_z}(\xi)k_z(\xi,\eta)\,d\xi.
\]

Tonelli and the pointwise energy inequality give exactly

\[
 \begin{aligned}
 I_Q(A)&:=Z_Q^{-1}\int_A e^{-HE(x)}(KQ)(x)\,dx\\
 &\le {e^{-Hh}\over Z_Q}\int e^{-HE(\eta,z)}Q(\eta,z)
                   c_{A,z}(\eta)\,d\eta\,dz\\
 &\le M e^{-Hh},
 \end{aligned}
\]

because `c_{A,z}(η) ≤ M Haar_J(A_z) ≤ M`. This proves the draft's lemma for nonnegative `Q`, not merely strictly positive `Q`.

- **Normalization:** with any other denominator `Z`, the final bound is `M exp(-Hh) Z_Q/Z`, not automatically `M exp(-Hh)`. The draft uses the matching denominator.
- **Frozen exterior:** no exterior variable is edited or independently resampled. The calculation first integrates old `ξ` at the *same* `z` as the target. It works separately at every boundary with finite positive conditional normalizer.
- **Exterior-dependent constants:** if the bounds are `M(z),h(z)`, the global conclusion is at most `∫ M(z) exp[-Hh(z)] Haar_J(A_z) π_Q(dz)`, where `π_Q` is the **Q-weighted Gibbs exterior marginal**, not exterior Haar. A uniform estimate follows from uniform constants. If energy control is available only on an exterior event `C`, then `I_Q(A∩C) ≤ M exp(-Hh) π_Q(C)`.
- **Many-to-one entropy:** the incoming column mass `c_A`, rather than an inverse map or Jacobian, controls the loss of information. Arbitrary measurable source-dependent cap centers are allowed for fixed `J`; there is no extra multiplicity charge once the stated density bound holds.
- **Reference measure matters:** the density is against Haar on the edited links, not on independent plaquettes, a gauge quotient, or the entire output including its fixed exterior. A deterministic reset of a continuous SU(2) variable is singular and has no finite such density. Likewise, leaving some coordinates in an enlarged `J` deterministically unchanged does not provide a full `J`-density.

### Probability versus replacement numerator

For strictly positive `Q`,

\[
 I_Q(A)=\mathbb E_{\mu_{H,Q}}
       \left[1_A\,{KQ\over Q}\right],
\]

not generally `μ_{H,Q}(A)`. It is that probability when `Q=1`, when `Q` depends only on the frozen exterior, or more generally when `KQ=Q` on `A`. The sufficient one-sided comparison is

\[
 Q(x)\le C(KQ)(x)\quad(x\in A).
\]

The draft's pairwise condition `Q(x)≤exp(Ln)Q(y)` implies this with `C=exp(Ln)`, hence the stated weighted probability bound. The reverse comparison does not suffice. For nonnegative `Q`, the same proof uses the inequality directly, without dividing by `Q` on its zero set.

A literal replacement numerator must evaluate **one fixed function** `Q` at the target. If an “old support” label changes with the source and produces `Q_{label(x)}(y)`, separate the labels and control their weights/normalizers; the displayed lemma does not silently identify them with a single `Q(y)`.

**Two explicit negative controls.**

1. In the actual one-link Wilson conditional problem with identity exterior, `E_J(U)=6s(U)`. Choose `Q(U)=exp[6Hs(U)]`; the reweighted law is Haar. Take `A={s(U)≥1}` and replace uniformly into `B={s(U)≤1/2}`. Then `Haar(A)=1/2`, the energy drop is at least `3`, and the kernel has finite density `M=1/Haar(B)` independent of `H`. Thus `μ_{H,Q}(A)=1/2` cannot be bounded by `M exp(-3H)` for large `H`. The replacement-numerator bound remains valid.
2. To check the removed `min{1,...}`, partition a Haar space into `B,A` of masses `b=.01,1-b`. Set `E=0` on `B`, `E=h` on `A`, `exp(-Hh)=.1`, `Q=10000` on `B`, `Q=1` on `A`, and replace uniformly into `B`. Then
   `I_Q(A)=.99·.1·10000/(.01·10000+.99·.1)=9.890208693...>1`, while `M exp(-Hh)=10`. These are strictly positive weights. Such cells can be taken in SU(2); this example tests the abstract lemma, not continuity of a Wilson action.

The entropy factor itself cannot be omitted: with the same two-cell construction but `Q=1`, `b=1/4`, and `exp(-Hh)=.1`, the event probability is `3/13>.1`.

## 2. Conditional-minimum Hessian and cap tail: confirmed

For the fundamental SU(2) trace, eigenvalues `exp(±iθ)` give the **exact**, not asymptotic, identity

\[
 s(g)=1-\cos\theta=\tfrac12\|I-g\|_{\rm op}^2.
\]

All plaquettes touching `J`, including boundary-crossing ones, belong in `E_J`; all other energy cancels. Fix a minimizer `V` of `E_J(·,z)`, put `X_e∈su(2)`, `a_e=||X_e||op`, and use `U_e(t)=V_e exp(tX_e)`. A forward or reversed factor has first- and second-derivative norms at most `a_e,a_e²`. The product rule therefore gives

\[
 |s(U_p(t))''|\le\Big(\sum_{e\in\partial p\cap J}a_e\Big)^2.
\]

Since every plaquette has four distinct links and each link has six incident plaquettes,

\[
 |E_J''(t)|\le\sum_p q_p\sum_{e\in\partial p\cap J}a_e^2
             \le24\sum_e a_e^2.
\]

**The stationary-variation assumption is satisfied:** the draft minimizes over the entire unrestricted product `SU(2)^J`. For every such simultaneous path, both positive and negative `t` are admissible, so the derivative of the **total** `E_J` at zero vanishes. Individual plaquette derivatives need not vanish; uniqueness or a positive Hessian is unnecessary. Taylor's integral remainder gives

\[
 E_J(Ve^X,z)\le e_*(z)+12\sum_e a_e^2
                    \le e_*(z)+12n\rho^2.
\]

This argument must not be transferred without modification to a minimizer constrained by a hard admissibility/sector condition, a boundary of a gauge-fixing domain, or a cap that exits the allowed state space.

**Repeated appearances:** periods at least four exclude them here. Otherwise occurrences, not just the set `∂p∩J`, must be counted. For example, with `U(t)=exp(itσ₁)` and `V=iσ₃`, the word `UVU^{-1}V^{-1}` has energy `1-cos(2t)` and second derivative `4` at zero; counting the variable `U` only once would incorrectly give the bound `1`.

The geodesic radius is the generator operator norm, not chordal radius. Identifying SU(2) with unit quaternions gives uniform sphere measure as Haar: multiplication is orthogonal and preserves that measure. Its polar area element gives

\[
 b(\rho)={2\over\pi}\int_0^\rho\sin^2\theta\,d\theta
 ={\rho-\sin\rho\cos\rho\over\pi}
 \ge {\rho^3\over6\pi}\ge {\rho^3\over24},\quad0<\rho\le1,
\]

using `sin θ≥θ/2` and `π<4`. Thus the conditional partition function is at least `b(ρ)^n exp[-He_*(z)-12Hnρ²]`. Bounding the event's Haar mass by one yields

\[
 \Pr_H(E_J\ge e_*(z)+h\mid z)
 \le\min\{1,b(\rho)^{-n}e^{-Hh+12Hn\rho^2}\}.
\]

Taking `ρ=H^{-1/2}`, `H≥1`, proves exactly the draft's exponent

\[
 -Hh+n(12+\log24+\tfrac32\log H).
\]

**Boundary uniformity is genuine but only relative to the minimum.** No measurable selection of minimizers is used: the conditional partition bound holds for each `z` separately, while `e_*(z)` is continuous. The frustrated one-link example has `e_*=6` and all configurations minimize. It refutes absolute-energy or bad-plaquette elimination conclusions from this theorem, not the theorem itself.

If a measurable covariant minimizer-cap kernel is separately desired, a Borel minimizer selector exists by nested finite closed covers of the compact argmin sets; intersection tests use minima over fixed compact sets and are Borel. For a compact symmetry group preserving `J`, energy, and Haar, average the base kernel as `Kbar_z=∫ g_* K^0_{g^{-1}z} dg`. This preserves the density and energy bounds and gives covariance. Averaging only the target while ignoring the transformation of the exterior is not the same construction. None of this selection machinery is needed for `thm:excess`.

## 3. Compatible-boundary application and counting: confirmed

The actual forest definition controls **every frozen touched edge**, including non-tree chords, in the tree frames. It is not merely a condition on the tree edges, which are automatically trivial in those frames. Given the root frames, cap samples have product density at most `b(ρ)^{-n}`; averaging normalized Haar root frames adds no entropy factor. The updated full-exterior-copy wording is accurate.

For `q_p` edited edges on a touched plaquette, the explicit kernel gives

\[
 \|I-y_p\|_{\rm op}\le q_p\rho+(4-q_p)\eta_J(z).
\]

Consequently `η_J≤ρ` implies `E_J(y)≤8|P(J)|ρ²≤48nρ²`; at `η_J=0`, incidence gives `E_J(y)≤(ρ²/2)Σ_p q_p²≤12nρ²`. At `ρ=H^{-1/2}`, at least `k` plaquettes of curvature greater than `p/√H` imply

\[
 H(E(x)-E(y))\ge kp^2/2-48n.
\]

With `M≤(24H^{3/2})^n`, this proves the stated exponential `exp[-kp²/2+n c_H]`, `c_H=48+log24+(3/2)log H`:

- with truncation by one for the raw Wilson conditional probability and the joint event `A_{J,k}`;
- **without** that truncation for the general replacement numerator;
- with `c_H` replaced by `c_H+L` for the reweighted probability under the additional pairwise `exp(Ln)` stability assumption.

For exactly flat compatible data, replace `48` by `12`. The no-new-rough-plaquette assertion follows from the **pointwise** output curvature and `p≥4`, not from the aggregate energy bound alone. For `k≥1`, the event is empty when `p/√H≥2`.

Writing `S` for the draft's packing parameter `s` to distinguish it from `s(g)`,

\[
 k\ge n/S,\quad p^2\ge4S c_H
 \quad\Longrightarrow\quad -kp^2/2+nc_H\le-np^2/(4S).
\]

This is correct for raw probability and the literal replacement numerator. A corresponding weighted probability assertion must use `c_H+L` in the absorption budget.

The sharing-plaquette adjacency degree is at most `6·3=18`. A deterministic spanning-tree traversal of a rooted connected set of size `n` has length `2(n-1)` and determines its visited set. Therefore the count is at most `18^{2(n-1)}`. Summing the resulting union bound gives exactly

\[
 \sum_{n\ge1}18^{2(n-1)}e^{-\kappa n}
 ={e^{-\kappa}\over1-18^2e^{-\kappa}},\qquad\kappa>2\log18.
\]

Finite volume only shortens the sum. No independence is used. This covers only the listed events `A_J∩{compatible outside_J}`. It does not construct a partition or cover of arbitrary bad configurations, bound incompatible exteriors, or remove the need for the energy-density assumption.

## 4. Essential negative controls for extending the result

**One witness cannot pay for all edited links.** The draft's actual-link counterexample is correct: put one link at `-I` and all others at identity. Precisely six plaquettes have energy two. Any connected `J` containing that link has `E_J=12`, independently of `n`, and its identity exterior is exactly compatible. No replacement can lower this nonnegative energy by more than `12`. Arbitrarily padding `J` therefore cannot establish an energy gain proportional to `n`. For any strictly violated proposed inequality, continuity also gives a positive-Haar neighborhood of counterexamples; the point example is not the only issue.

**Disjoint link edits can share energy terms.** In an otherwise identity four-dimensional lattice, take two consecutive edges of one plaquette to equal `g=iσ₃`. The full energy is `12`. Replacing either edge separately by `g^{-1}` lowers it to `10`; replacing both restores energy `12`. The other incident plaquette energies are unchanged. Thus the two individually computed gains `2+2` do not add. Small cap neighborhoods preserve a strict failure, so deterministic maps are not essential to this counterexample.

For disjoint blocks resampled once each, a product or sequential kernel with conditional density bounds `M_i` has joint density at most `∏M_i`. Additive energy gain additionally requires disjoint affected-plaquette sets, or gains proved along **every actual intermediate state** so that they telescope. Gains checked only against the common original configuration are insufficient.

**Adaptive support selection has entropy too.** In `N=100` independent Haar bits with `E(x)=Σ_i x_i` and `exp(-H)=.01`, select the first `1` and reset only that bit. Every selected fixed-singleton kernel has density `M=2` and lowers energy by one, but

\[
 \Pr(\exists i:x_i=1)=1-(100/101)^{100}=0.630288787\ldots>0.02.
\]

The invalid `0.02` is what applying a fixed-J bound to the adaptive support without accounting for its possible locations would produce. Equal-Haar cells in SU(2) give the same abstract example. Freeze supports termwise and count them, or prove a genuine aggregate incoming-density bound. Conditioning additionally on “this J was selected” changes the conditional Gibbs law and is not licensed by the raw fixed-exterior formula.

## 5. Independent checks and scope

In-memory Python diagnostics, seed `20261009`, passed:

- Complete `4^4` lattice enumeration: 1,024 links, 1,536 plaquettes, four distinct links per plaquette, six incidences per link, adjacency degree 18.
- 80 quaternion product-rule second-derivative tests, with arbitrary bases and frozen links: every plaquette and total Hessian bound passed. Maximum observed `|E_J''|/(24Σ||X||²)` was `0.110068`; 80 flat-minimum cap tests also passed.
- The padded one-defect example at `n=100` had energy `12`; the overlapping-edit energies were exactly `(12,10,10,12)`; 50 random editable links in the frustrated boundary gave energy `6` to error below `1.8e-15`.
- 10,001 radii in `[10^-6,1]` passed the cap lower bound; minimum observed `b(ρ)/ρ³` was `0.173590706`, versus the asserted `1/24`.
- The positive-Q and adaptive-support negative controls above were evaluated directly.

These computations are diagnostics, not substitutes for the analytic proofs above. No imported bad-event probability, mixing theorem, mass-gap assertion, or bound on compatibility probability was used. No build or repository test command that writes other files was run; only this audit file was written.

## Addendum: exact one-link unavoidable baseline

**Confirmed algebraically.** Use the draft's six frozen three-edge transports `S_j`, all oriented from the edited link's source to its target, so that `E_J(U)=Σ_j[1−Tr(U S_j^{-1})/2]`. Identify `U,S_j` with unit quaternions `u,s_j∈S³⊂R⁴`. The conventions are

\[
 \tfrac12\operatorname{Tr}(US_j^{-1})=u\cdot s_j,
 \qquad \|U-S_j\|_{\rm op}=\|u-s_j\|_{\mathbb R^4}.
\]

The quaternion norm includes all four real coordinates; it is **not** the unnormalized matrix Frobenius norm, whose square is twice as large. For `B=Σ_{j=1}^6 s_j` and `b=|B|∈[0,6]`,

\[
 E_J(u)=6-u\cdot B,\qquad e_*=6-b.
\]

If `b>0`, the minimizer is `u=B/b`; if `b=0`, every link value minimizes. The pairwise identity gives

\[
 D:=\sum_{i<j}\|s_i-s_j\|^2
   =6\sum_j\|s_j\|^2-\Big\|\sum_j s_j\Big\|^2
   =36-b^2,
 \qquad
 e_*={D\over6+b},\qquad {D\over12}\le e_*\le {D\over6}.
\]

There is no singular case: `6+b≥6`, including when `D=0`. Under a gauge change every staple has the same left/right endpoint action, an orthogonal action on `R⁴`; hence `b`, `D`, and `e_*` are gauge invariant. Equivalently,

\[
 D=\sum_{i<j}\|I-S_iS_j^{-1}\|_{\rm op}^2
   =2\sum_{i<j}s(S_iS_j^{-1}),
\]

where each product is a **closed, entirely frozen** loop. Thus `D` is an explicit boundary-defect label controlling the one-link minimum, not an assumed probabilistic estimate. Checks: identical staples give `(D,e_*)=(0,0)`; five `+I` and one `−I` give `(20,2)`; three of each give `(36,6)`.

**Count qualification:** restricting the rough-count statements to positive integer `k` is correct. At `k=0` the count condition is automatic, and the joint event is compatibility alone, so it need not be empty when `p/√H≥2`.
