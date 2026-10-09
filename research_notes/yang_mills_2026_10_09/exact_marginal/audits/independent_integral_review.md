# Independent integral, support, and reflection review

## Scope and source snapshot

**Verdict: the proposed elementary claims are correct under the stated conventions, with the minor wording qualifications below. No blocking mathematical error was found in this bounded review.**

This is an independent agent proof review, not external expert certification, a formal verification, or a novelty assessment. I reconstructed the calculations and ran separate in-memory diagnostics; I did not read, run, modify, or rely on the parent's tests.

- Review date: October 9, 2026, America/Los_Angeles.
- Reviewed parent: `research_notes/yang_mills_2026_10_09/exact_marginal/exact_marginal.tex`.
- **Reviewed final source SHA-256:** `e90239418b5679c33e8a0ffa11d7a45622f4960dc0d937395ed056cf7e66b9b1` (28,401 bytes), read and verified at `2026-10-09T16:16:33-07:00`.
- Principal scope: sections 1–3 and the residual-support statement in section 4. The separate `independent_lift_review.md` covers the requested sections 4–6 main line.
- Local conventions checked in `boundary_cost/boundary_cost.tex`: probability Haar, Wilson normalization, lattice size, cap bound, and site-reflection convention. Source SHA-256: `8bbfdee9e0be49d2cd7524ea718d2f489c34a17671ae2b41ded8b06e20498745`.
- Original elementary-cell class checked in `weighted_boundary/weighted_boundary.tex`. Source SHA-256: `ae5f41176f97d21f895855b42b9ab6f448905b5b3d1ea96acbb579eb5934fd8e`.

The parent's `D` is the user's removed set `I`; its `r(t)` is the user's remainder `R(t)`. Here the retained set is denoted `R` only when following the parent notation.

## 1. Exact one-link integral and factorization: confirmed

Use the actual model: a four-dimensional periodic cube with `L = 2^m >= 4`, each geometric plaquette counted once, one variable for each positively oriented link, inverse on the reverse, probability Haar, and

\[
s(U_p)=1-\tfrac12\operatorname{Tr}U_p.
\]

For a link \(e=(x,x+\hat\mu)\), the consistently oriented detours from its source to its target are, for \(\nu\ne\mu\),

\[
\begin{aligned}
S_{+\nu}&=U_{x,\nu}U_{x+\hat\nu,\mu}U_{x+\hat\mu,\nu}^{-1},\\
S_{-\nu}&=U_{x-\hat\nu,\nu}^{-1}U_{x-\hat\nu,\mu}
                 U_{x-\hat\nu+\hat\mu,\nu}.
\end{aligned}
\]

Cyclic invariance and invariance of the SU(2) trace under inversion give the plaquette terms \(1-\frac12\operatorname{Tr}(u_eS_{\pm\nu}^{-1})\). In unit-quaternion coordinates, \(\frac12\operatorname{Tr}(uv^{-1})=u\cdot v\). Hence

\[
E_e=6-u_e\cdot B_e,\qquad B_e=\sum_{j=1}^6s_{ej},\qquad
0\le b_e=|B_e|\le6,\qquad \min_{u_e}E_e=6-b_e.
\]

No plaquette contains two removed links, so every detour uses retained links only. Moreover, the entire energy is exactly \(E_0+\sum_{e\in D}E_e\), with **no duplicated plaquettes**. Integrating the removed variables at fixed retained configuration therefore factorizes. Shared retained links do not invalidate this conditional factorization and do not imply independence under the marginal.

Probability Haar on \(S^3\) gives

\[
\int e^{H u\cdot B}\,du
=\frac2\pi\int_0^\pi e^{Hb\cos\theta}\sin^2\theta\,d\theta
=F(Hb),\qquad F(t)=\frac{2I_1(t)}t.
\]

The Bessel normalization was cross-checked against the primary NIST DLMF integral representation, equation (10.32.2), with order \(\nu=1\), accessed October 9, 2026: `https://dlmf.nist.gov/10.32.E2`. The angular integral and its normalization also follow directly from spherical Haar measure.

Thus the retained Haar density is exactly

\[
Z_H^{-1}e^{-HE_0(z)}\prod_{e\in D}e^{-6H}F(Hb_e(z)).
\]

The coupling argument is **\(Hb_e\), not \(2Hb_e\)**. The normalizer is the original \(Z_H\); there is no gauge-volume factor. This conclusion is for a fixed removed set in the pure Wilson model, not a source-selected set or an arbitrary extra weighted interaction.

## 2. Remainder, cap constant, zero sum, and scaling: confirmed

The series

\[
F(t)=\sum_{j\ge0}\frac{(t^2/4)^j}{j!(j+1)!}
=1+t^2/8+O(t^4)
\]

gives \(F(0)=1\). At \(B_e=0\), every removed-link value minimizes the star, its integral is \(e^{-6H}\), and no normalized direction \(B_e/b_e\) should be introduced.

For \(t\ge0\), set \(r(t)=t-\log F(t)\). The sign in the split is correct:

