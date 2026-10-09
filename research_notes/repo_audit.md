# Repository baseline and verification scope

Baseline: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, inspected October 9, 2026.
All paths below are relative to the repository root.

## Claims and dates

| Source | Exact relevant claim | Scope in this investigation |
| --- | --- | --- |
| [R7], September 30, 2026 | All finite-order Hecke L-functions over \(\mathbb Q(\sqrt{-3})\), and all Dirichlet L-functions, are zero-free for \(\Re s>7/8\), allowing principal poles | Main reduction, moment hypotheses, low bound, and endpoint algebra examined; full proof not independently verified |
| [R11], October 5, 2026 | Alternative proof with boundary \(11/12\) | Used to reconstruct the prime-power extraction and Mellin argument |
| [RL] | Lean formalization associated with the \(7/8\) statement | Public target and final assembly inspected; static import preflight run |
| Root `README.md` | Results have different verification statuses; unformalized results can contain issues | A release entry alone is not independent validation |

The September 30 paper has 16,677 lines of TeX; the October 5 companion has
3,988. The latter says it was written with human assistance. It should not be
mistaken for a later improvement of \(7/8\). [R7, R11]

## The Lean target is the actual zeta function

The comparator configuration is
`lean/ComparatorChallenges/QuasiRiemannHypothesis.json`.
It identifies the solution module
`OAI.NumberTheory.DirichletL.Nonvanishing` and the declaration

```lean
OAI.riemannZeta_ne_zero_of_seven_eighths_lt_re
```

The public implementation has the statement

```lean
theorem riemannZeta_ne_zero_of_seven_eighths_lt_re
    {s : ℂ} (hs : (7 / 8 : ℝ) < s.re) : riemannZeta s ≠ 0
```

It calls `SevenEighths.ProbeFinalAssemblyUnconditional.zeta_nonzero`.
In `Detector/FinalAssemblyUnconditional.lean`, the required
`DetectorCertifiedBands` input is itself supplied by a theorem, rather than
left as an extra hypothesis on the public result. This is a useful interface
check, **not a verification of that theorem's proof**. [RL]

The `sorry` in
`lean/ComparatorChallenges/QuasiRiemannHypothesis.lean` is in the comparator's
challenge template. It is not the solution implementation; treating that stub
as a discovered gap would be a mistake.

The JSON permits only `propext`, `Quot.sound`, and `Classical.choice`, and sets
`enable_nanoda` to `false`. This records the requested checking configuration,
not a successful check. The final RH statement should be compared on
\(0<\Re s<1\), avoiding any ambiguity about a totalized function's value at
its meromorphic pole. [RL]

## Static preflight results

`research_notes/results/lean_preflight.json` records:

- Pinned and installed Lean version: **4.34.1**.
- `lake`, `comparator`, `landrun`, and `lean4export` are present on `PATH`.
- `lean/.lake` is absent: dependencies and local build artifacts have not been
  materialized in this checkout.
- Ordinary-import closure of the solution: **2,924 local modules**, **486,490
  local source lines**, and **251 distinct external import names**.
- No lexical hits for `sorry`, `admit`, `axiom`, `unsafe`, `native_decide`, or
  `sorryAx` after masking comments and ordinary strings in those local sources.

The import inventory includes broad aggregation modules, so it overcounts the
minimal declaration-level dependencies of this one theorem. External imports
are counted, not recursively audited. The absence of suspicious tokens says
nothing conclusive about generated declarations, elaboration, allowed axioms,
or whether the formalized definitions match the intended mathematics.

## Isolated verification attempt on October 9

The documented workflow was attempted in a fresh copy of the pinned Lean
source, with an eight-CPU affinity and a 900-second total limit after source
extraction. The result is **incomplete verification**, not a mathematical
failure of the paper.

| Stage | Outcome |
| --- | --- |
| `lake update` | Exit 0, 124.830 seconds |
| `lake exe cache get` | Exit 0, 14.624 seconds |
| `lake env comparator ComparatorChallenges/QuasiRiemannHypothesis.json` | Timed out with exit 124 after 760.033 seconds |

The comparator built and exported the challenge, then began compiling the
solution dependencies. The last reported solution-build task counter was
**4412/7061**. This counts build tasks, including dependencies/cached work;
it is not a percentage of mathematical proof verification.

There was **no final comparator verdict or final solution axiom report**.
The challenge's `sorry` warning is expected for that template, not a new gap.
Dependency local-change warnings accompanied the compatibility patches shipped
with the repository. The manifest was unchanged by setup.

Six critical source files in the isolated copy match the pinned Git source:
toolchain, Lake configuration, manifest, challenge source, comparator JSON,
and public solution module. Their hashes, stage timings, and the final status
are in `research_notes/results/comparator_attempt.json`; the full output is in
`research_notes/results/comparator_attempt.log`.

The approximately 12 GB source/build copy was retained at
`/tmp/rh-comparator-fkzoq9se`. No processes were left running in that directory
after the timeout. The working checkout's `lean/` was not modified.

To continue from the retained artifacts, if that temporary directory still
exists, run a longer comparator attempt there rather than downloading and
rebuilding the cold copy again:

