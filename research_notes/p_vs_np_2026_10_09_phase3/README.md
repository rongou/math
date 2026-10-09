# Structured YES families and shared decoding

October 9, 2026. Starting repository revision: `b7a801fa3`. Phase 1, Phase 2, and the repository manuscripts are unchanged.

A concrete structured-subfamily route to the Phase 2 certificate goal fails. Even in the fixed-positive-beta threshold regime, an ordinary small circuit can recognize an exponentially large family of easy truth tables and their small perturbations while every accepting certificate fixes almost all table entries. The circuit reuses decoded block values rather than enumerating the easy functions individually.

This is a negative control for a **specified weakening of YES completeness**, not a correct solver for full GapMCSP. It does not refute the magnification hypothesis, establish an unrestricted-circuit lower bound, or resolve P versus NP. The deductions are elementary; no novelty claim is made.

## The candidate examined

Phase 2 asks for a structural consequence of a small circuit that accepts **every** YES table and rejects every NO table. Its sufficient certificate goal leaves more than `log_2 K(m,s2)` coordinates free, where

\[
N=2^m,\qquad K(m,s)=(m+s+2)[16(m+s+2)^2]^s.
\]

A proposed shortcut is to use only a rich, explicitly generable subfamily of YES tables, with robustness under truth-table patches, and combine those facts with small outer gate count and rejection of all NO tables. The construction below shows these hypotheses are insufficient for one natural choice of subfamily. Counting centers, including full-support functions, and allowing a positive-power number of perturbations do not repair that choice.

The full target remains the OPS promise

\[
s_1=\left\lfloor\frac{N^\beta}{c\log_2N}\right\rfloor,
\qquad s_2=\lfloor N^\beta\rfloor.
\]

Here one fixed positive epsilon must work for every sufficiently small **fixed positive** beta. YES means inner circuit size at most s1; NO means size strictly greater than s2. The input to the outer solver is all N truth-table bits. OPS Theorem 1.4 and Definition 2.4 are the external source [S1]; neither is newly formalized here.

## A large structured family

Both inner and outer circuits use AND2, OR2, and NOT. Every gate, including NOT, is counted. Constants and primary input wires are free.

Let J_k be all Boolean functions on m address variables that depend on at most k of those variables. Such functions are called k-juntas [S2]. Let P be odd parity on **all m address variables**, and define the set of center truth tables

\[
\mathcal D=J_k\ \cup\ \{P\mathbin\oplus g:g\in J_k\}.
\]

Every k-element support is allowed, not just one fixed support. For k>=1 this includes every projection, all k-juntas, full parity, and parity XOR every k-junta. The second family has genuinely full-support examples; it is not another raw-scope restriction on the entire center.

For an integer t>=0 let

\[
A_t=\{T:\min_{d\in\mathcal D}\operatorname{dist}(T,d)\le t\},
\]

where distance counts differing truth-table coordinates. The new circuit computes **exactly** `1_{A_t}`. It need not accept easy tables outside A_t.

For a fixed k-element support there are `2^(2^k)` distinct center tables. When `2k<m`, the parity-shifted and unshifted families are disjoint. Thus D contains at least `2^(2^k+1)` centers, before even counting the additional supports.

## Every accepted table is easy

An arbitrary k-junta has a DNF using at most k shared input negations, at most `2^k` minterms, and their disjunction. This uses at most `k+k*2^k` gates, including constant cases. Computing full parity costs at most `4(m-1)` gates; XORing it with the junta adds four. Consequently every center has an inner circuit of size at most

\[
B_0(m,k)=k+k2^k+4m.
\]

Phase 2's explicit patcher changes at most t truth-table values with the conservative bound

\[
B_0(m,k)+m+tm+3.
\]

Zero changes require no patch gates. Therefore

\[
B_0(m,k)+m+tm+3\le s_1
\quad\Longrightarrow\quad A_t\subseteq\mathrm{YES}.
\]

Under this condition, `1_{A_t}` rejects every NO table, and even every gap table. Its failure as a full promise solver is **missing YES tables**, not unsound acceptance of NO instances.