\[
e^{-6H}F(Hb)=\exp[-H(6-b)-r(Hb)].
\]

Since \(F(t)\le e^t\), \(r(t)\ge0\). For the **geodesic angle** cap of radius \(0<\rho\le1\),

\[
\operatorname{Haar}(C_\rho)
=\frac2\pi\int_0^\rho\sin^2\theta\,d\theta
=\frac{\rho-\sin\rho\cos\rho}{\pi}
\ge\frac{\rho^3}{24}.
\]

For example, \(\sin\theta\ge\theta/2\) on this interval gives the stronger intermediate lower bound \(\rho^3/(6\pi)\). Taking \(\rho=(1+t)^{-1/2}\),

\[
e^{-r(t)}
\ge \frac{\rho^3}{24}\exp[-t\rho^2/2]
\ge \frac{e^{-1/2}}{24(1+t)^{3/2}}.
\]

Consequently the proposed \(\frac12+\log24+\frac32\log(1+t)\) bound is valid, including at zero. The slightly sharper first term \(t/[2(1+t)]\) is available but unnecessary. Also \(0<F'/F<1\) for \(t>0\), by the positive series and the tilted-Haar expectation of \(\cos\theta\). Thus the parent's derivative statement is correct.

Important qualifications:

- These integral/remainder identities hold for \(H\ge0\); the parent uses \(H\ge1\). The positive mixed derivative in the nonclosure argument requires \(H>0\).
- \(r(0)=0\), but \(r(H|B|)\) and \(6-|B|\) separately need not be differentiable at \(B=0\). Their combination \(-6H+\log F(H|B|)\) is smooth there. The final draft explicitly handles this distinction.
- Only the residual exponent has the uniform \(O(\log H)\) bound. The full log-integral factor has oscillation \(\log F(6H)=6H-r(6H)\), not \(O(\log H)\). The minimum cannot be discarded as an exterior-independent constant.

## 3. Affected support and residual oscillation: confirmed

For a retained edit \(J\), let

\[
A=\{e\in D:F_e\cap J\ne\varnothing\},
\]

where \(F_e\) is the union of its six detours. This is exactly the set of removed links sharing a plaquette with some link in \(J\). It is the set of *potentially* changed factors; a particular edit may leave some of them numerically unchanged.

Each retained link has six incident plaquettes, each containing at most one removed link. Therefore \(|A|\le6|J|\). Each \(F_e\) has 18 distinct retained links in the stated lattice-size class. The six rather than eighteen in the affected-star count uses the plaquette-disjointness hypothesis essentially.

For configurations equal outside \(J\), only terms indexed by \(A\) can change in \(W_D=-\sum_e r(Hb_e)\). Since each lies in \([-r_H,0]\),

\[
|W_D(z)-W_D(y)|\le |A|r_H,
\qquad r_H=\tfrac12+\log24+\tfrac32\log(1+6H).
\]

There is **no extra factor two** and **no extra factor \(H\)**. This is a bound on the residual log-weight, not on the complete marginal log-density.

## 4. Sparse pattern and inherited RP: confirmed with notation qualifications

The proposed pattern contains \(L(L/2)^3=V/8\) direction-zero links. A plaquette involving direction zero has its two parallel direction-zero links at opposite parity in one transverse coordinate, so at most one is removed. A plaquette not involving direction zero has no removed links.

For reflection \(x_i\mapsto2a-x_i\):

- If \(i=0\), the positive representative of a reflected direction-zero link starts at \(2a-x_0-1\). Its matrix must be inverted. The unrestricted \(x_0\) makes the pattern invariant.
- If \(i\ne0\), the transverse parity is preserved because \(2a-x_i\equiv x_i\pmod2\).

Thus invariance under all integer-site coordinate reflections is correct. It does not claim invariance under arbitrary coordinate permutations, unit transverse translations, or transverse half-integer-plane reflections.

If a reflection preserves \(D\), the retained projection commutes with it. A retained positive-half observable lifts to a fine positive-half observable, including the appropriate fixed-plane variables. The claimed equality of RP quadratic forms and inheritance from the fine measure follow directly. This concerns the **complete marginal**, not positivity of each induced interaction, a conditioned law, or an arbitrary non-invariant removal pattern.

Two small wording fixes are advisable in the reviewed snapshot:

1. **Section 3, lines 223–227:** specify bounded **real** test functions, as in the third-pass convention, or define reflection of complex functions anti-linearly, \(\Theta f=\overline{f\circ\vartheta}\). A purely geometric pullback without conjugation would make the displayed inequality false for \(f\equiv i\).
2. **Section 3, line 239:** replace “A plaquette has two parallel direction-zero links” with “A plaquette involving direction zero has two parallel direction-zero links”; the other plaquettes have none. This does not change the argument.

## 5. Failure of original elementary-cell additivity: confirmed

For one removed link at the origin in direction zero, vary the parallel middle links at transverse coordinates \(+1\) and \(-1\), with the same positive direction-zero orientation. The explicit detours above show that their contributions are \(e^{i\alpha}\) and \(e^{i\beta}\), not one with a spurious opposite sign. Therefore

\[
b^2=18+8\cos\alpha+8\cos\beta+2\cos(\alpha-\beta).
\]

At zero, \(b=6\), \(b_\alpha=b_\beta=0\), and \(b_{\alpha\beta}=1/6\). The proposed derivative follows:

\[
\partial_\alpha\partial_\beta\log F(Hb)\big|_{0,0}
=\frac H6\frac{F'(6H)}{F(6H)}>0.
\]

The two links cannot belong to one original unit four-cell: in that transverse coordinate they are separated by two sites, including on the period-four torus. No retained original plaquette contains both either. Hence the \(-HE_0\) contribution cannot cancel the displayed mixed dependence.

For arbitrary Borel cell potentials, use rectangular four-point differences, not derivatives of the proposed summands. Each summand depends on at most one varied link, so its rectangular difference vanishes. The exact smooth log-density has a nonzero difference for sufficiently small choices. This proves the pointwise obstruction without assuming smooth potentials.

**The final draft's added Haar-a.e. argument at lines 213–218 is sufficient.** Fubini makes the rectangular difference of an a.e. additive representation vanish a.e. in the common exterior and four independent link values. The continuous exact rectangular difference is nonzero on an open neighborhood of the displayed choice; product Haar assigns that neighborhood positive mass. Thus the identity slice is not being used as an unjustified restriction of an a.e. equality.

This rules out the indicated representation on original cells, even without imposing gauge invariance on the candidate cell terms. It does not rule out larger cells, auxiliary variables, special boundary restrictions, or all other kinds of representation.

## 6. Independent in-memory diagnostics

All checks below were separate Python standard-library programs supplied through standard input, with bytecode writes disabled. No test scripts or numerical artifacts were saved.

- Compared an 80-digit Decimal positive series for \(F\) against independently coded adaptive angular quadrature at ten values \(t=0,10^{-9},10^{-6},0.001,0.1,1,6,60,600,1000\), using a scaled exponential to avoid overflow. The largest observed relative discrepancy was \(2.687\times10^{-16}\). This is an observed floating-point comparison, not a certified quadrature error bound.
- Checked the cap lower bound at five radii, the remainder bound and derivative sign on the ten-point grid (away from zero for the strict sign), and the split identity at fifteen \((H,b)\) pairs including \(b=0\). Maximum observed split relative discrepancy: \(2.8\times10^{-78}\).
- Independent central mixed differences at \(H=0.01,1,10,100\), with angle step \(10^{-5}\), agreed with the displayed derivative to relative error below \(3.34\times10^{-11}\).
- Enumerated the `L=4` and `L=8` geometries: 48 site-reflection checks for the explicit pattern; no common cell for the witness pair in either volume; exact detour support and plaquette-incidence checks. Across the explicit pattern, seeded greedy disjoint patterns, and a six-neighbor saturation example, 33,662 singleton/multilink closure cases passed. The general factor six is attained by the saturation example.
- On a seeded `L=4` noncommuting quaternion-group configuration, all 1,024 star orientation/endpoint-covariance identities and all 1,536 plaquette gauge-invariance checks passed using exact integer arithmetic.

These finite quaternion checks test algebra and geometry, not the continuous SU(2) integral or a four-dimensional partition function. The numerical checks supplement, rather than replace, the written arguments above. No independent claim is made here about the parent's PDF build, reported test counts, mutation tests, or later RG/composition conclusions.


## Addendum — delta-only verification, October 9, 2026

**New final parent source SHA-256:** `29c5ff27d0fe50c67612ab1af732ab0e0b29b9b8966a234ded914d2a77f2b9f2`, independently matched against `exact_marginal.tex` at `2026-10-09T16:20:57-07:00`.

I inspected only the four requested precision changes and their immediate context:

1. Section 3, line 223 now explicitly restricts the RP statement to bounded **real** retained positive-half functions.
2. Section 3, lines 239–241 now distinguish plaquettes involving direction zero from those containing no removed links.
3. Section 5, lines 336–337 now specify conditional edited-coordinate density relative to product probability Haar on \(\mathrm{SU}(2)^J\).
4. Section 6, lines 401–402 now say **all affected effective labels** sum to \(G_J\), while the rough-label sub-sum is only bounded by \(G_J\).

**All four comments are resolved in this snapshot.** The original audit text and its earlier source hash are preserved as historical provenance; its precision comments are no longer outstanding. No new mathematical concern arose from these wording changes. This was not a new full review, and no mathematical tests or parent build checks were run.

The original independent scope is unchanged: sections 1–3 and the residual-support statement in section 4, with the companion audit's separately stated sections 4–6 scope. This addendum does **not** extend review to section 7 or to the whole third-pass/chessboard proof. All original limitations on certification and downstream conclusions remain. Only audit addenda were appended; the parent proof was not edited.
