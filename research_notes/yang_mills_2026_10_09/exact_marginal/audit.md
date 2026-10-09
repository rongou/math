# Self audit of exact marginalization and lifted repair

**October 9, 2026.** This file records the author's checks. The separate [integral review](audits/independent_integral_review.md) and [lift review](audits/independent_lift_review.md) are bounded independent agent reviews, not external expert certification or formal proofs. The original fine Wilson moment is a declared input from the third pass.

## Exact factorization and normalization

Every removed link has six incident plaquettes and 18 retained staple links. The condition that no plaquette contains two removed links makes the fine action `E_0 + sum_e E_e`; it does not require disjoint retained supports. Product **probability Haar** then gives the Bessel factor with `F(0)=1` and the exact full normalizer `Z_H`.

The factor `e^(-6H)` is retained. Omitting it without tracking the scalar changes the displayed partition function. The continuous SU(2) Bessel integral is not the finite Q8 or Z2 sum; the tests explicitly distinguish them. Even equal Euclidean norms of staple sums need not give equal Q8 integrals.

## Leading minimum versus remainder

For `m=6-b`, the log-factor is `-H m-r(Hb)` with `r=t-log F(t)`. The cap proof uses radius `(1+t)^(-1/2)`, gives `t(1-cos theta)<=1/2`, and loses `log 24+(3/2)log(1+t)` in volume. It is uniform at zero staple sum. No large-argument Bessel asymptotic is used where `Hb` can be small.

The full log-factor varies by `6H-r(6H)`, so calling it a logarithmic perturbation of `E_0` would be false. The extraction of the boundary minimum is essential. The separate leading and remainder functions have matching norm cusps at `B=0`; their combination is smooth. The repair proof uses no Hessian of the minimum itself.

## Genuine failure of original cell support

Opposite middle staple links at transverse positions `+1` and `-1` fit in no original unit cell. Varying them in a commuting subgroup gives `b=|4+exp(i alpha)+exp(i beta)|` and mixed log-response `(H/6) F'(6H)/F(6H)>0`. A sum of cell-supported functions has zero mixed four-point difference for this pair regardless of the regularity of its summands. For a representation only almost everywhere, Fubini forces the mixed difference to vanish almost everywhere, while the nonzero exact difference persists on open positive-Haar neighborhoods. Thus the argument does not rely solely on a measure-zero identity slice.

The argument concerns the original retained coordinates, with no auxiliary variables or change of lattice scale. It is not a claim that no larger-support description exists; the exact factor is such a description. Nor does support spreading itself imply loss of reflection positivity.

## Reflection inheritance

The explicit removed pattern uses **all** longitudinal coordinates and even transverse coordinates. Adding a parity restriction in the longitudinal direction would not be invariant under a normal site reflection, which reverses a link and shifts its canonical positive starting coordinate by one. The executable negative control catches that distinction.

For an invariant removed set, projection commutes with the reflection and a retained positive-half observable lifts to a fine positive-half observable. The fine reflection-positive quadratic form therefore remains positive. No independent positivity is claimed for the leading or remainder factors, and no generic reflection claim is made for a non-invariant removed set. The inherited local moment does not require such invariance because it is obtained by a pointwise fine lift.

## Complete lifted support

A retained edit `J` affects exactly the removed factors whose full 18-edge support touches it. Each incident original plaquette can identify at most one removed neighbor, so `a<=6n` and the lift `K=J union A` has at most `7n` links. The bound six can be attained by the six parallel transverse-neighbor links of a retained central link.

The energy `E_K` must include the **whole star** of every affected removed link. Keeping only the plaquettes that touch `J` loses terms depending on the removed variable being minimized. A finite exact negative control gives energy 12 for the full lift but 2 for that invalid truncation.

No removed link outside `A` can occur on a plaquette touching `K`: it cannot share one with `J` by definition or with `A` by removed-set independence. This is what licenses both the equality `G_J=min_(u_A) E_K` and the identification `g_J=min_(z_J,u_A) E_K` without hidden frozen variables.

Pointwise `g_J<=G_J<=E_K` and exact marginalization give the stated moment with cost `b_H(n+a)`. This is the actual endpoint measure, not an unrelated conditional ensemble.

## Retained kernel and weighted output

Choose a joint fine minimizer only to establish volume. Freeze its removed coordinates and vary the `n` retained edited coordinates in Haar caps. Stationarity of the smooth fine action and its ordinary incidence Hessian bound give energy at most `g_J+12n/H`. Projecting by minimization can only lower the energy. Thus the sublevel volume costs `n`, not the lift size `n+a`; no measurable minimizer selection is needed in the kernel definition.

The normalized sublevel is Borel and gauge covariant by continuity, compactness and Haar invariance. It is not an efficient sampler or a preservation theorem for fine conditional laws.

The residual change is at most `a r_H`, since only `a` factors can change and each is in `[-r_H,0]`. On a low-minimum rough event, the leading energy gain pays the source-to-output density ratio. Integrating old edited coordinates under probability Haar leaves the exact output marginal with normalizer `Z_H`. This yields measure domination, not just total accepted probability. The exceptional branch is controlled in the same `nu_D` by the inherited minimum tail.

## New inventory and composition scope

Effective labels include removed-star minima with maximum value six and support size 18; they are not individual removed plaquettes. The original curvature-only emptiness threshold is not valid for that inventory. Counting uses at most six label incidences per retained link, degree bound 102, and witness factor 18. The logarithmic-budget constants `4608`, `1728`, `144`, and `10405` are checked independently.

The accepted fixed-root kernel counts all possible current components at each step and therefore admits composition in the same fixed marginal. It does not assert a new independent marginal after every repair. Rejected/retained identity branches lack a small operator bound; repeated instances of the same label are not independent events. Joint fixed-configuration estimates use the overlap of the **lifted** supports, which can overlap even if retained edit supports are disjoint.

## Remaining limitation and validation

A second exact elimination need not factorize over links sharing no original plaquette, because induced factors have larger supports. The sparse operation introduces no new lattice spacing or running coupling. No closure under a true RG map, signed covering expansion, or continuum claim follows.

The 31 tests use exact finite-group probabilities and integer quaternion algebra where appropriate, plus floating-point diagnostics for the continuous one-link integral. Large-argument quadrature is numerically stabilized and not claimed as a rigorous integration certificate. Mutation checks validate specific finite tests, not the universal theorem. Earlier proof hashes and scalar Lean certificates retain their scope.

## Independent review resolutions

The independent reviewer confirmed the sections 1–6 main line subject to the original fine Wilson moment input. Four precision edits were applied: reflection positivity is stated for bounded **real** test functions; the sparse-pattern argument distinguishes plaquettes involving direction zero from those that do not; the kernel density is explicitly relative to product probability Haar **on the edited coordinates**; and the energy identity sums all affected effective labels, while the rough-only sum is bounded by that energy. None changes a constant, hypothesis used in the proofs, or executable check.

The independent scope does not cover section 7's adaptive/composition estimates or the full earlier analytic program. Their checks and proofs remain the author's responsibility; no whole-program independent certification is claimed.
