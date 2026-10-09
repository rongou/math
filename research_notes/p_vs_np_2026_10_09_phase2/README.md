# GapMCSP certificates and circuit sharing

October 9, 2026. Repository revision: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

This second investigation reconstructs a promise-specific restriction-and-counting argument, formalizes its counting step, and examines what fails when formulas become circuits with reused computations. It supplies elementary sharing bounds and explicit negative controls. It does **not** establish a new unrestricted-circuit lower bound, a new magnification theorem, or a P versus NP separation. Phase 1 and the repository manuscripts remain unchanged.

## Outcome

| Proposed step | Result |
| --- | --- |
| An accepting subcube larger than Low forces an error | Proved with actual Boolean-subcube semantics in Lean |
| Transfer a formula bound when the reuse surplus is logarithmic | Elementary consequence of the existing formula theorem |
| Use quadratic formula shrinkage with DAG gate count | False, even with the square-root remainder retained |
| Infer short acceptance certificates from small correct MCSP solvers without the exact threshold regime | False for zero and slowly growing exact thresholds |
| Obtain the needed certificate for general fixed-beta GapMCSP circuits | Not proved |

## Definitions and the exact target

An inner circuit computes a Boolean function of m variables. Its full truth table has N=2^m entries; these N entries are the input bits of the outer GapMCSP solver. Both inner and outer ordinary circuits use AND2, OR2, and NOT, with each gate counted once. Constants and input wires are free; a NOT gate is not free.

For thresholds s1 at most s2, the promise is:

- YES: inner circuit size is at most s1.
- NO: inner circuit size is strictly greater than s2.
- Gap: size is greater than s1 and at most s2; either solver output is allowed.

The magnification target retains the fixed-parameter order from OPS Theorem 1.4: one positive epsilon, every sufficiently small fixed positive beta, and unbounded truth-table lengths, with thresholds

\[
s_1=\left\lfloor\frac{N^\beta}{c\log_2 N}\right\rfloor,
\qquad s_2=\lfloor N^\beta\rfloor,
\]

for the theorem's universal c. Excluding outer circuits of size N^(1+epsilon) in this regime implies NP is not contained in P/poly [S1]. None of the constant-threshold examples below is a counterexample to that target.

An **input acceptance certificate** fixes some outer truth-table coordinates and forces the outer solver to accept every remaining completion. This is a monochromatic subcube, not an NP witness supplied to a verifier.

## The counting step is now formal

Let F be the coordinates fixed by an initial restriction, leaving r coordinates free. A further certificate fixes coordinates C. Only the newly fixed coordinates count:

\[
q_{\rm actual}=|C\setminus F|.
\]

When the two partial assignments agree on their overlap, their common completion set has exactly

\[
2^{r-q_{\rm actual}}
\]

elements. If the certificate uses at most q new coordinates, the completion set has at least 2^(r-q) elements, interpreting subtraction as natural-number subtraction.

For any correct promise solver, every accepted table belongs to

\[
\mathrm{Low}=\{T:\operatorname{Size}(T)\le s_2\}.
\]

Therefore an accepting certificate must satisfy

\[
2^{r-q}\le |\mathrm{Low}|.
\]

Conversely, if `|Low| < 2^(r-q)`, there is a completion outside Low, and hence a NO instance, agreeing with the restriction and certificate. A purported accepting certificate of that size is impossible.

`validation/PromiseCounting.lean` proves the actual Boolean-subcube cardinality, compatible intersection formula, overlapping-coordinate budget, witness outside Low, and certificate contradiction. It also proves that an accepted point whose every one-bit neighbor is rejected has no certificate omitting any coordinate. The proof is checked under pinned Lean 4.34.1 with only the three standard axioms. Its interface treats Low as a finite set; it does not pretend to formalize circuit minimization or infer short certificates from gate count.

A useful elementary upper bound on Low is

\[
K(m,s)=(m+s+2)[16(m+s+2)^2]^s.
\]

Pad an inner circuit to s gates, topologically order it, and choose a binary Boolean operation and two earlier wires for every gate, followed by an output wire. Allowing all 16 binary functions and even overcounting wire choices only increases the number of descriptions. Every ordinary circuit in our fixed basis is covered. Thus `|Low| <= K(m,s2)`.

