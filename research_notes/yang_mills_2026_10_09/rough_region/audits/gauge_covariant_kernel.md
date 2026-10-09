# Gauge-covariant finite-link cap replacement

**Audit date:** 2026-10-09. **Scope:** a direct finite-dimensional construction,
not an integrated energy/entropy inequality or a topology-preservation theorem.
All assertions below are proved here; no claim of novelty or literature
certification is made.

## 1. Setup and forest compatibility

Use independent oriented links of an untwisted four-dimensional hypercubic
lattice, with reverse links defined by inversion. On a periodic lattice assume
periods at least four. The construction is local and also applies on the
infinite lattice. Write `G = SU(2)` and let `mu` be probability Haar measure.
For a link configuration, vertex gauges act by

\[
 (g\cdot U)_{xy}=g_xU_{xy}g_y^{-1}.
\]

Let `J` be the finite set of editable independent links, `n = |J|`, and
`P_J` the plaquettes containing a link of `J`. Let `E_*` contain `J` and every
link on these plaquettes, let `F = E_* \ J`, and let `S` be the endpoints of
`E_*`. The frozen graph is **`(S,F)`, including isolated vertices**. The full
exterior `xi = U_{E\J}` is retained; write `b = xi_F`. All forests, roots and
orientations below are fixed from the graph, not chosen from the link values.

Choose a spanning forest `T` of `(S,F)` and one root `r_c` per component `c`.
Let `t_x(b)` be the ordered transport along the tree path `r_c -> x`, and put

\[
 h_x(b)=t_x(b)^{-1},\qquad
 R_e(b)=h_x(b)^{-1}b_{xy}h_y(b)\quad(e=(x,y)\in F).
 \tag{1}
\]

For tree edges `R_e = I`; for a non-tree edge, `R_e` is its fundamental-loop
holonomy based at the root. Reversing an edge inverts its residual. Define

\[
 c(A)=\|I-A\|_{\rm op},\qquad
 \epsilon_T(b)=\max_{e\in F\setminus T}c(R_e(b)),
 \tag{2}
\]

with an empty maximum equal to zero. The following are equivalent:

1. Every closed path of the frozen graph has identity holonomy.
2. Every non-tree residual is identity.
3. `b_xy = h_x h_y^{-1}` on every frozen edge.

The first condition implies the second by the fundamental loops. The
definition of `R_e` gives the second => the third, whose products telescope
around every closed path. Thus these are exactly
the conditions for a **pure-gauge graph completion**. Setting
`V_xy = h_x h_y^{-1}` on `J` then makes every cycle of `E_*`, and hence every
touched plaquette, flat. This deterministic completion is continuous on the
compatibility locus, but need not be gauge-equivariant.

For `eta > 0`, the approximate compatibility set

\[
 \Omega_\eta=\{b:\epsilon_T(b)<\eta\}
 \tag{3}
\]

is open. It contains a neighborhood of the identity frozen configuration:
there are finitely many continuous residual maps. This neighborhood need not
be uniform in forest path lengths. Exact compatibility means
`Omega_flat = {epsilon_T = 0}`, a closed set, **not** the strict set (3) at
`eta = 0`. Small elementary-plaquette curvature alone is not the hypothesis:
the specified fundamental frozen-loop residuals must be controlled.

## 2. Random frames: covariance, disconnected components, stabilizers

Draw independent `a_c ~ mu`, one for **every** frozen component, including each
isolated vertex. Set

\[
 s_x=h_x(b)a_{c(x)},\qquad V_{xy}=s_xs_y^{-1}\quad((x,y)\in J),
 \qquad V_e=\xi_e\quad(e\notin J).
 \tag{4}
\]

When compatibility is exact, (4) is pure gauge on `E_*`. The arbitrary root
frames parametrize all pure-gauge graph completions, with harmless redundancy;
no relative frame between different frozen components has been fixed.
For arbitrary `b`, every frozen edge has both endpoints in the same component,
so its value in these frames is

\[
 s_x^{-1}b_{xy}s_y=a_c^{-1}R_e(b)a_c.
 \tag{5}
\]

Consequently its operator distance from identity is exactly `c(R_e)`, uniformly
in the random frames; tree edges have distance zero.

Here is the full covariance calculation, valid for arbitrary vertex gauges:

\[
 \begin{aligned}
 t_x(g\cdot b)&=g_{r_c}t_x(b)g_x^{-1},\\
 h_x(g\cdot b)&=g_xh_x(b)g_{r_c}^{-1},\\
 R_e(g\cdot b)&=g_{r_c}R_e(b)g_{r_c}^{-1}.
 \end{aligned}
 \tag{6}
\]

In particular (2)--(3) are gauge invariant. Couple the root draws by

