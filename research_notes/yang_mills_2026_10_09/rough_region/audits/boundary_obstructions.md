# Boundary obstructions to rough-region replacement

**October 9, 2026. Scope:** finite, unrestricted SU(2) link configurations; no continuum or integrated-comparison theorem is asserted. The six-staple candidate is correct, including its normalization and open-set strengthening.

**Inputs read.** `research_notes/yang_mills_2026_10_09/audits/cutoff_bridge_obligations.md`, §5; and `preprints/The-canonical-massive-continuum-limit-of-the-two-dimensional-O3-model-October-4-2026/build/sections/comparison.tex`, lines 222–327 (`lem:editable-regions`) and 467–507 (`eq:orig-22`). O3 does **not** fill arbitrary frozen spins: its preceding region selection supplies exterior Lipschitz control and a collar. An analogous gauge boundary-compatibility hypothesis requires proof. The parent's integration argument is not repeated here.

## 1. Conventions and the claim being tested

Count each geometric plaquette once. Reverse links are inverses. Write
\[
 r(V)=\|I-V\|_{\rm op},\qquad
 w(V)=1-\tfrac12\operatorname{Tr}V=\tfrac12r(V)^2,
 \qquad S_W=H\sum_p w(U_p).
\]
Indeed SU(2) eigenvalues are \(e^{\pm i\theta}\), \(0\le\theta\le\pi\), so
\(r=2\sin(\theta/2)\) and \(w=1-\cos\theta\). Traces are real. Conjugating or inverting a plaquette changes neither quantity.

For editable links \(J\), freeze all other links to \(b\). Let \(A(J)\) contain **all** plaquettes touching \(J\), including crossing plaquettes, and define
\[
 E_J(U\mid b)=\sum_{p\in A(J)}w(U_p),\quad
 E_{\min}(b)=\min_U E_J(U\mid b),\quad
 k_t(U)=\#\{p\in A(J):r(U_p)>t\}.
\]
The minimum exists by compactness. The proposed all-small target is
\(\mathcal F_t(b)=\{U:r(U_p)\le t\text{ for every }p\in A(J)\}\).
A sampling kernel supported there cannot exist when this set is empty.

## 2. Six-staple frustration: an explicit four-dimensional configuration

Work inside the ordinary box with vertices \(\{-2,-1,0,1,2\}^4\). Let \(x=0\), \(y=e_0\), and \(J=\{(x,y)\}\), with its variable denoted \(U\). Its six plaquettes correspond to \(\nu=1,2,3\) and \(s=\pm1\). Define the frozen detour transporter \(V_{\nu,s}\) along
\[
 x\longrightarrow x+se_\nu
 \longrightarrow y+se_\nu\longrightarrow y.
\]
These paths have 18 distinct noncentral edges: their transverse edges use distinct signed directions at \(x,y\), and their middle edges occupy distinct parallel translates of \(J\). Thus their values can be prescribed independently.

Set every frozen link to \(I\), except the three positively oriented links
\((x+e_\nu,y+e_\nu)\), which are \(-I\). Then
\[
 V_{\nu,-}=I,\qquad V_{\nu,+}=-I.
\]
Orient each affected plaquette from \(x\) along \(J\), returning along its detour. Its holonomy is \(UV_{\nu,s}^{-1}\): three are \(U\), three \(-U\). This is an actual link assignment, not an independently specified, potentially inconsistent plaquette list. Additional frozen plaquettes may be rough; no exterior regularity was assumed.

Put \(a=\tfrac12\operatorname{Tr}U\). Exactly,
\[
 \boxed{E_J(U\mid b)=3(1-a)+3(1+a)=6},\qquad
 r(U)^2=2-2a,\quad r(-U)^2=2+2a.
\]
If \(a\ge0\), the three \(-U\) plaquettes have curvature at least \(\sqrt2\); if \(a\le0\), the three \(U\) plaquettes do. Consequently
\[
 \inf_U\max_{p\in A(J)}r(U_p)=\sqrt2,\qquad
 k_t(U)\ge3\quad(0\le t<\sqrt2).
\]
Equality in the minimax formula is attained by any traceless \(U\). At \(t=\sqrt2\), the all-small set is precisely the traceless two-sphere, of SU(2) Haar measure zero: even feasibility without slack need not permit an absolutely continuous filling density.

With normalized Haar measure, the conditional law of \(U\) is **exactly Haar for every finite \(H\)**: its Boltzmann factor is the constant \(e^{-6H}\). Thus \(\Pr(k_t\ge3\mid b)=1\), while \(E_J-E_{\min}\equiv0\). This does not contradict the parent's arbitrary-boundary **excess-above-minimum** tail theorem; that theorem cannot make this bad-plaquette event rare.