**The missing step is not counting.** It is obtaining a sufficiently large accepting subcube from the assumed small size of a correct outer circuit. No such general resource-to-certificate theorem has been proved here.

## Reconstruction of the formula argument

The ordinary-formula specialization of CHOPRS Theorem 60 gives the following baseline. For a fixed deficit delta>0, formulas of size N^(2-delta) cannot solve `GapMCSP[m^a, N^beta]` when beta<delta/2, for a suitable constant a [S2].

Its restriction process preserves a succinct all-zero completion, whose inner circuit size is polynomial in m. With simultaneous positive probability it leaves at least N^(delta/2-o(1)) table coordinates free while simplifying the outer formula to dependence on only O((log N)^3) coordinates. Counting then forces a high-complexity completion with the same solver output. In the OPS regime, s1 eventually dominates the polynomial-in-m bound, and s2=N^beta is small enough for the counting contradiction.

The formula resource is a **tree occurrence count**, not the number of distinct gates in a DAG. In the oracle-formula version, the initial potential is controlled by weighted SIZE3 and oracle adaptivity. Reusing one subcomputation under several parents requires accounting for multiple occurrences when unfolding it; the published potential estimate does not charge the computation only once. Exact ingredients, model conventions, and comparisons with known almost-formula results are in `sources/formula_sharing_audit.json`.

This reconstructs a literature argument, not a new proof of the external theorem. Parameter or model restrictions must not be silently removed.

## An elementary bound for circuits with little reuse

Discard gates that do not reach the output. Let S be the remaining number of internal gates. For an internal gate v, let d(v) count its outgoing **wires**, with parallel uses counted separately. Primary inputs are not internal gates. Define the reuse surplus

\[
R=\sum_{v\text{ internal}}\max(0,d(v)-1).
\]

Let w(v) be the number of directed wire paths from v to the output. Unfolding the circuit copies v exactly w(v) times. For a fixed v, choose one outgoing edge at each internal gate that has outgoing wires; a gate without any contributes a single dummy choice. Following the choices gives at most one path from v to the output. Every such path has an extension to these edge choices. Hence

\[
w(v)\le\prod_u\max(1,d(u))\le 2^R.
\]

The second inequality uses `d <= 2^(d-1)` for positive integers d. It follows that the unfolded formula has at most S*2^R internal gate occurrences, and at most

\[
L\le 1+S2^R
\]

leaf occurrences. Unary NOT gates can be pushed to the input literals without increasing that leaf count. Constants and an output directly on an input are included.

Consequently, if `S <= N^(1+epsilon)` and `R <= gamma log_2 N`, then

\[
L\le 1+N^{1+\varepsilon+\gamma}.
\]

Choose delta with `epsilon+gamma+delta<1`. For sufficiently large N this falls below N^(2-delta). Applying the existing formula bound therefore excludes such **restricted-sharing circuit families** for sufficiently small fixed beta. This is an elementary consequence, not a claimed improvement to known almost-formula frontiers. General small circuits may have R comparable to their size, and then this bound is useless for the magnification target.

The experiments in `experiments/sharing_probe.py` check path multiplicities and these bounds on actual DAGs. A repeated-use AND chain grows exponentially under syntactic unfolding while still computing a single input bit. Such examples refute a cheap bound on the **unfolding procedure**, not a lower bound on the minimum formula for that function.

## Quadratic gate shrinkage is an invalid generalization

For ordinary formulas, Tal's clean shrinkage estimate includes both `p^2 L` and `p sqrt(L)`, with an optional constant cost depending on the treatment of constant formulas [S3]. A tempting gate-count replacement is

\[
\mathbb E\operatorname{Size}(C\upharpoonright\rho)
\le A(p^2 S+p\sqrt S)+B.
\]

Here Size means optimal gate count, each outer input is left live independently with probability p, and A,B are fixed constants. This statement about *optimal* residual circuits is false for unrestricted circuits; so is the version omitting the square-root term.

