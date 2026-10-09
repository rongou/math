# P versus NP restriction lemma investigation

October 9, 2026. Source revision: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

The supplied family 112 depth-three theorem passes its configured Lean comparator. Its restriction lemma transfers to conjunctions of arbitrary predicates on bounded sets of raw input variables. That transfer does not extend to arbitrary circuit composition: six-bit parity gives an exact counterexample to replacing CNF width with maximum gate fan-in. The work below establishes these elementary transfers and limitations, not a complexity-class separation or a novel lower-bound breakthrough.

## The verified starting theorem

Family 112 constructs a fixed language in P whose length-n membership functions require `2^{omega(sqrt(n))}` gates in OR–AND–OR circuits. The actual theorem is in `lean/OAI/Computability/DepthThree/Main.lean:8`, and its declared scope is in `lean/docs/112.md:9`.

The targeted build and supplied comparator both exit successfully under the pinned Lean 4.34.1 toolchain. The theorem's axiom dependencies are exactly `propext`, `Classical.choice`, and `Quot.sound`. The comparator uses Lean's default kernel; its supplied configuration disables Nanoda. The challenge module's intentional `sorry` is not a hole in the solution. Build commands, exact pins, hashes, and scope are recorded in `validation/build_validation.json` and its numbered logs. A separate source audit found no substantive mismatch or extra public premise in the restriction lemma's statement and inspected definitions (`validation/static_semantics.json`).

Here is the reusable lemma. Let H be a width-k CNF, let b be at least one, and independently leave each input live with probability p, fixing other bits uniformly. Write

\[
\theta(k,b,p)=\sum_{\ell=b+1}^{k}\binom{k}{\ell}
                 \left(\frac{2p}{1-p}\right)^\ell.
\]

For `0 < p < 1` and `theta < 1`, there is one nonnegative cost W for each restriction sigma such that

\[
\mathbb E_\sigma W(\sigma)\le\frac1{1-\theta},\qquad
|\mathbb E_z G(z)H_\sigma(z)|
  \le W(\sigma)\operatorname{corr}_b(G)
\]

for every real-valued G on the live cube. The correlation measure is the maximum of `|E GJ|` over width-b CNF indicators J. The same W works for all G; it does not depend on a clause-count bound. This is `OAI.DepthThreeLowerBound.cnf_restriction_bound` in `Restriction.lean:59`.

The manuscript's proof uses signed combinations of narrow CNFs, with path weights normalized by counts of violated clauses. Its final circuit argument additionally uses the fact that each middle gate is a CNF accepting only positive inputs. The restriction lemma and that final circuit step must not be conflated.

## Local predicates admit the same restriction bound

Let Q be any Boolean predicate on r input bits. For each rejected assignment a, form the clause

\[
C_a(x)=\bigvee_{i=1}^{r}(x_i\ne a_i).
\]

Then, exactly,

\[
Q(x)=\bigwedge_{a:Q(a)=0}C_a(x).
\]

**Proof.** If Q(x) is true, x differs from every rejected a, so all clauses hold. If Q(x) is false, the clause indexed by a=x fails. There are at most `2^r` rejected assignments, and each clause has width at most r. An empty scope produces either the empty conjunction (true) or one empty clause (false).

Consequently, a finite conjunction of arbitrary predicates, each reading at most k **raw input variables**, is a width-k CNF after this expansion. Applying the source restriction lemma gives precisely the same theta and expected-cost bound, without a factor counting predicates or their forbidden patterns.

`validation/LocalPredicateCNF.lean` kernel-checks the predicate identity, conjunction and disjunction-of-conjunctions lifting, truth-table list construction, and the `2^r` clause bound using Std alone. Its axiom audit and compiler invocation are in `validation/local_predicate_lean.json`.

`validation/PredicateRestriction.lean` then proves the actual corollary against the repository's definitions, under the name `OAI.DepthThreeLowerBound.PredicateRestriction.predicate_restriction_bound`. It preserves the original theta, expectation, and universal quantification over real-valued G. The formal interface supplies at most k input positions per predicate and permits repetitions; no efficiency premise is hidden. Its check passes with exactly the original three permitted axioms (`validation/predicate_restriction.json`).

This is a semantic reduction, not an efficient compilation claim for growing r. Enumerating `2^r` patterns may be prohibitively expensive. Nor does a gate with k incoming wires necessarily depend on only k raw input variables when its wires carry intermediate computations.

