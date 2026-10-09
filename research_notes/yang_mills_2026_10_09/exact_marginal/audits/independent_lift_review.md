# Independent lift, moment, and retained-kernel review

## Scope, provenance, and verdict

**No blocking mathematical defect was found in the sections 4–6 lift/moment/kernel main line.** In particular, the moment cost uses \(n+a\), whereas the retained-cap density cost correctly uses **\(n\), not \(n+a\)**. No dependent star term, removed exterior variable, extra normalizer, or extra power of \(H\) is missing from those estimates.

This is a bounded independent agent proof review, not external expert certification, a formal proof certificate, or an audit of the entire manuscript. I independently checked the support partition, minimum identities, Hessian constant, measurability/covariance, threshold arithmetic, and measure domination. I did not read, run, modify, or rely on the parent's test implementation.

- Review date: October 9, 2026, America/Los_Angeles.
- Reviewed parent: `research_notes/yang_mills_2026_10_09/exact_marginal/exact_marginal.tex`.
- **Reviewed final source SHA-256:** `e90239418b5679c33e8a0ffa11d7a45622f4960dc0d937395ed056cf7e66b9b1` (28,401 bytes), read and verified at `2026-10-09T16:16:33-07:00`.
- Scope: sections 4–6, with the definitions and exact marginal from sections 1–3. The elementary integral/support/RP audit is in `independent_integral_review.md`.
- **Explicit input, not re-proved here:** for every deterministic fine-link set \(K\),
  \[
  \mathbb E_{\mu_H}e^{HE_K/128}\le e^{b_H|K|},\qquad
  b_H=\tfrac12\left(\tfrac32+\log24+\tfrac32\log(8H)\right)
       +\frac{\log2}{64}.
  \]
  This is the third-pass theorem in `boundary_cost/boundary_cost.tex`, SHA-256 `8bbfdee9e0be49d2cd7524ea718d2f489c34a17671ae2b41ded8b06e20498745`. Its entire chessboard/analytic proof is outside this review.

All conclusions below retain the parent's hypotheses: pure finite Wilson measure, probability Haar, `L = 2^m >= 4`, \(H\ge1\), fixed plaquette-disjoint removed set \(D\), and fixed nonempty retained edit \(J\).

## 1. Closure and the exact lifted minimum: confirmed

Write \(n=|J|\), \(A=\{e\in D:F_e\cap J\ne\varnothing\}\), \(a=|A|\), and \(K=J\cup A\). Since each retained link has six incident plaquettes and each contains at most one removed link, \(a\le6n\), and disjointness of retained and removed sets gives \(|K|=n+a\le7n\).

There are exactly two kinds of plaquettes in \(P(K)\):

1. A plaquette with no removed link. It must meet \(J\), so it occurs in \(E_{0,J}\).
2. A plaquette with a removed link. If it meets \(J\), its unique removed link is in \(A\). If it instead meets \(A\), plaquette-disjointness prohibits any second removed link. In either case it belongs to the full star of its unique \(e\in A\).

Conversely, every plaquette in \(E_{0,J}\), and **all six plaquettes** of every star in \(A\), touch \(K\). The pieces are disjoint. Therefore

\[
E_K(u_A,z)=E_{0,J}(z)+\sum_{e\in A}E_e(u_e,z)
\]

is an exact identity, not equality modulo an untracked exterior term. In particular, no variable from \(D\setminus A\) occurs in \(E_K\).

At fixed retained data, the removed variables minimize separately. Thus

\[
G_J(z)=E_{0,J}(z)+\sum_{e\in A}(6-b_e(z))
      =\min_{u_A}E_K(u_A,z),
\]

and, for \(w=z_{R\setminus J}\),

\[
g_J(w)=\min_{z_J}G_J(z_J,w)
      =\min_{z_J,u_A}E_K(u_A,z_J,w).
\]

Both equalities are correct. Retaining only those individual star plaquettes which touch \(J\) would invalidate the first identity: the other star plaquettes still constrain the minimizing \(u_e\). The parent explicitly avoids that error.

All minima are attained on compact products of SU(2). Their values are continuous because the underlying functions are jointly continuous and the minimizing domains are fixed and compact; equivalently, changes of a minimum are bounded by the uniform change of the original function. No uniqueness or differentiability of a minimized function is required, including at \(b_e=0\).