\[
 a'_c=g_{r_c}a_c.
 \quad\text{Then}\quad
 s'_x=h_x(g\cdot b)a'_c=g_xs_x.
 \tag{7}
\]

The `a'_c` are still independent probability-Haar variables. Thus the reference
law transforms by `V -> g.V`, with the transformed exterior copied unchanged.
There is no restriction that `g` equal identity on boundary vertices.

Stabilizers cause no exception. In fact a gauge fixing `b` on `F` has precisely

\[
 g_x=h_xd_ch_x^{-1},\qquad
 d_c\in\bigcap_{e\in F_c\setminus T}Z_G(R_e),
 \tag{8}
\]

as follows first along tree edges and then from the chord equations. For exact
data this centralizer is all of `G` in each component. Equation (7), now with
`g.b = b`, proves invariance under these stabilizers. All averages use
probability Haar; no orbit-volume, center or stabilizer factor occurs.
A deterministic boundary-only choice generally cannot replace the random
frames: if an edited link joins two frozen components with identity data,
independent constant gauges on the components fix `b` but act on its value as
`v -> g_1 v g_2^{-1}`. No single `v` is fixed by all such gauges.

## 3. Independent central caps and the joint kernel

For `0 < rho <= pi` use the central geodesic cap

\[
 C_\rho=\{Q:\theta(Q)\le\rho\},\qquad
 \theta(Q)=\arccos\bigl(\tfrac12\operatorname{Tr}Q\bigr).
\]

Polar coordinates `Q = cos(theta) I + i sin(theta) u.sigma` on the unit
three-sphere give probability-Haar radial density `(2/pi) sin^2(theta)`;
therefore its cap mass is

\[
 b(\rho)=\mu(C_\rho)
 =\frac{2}{\pi}\int_0^\rho\sin^2t\,dt
 =\frac{\rho-\sin\rho\cos\rho}{\pi}>0.
 \tag{9}
\]

Independently of the root frames, draw independent
`Q_e ~ 1_{C_rho} mu / b(rho)` on the independent links of `J`. Define

\[
 U'_{xy}=s_xQ_es_y^{-1}\quad(e=(x,y)\in J),\qquad
 U'_e=\xi_e\quad(e\notin J).
 \tag{10}
\]

Reverse links are inverses, not additional draws. Conditional on the frames,
left/right Haar invariance and centrality give the density

\[
 k_s(w)=\prod_{e=(x,y)\in J}
 \frac{\mathbf1_{C_\rho}(s_x^{-1}w_es_y)}{b(\rho)}
 =\prod_{e\in J}
 \frac{\mathbf1_{C_\rho}(V_e^{-1}w_e)}{b(\rho)}.
 \tag{11}
\]

For the equality, `s_x^{-1} w_e s_y = s_y^{-1}(V_e^{-1}w_e)s_y`.
Thus even conditional only on `V`, these are independent central caps about
`V_e`; independence is **not** asserted after averaging the reference away.
The joint law of `(V,U'_J)` has density (11) relative to
`R_b(dV) mu^J(dw)`, where `R_b` is the reference law. In particular the marginal
replacement density satisfies

\[
 k_b(w)=\int k_s(w)\,\prod_c d\mu(a_c),\qquad
 \int k_b\,d\mu^J=1,\qquad 0\le k_b\le b(\rho)^{-n}.
 \tag{12}
\]

This is a density on **edited links conditional on the exterior**, not a
full-lattice product-Haar density (the exterior is a Dirac mass).
For a general central cap `C_r` of positive Haar mass `v(r)`, the same proof
gives the requested bound `v(r)^(-|J|)`.

Products/inverses and the frame maps are continuous; the cap indicator is
Borel. Integrating these Borel maps against fixed probability laws proves
measurability of the reference and replacement kernels. They are defined for
all `b`, not just compatible data. For `n = 0`, use the identity kernel.

Use (7) and the **same** `Q_e` in the transformed experiment. Equations
(4), (10) give `(V',U'') = (g.V,g.U')` pointwise. Hence the joint reference/output
kernel is covariant. For the full replacement kernel `K` this states, for every
Borel event `A` and every vertex gauge `g`,

\[
 K(g\cdot U,g\cdot A)=K(U,A).
 \tag{13}
\]

Within a draw the exterior is exactly `xi`; in (13) the input exterior is
transformed along with the input. Gauges outside `S` are covered too, since
the remaining links are simply copied.

## 4. Curvature bounds

Let `q_p = |J intersect boundary(p)|`, so `1 <= q_p <= 4` for `p in P_J`.
Bi-invariance of operator distance on unitary matrices, inversion invariance,
and telescoping products give