Parity on N variables has an ordinary AND/OR/NOT circuit with at most 4N-3 gates. If m variables remain live, the residual parity depends on all m. Any binary/unary circuit depending on m distinct inputs needs at least m-1 binary gates when m is positive: in its reachable graph, there are `2b+u` edges and at least `b+u+m-1` edges by connectivity, so `b>=m-1`.

Thus, for a binomial live count M,

\[
\mathbb E\operatorname{Size}(C\upharpoonright\rho)
\ge \mathbb E\max(M-1,0)
=Np-1+(1-p)^N.
\]

For any fixed nonnegative A,B, choose fixed p>0 small enough that `4Ap<1/2`, then choose N so large that `2Ap sqrt(N)+B+1<Np/2`. The proposed upper expression is at most `4Ap^2 N+2Ap sqrt(N)+B`, strictly less than the necessary lower bound. The square-root term is negligible compared with Np at fixed p. The same argument excludes a universal leading shrinkage exponent strictly greater than one in p, with these fixed constants and a remainder sublinear in N at fixed p.

Parity is not claimed to solve GapMCSP. This excludes a size-only transfer to all circuits, not a promise-specific theorem exploiting correctness on the actual target.

## Correctness alone is insufficient without the right thresholds

There is a separate negative control that is itself a correct MCSP classifier.

For exact `MCSP[0,0]`, the accepted inner truth tables are just the two constants and the m positive projections. At m>=2, N=2^m, any two of these m+2 tables differ in at least N/2>=2 positions. Consequently every accepted table has only rejected one-bit neighbors.

An input acceptance certificate omitting coordinate i would also accept the table with bit i flipped. Therefore **every YES certificate must fix all N coordinates**. Under a compatible initial restriction leaving r coordinates free, all r remaining coordinates are necessary.

Nevertheless, a classifier is simply the OR of m+2 equality tests against those tables. Sharing N input negations, it uses

\[
N+(m+2)(N-1)+(m+1)=(m+3)N-1
\]

ordinary gates, or O(N log N). For every fixed positive epsilon, this is eventually below N^(1+epsilon).

This already has an O(N log N)-leaf formula, so the control is not an artefact of internal sharing. Thus “correct promise solver plus nearly linear size” does not uniformly imply short acceptance certificates across all threshold regimes. This example uses threshold zero; the OPS theorem needs every sufficiently small **fixed positive beta**, with thresholds growing with N. The example does not refute that hypothesis. The source formula proof's polynomial-in-m easy-completion guarantee is unavailable at threshold zero.

`experiments/certificate_controls.py` constructs the actual classifiers and checks the isolated YES points and certificate witnesses. The finite m=3 instance has five accepted tables, 47 gates, and eight necessary certificate coordinates. `validation/ZeroGateControl.lean` checks the actual gate-list interpreter, the exact zero-gate inner semantics, every rejected neighbor, and the impossibility of a proper certificate mask. The general family asymptotics above remain an elementary manual argument, with no claim of novelty.

### Slowly growing thresholds also give controls

The same phenomenon is not limited to threshold zero. Set `s(m)=floor(sqrt(m))` and consider exact `MCSP[s(m),s(m)]` for sufficiently large m. Every inner circuit of at most s gates depends on at most s+1 input variables, by the connectivity bound above. Two such functions together depend on at most `2(s+1)<m` variables. If their truth tables differ at one address, they differ at every address agreeing on those variables, hence at least `2^(m-2(s+1))>=2` addresses. Thus the accepted truth tables are isolated, and all YES certificates again require all N bits.

But the number of accepted tables is at most

\[
K(m,s)=2^{O(\sqrt m\log m)}=N^{o(1)}.
\]

An OR of their equality tests therefore has an outer circuit of size at most `N*(|Low|+1)-1=N^(1+o(1))`. This is an elementary counting-and-support upper bound; no enumeration of this asymptotic family or new Lean certification of it is claimed.

Both thresholds now grow without bound, but only as `sqrt(log N)`. They are still far below the OPS lower threshold for every fixed positive beta.