`inner_center` and the read-only Phase 2 patcher build actual gate lists. Tests check every small junta/shift construction in the stated bounds and additional patched examples. The general DNF and patching arguments above are manual proofs, not a formalization of circuit minimization.

## Small outer circuits without enumerating centers

For a chosen support I, partition the N table positions according to their assignment on I. There are `B=2^k` blocks, each of length `L=2^(m-k)`. A table on I is constant in each block. If a block contains w ones, its best constant approximation makes `min(w,L-w)` errors. Thus

\[
\operatorname{dist}(T,J_I)=\sum_{\text{blocks}}\min(w,L-w).
\]

The minimizing blockwise majority construction is standard; compare the conditional-mode function in the proof of Lemma 3.2 of [S2]. No query-complexity theorem from that paper is being used as a circuit-size theorem.

Our ordinary gate circuit:

1. Counts each block's ones and computes its majority, breaking ties toward zero.
2. Reuses that majority at every position in the block to compute mismatch bits.
3. Counts all mismatch bits and compares the result with t.
4. Repeats for each support, and for T XOR the fixed address-parity table, then ORs the answers.

The parity shift in this **outer** circuit only negates the N/2 table coordinates where address parity is one. It is not parity of the N input bits. The inner center's address-parity circuit and this fixed outer wiring transformation are different operations.

There are `D=2*binom(m,k)` detectors, not one detector per center function. All counters and comparisons are expanded into AND/OR/NOT gates. A q-input ripple-increment counter of width w uses `q*(5w-1)` gates; a comparison with an in-range constant uses `2w`. With `b=log_2 L+1` and `w=m+1`, the literal construction has

\[
S=\frac N2+D\left[N(5b-1)+B(2b+1)+4N+N(5w-1)+2w\right]+D-1
\]

and hence the loose uniform bound

\[
S\le50\binom{m}{k}N(m+1).
\]

The bit-vector and scalar interpreters check these actual circuits independently of the direct block-distance calculation.

### Where the sharing occurs

Each block-majority gate feeds two wires of the four-gate XOR at each of its L positions. Counting parallel outgoing uses separately, these nodes alone contribute

\[
R\ge D B(2L-1)=D(2N-B)
\]

to Phase 2's reuse surplus, after discarding gates not reaching the output. The implementation measures this on the actual reachable DAG.

This explains how the circuit avoids charging separately for exponentially many candidate functions and puts this **representation** outside the earlier logarithmic-reuse regime. It is not a lower bound on the reuse of every equivalent circuit, nor on the minimum formula size of this recognizer.

The B decoded block values are computed predicates, not B raw truth-table bits that can be fixed for free. Describing a center using those values does not produce an input certificate: the mismatch test still leaves the certificate obstruction proved below. A gate-cut argument must account for the cost of forcing computed values on raw inputs, rather than treating their number as that cost.

## Accepting subcubes are small

Two distinct k-juntas together depend on at most 2k address variables. A disagreement at one address repeats at all addresses agreeing on those variables. Their table distance is therefore at least `2^(m-2k)` when `2k<=m`. The same bound holds within the parity-shifted family, since the shift cancels.

When `2k<m`, a shifted and an unshifted center differ by parity XOR a function on at most 2k variables. Flipping an unused address variable toggles that difference, so their distance is exactly N/2. Overall the center separation is at least

\[
\Delta=2^{m-\max(1,2k)}.
\]

The maximum with 1 matters at k=0: the parity shift reduces the separation from N to N/2.

**Separated-ball lemma.** If distinct centers have distance greater than `2t+1`, every coordinate subcube contained in A_t lies within one radius-t ball, and has dimension at most t.

**Proof.** Two points in different radius-t balls cannot be adjacent: their centers would otherwise be at distance at most `t+1+t`. A coordinate subcube is connected by single-coordinate changes, so it cannot move between balls. In a d-dimensional subcube inside one ball, choose every free bit opposite the center's bit. That completion differs from the center in at least d positions, hence d<=t.

The endpoint is strict. Centers `000` and `111` at radius one satisfy unique-decoding separation `distance>2t`, but their two balls together cover the entire three-dimensional cube. Preventing overlap is not enough; adjacency must also be prevented.

