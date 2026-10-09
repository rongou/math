# Prefix splicing and connected YES families

October 9, 2026. Starting tracked revision: `b7a801fa3`. The 99 artifacts in Phases 1–4, including their uncommitted files, are preserved.

**Outcome: making the accepted family connected does not supply the missing certificate argument.** A small ordinary circuit can retain the Phase 4 noisy family and also accept every exact prefix splice of two of its center functions. The resulting accepted set is connected by one-bit steps, consists entirely of YES instances in the specified fixed-beta regime, and still has no sufficiently large accepting coordinate subcube.

The algorithmic ingredient is a weighted version of the Phase 4 implication-graph calculation. It finds the longest extendable prefix and suffix without enumerating all cuts or center functions. This is an elementary construction, not a novelty claim or a P-versus-NP separation.

The new set includes **exact splices of centers**, not arbitrary noisy splices or unlimited repeated splicing. Full GapMCSP completeness remains absent.

## Why test splicing

View an m-input function as its truth table of length N=2^m in the standard binary address order. For a cut j in {0,...,N}, define

\[
\operatorname{splice}_j(f,g)(x)=
\begin{cases}f(x)&x<j,\\g(x)&x\ge j.\end{cases}
\]

An address comparison costs at most 2m ordinary AND/OR/NOT gates, and a two-way selector costs four. Thus, using the actual union of the two reachable input circuits,

\[
\operatorname{Size}(\operatorname{splice}_j(f,g))
\le |G_f\cup G_g|+2m+4.
\]

When this budget is at most s1, a full correct solver must accept the splice. As j increases, at most one truth-table coordinate changes. Hence such splices force paths between cheap tables, a property missing from the separated-ball controls.

This is a statement about the specified address order. An arbitrary permutation of table positions could require an expensive selector and is not silently included.

## The enlarged family

Keep the Phase 4 center set

\[
\mathcal D_0=J_k\cup(P\oplus J_k),\qquad
C=\{\phi(f,g):f,g\in\mathcal D_0,
      \phi:\{0,1\}^2\to\{0,1\}\},
\]

where P is full **address** parity and all k-element supports are allowed. Let

\[
T=\bigcup_{c\in C}B_R(c),\qquad
\operatorname{Sp}(C)=\{\operatorname{splice}_j(f,g):f,g\in C,\ 0\le j\le N\},
\qquad A=T\cup\operatorname{Sp}(C).
\]

T is the existing Phase 4 noisy family. The new recognizer computes exactly `1_A`, under the old decoder's radius condition for T. It retains every old accepted input, rather than replacing the noisy family with noiseless examples.

A is connected in the N-dimensional Boolean cube. Each ball point can return to its center by removing errors one at a time. The splice paths connect every pair of centers, and every splice point lies on one of those paths. This proves connectedness of A; it does not claim that every possible total extension of GapMCSP has a connected accepting set.

## The same inner budget suffices

The primitive circuit bound from Phase 3 is `B0=k+k*2^k+4m`; each Phase 4 center has a circuit of size at most `2B0+4`. Consequently every exact splice of two centers has size at most

\[
4B_0+2m+12.
\]

Use the unchanged parameters

\[
s_1=\left\lfloor\frac{N^\beta}{cm}\right\rfloor,
\quad s_2=\lfloor N^\beta\rfloor,
\quad k=\left\lfloor\log_2\frac{s_1}{8m}\right\rfloor,
\quad r=\left\lfloor\frac{s_1}{4m}\right\rfloor,
\quad R=2r.
\]

For fixed `0<beta<1/5` and fixed `c>=1`, eventually `m>=2`, `k<=m`, and `s1>=64m`. Then `B0<=5m+s1/8`, so

\[
4B_0+2m+12\le\frac{s_1}{2}+22m+12\le s_1.
\]

Phase 4 already gives `T subset YES` at these parameters. Therefore **A is a subset of YES**, and this new circuit also rejects all NO and gap tables. It can still reject other YES tables.

`inner_splice` builds actual comparator/selector gates and records the reachable shared input cones. Its `2m+4` bound includes all NOT gates. The general resource argument is not a claim about optimal circuit size.

## Replace cut enumeration by matching lengths

For an arbitrary table X, define

\[
p(X)=\max\{j:X_{[0,j)}=f_{[0,j)}\text{ for some }f\in C\},
\]

and similarly let q(X) be the maximum suffix length that matches some center. The two witnessing centers need not be equal. Exactly,

\[
X\in\operatorname{Sp}(C)\quad\Longleftrightarrow\quad p(X)+q(X)\ge N.
\]

For the reverse implication, choose a cut between N-q and p; the matching prefix and suffix cover the whole table. The forward implication follows from the cut used by the splice.

Computing these lengths by enumerating C would be too costly at the target parameters. Instead we exploit the Phase 4 representation by two primitive truth tables.

## Earliest inconsistency in a partial 2-CNF model

