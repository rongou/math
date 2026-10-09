# Riemann Hypothesis research

Research date: **October 9, 2026**. Repository baseline:
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

**The most useful starting point is this repo's character-sum machinery, but
reaching the critical line requires a new estimate, not simply better numerical
constants.** Below is a concrete sufficient estimate, two obstructions to easy
extensions, and a next research task. This is not a proof of RH.

Clay Mathematics Institute still lists RH as unsolved. Its target is

\[
  \zeta(\rho)=0,\quad 0<\Re\rho<1
  \quad\Longrightarrow\quad \Re\rho=\tfrac12.
\]

The pole at 1 and the trivial zeros are outside this statement. [C1]

## What the repository changes

Family 003 claims a zero-free half-plane \(\Re s>7/8\) for zeta and larger
families of L-functions, with an associated Lean implementation. The
September 30 manuscript is the stronger result; the October 5 companion
presents an alternative \(11/12\) proof. Later publication does not mean a
stronger exponent. These claims are useful research inputs **conditional on
validation**, not evidence that RH has already been resolved. [R7, R11, RL]

For zeta, the claimed \(7/8\) result and the functional equation would confine
nontrivial zeros to \(1/8\le\Re\rho\le7/8\), not to a line. [R7, C2]

## Concrete findings

1. **The companion's single-sum extraction loses substantial power.** It
   averages over sextic twists, then extracts copies of the desired sum from
   rows indexed by sixth powers. Its stated second-moment estimate gives
   \(11/12\). Even if that estimate extended to every averaging scale, the
   resulting two-term extraction bound optimizes only to \(6/7\). This is a
   limitation of that inequality, not of every possible version of the method.
2. **The stronger paper has a separate low-side bottleneck.** Its Mellin signal
   has exponent \(C(s)=s-11/16\), while its direct estimate is
   \(Z^{3/16+\varepsilon}\). Their crossover is exactly \(7/8\). Improving only
   the final row-count certificate cannot move that crossover. With the same
   signal, approaching \(1/2\) would require a low bound approaching
   \(Z^{-3/16+\varepsilon}\): a \(3/8\) improvement in the exponent.
3. **There is a precise, unproved moment target that would suffice.** For the
   companion's original Möbius sums \(A_u(D)\), suppose for every fixed integer
   \(m\ge1\) and every \(\varepsilon>0\),
   \[
     \sum_{0<Nu\le D^3}|A_u(D)|^{2m}
       \ll_{\nu,S,W,m,\varepsilon}D^{m+3+\varepsilon}.
   \]
   Sixth-power extraction would give
   \[
     A_1(D)\ll D^{1/2+5/(4m)+\varepsilon}.
   \]
   Choosing a sufficiently large **fixed** \(m\) for each requested exponent
   loss gives square-root cancellation up to every positive power. The Mellin
   argument then excludes zeros to the right of \(1/2\). Even the trivial
   Hecke target over \(\mathbb Q(\sqrt{-3})\) would suffice for ordinary RH.

The deductions, assumptions, and proofs are in `exponent_analysis.md`.
The all-moments estimate is a **research target**, not a consequence established
by the repo or these checks. An arbitrary-coefficient version is false; actual
Möbius cancellation is indispensable.

## Fourth moment expansion and elementary bound

`fourth_moment.md` now derives the exact Poisson formula with all 15 shared-prime
patterns retained. It also groups the full diagonal into a nonnegative sum and
proves an exact unit-symmetry filter: only product columns whose norms agree
modulo 36 contribute under radial averaging.

The elementary bound obtained is \(O(D^{5+\varepsilon})\) at
\(H=D^{4/3}\), versus the pilot target \(O(D^{10/3+\varepsilon})\).
It is a genuine deduction but gives **no new zero-free region**. The remaining
off-diagonal sum and its missing \(D^{5/3}\) saving are stated explicitly.

## Coprime reflection test

`coprime_reflection.md` carries the calculation one step further. The Möbius
Gauss kernel converts exactly to a divisor-weighted cubic-theta kernel, and
unfolding the divisor weight gives the repo's bilinear cubic twist.

