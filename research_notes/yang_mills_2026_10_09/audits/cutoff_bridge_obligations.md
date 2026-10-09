# Cutoff-bridge obligations: O(3), its O(4) inputs, and 4D Wilson SU(2)

**Audit date:** October 9, 2026. **Repository snapshot:** `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

**Scope/status.** This is a statement/dependency audit, not certification of the analytic proofs or a Yang–Mills proof. Finite-volume spectral algebra is excluded: the small-test threshold is only an interface to that separate audit. “M3” means a statement with a proof supplied in the O3 manuscript, possibly using the listed imports; “M4” means an imported O4 manuscript estimate. Neither designation means Lean-verified.

**Exact locator convention.** All paths are relative to `/home/rou/src/math`; aliases below include `build`:

- `O3` = `preprints/The-canonical-massive-continuum-limit-of-the-two-dimensional-O3-model-October-4-2026/build`
- `O4` = `preprints/Sharp-mass-bounds-for-the-two-dimensional-O4-model-September-23-2026/build`

The O3-to-O4 citation translation is itself explicit in `O3/reference-locators.tex:32-138,139-208,234-309`. A locator such as `O3/sections/trace.tex:33-108` therefore specifies an exact repository file and source-line range.

## 1. The actual quantitative bridge

The dependency chain is

\[
\text{preliminary doubling estimate}
+\text{calibrated, endpoint-matched exact RG}
+\text{integrated density comparison}
\Longrightarrow\text{one reference test valid at every finer cutoff}.
\]

It is **not** “a gap at one bare coupling plus asymptotic freedom.” The following are the load-bearing quantitative statements.

### 1.1 Preliminary mixing must beat a particular exponential scale — M3

For some fixed \(\eta>0\),
\[
X(b)=C e^{(4\pi-\eta)b},
\qquad
|\operatorname{Cov}(F,G)|\le
 C(1+b+|A|+|A'|+d)^{p_{\rm mix}}
 \mathcal L(F)\mathcal L(G)e^{-cd/X(b)}.
\]
Here \(\mathcal L(F)=\|F\|_\infty+\max_x\operatorname{Lip}_xF\). The constants work for **every** assignment \(0\le\beta_e\le b\), including deleted bonds, on unpinned rectangular tori with both sides at least \(CX(b)\), and on every finite free subgraph. For each fixed aspect bound, homogeneous even rectangles also satisfy
\[
0\le\Delta_b(n,w):=4\log Z_b(n,w)-\log Z_b(2n,2w)
 \le C(1+b+n+w)^{p_{\rm mix}}e^{-c\min(n,w)/X(b)}.
\]
The polynomial exponent is not numerically specified in O3. The associated uniqueness assertion concerns the **periodic local limit**, not an asserted classification of all Gibbs states. **Locators:** `O3/sections/preliminary.tex:10-49` (`prop:preliminary`), `924-943`.

The strict saving has a specified mechanism, not a supplied numerical value:

- Pinned-cell iteration: \(\log(R_*/R)\le4\pi h+C_D\sqrt{B\log B}\), reaching stiffness \(B^{-D}\), uniformly in pins and weakened bonds; premise \(\log(2+S)\le16B\) must hold at every proposed step.
- Initial square: \(S=\lfloor e^{2\pi bu}\rfloor\), stiffness at most \(b(1-3u/4)\), for one fixed sufficiently small \(u>0\).
- Total logarithmic length: \((4\pi-\pi u)b+o(b)\); one may take \(\eta=\pi u/2\) after polynomial enlargements.

**Locators:** `O3/sections/preliminary.tex:127-137,185-198,612-698` (`lem:prelim-iteration`, `lem:prelim-initial-reduction`). Arbitrary-observable/neutral-sector mixing additionally uses conditional ferromagnetic XY/Ising decompositions, association, and a fractional two-point bound with exponent \(1/3\); one-site rotation decorrelation alone is insufficient. Bond-deletion monotonicity is used in restoring cut bonds. **Locator:** `O3/sections/preliminary.tex:826-938`.

This uniformity is for the original nearest-neighbor model, not arbitrary generated or signed interactions. The reference test uses it at the original cutoff; generated endpoint densities are handled by the separate RG/comparison estimates.

### 1.2 Exact RG needs almost dimension-two contraction — M3 over M4 infrastructure

Distinguish the manuscript's **coupling drift** \(\gamma_{\rm drift}=\log L/(2\pi)\) from the parent's physical mixing exponent. The reference scales and caps are
\[
\begin{gathered}
H_j=H+\gamma_{\rm drift}j,\quad
\mathfrak m_j=\lceil(\log H_j)^2\rceil,\quad
p_j=(\log H_j)^{P_0},\quad
t_j=H_j^{-1/2}p_j,\quad T_j=H_j^{-49/100},\\
 b_j\in[H_j/2,2H_j],\quad g=b_j^{-1/2},\quad
\|f\|_{8,j,64}\le H_j^{-2.05},\qquad
\|k\|_{j,64}\le e^{-p_j^{1/4}}.
\end{gathered}
\]
The positive observation is normalized by \(z_2(b)=(1-e^{-2b})/(2b)\), so it preserves the partition function exactly (`O3/sections/setup.tex:73-115`). Thresholds remain fixed while comparing precise couplings. Norms require all mask reads and positive **and negative** eligibility tests; support size is at most \(C\mathfrak m_j^2s\), record length at most \(C\mathfrak m_js\), and projected load satisfies \(4s/L\le s'\le D_*(1+s/L)\). Winding provenance is retained even for a resulting constant. The coefficient norm uses one fixed exponential path exponent, not a shrinking sequence of norms. **Locators:** `O3/sections/setup.tex:31-71,215-265,328-398,424-465,513-563`.

For the normalized shape discrepancy \(u\), precise-coupling discrepancy \(\lambda\), and common-tail history error \(\epsilon_h\),
\[
\begin{aligned}
 b'&=b+\alpha_h(\mathbf P)+\kappa_h(\mathbf P)/b+\Delta,
 &|\Delta|&\le C_LH_j^{-1.05},\\
 u'&\le qu+C_L\operatorname{poly}(H_j)\epsilon_h
       +C_L(\log H_j)^C|\lambda|/H_j,\\
 |\lambda'-\lambda|&\le C_Lu+C_L\operatorname{poly}(H_j)\epsilon_h
       +C_L(\log H_j)^C|\lambda|/H_j,
 &q&<L^{-2+\upsilon}.
\end{aligned}
\]
Identical histories have \(\epsilon_h=0\); histories sharing their last \(r\) regular observations admit \(\epsilon_h=(A_0/L^2)^r\). Regular differences use seven derivatives of inputs whose individual bounds use eight; no repeated derivative loss is allowed. Constants are common to admitted histories and periods. **Locators:** `O3/sections/rg.tex:80-122` (`thm:rg-step`); `O3/sections/free.tex:225-270` (`prop:free-bounds`). The latter supplies fixed-strip analyticity, exponential row/column moments, affine preservation, and \(\nabla_f^sP=O(L^{-s})\), in particular through order three.

The improved rate uses full internal invariant packets, zero affine Hessian, tangent inversion, and **spatial inversion**: the linear–quadratic spatial cross term cancels. Surviving terms cost \(CL^{-4}\) before the \(L^2\) anchor sum. Thus both canonical diagonal response and regular error have \(CL^{-2}\) contraction, the latter with a uniform-in-\(j\) \(o_H(1)\) addition. This is not the original O4 rate. The actual-integral remainder bounds are \(C_Lg^{4.6}\), and \(C_Lg^{4.5}\) times discrepancy; seeded sums retain \(e^{-p^{3/10}}\), stronger than the gas cap. Affine extraction costs \((t')^{-2}\), leading to the summable \(H_j^{-1.05}\) kick error. **Locators:** `O3/sections/rg.tex:26-66,599-618,886-940,967-1102,1113-1123,1175-1208`.

**Order of choices is essential:** fix derivative orders, support/geometry losses and a sufficiently small desired \(\upsilon>0\); choose large dyadic \(L\), canonical caps/comparison weights, then \(P_0\), then \(H\). The leading \(C/L^2\) constants must be independent of \(L\) before choosing it; delayed small terms must be uniform for every \(H_j\ge H\). Neither uniformity as \(\upsilon\downarrow0\) with all parameters fixed nor uniformity in variable \(H\) is asserted. **Locator:** `O3/sections/rg.tex:1273-1296`.

### 1.3 Same terminal coupling, not merely large bare couplings — M3

There is a shot at every depth \(N\) ending at **exactly** \(b_0=H\), strictly inside all admission bands, with
\[
\alpha_\infty=-\frac{\log L}{2\pi},\quad
\beta_N=H+\frac{\log L}{2\pi}N+O_{L,H}(\log(2+N)),\quad
b_j=H_j-\frac{\kappa_\infty}{\gamma_{\rm drift}}\log(H_j/H)+O_L(1).
\]
The last error is uniform in depth; O3 does **not** evaluate \(\kappa_\infty\) here. The imported general-tangent-dimension coefficient is
\(4A_D(n)-A_D(2n)=-3D(D-1)\log n/(4\pi)+O(1)\); O3 sets \(D=2\). Uniformity of these finite-volume **coefficients**, not a bare Laplace remainder uniform in blocking depth, is what is used. The canonical orbit is a finite *formal coefficient operation* assigned within an exact representation; “formal” here does not mean formalized in Lean. **Locators:** `O3/sections/shooting.tex:28-55,57-142,144-180,219-258`; `O3/sections/rg.tex:835-868,1108-1173`.

For \(N\ge K\), matching the last \(K\) layers gives
\[
u_j+|\lambda_j|\le C_H(1+K)^C\rho^{K-j},\qquad
\max(q,A_0/L^2)<\rho<L^{-2+\upsilon},
\]
using bounded top shape data and the **opposite-end boundary condition** \(\lambda_0=0\). Writing \(\varepsilon_H=\sup_j C_L(\log H_j)^C/H_j\), \(a=(1-\varepsilon_H)^{-1}\), the proof requires
\[
a\rho<1,\qquad
\frac{\varepsilon_H}{\rho-q}\frac{aC_L}{1-a\rho}<\tfrac12.
\]
The \(|\lambda|/H_j\) forcing is not simply summable; the two-boundary absorption is indispensable. No uniqueness of the shot, bound on \(N-K\), or bound on the bare-coupling ratio is required. **Locator:** `O3/sections/shooting.tex:260-344` (`prop:endpoint-matching`).

After removing a scalar **exactly proportional to terminal volume** \(v\),
\[
\|X_N-X_K\|_\infty\le D_Hv\delta_K,\qquad
\sup_x\sum_{\lambda:x\in P_\lambda}e^{64s_\lambda}
 \|k_{N,\lambda}-k_{K,\lambda}\|_\infty\le D_H\delta_K,
\quad \delta_K=L^{-(2-\upsilon)K}.
\]
These bounds are uniform in \(N\ge K\) and admitted periods; polynomial factors in \(K\) are absorbed in the strict spare rate. Period-dependent corrections remain in winding lists, never in the discarded scalar. Standard axis endpoint densities are positive and seam-reflection-positive; reflection positivity is **not** asserted for inclined/oblique endpoints. Mirrored inclined shots have equal terminal couplings to each other, not necessarily \(H\); their common-coordinate endpoint comparison uses \(K=N\). **Locator:** `O3/sections/shooting.tex:269-364`.

### 1.4 Signed covering weights require an integrated comparison — M3

The gas must cover the complete bad-bond set **exactly once**, with nonempty fixed inventories and disjoint complete supports. It is not an optional polymer partition function. For a standard endpoint base density, with a common label list and \(d_\lambda=\|\widetilde k_\lambda-k_\lambda\|_\infty\),
\[
\frac1Z\int e^X|\widetilde\Xi-\Xi|\,dq
 \le \exp\!\left(\sum_\lambda d_\lambda e^{2s_\lambda}\right)-1.
\]
The support-hit envelope of \(|k|+|\widetilde k|\) must remain within a fixed multiplier of the cap. Only the **base complete density** must be positive and reflection positive; the perturbing weights may be signed/complex. The bound applies on sufficiently large bounded-aspect axis tori with periods divisible by \(2B_T\), uniformly in depth and periods. **Locator:** `O3/sections/comparison.tex:13-80` (`prop:integrated-comparison`).

The difficult hypotheses behind this estimate are quantitative:

- \(t=H^{-1/2}p\), \(p=(\log H)^{P_0}\), \(D_1\asymp(\log H)^2\), \(d\asymp D_1\). Split \(X=-\sum_eY_e+X_{\rm rem}\), with \(Y_e\ge0\), \(|X_{\rm rem}|\le C_Lv\), and \(n\)-site edit cost at most \(C_Ln\). Also \(Z\ge e^{-C_Lv\log H}\).
- Selected-row moment: \(\mathbb E e^{\theta\sum_{e\in I}Y_e}\le e^{C_L|I|B_T^2\log H}\), \(\theta=1-C_LD_1/B_T\).
- Measurable independent-cap filling removes exactly the selected inventories, creates no new bad boundary bonds, and has density at most \(e^{Cn\log H}\). Relevant rows number at most \(Cd^2n\); old energy is at least \(cp^2n/d^2\), filled energy at most \(C_Ld^2p^2n\).
- Choose \((1-\theta)C_Ld^2<c/(4d^2)\), then \(p^2/d^2\gg d^2B_T^2\log H+\log H+1\). The integrated edit gain is \(e^{-c'p^2n/d^2}\). With \(R=C_L\mathfrak m_0^2\), both edit and gas support-hit sums with weights \(e^{2\,\mathrm{size}}\) are below \(1/(16R)\).

**Locators:** `O3/sections/comparison.tex:100-165,243-268,288-327,355-371,467-507,538-585`. Geometry is fixed from the original configuration; filled configurations are **not reclustered**. Restricted signed sums are never denominators. Exact forest identities need every negative status query in its support (`373-449`).

Consequently \(\sum d_\lambda e^{2s_\lambda}\le D_Hv\delta_K\), and, including the exponent discrepancy,
\[
|\log Z_N^{\rm stripped}-\log Z_K^{\rm stripped}|
 \le C_Hv\delta_K\quad\text{when }v\delta_K\text{ is small}.
\]
A naive division of an absolute gas estimate by a small covering sum would not give this. There is no O4-style extra \(e^{\zeta K}\) loss. **Locator:** `O3/sections/comparison.tex:588-610`.

### 1.5 Choose the reference box, then freeze it — M3

`O3/sections/trace.tex:33-108` (`prop:trace-small-box`) explicitly assumes the four preceding ingredients. Choose
\[
0<\upsilon/2<\chi<\min\{1,\eta/(2\pi)\},\qquad
m_K\asymp L^{(1-\chi)K}.
\]
At the reference cutoff, the microscopic side is \(m_KL^K\), while
\[
X(\beta_K)\le C_H K^{C_H}L^{(2-\eta/(2\pi))K},\qquad
\frac{m_KL^K}{X(\beta_K)}
 \ge C_H^{-1}K^{-C_H}L^{(\eta/(2\pi)-\chi)K},
\]
so preliminary doubling tends to zero despite its polynomial prefactor. Meanwhile
\[
m_K^2\delta_K\asymp L^{-(2\chi-\upsilon)K}\longrightarrow0.
\]
Apply the partition comparison to the rectangle and its double; bulk scalars cancel. One sufficiently large **finite** \(K_0\) and \(M_0=m_{K_0}\) then give \(\Delta_{\beta_N}\le2^{-10}\) at the same physical box for **all** \(N\ge K_0\). The periods may satisfy any fixed divisibility/size requirements and any fixed finite list of rational aspects. There is no uniformity over arbitrary aspect ratios.

This is a two-dimensional budget with physical preliminary length exponent \(1-\eta/(2\pi)\) and comparison exponent \(2-\upsilon\): feasibility requires choosing \(\upsilon<\eta/\pi\). The box must not be allowed to grow with final cutoff \(N\) after it has been frozen. The subsequent spectral/volume interface is stated at `O3/sections/trace.tex:307-344`; its algebra is not audited here.

## 2. Imported versus formalized: do not enlarge the scope

### O4 inputs actually being reused

| Imported ingredient | Exact O4 source; O3 treatment |
|---|---|
| Pinned currents, band estimates, orientation exploration, neutral observables and cutouts | `O4/sections/preliminary.tex:66-123,1022-1099,1246-1284`; O3 changes the current/contact algebra and supplies the strict initial saving (`O3/sections/preliminary.tex:99-125,612-698`). O4's local signed/twisted pinned class does **not** extend its full mixing conclusion beyond nonnegative untwisted couplings (`O4/sections/preliminary.tex:52-57,73-100`). |
| Scalar free kernels and positive completion | `O4/sections/linear.tex:61-100,195-220`; `O4/supplements/analytic-rg.tex:33-179`. O4 states history loss \(L^{-h}\); O3 proves the stronger common-tail rate and inclined variants in `O3/sections/free.tex:225-270,405-465`. |
| Ownership, complete reads, local Gaussian marginals, joint majorants, exact connected reassembly | `O4/supplements/geometry-rg.tex:13-62,307-392`; `O4/supplements/joint-majorants.tex:8-112,205-294`; `O4/sections/renormalization.tex:708-737,857-945`. The Gaussian lemma requires covariance bounded above, summed square-root endpoint charges at most \((64c_*)^{-1}\), and the individual ratio-size condition; overlapping factors need a **joint** bound, not independence. O3 verifies its ambient-coordinate modifications in `O3/sections/rg.tex:266-297,599-769`. |
| Fixed coefficient norm and compensation | `O4/supplements/canonical-norm.tex:65-128,255-278`: \(CL^{2-n}\) for degrees 3–6, only \(C/L\) for compensated quadratics. O3's improved quadratic/error \(L^{-2}\) gain is additional, not imported. |
| Calibration and two-boundary matching | `O4/sections/calibration.tex:259-266,299-344`; `O4/sections/trajectories.tex:177-259`. O3 imports the general-\(D\) coefficient and argument structure, not O4's drift or mass theorem. |
| Cover-removal identities, filling and forest organization | `O4/sections/comparison.tex:264-296,410-449,597-660`. O4 fills a **one-dimensional square boundary** in \(S^3\), with bound \(C(1+L_0)^{3/2}\); O3 supplies the \(S^2\) filling and the new integrated estimate. |

For comparison, O4 has \(X_4(\beta)=\exp[\pi\beta+C\sqrt{(1+\beta)\log(2+\beta)}]\), covariance prefactor exponent **20**, and calibration \(\beta_K(h)=K\log L/\pi+(\log K)/(2\pi)+O_{L,H}(1)\). Its physical preliminary length is only subexponential in \(K\). O4 endpoint error is \(C_He^{-d_HK}\), without a numerical rate; its good-set comparison loses \(e^{\zeta_HK}\), \(0<\zeta_H<\gamma_H/2\), and requires small exceptional probability under **both** laws. It admits \((2M)^2\le e^{c_HK}\); \(M_K=\exp(K^{3/4}+O(1))\) then suffices. None of these weaker rates substitutes for O3's nearly quadratic contraction against its exponentially large physical preliminary length. **Locators:** `O4/sections/preliminary.tex:22-49`; `O4/sections/comparison.tex:77-175`; `O4/sections/assembly.tex:28-95,109-150`.

### What the Lean artifact says

The broad family-215 heading is not the formalization scope. `lean/docs/215.md:3-15` links only the all-temperature finite-free-graph **spin two-point decay** result and expressly excludes the infinite-volume and separate O4 gap claims. Its actual definition is `lean/OAI/Probability/ClassicalON/Model.lean:46-51`; implementation is `lean/OAI/Probability/ClassicalON/Main.lean:19-42`; manifest entry is `lean/formalization.yaml:1077-1079`. It asserts existence of \(A\) and \(m>0\) with exponential spin-correlation decay for bounded nonnegative bonds, **not** the required quantitative dependence on \(\beta\), neutral-observable mixing, torus doubling, exact RG, or the O3 continuum construction.

`lean/ComparatorChallenges/ClassicalON.lean:53-54` is the challenge statement with `sorry`, not the implementation proof. `lean/ComparatorChallenges/ClassicalON.json:1-14` points to the implementation and lists permitted standard axioms. This audit inspected source and scope, not a fresh Lean build or transitive axiom check. The cutoff bridge remains **manuscript-level**, not a consequence of that catalogued formalization.

## 3. Tight obligations for a Wilson SU(2) analogue

These are proposed analytic obligations, **not established transfers**; the gauge comparison is an assessment inferred from the cited definitions. In the usual fundamental-representation convention the Wilson variables are links, with action \(S_W=\beta\sum_p(1-\tfrac12\operatorname{ReTr}U_p)\); identifying \(SU(2)\simeq S^3\) does not turn this into O4's site-spin nearest-neighbor action. Wilson's construction is the relevant starting point [E1, §III, (3.27)–(3.29)].

1. **Replace global-spin decorrelation by a physical, gauge-invariant estimate.** O3's spatially varying rotations change its action and produce stiffness/Ward estimates; local gauge transformations \(U_{xy}\mapsto h_xU_{xy}h_y^{-1}\) leave the Wilson action unchanged. Thus the direct gauge-direction score supplies no analogous physical stiffness gain. Gauge averaging of gauge-variant quantities is not physical mixing. Establish a preliminary small-test/doubling estimate for the actual Wilson measure, including the weakening/cutout class actually used; do not assume O3's XY/Ising association applies. O3 dependency: `O3/sections/preliminary.tex:99-125,826-938`. Gauge distinction: [E1; E2].
2. **Rebuild locality and rough-region edits in link variables.** Plaquettes share links and obey non-Abelian Bianchi constraints with parallel transports/orderings; periodic lattices have additional global constraints. They cannot be independently cap-filled as site spins. Every edit must retain all affected plaquettes, transport paths, status queries and boundary data, and prove its entropy, energy and support-hit bounds. Solving constraints is not a shortcut to a local simple action: Batrouni's explicit elimination instead produces a complicated effective action. O3 target: `O3/sections/comparison.tex:243-268,373-449,467-507`; primary constraint locators: [E3, §III, (III.2)–(III.5); E4].
3. **Account for topology and holonomy rather than silently selecting a trivial sector.** O3's filling extends loops into \(S^2\); this does not assert that all two-dimensional spin configurations are topologically trivial. The putative four-dimensional analogue faces three-dimensional boundary data: degree-nonzero maps \(S^3\to SU(2)\simeq S^3\) cannot extend over a ball. Small plaquette curvature also does not imply a globally near-identity link representative on a torus: flat commuting links can retain nontrivial cycle holonomies. Smooth/admissible lattice gauge fields can carry integer topological charge [E5]; the full rough link configuration space is not thereby decomposed into disconnected sectors. At zero theta one must still include nontrivial configurations. A surgery must retain the obstruction data or price its changes, not assume a topology-preserving small-field filling always exists. O3 contrast: `O3/sections/comparison.tex:288-327`; [E4; E5].
4. **Construct an exact gauge-compatible RG class, not a plaquette-only truncation.** Retain generated loop/multi-loop interactions, regular and large-field remainders, and period-dependent records. Prove normalized blocking and the needed seam reflection positivity, plus uniform fluctuation covariance/score estimates after handling gauge null directions and residual modes. O3's addition of a normal scalar resolves tangent-frame geometry, not gauge degeneracy (`O3/sections/rg.tex:252-322`). Recompute the marginal sector and every contraction exponent: \(F=dA+A\wedge A\) gives cubic as well as quartic gauge-potential interactions, so the spin-packet parity cancellation is no license to discard cubic terms [E6, §1, (1)]. Even the O3 counting \(L^{-4}\times L^2\) would become order one with \(L^4\) anchors unless field/derivative scaling supplies additional gains. These are reasons to rederive \(\alpha\), not arguments that \(\alpha>0\) is impossible.
5. **Prove matching and integrated comparison with quantified uniformities.** Specify physical units and matched renormalized coordinates, prove admission and summable nonperturbative kick errors, then bound complete endpoint differences uniformly in final cutoff \(N\ge K\), volume and allowed backgrounds. Establish a Wilson analogue of the volume-linear integrated bound in §1.4 with signed generated weights and a positive base law. Constants must not hide growth with \(N-K\), boundary data, or reference depth. Only then test the budget in §4. The O3 templates are `O3/sections/shooting.tex:160-180,269-350` and `O3/sections/comparison.tex:62-80,588-610`.
6. **Reconstruct the same physical fields, separately from transferring a partition test.** O3 carries sources exactly with \(R_j=H_j^{-1/10}\), \(z_x=z'_{[x]}/(l^2c_j)\), \(c_j>0\), \(|c_j-1|\le C_LR_j\), a source contraction \(q_s<1\), and \(B_N=\prod c_{j,N}^{-1}\), \(|\log B_N|=O(1+N^{9/10})\). Source differences converge at fixed bottom layers; this is not a growing-volume assertion. Product comparison uses the summable \(H_j^{-11/10}(\log H_j)^D\) sensitivity. O3 keeps source-degree-two-and-higher scalar terms in source-supported records, not discarded volume scalars. **Locators:** `O3/sections/sources.tex:11-19,51-67,96-138,485-535,561-592`. Gauge fields instead require gauge-invariant local/composite observables, their operator mixing and identity/contact subtractions, moment bounds, nonvanishing limits, Euclidean/reflection properties and a dense physical observable algebra [E6, §4]. O3 supplies separate factorial bounds, field convergence and observable-independent clustering exponents in `O3/sections/continuum.tex:45-75,185-204` and `O3/sections/os.tex:60-79,349-373`. A lattice test alone supplies none of that field reconstruction.

Two scope guards: O4 itself makes continuum gap transfer conditional on convergence of norms and semigroup matrix elements on a dense centered set (`O4/sections/physical.tex:30-58`); O3's later extension from prescribed shots to all large bare couplings additionally requires **sensitivity**, \(|\Delta_{2,j}-\Delta_{1,j}|\le C_LH_j^{-1.01}(u_j+|\lambda_j|)+C_L\operatorname{poly}(H_j)\epsilon_h\), not just the kick-size bound (`O3/sections/trajectories.tex:227-247`). Neither is implicit in the reference-box bridge.

## 4. Check of the parent's schematic budget

**Exact parent gluing contract (accepted, not re-audited).** Set \(F_N(R)=\log Z_{\beta_N}((RB^N)^4)\), \(\widetilde F_N(R)=F_N(R)-c_NR^4\), and \(\mathfrak D_N(M)=16F_N(M)-F_N(2M)\). A uniform comparison \(|\widetilde F_N(R)-\widetilde F_K(R)|\le CR^4\epsilon_K\) for every \(N\ge K\) and both \(R=M,2M\) gives \(|\mathfrak D_N(M)-\mathfrak D_K(M)|\le32CM^4\epsilon_K\). Thus require \(\mathfrak D_K(M)\le\varepsilon_*/2\) and \(32CM^4\epsilon_K\le\varepsilon_*/2\), with \(\varepsilon_*=1/2048\), so each allowance is \(1/4096\). At each cutoff, **the same** \(\beta_N\) and volume-independent \(c_N\) must serve both boxes in one fixed measure/physical-scale convention; \(c_N\) may vary with \(N\), but not with \(R\). The reference must belong to the same matched renormalized trajectory: a tiny-beta strong-coupling check cannot simply replace its weak-coupling \(\beta_K\), and relabeling a tiny-beta model by a large depth does not establish a small comparison error. **Locator:** `research_notes/yang_mills_2026_10_09/finite_volume_criterion.tex:356-388`.

Treat the parent's quantities as **hypotheses of a chosen scheme**, not estimates proved here for Wilson SU(2). Let \(B>1\), comparison error on a physical box of side \(R\) be bounded by \(C R^4B^{-\alpha K}\), and preliminary physical mixing length satisfy \(\ell_K\le B^{\gamma K+o(K)}\), with \(\gamma\ge0\). Assume constants uniform in \(N\ge K\), valid comparison throughout the chosen growing-box range, and a preliminary test bound with prefactors whose logarithms are \(O(K+\log R_K)\), as supplied by O3’s polynomial prefactors and shooting asymptotics.

If
\[
\boxed{4\gamma<\alpha},
\]
choose a fixed \(\theta\) with \(\gamma<\theta<\alpha/4\) and \(R_K\asymp B^{\theta K}\), rounding to the required periods. Then
\[
R_K/\ell_K\ge B^{(\theta-\gamma)K-o(K)}\to\infty,
\qquad
R_K^4B^{-\alpha K}\asymp B^{-(\alpha-4\theta)K}\to0.
\]
The first ratio grows exponentially, so an \(e^{-cR_K/\ell_K}\) preliminary bound beats prefactors whose logarithms are \(O(K+\log R_K)\). Fix a finite \(K_0\) once both the reference-test error and the transfer error fit inside the independently established test margin; keep \(R_0=R_{K_0}\) fixed for all later cutoffs. Comparison must also hold on every enlarged/auxiliary box read by that test. Crucially, \(R^4\) is **terminal/physical** volume, not microscopic volume \(R^4B^{4N}\).

Thus the budget is sufficient for this volume-linear comparison plus power-growing reference-box scheme. It is **not necessary for Yang–Mills**, does not provide a 4D finite-volume criterion, and does not establish any of its analytic premises. Failure of the inequality means these particular upper bounds leave no strict power-scale window; it does not prove failure of the theory or even of a better bridge. Localized comparison, cancellations, better preliminary decay, subleading gains in a borderline case, or a directly established fixed reference test can change the budget. No value of \(\alpha\) or \(\gamma\) for 4D Wilson SU(2) is supplied by the inspected O3/O4 statements.

## 5. One best next analytic target

**Determine the validity and exact boundary-data scope of a gauge-covariant integrated rough-region replacement lemma for a finite 4D Wilson block at fixed large terminal coupling \(H\).** Take \(t=H^{-1/2}(\log H)^P\) and bad inventory \(D(U)=\{p:\|I-U_p\|_{\mathrm{op}}>t\}\), with fixed sufficiently large \(P\). Work with a measurable kernel on interior **links**, retaining the exterior and all required holonomy/topological data. Seek the analogues of: an \(e^{C n\log H}\) filling-density cost; no unrecorded newly bad boundary plaquettes; and an integrated gain \(e^{-cHt^2 n/(\log H)^C}\) strong enough to sum support-hit forests, with \(n\) the number of edited links. If uniform filling is obstructed, identify the additional retained defect/sector labels and their required price rather than deleting those configurations.

The exact spin-model targets are `O3/sections/comparison.tex:243-268` (`lem:editable-regions`) and `467-507` (`eq:orig-22`). This single local question tests the most model-sensitive route to the parent's **volume-linear** error; answering it would still not supply RG closure, \(\alpha\), preliminary mixing, or a Yang–Mills theorem.

### External primary-source locators used only for the gauge assessment

- **E1:** K. G. Wilson, *Confinement of quarks*, Phys. Rev. D **10** (1974), 2445–2459, §III, Eqs. (3.27)–(3.29); DOI `10.1103/PhysRevD.10.2445`. <https://doi.org/10.1103/PhysRevD.10.2445>
- **E2:** S. Elitzur, *Impossibility of spontaneously breaking local symmetries*, Phys. Rev. D **12** (1975), 3978–3982; DOI `10.1103/PhysRevD.12.3978`. <https://doi.org/10.1103/PhysRevD.12.3978>
- **E3:** G. G. Batrouni, *Plaquette formulation and the Bianchi identity for lattice gauge theories*, Nucl. Phys. B **208** (1982), 467–483, §III, Eqs. (III.2)–(III.5) in the LBL-14693 author preprint; DOI `10.1016/0550-3213(82)90231-0`. <https://doi.org/10.1016/0550-3213(82)90231-0>
- **E4:** G. G. Batrouni, *String, corner, and plaquette formulation of finite lattice gauge theory*, Phys. Rev. D **30** (1984), 1782; abstract's finite-period/global-Bianchi statement; DOI `10.1103/PhysRevD.30.1782`. <https://doi.org/10.1103/PhysRevD.30.1782>
- **E5:** M. Lüscher, *Topology of lattice gauge fields*, Commun. Math. Phys. **85** (1982), 39–48; abstract's small-action/topological-charge statement; DOI `10.1007/BF02029132`. <https://doi.org/10.1007/BF02029132>
- **E6:** A. Jaffe and E. Witten, *Quantum Yang–Mills Theory*, official Clay problem description, §1 Eq. (1), PDF p. 2, and §4, PDF pp. 5–6. Used for the definition/observable requirements, not as a contemporary status report or a solution. <https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf>