Fix a support pair I,J, one of the canonical operations AND/NAND/XOR, and the two global parity-shift flags. As in Phase 4, the primitive truth-table entries are unknown Boolean variables. An observed table bit at an address imposes binary constraints on two such variables. This remains true for a **partial** prefix or suffix: unobserved entries impose no constraint.

There are `v=2^(k+1)` unknown Boolean variables and `2v` implication-graph vertices in this direct representation. Overlapping supports are permitted. The operation and shift flags are fixed for the whole model, not selected separately at different addresses.

Label an implication edge with the earliest prefix length at which it becomes active. A violation at address i activates its two implication edges at time i+1; if several clauses activate the same edge, take their minimum time. Use infinity for an edge that never appears, and zero on the diagonal.

A path becomes available when all its edges have appeared. Its activation time is their maximum; the earliest available path minimizes that maximum. Thus the bottleneck recurrence is

\[
D^{j+1}_{uv}=\min\bigl(D^j_{uv},\max(D^j_{uj},D^j_{jv})\bigr).
\]

Thresholding at any time t turns this recurrence into ordinary Boolean reachability. The Phase 4 2-SAT criterion [S1] therefore gives the first inconsistent prefix length as

\[
u=\min_{\ell}\max\bigl(D_{\ell,\bar\ell},D_{\bar\ell,\ell}\bigr),
\]

where one complementary pair is taken per variable. A model remains satisfiable through prefix length u-1. If it is satisfiable on the whole table, use u=N+1.

For the union of models, take the **maximum** of their first-inconsistency times. This finds p+1. Reverse the table order to obtain q+1. The final splice test is consequently `(p+1)+(q+1)>=N+2`.

The maximum is taken over whole fixed models. Switching the model at each address would not describe a single center function and is not what the circuit does.

## An ordinary gate implementation

The implementation uses unsigned words of width `w=m+1`. Finite edge times are at most N. During the bottleneck calculation, infinity is the largest unsigned word, `2^w-1`; the final model result is clamped to N+1. These two sentinels must not be confused.

Comparisons, minima, maxima, additions, and the final test are all expanded into AND2/OR2/NOT gates. A min or max uses at most `8w+1` such gates. No unit-cost arithmetic or SAT oracle is present.

For one model and one direction, forming weighted edges costs O(Nw), and the bottleneck circuit costs O(w*2^(3k)). There are `12*binom(m,k)^2` models. Hence

\[
S_{\rm splice}=O\!\left(\binom{m}{k}^{2}(m+1)(N+2^{3k})\right).
\]

Here `binom(m,k)^2` denotes the square of the binomial coefficient. ORing this circuit with the existing Phase 4 noisy recognizer preserves that order of growth. In particular, for the fixed-beta parameters,

\[
S_A\le N^{1+2H(\beta)+o(1)}.
\]

For any fixed epsilon>0, sufficiently small fixed beta therefore gives a circuit below `N^(1+epsilon)`. Beta does not vary with m. This has the quantifier order of the proposed weak target, while **not** having full YES completeness.

`FoldingBuilder` applies only local Boolean identities, constant-word identities valid for all unsigned inputs, and sharing of identical already-built nodes. It never deduces an identity by evaluating the unknown input. The unoptimized gate bound is computed before those simplifications; allocated ordinary gates are checked against it. Finite circuits are independently interpreted both scalarly and as Boolean bit vectors.

## Connectedness invalidates the old radius bound

The old proof that every accepting subcube has dimension at most R cannot be carried over. For example, take the R-ball around zero, and allow the prefix step with its first R+1 bits equal to one. Every completion on those first R+1 free coordinates is accepted: it either has at most R ones and lies in the ball, or is that prefix step. This is an accepted subcube of dimension R+1.

The finite m=4, k=0, R=2 test checks this on all eight completions of the first-three-coordinate cube. It also checks that adding the splice paths changes four disconnected noisy components into one connected set.

This is why the argument below uses cardinality, not the old separated-ball lemma.

## Cardinality still prevents the needed certificate

Regardless of overlap between balls or splices,

\[
|A|\le |C|\sum_{i=0}^{R}\binom Ni+(N+1)|C|^2.
\]

The second term counts a cut and an ordered pair of centers; duplicates only make it an overcount. From the primitive description bound,

\[
\log_2|C|\le \ell:=6+2m+2^{k+1}.
\]

Since `sum_{i<=R} binom(N,i) <= (R+1)N^R`, an explicit integer upper bound on log_2 |A| is

\[
B=1+\max\{\ell+Rm+\operatorname{bitlength}(R+1),\ m+1+2\ell\}.
\]

For the fixed-beta parameters this is `O(N^beta/m)`. Every accepted coordinate subcube has at most |A| points, so its dimension is at most B. The same conclusion applies after an initial restriction: the final accepting subcube, not the number of computed gate values, is being counted.

This remains too small to trigger the Phase 2 counting contradiction. Its comparison is against `log_2 K(m,s2)`, where `K(m,s)=(m+s+2)[16(m+s+2)^2]^s` and `log_2 K(m,s2)>=4s2`. Here `B=o(s2)` for each fixed beta>0. Thus the connected-family circuit satisfies the tested hypotheses without furnishing the required free-coordinate count.