\[
 \Bigl\|\prod_i A_i-\prod_i B_i\Bigr\|_{\rm op}
 \le\sum_i\|A_i-B_i\|_{\rm op},\qquad
 c(Q)=2\sin(\theta(Q)/2)\le\theta(Q).
 \tag{14}
\]

Compute each plaquette in the `s` frames: edited edges are `Q_e` (or their
inverses), frozen edges are (5). On `Omega_eta`, or with exact residuals and
`eta = 0`, (14) proves the sharper bound

\[
 c(U'_p)\le
 \sum_{e\in\partial p\cap F}c(R_e)+q_p\rho
 \le(4-q_p)\eta+q_p\rho.
 \tag{15}
\]

The sum counts edge occurrences. More generally set

\[
 \delta_T(b)=\max_{p\in P_J}
       \sum_{e\in\partial p\cap F}c(R_e).
\]

The reference (4) satisfies `c(V_p) <= delta_T(b)`. Moreover
`||U'_e - V_e||_op <= rho` on `J`, and they agree on all other links, so

\[
 \|U'_p-V_p\|_{\rm op}\le q_p\rho,\qquad
 c(U'_p)\le\delta_T(b)+q_p\rho\le\delta_T(b)+4\rho.
 \tag{16}
\]

This also proves the general `delta + 4r` assertion for any reference law
supported on `c(V_p) <= delta` and caps of operator radius at most `r`.
Untouched plaquettes are exactly unchanged. No independent plaquette draws
are made.

## 5. SU(2) constant checks (pointwise only)

Each independent link lies on at most six plaquettes. Thus

\[
 |P_J|\le6n,\qquad \sum_{p\in P_J}q_p\le6n,\qquad
 E_J(W):=\sum_{p\in P_J}\left(1-\tfrac12\operatorname{Tr}W_p\right)
       =\tfrac12\sum_{p\in P_J}c(W_p)^2.
 \tag{17}
\]

Take `H >= 1` and `eta = rho = H^(-1/2)`. From (15),

\[
 \max_{p\in P_J}c(U'_p)\le4/\sqrt H,\qquad
 E_J(U')\le48n/H.
 \tag{18}
\]

**Exact compatibility improves 48 to 12:** with `eta = 0` and the same `rho`,

\[
 E_J(U')\le\frac{1}{2H}\sum_p q_p^2
 \le\frac{4}{2H}\sum_p q_p\le12n/H.
 \tag{19}
\]

This uses edited-edge incidence, not just `|P_J| <= 6n`.
For `0 <= t <= 1`, `sin(t) >= t/2`. Equation (9) and `pi < 4` give

\[
 b(\rho)\ge\frac{\rho^3}{6\pi}\ge\frac{\rho^3}{24},\qquad
 b(H^{-1/2})^{-n}\le(24H^{3/2})^n.
 \tag{20}
\]

If at least `k` **touched** plaquettes of the old configuration have
`c(U_p) > p_*/sqrt(H)`, then `E_J(U) >= k p_*^2/(2H)`. For the shifted Wilson
factor `exp(-H E_J)`, the requested exponent is the following pointwise
arithmetic, with no integration asserted:

\[
 -H E_J(U)+H E_J(U')+n\log b(H^{-1/2})^{-1}
 \le-\frac{k p_*^2}{2}
       +n\left(48+\log24+\tfrac32\log H\right).
 \tag{21}
\]

Replace `48` by `12` under exact compatibility. The unshifted Wilson weight
gives the same ratio. If `p_* >= 4`, no output touched plaquette exceeds the
strict bad threshold. This condition alone does **not** make (21) negative.
For `k >= 1` the old event is empty unless `p_*/sqrt(H) < 2`, since `c <= 2`.

## 6. Optional selector repair; not needed for the forest kernel

The deterministic choice `a_c = I` already supplies a continuous, hence
measurable, low-curvature reference on approximate forest-compatible data.
It is its **law**, not necessarily that deterministic choice, that must be
made equivariant.

More generally, on a finite lattice let `v(xi)` be any Borel reference selector
with a gauge-invariant support requirement, for example
`max_{p in P_J} c((xi,v)_p) <= delta(xi)` with invariant `delta`. Average over
the full vertex gauge group with probability Haar:

\[
 \mathcal R_\xi=
 \int\delta_{\gamma^{-1}\cdot v(\gamma\cdot\xi)}\,d\gamma.
 \tag{22}
\]

The change of variable `alpha = gamma g` proves
`R_{g.xi} = g_* R_xi`. Attach exterior `xi`: transforming the exterior before
selection and undoing that transformation restores it exactly. The support
requirement is preserved, and central cap convolution retains (12), (16).
Averaging an output alone while holding its input fixed would not justify this.

For completeness, an exact minimizer of a continuous objective on the compact
space `G^J`, jointly continuous in the finite exterior, has a Borel selector:
the minimum value is continuous; whether the compact argmin meets a fixed
compact set is closed in the parameter. Successively choose the first member
of nested finite compact covers meeting the argmin, with diameters tending
to zero. The unique limit is a Borel minimizer. Formula (22) repairs its possible
non-equivariance when the objective is gauge invariant. A conditional **action**
minimizer need not satisfy a prescribed maximum-plaquette bound; that support
property must be proved separately (or built into the optimization).

## 7. Bianchi identities and limits of the claim

Every output is one complete link configuration. All link-induced Bianchi
identities, including identities involving both edited and frozen links, are
therefore automatic. To make the non-Abelian ordering explicit, write
`P_ij = U_ij(x)` and
`P_hat_ij = U_k(x) U_ij(x+hat{k}) U_k(x)^{-1}`, where `{i,j,k}={1,2,3}`.
Direct link cancellation gives the cube identity

\[
 \widehat P_{23}\,P_{13}\,\widehat P_{12}
   =P_{12}\,\widehat P_{13}\,P_{23}.
 \tag{23}
\]

Both sides are the transport along the path `123` from `x` to the opposite
corner times the inverse transport along `321`. This illustrates the necessary
parallel transports and ordering; an unordered product of six face matrices
is not the asserted identity. No additional constraint Jacobian is inserted.

**No topology-preservation assertion.** Exterior links and loops using only
those links are preserved. Holonomies of loops meeting `J`, admissible-field
sector labels, and any smooth/interpolated topological charge are not asserted
to be preserved. Exact frozen graph compatibility is stronger than mere
existence of a plaquette-flat extension: it demands trivial holonomy on *every*
frozen cycle, including noncontractible ones. The construction neither proves
this condition typical nor supplies an unconditional filling of incompatible
boundary data. The parent's integrated estimate and any required treatment of
obstruction/sector data remain separate work.

## 8. Check against the parent's finite statement

Reviewed **Sections 5--6, lines 218--308** of
`rough_region/rough_region_replacement.tex`, SHA-256
`b55b3ed803da1bec281ba84cc5bd21afe2ba43be90a407da46774e8dea1aafd0`.
The draft was read, not edited. Its `T_x, h_x, A_C, S_x, eta_J` agree with
`t_x, h_x, a_c, s_x, epsilon_T` above: maximizing over all frozen edges rather
than just chords makes no difference, since tree residuals vanish.

**Verdict:** the finite compatibility lemma and cap construction are correct
under the stated fixed-`J`, fixed-`rho`, finite-lattice assumptions. No missing
Borel, boundary-connectedness, free-gauge-action, or equivariant-selector
hypothesis is needed. In particular:

- The deterministic forest and fixed root/cap probability laws make the joint
  sampling map Borel. The closed condition `eta_J <= rho` is also Borel; it need
  not itself be open. The strict positive-tolerance condition is open.
- Root coupling (7) proves covariance under all site gauges, including boundary
  gauges and stabilizers, with isolated vertices already included in the draft.
- The joint edited-link density bound, frozen-frame formula, reversed-edge
  bound, and energy constants `48` and `12` follow exactly as in (11)--(20).
  No measurable choice of conditional minimizers enters Sections 5--6.

**One wording correction recommended at lines 263--264:** only the
**edited-link marginal** depends solely on `z|F_J`. If `y` denotes the full
output, as in the displayed construction, its deterministic exterior also
necessarily depends on all of `z`. A precise formulation is

\[
 K_z(x,dy)=\delta_z(dy_{J^c})\,
             k_{z|F_J}(y_J)\,d\mu^J(y_J).
 \tag{24}
\]

This is a notational clarification, not a defect in the given construction.
The integrated theorem and broader cutoff claims are outside this review.

**Supplementary diagnostics:** a fixed-seed (`20261009`), in-memory unit-
quaternion check on the `4^4` torus edited the eight links incident to one
vertex. Its frozen graph had two components, one an isolated vertex; there
were 24 touched plaquettes. Exact and positive-residual fixtures verified the
forest/frame covariance, frozen residual bounds, central conditional-cap
arguments, (15), the incidence constants and both energy bounds. Every cube
in both output configurations was checked against (23). Maximum errors were
`6.68e-16` for frames, `6.38e-16` for edited links, `1.41e-15` for residual
covariance and `2.36e-15` for cube identities. Cap-volume lower-bound checks
at radii `1, 0.7, 0.1, 0.01` passed. These are floating-point diagnostics,
not proofs or statistical validation of the sampling law; the proofs above
supply the normalization and covariance assertions. No test files were written.