More directly, a varying choice `beta(m)=3*log_2(m)/(2m)` turns the OPS-shaped thresholds into `floor(sqrt(m)/c)` and `floor(m^(3/2))`. The near-linear recognizer for the exact low set at the smaller threshold also solves this gap problem: rejecting gap instances is permitted. Its YES certificates still require all N bits. Thus even preserving the displayed threshold ratio while replacing fixed beta by a vanishing beta(m) admits easy counterexample families. This is not a counterexample to the published fixed-beta theorem.

## A constructive guarantee at growing thresholds

The threshold dependence is not merely a caveat. Let an m-input base function have a circuit of size s0. Flipping its truth-table values at t distinct addresses, for t>=1, can be done with at most

\[
s_0+m+tm+3
\]

gates: m shared input negations, t minterms of m-1 AND gates each, t-1 OR gates, and four gates implementing XOR with the base output. Zero changes need no extra gates.

Hence, if `s0+m+rm+3 <= s1`, all completions varying any r chosen table positions around that base function are YES instances, and every correct solver must accept that subcube. The constructor and its cost are checked in `experiments/certificate_controls.py`.

For the OPS thresholds, this elementary construction guarantees roughly `N^beta/(log N)^2` freely varying coordinates around a sufficiently cheap base table. The coarse counting contradiction instead requires more than `log_2 K(m,s2)=O(N^beta log N)` unqueried coordinates. These are deliberately nonoptimal estimates, **not a claim that a polylogarithmic improvement would resolve P versus NP**. Neither estimate involves the outer circuit size. The missing resource-sensitive argument is still absent.

## Exact small promise instances

`experiments/promise_atlas.py` enumerates all inner three-variable circuits of at most two gates, retaining sharing, ordered input choices, duplicate wires, and unused gates. This classifies all 256 truth tables into exact sizes zero, one, two, or greater than two in the declared basis. For the concrete promise `[s1,s2]=[1,2]`, it records YES, gap, and NO instances, explicit low-size circuits, and every Boolean subcube.

A **promise-compatible accepting subcube** here means one containing no NO instance. It is accepted by the maximal correct separator `1_Low`, but another correct solver may reject its gap points. Feasible promise certificates must not be presented as certificates possessed by every given classifier.

The corpus supplies a simple counterexample to treating the counting inequality as sufficient. There are exactly 40 tables in Low, so cardinality alone only forces three fixed coordinates (using the exact low-set size, not the looser description bound K). At the zero table, however, the smallest promise-compatible accepting certificate fixes seven coordinates. The mask fixing coordinates zero through six leaves only `{0,128}`: zero is YES and 128 is a gap instance. This also checks the strict upper endpoint and the need to allow gap completions in Low.

There is also a direct basis-sensitive proof of the key finite witnesses. A nonmonotone function depending on all three inner variables needs more than two gates: two gates reaching three essential inputs must both be binary, hence both AND/OR and therefore monotone. Every one-point indicator except the point `111` is nonmonotone and depends on all three variables. The `111` indicator has two AND gates. This explains the zero table's seven required coordinates without relying solely on a search hash. The complement of the `111` indicator is also nonmonotone with three essential variables, supplying the eighth essential-coordinate witness from the all-one table.

The outer search exhausts its stated two-gate budget and finds no classifier. A separate small analytic argument is stronger: eight listed YES/NO pairs differ in exactly one distinct table coordinate each, forcing every valid solver to depend on all eight input bits. The bounded-fan-in connectivity bound therefore requires at least seven binary gates. This does not establish that seven gates suffice or determine the exact minimum.

`validation/AtlasWitness.lean` kernel-checks the explicit two-slot circuit grammar, all 40 Low witnesses, the certificate masks, and the eight promise edges. The mathematical normalization of arbitrary at-most-two-gate DAGs into that grammar and the general connectivity bound are not separate Lean theorems in that file. Small finite circuits and constant thresholds are falsification controls, not evidence of an asymptotic lower bound in the OPS regime.

## What remains open in this investigation

The sufficient structural goal is now explicit. Assume an N^(1+epsilon)-size circuit correctly solves the OPS promise. Derive a restriction with a known YES completion and an accepting certificate that leaves more than `log_2 K(m,s2)` table entries unconstrained. The formal counting bridge would finish the contradiction.