The direct reuse fails for identifiable reasons: a Cauchy–Schwarz step loses
\(D\), and the resulting row scale \(D^{8/3}\) exceeds the canonical target
scale \(D^2\). Even a hypothetical weighted version of the usual completed
bound would give only \(D^{14/3+\varepsilon}\), not P4. That hypothetical
bound is **not a new proved estimate**.

Unrestricting the converted kernel also introduces an artificial diagonal of
size \(D^{4+o(1)}\). This is not a lower bound on the whole energy: other
terms can cancel it. It pinpoints a term that a correct centered calculation
must retain and cancel explicitly.

**Next mathematical input:** a centered bilinear cubic-theta dispersion
estimate preserving both factor variables and the exact gcd corrections.
The current method does not supply it. Increasing the moment order or simply
iterating the existing mean-square bound does not repair these gaps.

The separate seven-eighths verification was attempted in an isolated copy.
Dependency setup succeeded, but the solution build timed out without a
comparator verdict. Its warm build is retained; see `repo_audit.md` and
`results/comparator_attempt.json`. There is
no defensible completion date or compute budget for an RH breakthrough.

## Files and verification

| File | Purpose |
| --- | --- |
| `repo_audit.md` | Exact manuscript and Lean targets, dependency scope, remaining verification |
| `exponent_analysis.md` | Extraction barriers, sufficient all-moments estimate, exact certificate |
| `research_plan.md` | Fourth-moment pilot, bootstrap alternative, proof standards |
| `fourth_moment.md` | Completed expansion, masks, Poisson formula, elementary bound, unresolved cancellation |
| `coprime_reflection.md` | Exact cubic conversion, bilinear reduction, failed descent range, artificial diagonal |
| `references.md` | Local source anchors and checked primary literature |
| `checks/exponent_budget.py` | Exact rational exponent and polynomial calculations |
| `checks/lean_preflight.py` | Read-only static import inventory; not a proof checker |
| `checks/fourth_moment.py` | Exact Eisenstein, finite-field, CRT, and cyclotomic checks |
| `checks/FourthMomentPatterns.lean` | Six kernel-checked finite lemmas; not an analytic formalization |
| `checks/coprime_reflection.py` | Exact cubic conversion tests and explicitly conditional scale calculations |
| `checks/CoprimeScaleObstruction.lean` | Six kernel-checked scale lemmas, not an analytic transformation theorem |
| `checks/run_comparator.py` | Opt-in isolated build runner; downloads dependencies and uses significant disk/time |
| `results/` | Reproducible calculation and preflight outputs |

Run from the repository root. The Python checks require Python 3.10 or newer
and no additional Python packages. The last two commands use the pinned Lean
4.34.1 toolchain with `Std`, without fetching the project's Lake dependencies:

```sh
python3 -m unittest discover -s research_notes/checks -p 'test_*.py' -v
python3 research_notes/checks/exponent_budget.py
python3 research_notes/checks/lean_preflight.py
python3 research_notes/checks/fourth_moment.py
python3 research_notes/checks/coprime_reflection.py
(cd lean && lean ../research_notes/checks/FourthMomentPatterns.lean)
(cd lean && lean ../research_notes/checks/CoprimeScaleObstruction.lean)
```

**Checked here:** 47 Python tests pass, including the endpoint polynomial
certificate, 1,076 local/CRT Fourier equalities, and the coprime Gauss and
bilinear conversion checks. Twelve small finite/scale Lean lemmas also check;
their reports use at most the three standard permitted axioms. The static import inventory
finds 2,924 local modules and 486,490 source lines. This is a module closure,
not a minimal proof dependency count.

**Not established:** a successful seven-eighths comparator verdict, a full
independent manuscript verification, or a formalization of the analytic
fourth-moment argument. P4 and the all-moments estimate remain unproved.
Repository changes are confined to `research_notes`; the verification attempt
also has an isolated temporary source/build copy. Reference keys resolve in
`references.md`.