The local frozen dependence is confined to

\[
F_K=\left(\bigcup_{p\in P(K)}\partial p\right)\setminus K
\subset R\setminus J.
\]

A coarse count gives \(|F_K|\le18|K|\). Thus neither the energy/minimum nor the sublevel kernel secretly depends on distant retained data or on deleted variables outside \(A\). Also \(\mathcal E_D-G_J\) and \(W_D-W_J\) are constant during a \(J\)-edit, exactly as required for the later comparison.

## 2. Inherited moments and exceptional tail: confirmed conditional on the declared input

For every full fine configuration \(U\),

\[
0\le g_J(U_{R\setminus J})\le G_J(U_R)\le E_K(U).
\]

The last inequality uses the actual \(U_A\) as one candidate in the minimum. Since \(\nu_D\) is exactly the projection of \(\mu_H\), expectations of retained-coordinate functions agree without a likelihood correction. Applying the explicit fine moment input gives

\[
\mathbb E_{\nu_D}e^{HG_J/128},\quad
\mathbb E_{\nu_D}e^{Hg_J/128}
\le e^{b_H(n+a)}.
\]

The retained marginal's residual weight does not need to be bounded again for this step. Nor is reflection invariance of \(D\) needed: the fine moment input and exact projection already suffice.

Markov at \(v=kp^2/(4H)\) gives precisely

\[
\nu_D(g_J>kp^2/(4H))
\le\min\{1,e^{-kp^2/512+b_H(n+a)}\}.
\]

The factor \(512=128\cdot4\) and cancellation of \(H\) are correct. This is a probability in the **actual retained exterior marginal**, not a conditional bound uniform over frozen exteriors. It is valid for deterministic \(J\); substituting a configuration-selected \(J\) without a separate counting/selection argument would not follow from this theorem.

## 3. Why the cap cost is retained dimension only: confirmed

Fix \(w\), choose any joint minimizer \((v_J,v_A)\) of the smooth fine energy, and **hold \(v_A\) fixed**. For \(e\in J\) vary

\[
U_e(t)=v_e\exp(tX_e),\qquad
X_e\in\mathfrak{su}(2),\qquad h_e=\|X_e\|_{\rm op}\le H^{-1/2}.
\]

Because this is a joint global minimum on a smooth compact manifold, the first derivative of \(E_K\) in this path is zero at \(t=0\). One must use a joint minimizer, not an arbitrary original retained configuration with only its removed variables minimized.

For an individual original plaquette, the product rule, unitarity, and \(\frac12|\operatorname{Tr}M|\le\|M\|_{\rm op}\) give

\[
|s(U_p(t))''|
\le\left(\sum_{e\in\partial p\cap J}h_e\right)^2
\le4\sum_{e\in\partial p\cap J}h_e^2.
\]

This covers inverse-oriented factors as well: their first and second derivative norms are still \(h_e\) and \(h_e^2\). A plaquette not meeting \(J\) has zero derivative, even if it belongs to a lifted star. Each varied link belongs to six plaquettes, so

\[
|E_K''(t)|\le24\sum_{e\in J}h_e^2.
\]

Taylor's integral remainder contributes a factor \(1/2\). Hence

\[
E_K(v_Je^X,v_A,w)\le g_J(w)+12\sum_{e\in J}h_e^2
                  \le g_J(w)+12n/H.
\]

Since \(G_J(y_J,w)\le E_K(y_J,v_A,w)\), the entire product of these **\(n\) retained caps** lies in the desired sublevel. No cap in any removed variable is integrated, so charging \(n+a\) here would be unnecessary. The fixed removed witness is legitimate even when a new minimizer of the removed variables would jump discontinuously.

With \(H\ge1\), the angle radius \(H^{-1/2}\le1\) has Haar mass at least \(1/(24H^{3/2})\). Thus the sublevel volume obeys

\[
v_J(w)\ge(24H^{3/2})^{-n},
\]

and its normalized restriction has density at most

\[
M_J=(24H^{3/2})^n=e^{\ell_Hn},\qquad
\ell_H=\log24+\tfrac32\log H.
\]

The constants 24, 12, and the exponent \(n\) are all justified independently. This argument never differentiates \(G_J\), \(g_J\), or \(|B_e|\) at a cusp.