## Bottom oracle gates can be eliminated

Consider an OR–AND circuit whose shared bottom gates are arbitrary predicates of at most q raw input bits. Count B bottom gates, M middle gates, and one output gate, so its size is `S=B+M+1`.

First express each predicate on its distinct raw variables, removing repeated input wires. Expand each bottom predicate once into at most `2^q` clauses, retaining sharing of the new clauses across all middle gates that used the old predicate. The result is an ordinary OR–AND–OR circuit for the same function with

\[
S_{\rm compiled}\le B2^q+M+1\le S2^q.
\]

Therefore, conditional on the verified source theorem, its hard language still requires `2^{omega(sqrt(n))}` gates in this bottom-oracle model whenever `q(n)=O(sqrt(n))`. Indeed, subtracting `q(n)` from the base-two logarithm of the ordinary depth-three lower bound cannot make its ratio to `sqrt(n)` bounded.

This argument handles **bottom predicates on raw bits only**. It is not a simulation of circuits with arbitrarily placed internal oracle gates. The compilation and size bound have exhaustive finite tests for small predicates and seeded tests for shared circuit layouts in `experiments/locality_probe.py`; the general gate-count argument above is elementary and is not asserted to be kernel-formalized.

## A six bit counterexample to unrestricted composition

A tempting extension is to keep the same correlation inequality and theta but let H be any Boolean circuit, with k interpreted as its maximum gate fan-in. That extension is false.

Let H indicate even parity on d input bits. A restriction leaving m live bits gives either parity or its complement when m is positive. Let

\[
\chi_m(z)=(-1)^{z_1+\cdots+z_m}.
\]

A consistent width-one CNF is a subcube. If it leaves any coordinate free, its correlation with `chi_m` is zero by cancellation. If it fixes every coordinate, the absolute correlation is `2^{-m}`. The false CNF contributes zero. Thus, for positive m,

\[
\operatorname{corr}_1(\chi_m)=2^{-m},\qquad
|\mathbb E\chi_m H_\sigma|=\frac12.
\]

Every cost satisfying the inequality for **all G** must therefore satisfy

\[
W(\sigma)\ge 2^{m-1}.
\]

This lower bound is exact: H_sigma is the sum of its `2^{m-1}` accepted singleton indicators, each a width-one CNF. When m=0, the exact minimum is the constant value of H_sigma, zero or one. Averaged over a uniformly fixed full assignment, that value is one-half for d at least one.

Since the number of live bits is binomial with parameters d and p, the exact expected minimum cost is

\[
\mathbb E_\sigma W_{\min}(\sigma)=\frac{(1+p)^d}{2}.
\]

Take `d=6`, `b=1`, and `p=1/4`. Even parity has an ordinary AND/OR/NOT circuit with 21 gates and maximum fan-in two; the included circuit construction has depth ten and is checked on all 64 inputs. Substituting `k=2` into the proposed extension would give

\[
\theta=\left(\frac{2/4}{3/4}\right)^2=\frac49,
\qquad\mathbb E W\le\frac95.
\]

But the necessary cost is

\[
\mathbb E W\ge\frac{(5/4)^6}{2}
=\frac{15625}{8192}
>\frac95.
\]

The strict difference is `4397/40960`. `experiments/locality_probe.py` checks the subcube correlations, matching singleton decompositions, all 729 six-bit restrictions, and the rational weighted sum. It also verifies the expectation identity exhaustively through dimension eight. These finite checks supplement the proof, rather than establish its all-dimension conclusion.

`validation/ParityCertificate.lean` provides a separate kernel-checked finite certificate. With restriction probabilities written over the common denominator `8^6`, it verifies a total probability numerator of `262144`, a cost numerator of `500000`, every required subcube maximum through six live bits, and `5*500000 > 9*8^6`. All 19 theorem axiom lists are empty. The conversion of this certificate to the real-valued all-G inequality is the analytic argument above, not an additional Lean theorem (`validation/parity_certificate.json`).

**This does not contradict the paper.** CNF width is a bound on a clause's raw-variable scope, not on each gate's incoming wires in a composed circuit. The example rules out this specific extension, not all circuit restriction arguments, all depth-dependent bounds, or P versus NP itself.

## The magnification target remains a separate hypothesis

Oliveira, Pich, and Santhanam's Theorem 1.4 gives a sufficient target [S1]. Let an m-input function's truth table have length `N=2^m`. For the theorem's universal constant c, establish some fixed positive epsilon such that, for every sufficiently small fixed positive beta,