```sh
cd /tmp/rh-comparator-fkzoq9se/lean
timeout --signal=TERM --kill-after=10s 3600s \
  lake env comparator ComparatorChallenges/QuasiRiemannHypothesis.json
```

That continuation has **not** been run. A repeatable cold-start workflow is
available as `python3 research_notes/checks/run_comparator.py --run --seconds 900`; it explicitly
opts into dependency downloads and creates another temporary copy.

The twelve small finite/scale lemmas in the two research Lean files were
checked separately. They do not validate the analytic seven-eighths proof.

### Completing the independent validation

For a fresh verification rather than resuming the warm copy, follow the repository's
`lean/ComparatorChallenges/README.md`:

```sh
cd lean
lake update
lake exe cache get
lake env comparator ComparatorChallenges/QuasiRiemannHypothesis.json
```

Archive the resolved dependencies, exact commands, versions, logs, exit codes,
and final axiom report. Review dependency or manifest changes instead of
silently accepting a different baseline. Build only the relevant target, not
the entire OAI library.

Once the implementation is built, inspect its elaborated statement and
`#print axioms OAI.riemannZeta_ne_zero_of_seven_eighths_lt_re`. Validate the
Dirichlet/Hecke comparisons as well before using those stronger statements in
a family-wide argument. Kernel checking, external checking, and mathematical
statement review are separate checks; the last remains necessary even when
the first succeeds.

## Mathematical dependency outline

### The simpler companion

[R11] organizes its argument as follows:

1. Define smoothed ideal Möbius sums with sextic row twists.
2. Claim a square-root-sized second moment on average over
   \(0<Nu\le H=D^{1+\vartheta}\), for each fixed
   \(0<\vartheta\le1/10\).
3. Expand the square and apply Poisson summation. A Gauss-sum identity changes
   Möbius coefficients into cubic theta coefficients.
4. Complete the theta coefficients by retaining cube factors, reflect the
   completed sum, and apply a quadratic large sieve.
5. Undo cube completion by Möbius inversion. A two-Poisson recursion handles
   the long cube-divisor remainder while preserving masks and fixed twists.
6. Extract the desired sum from rows \(u=p^6\); use Mellin transforms to obtain
   the \(11/12\) half-plane.

Step 6 is independently reconstructed in `exponent_analysis.md`. That does
not verify Steps 2–5.

### The stronger manuscript

[R7] uses a different probe and a family-wide supremum \(\beta_*\) of possible
zero real parts. Its common-signal continuation proposition is parameterized
by \(\sigma_0\in(1/2,1)\). With \(C(s)=s+c\), it requires

\[
 |J_\eta(Z)|\ll_\eta Z^{C(\sigma_0)+\omega},\qquad
 |J_\eta(Z)-f_\eta(Z)|\ll_\eta Z^{C(\beta_*)-\sigma},
\]

where \(0<\omega<\beta_*-\sigma_0\) and \(\sigma>0\) are independent of
\(\eta\). The signal is a Mellin integral containing
\(H_\eta(s)/L_K^S(s,\eta)\), with \(|H_\eta-1|\le1/2\).
The bounds continue every reciprocal past a common distance below
\(\beta_*\), contradicting its definition. The supremum need not be attained.
Fixed-character constants and thresholds may depend on the character;
the exponent gap cannot. [R7, `lem:continuation-criterion`]

For Part II:

- \(C(s)=s-11/16\); the direct bound is
  \(Z^{3/16+\varepsilon}\).
- The high comparison uses prime compensation, a marked inverse second
  moment, and a separate fourth moment of **plain** character polynomials.
- The contradiction assumes
  \(0<\Delta=\beta_*-7/8\le1/24\), using Part I.
- Its dynamic parameter is \(\kappa=2\beta_*-1\in(3/4,5/6]\).
  The plain-moment lemma is stated only for \(3/4\le\kappa\le1\).
- The ideal low and high margins are respectively \(\Delta\) and
  \((51/64)\Delta\), before allocating all other losses. [R7]

The exact endpoint identity behind one high-side bound was checked here. The
low-side threshold and the restricted \(\kappa\)-range remain substantive
obstacles to treating this as an iteration toward \(1/2\).

## What an extension must preserve

- **Actual arithmetic functions:** a bound on a newly defined surrogate is
  useful only after proving its identity with the original Möbius/L-function
  object.
- **Zero extensions:** even a sixth-power character value is an indicator of
  coprimality, not identically 1. Canceled character powers can retain masks.
- **Principal contributions:** separate genuine poles, zero frequencies, and
  inducing characters in the finite exceptional family before discarding terms.
- **Quantifiers:** parameter and height choices must obey the stated dependency
  order; do not quietly use a different exponent gap for each target character.
- **Full scale ranges:** an estimate on fixed compact parameter ranges cannot
  automatically be continued to a boundary where those ranges degenerate.
- **Normalization:** multiplying the probe by a power of \(Z\) shifts both the
  direct bound and the signal, leaving their crossover unchanged.

These are extension requirements and audit priorities, not allegations of gaps
in the existing manuscripts.