For `0<=t<=N`, the bound is sharp at **every** accepted table. At a table whose error set relative to its center has size at most t, choose a t-element free set containing that error set and fix everything else to the center. This gives an accepting t-dimensional subcube. Thus the minimum number of fixed coordinates in an input acceptance certificate is exactly

\[
N-t.
\]

Under an arbitrary initial restriction, the same upper bound t on the final number of free entries still holds. If the restriction leaves r coordinates free and a certificate adds at most q fixed coordinates, then `r-q<=t`. Overlap with already-fixed coordinates is not charged again.

### Formal scope

`validation/SeparatedTubes.lean` proves the general one-center lemma, its free-coordinate bound, and the relative-certificate statement using Phase 2's **actual Boolean-subcube definitions**. It also proves that disagreements between locally supported inner functions repeat on an address subcube and deduces the k-junta distance lower bound.

Eleven theorem axiom reports use only `propext`, `Classical.choice`, and `Quot.sound`. There are no added axioms or native-evaluation proof shortcuts. The cross-family parity balance, general circuit construction, exact sharpness at arbitrary accepted points, and asymptotic parameter analysis remain the manual arguments given here; the Lean file does not silently prove full GapMCSP correctness.

## The fixed beta parameters work

Fix `0<beta<1/3` and a constant `c>=1`. For sufficiently large m, use the OPS-shaped thresholds above and choose

\[
k=\left\lfloor\log_2\frac{s_1}{8m}\right\rfloor,
\qquad t=\left\lfloor\frac{s_1}{4m}\right\rfloor.
\]

Eventually `m>=2`, `s1>=64m`, and `2k<m`. Because `k<=m` and `2^k<=s1/(8m)`,

\[
B_0+m+tm+3\le6m+3+\frac{3s_1}{8}\le\frac{s_1}{2}\le s_1.
\]

In particular **every accepted table really is a YES instance in the growing-threshold regime**. Also

\[
k=\beta m-2\log_2m+O(1),\qquad
t=\Theta(N^\beta/m^2),\qquad
\Delta=N^{1-2\beta}\,m^4\,\Theta(1).
\]

Since `1-2beta>beta`, eventually `Delta>2t+1`. Thus the certificate conclusion applies at those same lengths. Beta is fixed, not a vanishing function of m.

Let `H(u)=-u log_2 u-(1-u)log_2(1-u)`. The elementary binomial bound

\[
\binom mk\le2^{mH(k/m)}
\]

follows by retaining the kth summand in `1=(u+(1-u))^m` at `u=k/m`. Therefore

\[
S\le N^{1+H(\beta)+o(1)}.
\]

Given **any fixed epsilon>0**, choose beta_0>0 small enough that `beta_0<1/3` and `H(beta)<epsilon` for `0<beta<beta_0`. For every such **fixed** beta, the displayed construction eventually has `S<N^(1+epsilon)`.

This matches the small-circuit quantifier order relevant to the proposed shortcut. It is not an OPS counterexample, because full YES completeness was deliberately weakened.

The selected centers number at least `2^(2^k+1)`, with `2^k=Theta(N^beta/m^2)`. Every center's entire radius-t neighborhood is accepted. Nonetheless no accepting certificate, even after an initial restriction, leaves more than t positions free. Since `t<s2` and `log_2 K(m,s2)>=4s2`, it cannot supply Phase 2's counting contradiction.

The symbolic integer examples in `tube_results.json` check sample lengths with rational beta and integral beta*m; no astronomically large circuits are materialized. Their illustrative `c=1` does not identify the universal constant in OPS. The all-large-length argument above works for every fixed c>=1, independently of those samples.

## Why this is not a full promise solver

For all sufficiently large lengths, `m>=2k+2`. Take parity on any k+1 address variables. It has a circuit with at most 4k gates, so eventually it is a YES table. It is balanced on a variable omitted by every k-element support, and its XOR with full parity is parity on `m-k-1>k` variables. Its distance from every center in D is consequently N/2. Our circuit rejects it since t<N/2.