## 4. Kernel measurability, local dependence, and covariance: confirmed

Define the edited-coordinate density by

\[
k_w(y_J)=\frac{\mathbf1\{G_J(y_J,w)\le g_J(w)+12n/H\}}{v_J(w)}.
\]

Continuity of \(G_J\) and \(g_J\) makes the indicator jointly Borel. Parameter integration makes \(v_J(w)\) Borel, and the cap argument makes it strictly positive for every \(w\). This defines a Borel probability kernel, independent of the original values in \(J\), with the prescribed frozen exterior. Continuity of \(v_J\) is not needed or asserted. The minimizing pair is only an existence witness in the volume proof; no measurable minimizer selection enters the definition.

Gauge transformations preserve each fine plaquette energy and act by Haar-preserving endpoint multiplication on each link. They give bijections of the minimizing domains and of the retained sublevels. Consequently \(g_J(w^h)=g_J(w)\), sublevel volume is preserved, and the normalized-restriction kernel is gauge covariant. This reasoning remains valid when minimizers are nonunique.

For a spatial symmetry preserving \(D\), the same construction is covariant as a *family* under \(J\mapsto\vartheta J\). Invariance of one fixed-\(J\) kernel requires the symmetry to preserve \(J\) as well. Neither kind of covariance asserts that applying the repair kernel preserves reflection positivity of the output measure.

**Precision fix — section 5, lines 334–340:** “with density at most” should explicitly mean **conditional density on the edited coordinates with respect to product Haar on \(\mathrm{SU}(2)^J\)**. Except when all retained links are edited, a kernel freezing the other continuous coordinates has no full-retained-space Haar density. The proof uses the correct edited-coordinate interpretation.

## 5. Effective rough labels and gain arithmetic: confirmed with one wording correction

The declared effective labels are exactly:

- original plaquettes containing no removed link, value \(s(z_q)\), support four retained links;
- removed stars, value \(m_e=6-b_e\), declared support \(F_e\), of size 18 in this lattice class.

**Wording correction — section 6, lines 398–400:** after defining the count of rough labels, “Their values sum exactly to \(G_J\)” should read:

> The values of all effective labels whose declared supports meet \(J\) sum exactly to \(G_J\); the sum over just the rough ones is bounded by \(G_J\).

The subsequent proof uses precisely this valid nonnegative-sum inequality, so this is not a failure of its constants or inference.

For \(\tau=p^2/(2H)\), the strict roughness threshold gives \(G_J(z)>k\tau\) when \(N_p^D(J;z)\ge k\). On the accepted low-minimum branch,

\[
G_J(y)\le kp^2/(4H)+12n/H.
\]

Since \(kp^2\ge96n\),

\[
H(G_J(z)-G_J(y))\ge kp^2/8,
\qquad
N_p^D(J;y)\le\frac{2HG_J(y)}{p^2}
\le k/2+24n/p^2\le3k/4.
\]

Unaffected terms cancel, so this is the required gain in \(\mathcal E_D\), not just in an unrelated local energy. The strict source inequality safely implies the displayed weak gain bound.

A star value can reach six, whereas a plaquette value is at most two. Thus all effective rough labels are empty at \(p^2\ge12H\); the \(4H\) cutoff applies only to the surviving plaquette labels. No eliminated individual plaquette becomes a retained observable, and reducing these effective counts does not reconstruct an original deleted-plaquette inventory.

## 6. Accepted output domination: confirmed

Let \(q(z)=e^{-H\mathcal E_D(z)+W_D(z)}\). On an accepted input/output pair with the same exterior,

\[
\frac{q(z)}{q(y)}
\le\exp[-kp^2/8+a r_H],
\]

because only the \(a\) affected residual terms change, each across a range of width at most \(r_H\). There is no factor two or extra \(H\) in that residual term.

