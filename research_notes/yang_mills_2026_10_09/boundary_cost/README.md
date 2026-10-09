# Marginal boundary costs and partial cooling

**Third research pass, October 9, 2026.** This adds a statistical cost for boundary-forced energy in the **raw Wilson measure**, a near-minimum replacement kernel, and a counted tail for actual rough-link components. It does not assume arbitrary frozen boundaries can be made smooth. **No continuum construction, cutoff comparison, mass-gap proof, or novelty claim is made.**

**Follow-up:** the [fourth pass](../weighted_boundary/README.md) now proves a one-region weighted comparison for bounded reflection-symmetric elementary-cell interactions, identifies the missing marginal-density condition for general weights, and controls specified accepted-repair compositions. It does not establish general RG/signed-covering closure. The statements below retain their third-pass scope.

Read the [proof](boundary_cost.pdf), [LaTeX source](boundary_cost.tex), [self-audit](audit.md), and [source ledger](sources.md). The first two passes' proof sources are unchanged.

## Main bound

Use the preceding pass's four-dimensional SU(2) Wilson model with probability Haar and weight `exp(-H E)`, `H >= 1`. This pass is restricted to **periodic cubes of side `L = 2^m`, `m >= 2`**. Let `J` be a fixed set of `n` edited links, `E_J` include every affected plaquette, and `e_*,J(z)` be its minimum with exterior `z` frozen. Set

\[
a_H=\tfrac32+\log24+\tfrac32\log(8H),\qquad
b_H=\tfrac12a_H+\frac{\log2}{64}.
\]

The proof gives

\[
\mathbb E_{\mu_H} e^{H E_J/128}\le e^{b_H n},\qquad
\Pr_{\mu_H}(e_{*,J}\ge v)\le\min\{1,e^{-Hv/128+b_Hn}\}.
\]

The minimum estimate is in the **actual Wilson exterior marginal**, not conditional on an arbitrary fixed exterior. It pays for high-minimum exteriors without contradicting the frustrated star's conditional energy `E_J = e_* = 6`.

The proof combines a global product-cap lower bound for `Z_H`, directly derived **site-reflection positivity**, the standard event chessboard inequality, reflected side-two stars, and a 64-class link decomposition. Layer-cake integration and Hölder account for overlap without asserting independence. The imported chessboard theorem is explicitly identified; the application is a written argument, not Lean-certified analysis.

For one link there is a sharper bound

\[
\Pr(e_*\ge u)\le\min\{1,e^{-Hu+64a_H}\},\qquad
\Pr(\mathcal D\ge d)\le\min\{1,e^{-Hd/12+64a_H}\},
\]

where `D` is the preceding pass's pairwise staple-holonomy mismatch. This supplies a raw marginal rarity estimate that was absent in the second pass.

## A replacement that retains the unavoidable minimum

For every frozen exterior, sample the edited links uniformly from

\[
B_J(z)=\{y:E_J(y,z)\le e_{*,J}(z)+12n/H\}.
\]

The previous minimizer-cap lemma gives this sublevel set Haar volume at least `(24 H^(3/2))^(-n)`. Its normalized restriction is therefore a **Borel, gauge-covariant kernel with explicit density bound**, without choosing a minimizer measurably. It freezes all exterior links. This is an existence construction, not an efficient sampling algorithm.

If the source has at least `k` rough affected plaquettes at threshold `p/sqrt(H)`, and

- `e_*,J <= k p^2/(4H)`, and
- `k p^2 >= 96n`,

then every output has at most `3k/4` rough affected plaquettes and scaled energy gain at least `k p^2/8`. Individual new rough plaquettes are allowed; the **total count** decreases.

With the additional density budget `k p^2 >= 16n(log 24 + 1.5 log H)`, the literal positive-weight replacement integral is bounded by `exp(-k p^2/16)`. The exceptional high-minimum label has raw probability at most

\[
\exp[-kp^2/512+b_Hn].
\]

**The scopes cannot be merged silently:** the replacement integral evaluates the weight at the output and is not a general reweighted probability; the exceptional-label bound is for the raw Wilson measure only.

## Actual rough components and selection costs

For any fixed `J`, without forest compatibility,

\[
\Pr(N_p(J)\ge k)\le\min\{1,e^{-kp^2/256+b_Hn}\}.
\]

Let the rough-link set contain every link incident to a rough plaquette, with adjacency defined by sharing any plaquette. For its actual source-dependent component `C_p(e0)` through a fixed root,

\[
\Pr(|C_p(e_0)|\ge n)
\le\min\{1,18^{2(n-1)}e^{-n[p^2/1024-b_H]}\}.
\]

Every selected link has a rough witness; one plaquette witnesses at most four links. A fixed-size connected subset therefore has at least `n/4` rough affected plaquettes. Summing over possible subsets pays the selection cost. **No Gibbs formula is used after conditioning on which region was selected.** The tail decreases exponentially when `p^2/1024-b_H > 2 log 18`, eventually true for `p = (log H)^P`, `P > 1/2`.

For several fixed retained-minimum labels, the proof also gives an exponential moment with loss equal to the maximum affected-plaquette overlap. Disjoint link sets can still have overlap up to four.

## Remaining analytic task

The raw statistical and partial-cooling statements do **not** yet provide:

1. An all-small filling or the previous forest compatibility for every selected region. Flat winding holonomy gives a zero-energy counterexample to identifying those notions.
2. Removable energy on the high-minimum class. The frustrated star still cannot release any energy at its fixed boundary.
3. A uniform replacement theorem for an adaptively selected sequence of regions, with all density costs and energy gains tracked along actual outputs.
4. Control of the exceptional labels under general positive weights, signed covering expansions, or interactions generated by exact RG.
5. The fixed-physical-size partition-function defect bound, cutoff comparison, or a nontrivial continuum theory.

**Best next target:** extend the partial-cooling and exceptional-label decomposition to the weighted integration needed by the comparison argument, or construct controlled compatible enlargements. Keep the weight at the output, pay region counts, retain unavoidable minima/holonomies, and do not infer conditional repairability from marginal rarity.

## Checks

```bash
./check.sh
pdflatex -interaction=nonstopmode -halt-on-error boundary_cost.tex
pdflatex -interaction=nonstopmode -halt-on-error boundary_cost.tex
```

The [20 standard-library tests](checks/check_boundary_cost.py) cover the reflection geometry, class decomposition, exact constants, sublevel-kernel support and one-link volume, source-component witness density, and negative controls. They include exact chessboard checks in a **different, two-dimensional Z2 model**, not numerical SU(2) probabilities. [Captured output](checks/output.txt).

This pass is **self-audited**, not independently agent-reviewed or externally certified. No new Lean formalization is claimed.