Thus even including full parity and every raw projection did not recover full YES completeness. Adding one rejected example is not a proposed repair: the counterexample identifies missing hypotheses, not a way to turn this recognizer into a full solver.

The omitted functions already have polynomial-in-m inner circuits. Therefore the recognizer also fails the easy-completion premise of the published formula argument reconstructed in Phase 2. There is no conflict with that formula theorem.

## Verification and reproduction

The recorded finite checks include:

- 21 Python regression tests.
- 54 actual outer-circuit constructions, checked on all their inputs: 6,480 comparisons, across m=1,2,3, all k<=m, two shift modes, and radii 0,1,2.
- Independent block-majority distances checked against explicit center enumeration, plus scalar versus bit-vector circuit checks.
- All 87 center-set/radius configurations satisfying the separated-ball hypothesis through three outer coordinates, including empty center sets.
- Every one of the 6,561 subcubes in a selected eight-bit instance: m=3, k=1, t=1, with parity shifts. It has 16 centers at distance four, 144 accepted tables, 1,917 literal gates, and minimum certificate size seven at every accepted table. The one-gate inner function AND(x0,x1), truth-table integer 136, is rejected. This is a finite geometry control, not an asymptotic MCSP lower bound.
- 48 additional actual inner-center/patch constructions, with ordinary outer-gate acceptance checked.
- Reachable-wire sharing counts, strict-separation endpoint controls, and exact sample parameter inequalities.
- Eleven Lean theorems and the preservation of all 70 tracked files in the two preceding investigations.

From the repository root:

```bash
research_notes/p_vs_np_2026_10_09_phase3/validation/check.sh \
  /tmp/family112-build-validation.xWSfhA/project/lean
```

The argument can be replaced by another built Mathlib project with the intended pinned Lean 4.34.1 dependencies. Omitting it runs the finite Python checks but explicitly skips Lean. The script compiles the unchanged Phase 2 helper into its own temporary directory and replays, rather than overwrites, the saved experiment. It does not rerun the family 112 comparator or rebuild the external literature.

The complete run is recorded in `validation/integration_checks.log`: exit zero, about 20 seconds, and approximately 6.6 GiB peak resident memory. An initial 4 GiB Lean allocation cap failed while loading the Mathlib-heavy Phase 2 helper; that attempt is retained in `validation/integration_attempt_4GiB.log`. The successful driver uses `-M16384`. The failed run is not accepted as verification. All 81 preceding Python tests also pass (`validation/prior_regression.log`).

## Updated stopping point

The resource-sensitive certificate lemma for **full** fixed-beta GapMCSP is still absent. This phase rules out deriving it using only soundness against NO tables, small ordinary circuit size, and completeness on the specified noisy-junta/parity-shift family.

A next candidate must use completeness beyond this family, or a different explicitly justified structured family. One possible line to test is the closure of cheap inner computations under Boolean combinations, with the actual s1 budget tracked. Merely adding a few examples or observing that the centers are numerous is not such an argument. No useful general sharing-sensitive inequality is claimed here.

These are ordinary composed circuits with no oracle gates. The construction does not establish or refute closure of the intended full method under the particular internal-oracle models in the locality literature. That separate audit requirement from Phase 2 remains.

## Sources

- **S1** Oliveira, Pich, and Santhanam. *Hardness Magnification Near State-of-the-Art Lower Bounds*. Theory of Computing 17(11), 2021, Theorem 1.4 and Definition 2.4.
- **S2** Liu, Chen, Servedio, Sheng, and Xie. *Distribution-Free Junta Testing*. STOC 2018, definition of juntas and the conditional-mode construction in the proof of Lemma 3.2. This is background attribution, not a source for the Phase 3 counterexample or its gate bound.
- **Phase 2** `../p_vs_np_2026_10_09_phase2/`: patching construction, circuit conventions, the Boolean-subcube counting interface, and the fixed-beta target audit.

Exact source locations and the limits of the bounded literature check are in `sources/structured_family_audit.json`. Formal versus manual scope and the self-review checklist are in `validation/review.json`.