Only a very restricted sharing regime follows from the elementary unfolding estimate. Generic gate-count shrinkage is false, correctness without the growing-threshold conditions is insufficient, and counting does not itself manufacture a certificate. No valid general-circuit derivation of the sufficient goal was found in this pass.

For this approach, the next candidate should exploit a property of the growing-threshold promise that is absent from the controls, and account quantitatively for shared computations. It need not use every YES instance: a sufficiently rich structured subfamily could suffice. Its response to the *specific* internal-oracle models in the locality literature must also be checked; bottom-only robustness is not enough to conclude that a full locality barrier applies.

## Reproduction and verification

All new files are confined to this directory. The first investigation is read-only and its 42-file manifest is checked by the reproduction script.

From the repository root, run:

```bash
research_notes/p_vs_np_2026_10_09_phase2/validation/check.sh \
  /tmp/family112-build-validation.xWSfhA/project/lean
```

The argument is the existing pinned Lean 4.34.1 project with compiled Mathlib dependencies. Another built project using the exact intended toolchain and dependencies can be supplied instead. Omitting the argument runs the Python and two Std-only finite checks but explicitly skips `PromiseCounting.lean`.

The complete coordinator run passes:

- 48 Python regression tests.
- 12,354 DAG descriptions checked against the sharing bounds, with 20,738 semantic comparisons of materialized unfolded trees.
- Exact replay of the small promise atlas: 14 YES, 26 gap, and 216 NO tables; all bounded circuits and subcubes enumerated as documented.
- The actual 47-gate zero-threshold network, its classification semantics and full-certificate property checked in Lean.
- The finite two-slot circuit grammar, low-set witnesses, certificate masks, and eight promise edges checked in Lean.
- The general Boolean-subcube counting and isolated-YES lemmas checked in Lean using Mathlib.
- The preceding investigation's recorded files unchanged.

Commands and axiom reports are in `validation/integration_checks.log`. The finite atlas theorems have empty axiom dependencies; the zero-threshold file uses standard `propext`; the general Mathlib counting file uses the standard `propext`, `Classical.choice`, and `Quot.sound`. No new axioms or native-evaluation proof shortcuts are introduced.

**Resource note:** the full finite classifier check exceeded Lean's `-M4096` memory limit. The successful script uses `-M16384` for that one file; the entire run's measured peak resident memory was about 14.6 GiB. The failed resource-limited attempt is preserved as `validation/integration_attempt_4GiB.log`. Its error-generated placeholder declarations are not accepted proofs; only the successful exit-zero run and its permitted axiom lists support the claims.

The generic DAG-to-formula bookkeeping, circuit-description bound, growing-threshold control, patching cost, and seven-gate analytic consequence have explicit manual arguments and independent review rather than a claim that the entire chain is formalized. Neither the external formula lower-bound proof nor the P-versus-NP magnification theorem was rebuilt in Lean.

## Sources and verification scope

- **S1** Oliveira, Pich, and Santhanam, *Hardness Magnification Near State-of-the-Art Lower Bounds*, Theory of Computing 17(11), 2021. Theorem 1.4 and Definition 2.4 govern the magnification target.
- **S2** Chen, Hirahara, Oliveira, Pich, Rajgopal, and Santhanam, *Beyond Natural Proofs: Hardness Magnification and Locality*, JACM 69(4), 2022. Theorem 60 and its proof provide the formula baseline; the source audit records comparisons with other restricted models.
- **S3** Avishay Tal, *Shrinkage of De Morgan Formulae by Spectral Techniques*, FOCS 2014, Theorem 1.2 and Claim 6.2; see the source audit for exact references.
- **Phase 1** The read-only preceding investigation is `research_notes/p_vs_np_2026_10_09/`. Its manifest is retained in `validation/phase1_manifest.json`.

The formal counting bridge has actual Boolean-subcube semantics. The external formula theorem, circuit-description asymptotics, general sharing argument, and resource-sensitive missing step are not silently imported as newly proved Lean facts. Experiment coverage, code tests, exact proof commands, and source hashes are retained alongside the artifacts.
