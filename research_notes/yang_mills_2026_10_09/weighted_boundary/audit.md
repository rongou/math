# Self audit of the weighted comparison

**October 9, 2026.** The main results are written finite-measure and finite-lattice arguments. This is a same-agent self-audit, not independent certification. The [separate third-pass audit](audit_third_pass.md) addresses the imported chessboard application.

## Two different sufficient routes

For a general positive weight, the local marginal density is `r_J = E_mu[Q|F_J]/E_mu Q`, with the **full** normalizer. The event `e_*,J > u` depends only on the frozen touched links, of which there are at most `18|J|`. Hölder gives the declared probability estimate from an `L^r` bound on this projected density. Neither that bound nor useful constants follow merely from local edit stability.

The elementary-cell class takes a different route: prove the required reflection positivity and energy moments **directly under its weighted measure**. This does not claim a local Radon–Nikodym norm bound relative to raw Wilson measure. Keeping these arguments separate avoids silently assuming the general condition for all extensive interactions.

## Exterior-only counterexample

The high-minimum event for one link has raw probability `t` strictly between zero and one because both frustrated and identity staple configurations have open neighborhoods on opposite sides of the threshold. The two-level weight assigns any target probability `s` to that event while staying exactly constant on edited-link fibers. It is positive, finite, gauge invariant, and supported on the 18 frozen staple edges.

The local likelihood norm grows as `s^r t^(1-r) + (1-s)^r(1-t)^(1-r)`. This is precisely the uncontrolled quantity; there is no contradiction with a theorem that assumes its bound. The continuous version is an exponential of a continuous function of the minimum and also changes no edit ratio. Its amplitude is not uniformly bounded as the bias grows.

## Output domination and normalization

The accepted transition is `T(x,dy)=1_A(x) K_J(x,dy)`. On its support, multiply the kinetic energy-drop inequality by the **input-to-output** weight comparison `Q(x) <= exp(dn) Q(y)`. The Haar density bound is with respect to the edited output links only. Integrating the original edited coordinates contributes at most one. The same full `Z_Q` remains in the output integral.

This proves `nu_Q T <= exp[-g+(ell_H+d)n] nu_Q` as measures, not merely a total-mass bound. It controls nonnegative output observables, and absolute values of integrable signed/complex test functions. It does not admit signed base measures or turn an arbitrary output-weighted replacement integral into a source probability.

The accepted kernel has total mass `nu_Q(A)`, not one. A process that stays put on rejected sources is a different kernel; a probability-preserving kernel cannot in general have total output bounded by a constant less than one times the original probability measure.

## Elementary-cell class

The declared family is bounded, real, gauge invariant, translation covariant and site-reflection covariant. The geometric support is an elementary four-cell, including its 32 links. Each cell contains 24 plaquettes; each link belongs to eight cells; each plaquette belongs to four cells. The covariance includes inversion of reversed links, not just relabeling tails.

Centering each potential by its infimum preserves the measure up to a scalar and preserves reflection covariance. The resulting `0 <= W <= epsilon V` gives:

- partition lower bound `Z_W >= exp(-4V a_H)`;
- constrained numerator at most `exp(-H M u+epsilon V)`;
- disseminated star exponent `-Hu+64a_H+16epsilon`;
- after layer-cake and 64-fold Hölder, local moment constant `b_H+epsilon/8` at exponent `H/128`.

The global oscillation occurs only before the chessboard `1/M` power. It is not carried as an `exp(epsilon V)` factor in the final local probability. No cancellation or independence of plaquette variables is used.

An elementary cell cannot meet both strict halves of a site-plane reflection. The conditional half-integral square proves reflection positivity for this class even if individual real potentials have either sign. Positive density and reflection **symmetry alone** do not suffice for interactions crossing both strict halves; the exact antiferromagnetic two-spin control demonstrates that distinction.

Only cells touching edited links can change, so the edit cost is at most `8epsilon n`. For `W=gamma sum s(U_p)^2`, the displayed elementary decomposition has `epsilon=24|gamma|`, and direct affected-plaquette counting improves the edit constant to `24|gamma| n`. The proof does not claim that exact RG retains such support or reflection properties.

## Repair versus exception

The original near-minimum kernel still refers to the **Wilson** energy, not a new minimizer of the perturbed action. Its Wilson energy drop is valid independently of the weight. The edit-oscillation cost accounts for the perturbation.

The low-minimum branch uses `k p^2 >= 96n` for count reduction and kinetic gain. The weighted probability/output domination then has exponent `-k p^2/8+(ell_H+8epsilon)n`. The high-minimum branch is paid under the same weighted measure with exponent `-k p^2/512+(b_H+epsilon/8)n`. The two additional absorption conditions are stated separately.

A direct rough-probability bound from the weighted moment is stronger than the split sum. The split's value is its accepted-output estimate, not improved constants for raw event probability.

## Composition and its limit

Order of measures is preserved by a nonnegative kernel. Thus `nu T_i <= c_i nu` composes into product domination for specified successful repairs. Each low-minimum gate is tested at its actual intermediate state; there is no addition of energy gains all calculated against the initial configuration. Overlapping affected plaquettes therefore cause no invalid telescoping in this statement.

For a fixed-family support policy, sums of the one-step constants account for possible geometries. Arbitrary roots require their location count. An unrestricted history-dependent policy needs its own encoded-history or aggregate bound. One cannot condition on selected support and pretend the old Gibbs conditional law remains unchanged.

For the specified fixed-root adaptive kernel, the current component is chosen afresh and a rejected source gives the accepted kernel zero mass. Its support count gives `sum_n 18^(2(n-1)) exp(-d_H n) = exp(-d_H)/(1-324 exp(-d_H))`. The exponent is `d_H=p^2/32-ell_H-8epsilon`, and `p^2>=384` guarantees the energy/count budget for `k=ceil(n/4)`. The domination factor is less than one only when `d_H>log 325`, not merely when the geometric series converges. The aggregate bound permits repeated **accepted** steps at that root, not an uncontrolled full repair process.

The exceptional identity branch is only `1_B nu`. Repeating it retains mass `nu(B)`, not `nu(B)^2`; it is not dominated by `nu(B) nu`. Joint minimum bounds with maximum plaquette overlap apply to labels in one configuration, not automatically to a history of changed exteriors. This is the principal remaining iteration gap.

## Scope and validation

The 30 tests use exact rational probabilities and finite kernels, integer Q8 link algebra, `4^4` cell geometry, and exact weighted `4x4` two-dimensional Z2 sums. The Z2 state enumeration is justified by the GF(2) incidence image and its equal fiber sizes. The tests do not evaluate a four-dimensional SU(2) partition function.

The source-state checks include positive weights that cancel Wilson suppression, where the theorem's perturbation constants correctly become too large to yield a useful tail. Passing tests is not a proof of the universal analytic claims. No new Lean certificate, external approval, novelty, RG closure, or continuum result is asserted.