## A repaired witness and a new missed YES table

The previous six-address-variable parity witness is now accepted. For k=1, parity on the lowest three variables is a splice at the halfway cut of

\[
f=P\oplus x_3\oplus x_4\quad\text{and}\quad\neg f.
\]

Both are Phase 4 centers. This is a real enlargement, not merely a relabeling of the earlier counterexample.

However, for `m>=4k+3`, parity on the **lowest** 2k+1 address coordinates is still a missed YES table. For every cut, at least one half of the full address space lies wholly on one side of it. On that half the splice equals one Phase 4 center, determined by at most 2k raw coordinates and the parity of the remaining free address variables.

The target does not use the highest address coordinate fixed by the half. Among the m-1 free coordinates, there is one in the target support outside the center's raw support, and another outside both supports. Flipping these two coordinates preserves all center features but toggles the target. It follows that the center disagrees with the target on exactly half of that half-cube. Therefore every exact splice differs from the target in at least N/4 positions.

The target is also at distance N/2 from every old center. Since R=o(N), it lies in neither part of A. Yet it has an ordinary circuit with at most 8k gates, so it is a YES instance at the specified large lengths.

At m=7, k=1 the finite check finds exact splice distance 32, old-center distance 64, and rejects the eight-gate three-variable parity table. This is not a NO instance and is not a counterexample to the full magnification hypothesis.

## Verification scope

The finite suite contains 19 tests, including:

- All unsigned min/max/comparison/addition cases through word width four, constant/infinity handling, and local folding versus an independent unoptimized circuit.
- Thresholded bottleneck matrices checked against independent graph traversals.
- 768 small table/model cases checked using explicit primitive functions, numeric bottleneck graphs, and ordinary gate circuits. Both prefix and suffix results are checked.
- Three complete outer-circuit replays, totaling 66,048 input comparisons. The m=3, k=1 instance happens to accept the whole small cube; it is a completeness check, not hardness evidence.
- A connected 16-input example with 616 accepted tables and an explicit three-dimensional subcube that disproves reuse of the old R=2 bound.
- 24 larger numeric matching comparisons against explicitly enumerated center sets, 32 actual inner selector circuits, and the two parity witnesses.
- Exact fixed-beta sample inequalities; no astronomically large circuit is materialized.

`PrefixSplicing.lean` checks eight statements: the thresholded min/max identity; splice endpoints and single-coordinate steps; finite splice membership/cardinality; actual matching-prefix/suffix reconstruction; and the accepting-subcube cardinality bound. Only standard permitted axioms occur. The general weighted 2-SAT compiler, global connectedness argument, inner/asymptotic gate bounds, and parity witness argument are not claimed fully Lean-formalized.

An initial Lean compilation exposed a decidable-equality instance mismatch in the complement-cardinality rewrite. The final proof normalizes `card_compl` before using the previous theorem. The failed attempt is retained separately and its error-generated placeholder is **not** accepted as a proof.

## Reproduction

```bash
research_notes/p_vs_np_2026_10_09_phase5/validation/check.sh \
  /tmp/family112-build-validation.xWSfhA/project/lean
```

The argument may be replaced by another built project with the pinned Lean 4.34.1 dependencies. Omitting it runs the Python suite and exact replay but explicitly skips Lean. The script retains its fresh helper directory and does not rewrite any earlier investigation. The formal check uses the previously established 16 GiB Lean allocation cap.

The complete run in `validation/integration_checks.log` exits zero, takes about 41 seconds, and peaks at approximately 6.6 GiB resident memory. The 126 prior Python tests also pass (`validation/prior_regression.log`), for 145 passing tests overall. The valid theorem axiom reports and proof hashes are recorded separately in `validation/formal_validation.json`.

## Decision after this pass

The hypotheses tested so far—local perturbation robustness, one binary-composition round, exact prefix-splicing paths between the center functions, and connectedness of the whole accepted set—can all hold for a small, sound **partial** recognizer with long input certificates.

This does not disprove full budgeted closure or the existence of a useful full-solver theorem. It does show why automatically adding another family closure or another finite atlas is not presently a convincing route to the desired lower bound.

A useful continuation should identify a quantitative consequence of **full** YES completeness that fails for this connected control and materially uses outer circuit size, or seek external complexity-theory review of the certificate route. No positive general-circuit certificate-extraction lemma has been obtained.

## Sources

- **S1** Aspvall, Plass, and Tarjan, *A Linear-Time Algorithm for Testing the Truth of Certain Quantified Boolean Formulas*, Information Processing Letters 8(3), 1979, Theorem 1. The implication-graph criterion is reused from the Phase 4 source audit. The weighted threshold lift is the elementary recurrence proved here, not an imported gate-size theorem.
- **Prior phases** Provide the OPS target audit, primitive/binary center definitions, circuit conventions, patching bounds, and Boolean-subcube framework.

Scope and self-review records are in `sources/splicing_audit.json` and `validation/review.json`.