\[
\operatorname{GapMCSP}
\left[\frac{N^\beta}{c\log_2 N},N^\beta\right]
\notin\operatorname{Circuit}[N^{1+\varepsilon}].
\]

Then NP has no polynomial-size circuit families, which implies P is different from NP. The input to the circuit being lower-bounded is the **whole N-bit truth table**, not the m-bit input of the represented function. These are unrestricted-depth, bounded-fan-in solver circuits. Definition 2.4 uses YES for represented circuit size at most the lower threshold and NO for size **strictly greater than** the upper threshold. The intervening range, including the upper endpoint, is unpromised. Thresholds are integer-valued; the displayed expressions suppress rounding. One fixed epsilon must work for every sufficiently small fixed beta; infinitely many hard lengths for each beta suffice.

This hypothesis has not been proved here, and the literature implication has not been formalized in this investigation. In particular, a depth-three lower bound for the repository's language in P cannot be substituted for this hypothesis. Every polynomial-time language has polynomial-size unrestricted circuits [S3].

## Uniform truth tables create another obstruction

There is also a simple distribution mismatch. This is an elementary counting deduction, not a new hardness theorem.

An m-input Boolean circuit with at most s gates over the basis of all 16 binary Boolean functions can be described by a topological gate list, two input indices per gate, and an output index. Including two constants and padding shorter lists gives the upper bound

\[
K(m,s)=(m+s+2)\,[16(m+s+2)^2]^s
\]

on the number of distinct functions computable with at most s gates. Overcounting descriptions is harmless.

Let s be the ceiling of the upper GapMCSP threshold `N^beta`, with fixed `0<beta<1`. Any total Boolean extension of that promise which accepts low-complexity tables can accept only tables of circuit complexity at most the upper threshold: all higher-complexity tables are promised NO instances. Under the uniform distribution on all N-bit tables, its positive density is at most

\[
\frac{K(m,s)}{2^N}=2^{-N+O(N^\beta\log N)}=o(1).
\]

For the associated sign g, the constant-true CNF gives

\[
\operatorname{corr}_b(g)\ge|\mathbb E g|=1-o(1).
\]

Thus the source proof's small-correlation, nearly balanced-sign strategy cannot be directly imposed on a total extension of GapMCSP under the uniform whole-table distribution. A suitable different distribution, reduction, or slice would need its own argument. This says nothing against distributions other than uniform whole tables or against lower-bound methods not using this correlation criterion.

## What the locality evidence establishes

The predicate expansion proves that the source lemma is insensitive to the internal description of a bounded-arity predicate on raw variables. The circuit simulation proves robustness to one specified bottom layer of local gates.

The directly relevant oracle upper bound is Proposition 64 of the published JACM version of [S2] (Proposition 63 in the arXiv version). For the OPS construction with parameter s, it permits `N poly(s)` gates and oracle gates, oracle arity `poly(s)`, and oracle adaptivity `poly(s)`. An oracle can read computed wires, not just raw inputs. Bottom-layer robustness alone therefore does not establish the closure property needed to apply that locality obstruction. Nor does the literature exclude every random-restriction method; it also contains a non-localizable random-restriction lower bound. Exact model and version distinctions are in `sources/magnification_audit.json`.

The immediate conclusions are narrower and definitive:

- Increasing bottom predicate expressiveness does not by itself produce the missing bridge.
- Replacing CNF width by maximum circuit gate fan-in fails, already on six-bit parity.
- Uniform whole-table CNF correlation is unsuitable for the stated GapMCSP promise.
- This language in P cannot itself have superpolynomial unrestricted-circuit complexity. Its current depth-three lower bound does not supply the GapMCSP magnification hypothesis.

A next candidate lemma must address composition or reuse without the disproved width substitution, and must apply to the correct magnification problem and distribution. Neither an additional circuit layer nor a better constant in the current estimate automatically meets those requirements.

## Verification results