Writing the kernel as \(\delta_w(dw')k_w(y_J)\,dy_J\), test the accepted output measure against any nonnegative measurable \(f(y_J,w)\). Insert the preceding density ratio and \(k_w\le M_J\), then integrate the original \(z_J\) over its probability-Haar space. That source integral is at most one. The remaining output integral is exactly \(Z_H\nu_D(f)\), cancelling the original normalization. Thus

\[
\nu_DT_{J,k}\le
\exp[-kp^2/8+\ell_Hn+a r_H]\nu_D.
\]

The accepted kernel has mass one on accepted sources, so its total output mass equals the accepted source probability. Combining with the exceptional tail from section 2 gives the parent's two-term bound. The additional absorption assumptions correctly yield exponents \(-kp^2/16\) and \(-kp^2/1024\). The direct source-only rough-count estimate also has the stated denominator \(256\), from \(128\cdot2\).

This derivation needs no new restricted partition function, no density of the frozen exterior conditional law, and no claim that the sublevel kernel reproduces the original conditional distribution.

## 7. Independent diagnostics and exclusions

I ran separate, in-memory, Python standard-library checks with seed `20261009` (geometry shuffles used `seed + L`), not the parent's diagnostics:

- Built the full four-dimensional `L=4` and `L=8` link/plaquette incidence structures. Tested the explicit sparse pattern, independently generated greedy plaquette-disjoint patterns, and a six-neighbor saturation pattern.
- Across **33,662** singleton/multilink edit cases, checked \(a\le6n\), exact equality of the fine plaquette set \(P(K)\) with the disjoint union of unremoved affected plaquettes and **whole** affected stars, absence of \(D\setminus A\) from \(P(K)\), and the frozen-support bound. The saturation example attained \(a=6\) for \(n=1\).
- Independently enumerated a finite **Q8 analogue** on an `L=4` torus with one retained edit and two affected removed links: all **512** assignments, grouped into eight retained slices. Direct fine plaquette minimization agreed with the reduced minimum on every slice; minimizing over the retained variable also agreed, giving joint energy 8 for that sampled exterior.
- In that finite analogue the removed minimum was explicitly \(6-\max_i|B_i|\), **not** the continuous SU(2) minimum \(6-|B|\). Therefore this test checks the support/minimization structure without falsely identifying finite-group and SU(2) Haar integrals. Continuous integral diagnostics are recorded separately in the integral audit.

These finite checks are not proofs of a continuous minimizer-cap volume, an analytic moment theorem, or output domination; those steps were checked by the written arguments above. No test files, source files, PDFs, or other parent artifacts were changed.

Not audited here: the entire third-pass chessboard proof; section 7's adaptive/composition/counting claims; an actual continuous minimization or sampling implementation; the parent's reported PDF build, 31 diagnostics, or five mutation rejections; repeated marginalization/RG stability; exceptional-branch contraction; continuum, mass-gap, or novelty claims. The final source's nonempty-family change in section 7 was observed but is not represented as an independent audit of that section.

**Handoff conclusion:** the requested sections 4–6 argument is supported under its stated hypotheses and explicit fine-moment input. The two wording corrections above, plus the RP test-function and plaquette-direction qualifications in the integral audit, are the only outstanding precision points identified in this bounded review.


## Addendum — delta-only verification, October 9, 2026

**New final parent source SHA-256:** `29c5ff27d0fe50c67612ab1af732ab0e0b29b9b8966a234ded914d2a77f2b9f2`, independently matched against `exact_marginal.tex` at `2026-10-09T16:20:57-07:00`.

I inspected only the four requested precision changes and their immediate context:

1. Section 3, line 223 now explicitly restricts the RP statement to bounded **real** retained positive-half functions.
2. Section 3, lines 239–241 now distinguish plaquettes involving direction zero from those containing no removed links.
3. Section 5, lines 336–337 now specify conditional edited-coordinate density relative to product probability Haar on \(\mathrm{SU}(2)^J\).
4. Section 6, lines 401–402 now say **all affected effective labels** sum to \(G_J\), while the rough-label sub-sum is only bounded by \(G_J\).

**All four comments are resolved in this snapshot.** The original audit text and its earlier source hash are preserved as historical provenance; its precision comments are no longer outstanding. No new mathematical concern arose from these wording changes. This was not a new full review, and no mathematical tests or parent build checks were run.

The original independent scope is unchanged: the sections 4–6 lift/moment/kernel main line, using the sections 1–3 definitions and the original fine Wilson moment as an **explicit input**. This addendum does **not** audit section 7 or the whole third-pass/chessboard proof. All original limitations on certification and downstream conclusions remain. Only audit addenda were appended; the parent proof was not edited.