### Open boundary data, not only central signs

Fix \(0<\delta<\sqrt2-t\), and impose the strict inequalities
\[
 \|V_{\nu,-}-I\|_{\rm op}<\delta,\qquad
 \|V_{\nu,+}+I\|_{\rm op}<\delta.
 \tag{1}
\]
They define a nonempty open set of frozen-link data. For example, perturbing each of the 18 edges by less than \(\delta/3\) suffices: telescoping a product of three unitaries bounds its change by the sum of their changes.

For any \(U\),
\[
 |r(UV^{-1})-r(UV_0^{-1})|
 \le\|V-V_0\|_{\rm op}.
\]
The same sign choice according to \(a\) therefore gives **at least three** affected plaquettes with curvature \(>\sqrt2-\delta>t\). Thus \(\mathcal F_t(b)=\varnothing\) throughout (1). Every nonempty such open set has positive product Haar measure and positive frozen-data marginal under the finite-volume Wilson law, whose density is everywhere positive. This is not a uniform-in-\(H\) lower probability estimate.

Also \(|\operatorname{Tr}M|/2\le\|M\|_{\rm op}\) implies
\[
 |E_J(U\mid b)-6|\le6\delta,\qquad
 E_{\min}(b)\ge6-6\delta,\qquad
 \operatorname{osc}_U E_J\le12\delta.
 \tag{2}
\]
For the target \(t=H^{-1/2}(\log H)^P\to0\), a fixed sufficiently small \(\delta\) works for all sufficiently large \(H\). A gauge change conjugates plaquette holonomies and preserves every obstruction above; the displayed central signs merely specify a convenient representative.

## 3. Frozen-loop obstruction, with a sharp finite-area bound

Let \(D\) be a rectangular lattice disk with \(m\) plaquettes, whose perimeter links are frozen. Suppose its plaquettes belong to \(A(J)\). Write \(h_C\) for its fixed perimeter holonomy and
\(\alpha=\arccos(\tfrac12\operatorname{Tr}h_C)\in[0,\pi]\).

Peel the rectangle one plaquette at a time, row by row. Replacing the peeled boundary arc multiplies the based boundary word by a transported plaquette or its inverse. Iteration gives an **ordered** product of conjugated plaquettes, each used once. No commutation of plaquettes is assumed. The SU(2) angle is conjugation-invariant and subadditive, hence
\[
 \alpha\le\sum_{p\in D}\theta_p,\qquad
 \boxed{\max_{p\in D}r(U_p)\ge2\sin\frac{\alpha}{2m}},\qquad
 \boxed{\sum_{p\in D}w(U_p)\ge m\left(1-\cos\frac\alpha m\right)}.
 \tag{3}
\]
For completeness, if \(\theta(A)+\theta(B)\le\pi\), quaternion multiplication gives
\(\tfrac12\operatorname{Tr}(AB)\ge\cos(\theta(A)+\theta(B))\); otherwise subadditivity is automatic. This proves the angle inequality.

For the energy inequality, the case \(\alpha=0\) is trivial. Otherwise reduce the nonnegative angles proportionally until their sum is \(\alpha\), which can only reduce \(1-\cos\theta\). For two resulting angles \(a,b\), their sum is at most \(\pi\), and
\[
 (1-\cos a)+(1-\cos b)
 =2-2\cos\tfrac{a+b}{2}\cos\tfrac{a-b}{2}
 \ge2\left(1-\cos\tfrac{a+b}{2}\right).
\]
Repeatedly average a maximum and a minimum. The variance decreases by half their squared difference, hence tends to zero; energy never increases. This proves (3). The case \(m=1\) is immediate.

Thus, for \(0\le t\le2\), a necessary condition for an all-small fill is
\[
 \alpha\le 2m\arcsin(t/2).
 \tag{4}
\]
Whenever its right side is less than \(\pi\), the strict reverse inequality specifies an open obstruction set of frozen perimeter data. Taking one perimeter link \(-I\), all others \(I\), realizes \(\alpha=\pi\). Nontrivial frozen holonomy rules out **exact** flatness for any finite \(m\), but not necessarily small curvature on a sufficiently large disk.

Here is explicit sharpness. On a width-\(m\), height-one strip, \(m\ge2\), set horizontal links to \(I\), and vertical links at column \(j\) to
\(A_j=\exp(i j\alpha\sigma_3/m)\), where \(\sigma_3=\operatorname{diag}(1,-1)\). Freeze the perimeter and edit the internal vertical links. Then every disk plaquette is \(A_jA_{j-1}^{-1}=\exp(i\alpha\sigma_3/m)\), attaining both bounds in (3). Extending these links independently of coordinates 2 and 3, with other links \(I\), gives an explicit four-dimensional configuration; all other plaquette orientations are flat. This proves sharpness for these boundary data, not a general filling theorem.