| Check | Result | Evidence |
| --- | --- | --- |
| Supplied family 112 theorem | Targeted build and configured comparator pass | `validation/build_validation.json` |
| Local predicate CNF construction | 11 Std-only theorems checked | `validation/local_predicate_lean.json` |
| Actual predicate restriction corollary | 9 declarations checked, including the full bound | `validation/predicate_restriction.json` |
| Finite parity certificate | 19 theorems checked, no axioms | `validation/parity_certificate.json` |
| Python regression tests | 33 tests pass after review fixes | `validation/post_review_checks.log` |
| Original restriction construction | 3,951 formula instances; 602,754 formula/cutoff/restriction cases; 1,940,682 pointwise expansions | `experiments/restriction_results.json` |
| Original expected-cost bounds | 38,306 coefficient comparisons and all 11,535 eligible geometric comparisons pass | `experiments/restriction_results.json` |
| Predicate and shared-circuit compilation | All 278 Boolean predicates of arity zero through three; 306 circuit layouts | `experiments/locality_results.json` |

The original-lemma experiment exhausts canonical clause multisets with at most two clauses through dimension four, then adds specified and seeded examples through dimension six. It does not exhaust arbitrary CNFs. It retains indexed duplicate clauses and tests true/false constants, overlap, incompatible paths, empty live sets, finite mixtures, and reverse-counting identities. No original-lemma counterexample was found in this bounded suite.

An adversarial agent review identified a mismatch between repeated input-wire arity and distinct raw-variable scope in the initial Python compiler. The compiler now normalizes repeated coordinates before expansion, and explicit regression tests cover the reported witness. The mathematical existence proof was unaffected. The review also prompted narrower wording about the impossible superpolynomial unrestricted-circuit target for a language in P. Review records and resolutions are in `validation/peer_review.json` and `validation/review_resolutions.json`.

## Reproducing the checks

The finite experiments use Python's standard library and exact `Fraction` arithmetic, not a floating-point optimizer. The convenience script runs both full bounded experiments, the regression suite, and the two Std-only proof files:

```bash
research_notes/p_vs_np_2026_10_09/validation/check.sh
```

Supply a fully built OAI Lean project directory as its sole argument to also check `PredicateRestriction.lean`; the script compiles its local helper into a fresh temporary directory. It does not build the repository or rerun the family 112 comparator. `validation/integration_checks.log` records a successful coordinator run with that argument, and `validation/post_review_checks.log` records the final Python compiler fixes.

Individual finite commands, from the repository root:

```bash
python3 -m unittest discover \
  -s research_notes/p_vs_np_2026_10_09/experiments -p 'test_*.py' -v
python3 research_notes/p_vs_np_2026_10_09/experiments/restriction_check.py \
  --output research_notes/p_vs_np_2026_10_09/experiments/restriction_results.json
python3 research_notes/p_vs_np_2026_10_09/experiments/locality_probe.py \
  --output research_notes/p_vs_np_2026_10_09/experiments/locality_results.json
```

The independent Std-only predicate proof is checked with:

```bash
lean +leanprover/lean4:v4.34.1 --trust=0 --error=warning \
  research_notes/p_vs_np_2026_10_09/validation/LocalPredicateCNF.lean
```

For family 112, after obtaining the repository's exact pinned dependencies, run:

```bash
cd lean
lake build +OAI.Computability.DepthThree.Main +ComparatorChallenges.DepthThree
lake env comparator ComparatorChallenges/DepthThree.json
```

This investigation ran those commands in an isolated source snapshot, without `lake update` or changes to the tracked repository. Full commands, cache setup, source manifests, compiler hashes, and successful outputs are retained in the validation logs. Finite tests are not substitutes for the source theorem's proof, and the formal check certifies the encoded theorem rather than an unstated extension to other computational models.

## Sources

- **S1** Igor C. Oliveira, Jan Pich, and Rahul Santhanam. *Hardness Magnification Near State-of-the-Art Lower Bounds*. Theory of Computing 17(11), 2021. Theorem 1.4.
- **S2** Lijie Chen, Shuichi Hirahara, Igor C. Oliveira, Jan Pich, Ninad Rajgopal, and Rahul Santhanam. *Beyond Natural Proofs: Hardness Magnification and Locality*. JACM, 2022; arXiv version 1911.08297. Consult the source audit for model-specific scope.
- **S3** Stephen Cook. *The P versus NP Problem*. Clay Mathematics Institute official problem description.
- **Repository** Family 112 manuscript and proof artifacts at the source revision above; especially `Restriction.lean`, `Core.lean`, `Model.lean`, and manuscript sections 2 and 5.

The compiler transfer, counting bound, and parity obstruction above are elementary consequences or calculations presented with proofs. No claim of novelty, P versus NP resolution, or formal verification of the external magnification theorem is made.