## 4. Flat extension, small curvature, and topology are different issues

**Exact flatness:** the loop product calculation forces identity holonomy around every rectangle tiled by exactly flat plaquettes. Conversely, boundary data already of pure-gauge form \(U_{xy}=g_xg_y^{-1}\) extend flat by assigning arbitrary values of \(g\) at the remaining vertices; every plaquette telescopes to \(I\). Neither assertion is an extension theorem for arbitrary curved boundary data.

**Small curvature:** (3)–(4) quantify a finite-area compatibility condition, not an integer sector. Extra area can distribute nontrivial holonomy into small plaquettes, as the strip demonstrates. Conversely, on a periodic lattice of length \(L_0\), choose \(0<\phi\le\pi\). Constant links
\(U_0=\exp(i\phi\sigma_3/L_0)\), \(U_1=U_2=U_3=I\), have all plaquettes flat but cycle holonomy \(\exp(i\phi\sigma_3)\ne I\). A periodic gauge transformation only conjugates this holonomy; it cannot make all links identity.

**Unrestricted discrete topology:** with fixed exterior, the configuration space is \(SU(2)^J\), hence path connected. Explicitly, each link has a path \(\exp(is\theta\,\mathbf n\cdot\boldsymbol\sigma)\) to its assigned value; take their product paths. Prescribed gauge transformations at finitely many boundary vertices extend arbitrarily to the remaining vertices. Even vertex samples of a continuous boundary map of nonzero degree produce a flat discrete pure-gauge filling by the preceding construction. That does **not** extend the prescribed continuous map between vertices.

Accordingly, the degree warning in the prior audit's §3, item 3 must not be read as a discrete-link no-go. A degree argument needs additional continuous interpolation, bundle, or regularity constraints that are actually retained. Primary context: M. Lüscher, *Topology of lattice gauge fields*, Commun. Math. Phys. **85** (1982), 39–48, abstract and §1, DOI `10.1007/BF02029132`, treats integer charge under small-action restrictions. No such charge classification or four-cell extension theorem is assumed here.

## 5. What a replacement theorem must retain or pay

1. **Feasibility is a hypothesis, not an entropy estimate.** Prove a compatible center with strict curvature slack on the complete affected set, using genuinely controlled exterior data. No finite density allowance can sample an empty target. These examples do not refute a theorem restricted to an appropriately selected good collar.
2. **Retain unavoidable defects and boundary dependence.** If the exterior is unchanged, record the residual bad inventory and relevant relative staple/based-loop holonomies, with transport paths and ordering. In the star at least three defects remain. Starting from \(U=I\), making the three old \(-U\) plaquettes good forces all three formerly good \(U\) plaquettes bad when \(t<\sqrt2\), since their squared curvatures sum to 4. Thus “remove the old inventory without new bad plaquettes” fails explicitly. The required labels here are geometric/holonomy data, not invented disconnected topological sectors.
3. **Only excess energy can be released at fixed boundary.** For every edit,
   \[
   H(E_J(U\mid b)-E_J(U'\mid b))
   \le H(E_J(U\mid b)-E_{\min}(b)).
   \]
   This is zero in the balanced star; on (1) it is at most \(12H\delta\). The unavoidable baseline is at least \(H(6-6\delta)\), not the desired small-field scale \(Ht^2\). A boundary-dependent minimum cannot be dropped as a volume-only scalar. Its suppression can instead be paid in the exterior marginal, but a uniform conditional bad-count tail does not supply that payment.
4. **Changing the exterior is a different edit.** Enlarge \(J\) to move constraining staples/loops, or retain a flux-carrying region with enough area to satisfy (4). Count every newly affected plaquette, link, and eligibility query, together with entropy and energy costs. Merely enlarging a collar without checking its new fixed boundary is insufficient.

**Bottom line:** the arbitrary-boundary all-small assertion fails on an open, positive-measure boundary set. The parent's excess-energy theorem remains compatible with this failure. A successful integrated argument must establish compatible-region selection, retain defects, or pay for obstructed exterior data—not delete them.

**Checks:** direct finite-link/quaternion checks verified the 18-edge geometry and six plaquette orientations, constant energy and forced bad counts (1,000 samples), open perturbation bounds (3,000 samples), and strip sharpness for \(m=2,\ldots,24\). These are sanity checks; the displayed elementary derivations are the proofs.
