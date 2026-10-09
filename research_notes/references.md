# Sources and claim status

Primary literature was checked on October 9, 2026. The local baseline is
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.
Web sources establish the cited historical theorems or the dated status;
they do not validate the new research targets.

## Local sources

### R7 The stronger manuscript

OpenAI, **The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re(s)>7/8**,
September 30, 2026.

Source:
`preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/build/paper.tex`.

Useful stable TeX labels and locations at this revision:

| Label | Subject | Approximate source lines |
| --- | --- | --- |
| `thm:main` | Main claim | 116–130 |
| `lem:continuation-criterion` | Common-signal continuation | 399–521 |
| `prop:probe-low`, `old-eq:5.11` | Direct bound and Mellin crossover | 8559–8650 |
| `lem:marked` | Marked inverse second moment | 9250–9281 |
| `lem:plain` | Plain fourth moment and \(\kappa\)-range | 12531–12600 |
| `eq:common-high-exponent` | One-bin exponent accounting | 15699–15755 |
| `eq:balanced-endpoint-certificate` | Exact positivity identity | 15995–16074 |
| `prop:parameter-order` | Uniform margins and dependency order | 16189 onward |

### R11 The simpler companion

OpenAI, **The Quasi-Riemann Hypothesis**, October 5, 2026.

Source:
`preprints/The-Quasi-Riemann-Hypothesis-October-5-2026/build/paper2.tex`.

- `sec:outline`: five-step proof outline.
- `sec:reduction`, `thm:ms`, `eq:ms`: the original second moment and its
  uniformity in smooth weights.
- `eq:prime-extract`, `eq:mobius-saving`: extraction and \(11/12\) exponent.
- The remainder of `sec:reduction`: Mellin contradiction and quadratic base
  change to Dirichlet L-functions.
- `sec:descent`, `prop:canonical`, `eq:positive-gap`: the strict row/target
  gap required by the two-Poisson recursion.
- `prop:R`, `eq:R`: the completed normalized energy bound.
- `eq:cube-cutoff`, `lem:cube-reduction`, `eq:transfer-scales`: cutoff,
  hypotheses, and genuine shortening step.
- `eq:T`, `eq:completed-twist`, `lem:reflection`: the allowed multiplicative
  twist and precise scope of the theta reflection.
- `lem:poisson`, `eq:poisson` (around lines 879–936): the excluded-prime
  Poisson normalization independently derived in `fourth_moment.md`.
- `lem:arithmetic`, `eq:gj`, `eq:convert1`, `eq:convert2`: cubic/sextic
  Gauss normalizations; small-prime checks are in `test_fourth_moment.py`.

### RL Lean interfaces and configuration

- `lean/docs/003.md`: declared scope of formalization.
- `lean/OAI/NumberTheory/DirichletL/Nonvanishing.lean`: public zeta and
  Dirichlet targets.
- `lean/OAI/NumberTheory/DirichletL/Detector/FinalAssemblyUnconditional.lean`:
  final source of the certified-band input.
- `lean/OAI/NumberTheory/DirichletL/Detector/FinalAssemblyCertifiedBands.lean`:
  transition from that input to nonvanishing.
- `lean/ComparatorChallenges/QuasiRiemannHypothesis.json`: comparison and
  permitted-axiom configuration.
- `lean/ComparatorChallenges/README.md`: documented verification commands.
- `lean/lean-toolchain`, `lean/lakefile.lean`, `lean/lake-manifest.json`:
  build and dependency baseline.

## External primary references

### C1 Current problem status

Clay Mathematics Institute, **Riemann Hypothesis**. The page labels the
problem “Unsolved” and states the critical-line target.

`https://www.claymath.org/millennium/Riemann-Hypothesis/`

### C2 Official mathematical problem description

Enrico Bombieri, **Problems of the Millennium: the Riemann Hypothesis**,
Clay Mathematics Institute. Section I supplies the analytic continuation,
functional equation, and statement; Section V discusses explicit-formula
positivity and the spectral/geometric viewpoint. Its old numerical records
are not used as current records here.

`https://www.claymath.org/wp-content/uploads/2022/05/riemann.pdf`

### C3 Li positivity

Enrico Bombieri and Jeffrey C. Lagarias, **Complements to Li's Criterion for
the Riemann Hypothesis**, Journal of Number Theory 77 (1999), 274–287.
Introduction and Theorem 1; the introduction states Li's derivative formula
and equivalence. The first PDF page was inspected visually because its text
extraction is corrupted. This complements Xian-Jin Li's 1997 theorem.

`https://websites.umich.edu/~lagarias/doc/bombieri.pdf`

DOI: `10.1006/jnth.1999.2392`.

### C4 The de Bruijn Newman constant

Brad Rodgers and Terence Tao, **The De Bruijn-Newman constant is non-negative**,
arXiv:1801.05914, first submitted January 18, 2018; inspected version 5,
revised July 3, 2021. The abstract states \(\Lambda\ge0\) and RH's equivalence
to \(\Lambda\le0\).

`https://arxiv.org/abs/1801.05914v5`

### C5 Jensen hyperbolicity

Michael Griffin, Ken Ono, Larry Rolen, and Don Zagier, **Jensen polynomials for
the Riemann zeta function and other sequences**, PNAS 116 (2019), 11103–11110;
arXiv:1902.07321. Theorem 1 in the inspected version 2 states eventual
hyperbolicity at each fixed degree; this does not assert all degrees and
shifts simultaneously.

`https://arxiv.org/abs/1902.07321v2`

`https://arxiv.org/pdf/1902.07321`

DOI: `10.1073/pnas.1902572116`.

### C6 Rigorous finite height verification

Dave Platt and Tim Trudgian, **The Riemann hypothesis is true up to
3·10^12**, Bulletin of the London Mathematical Society 53 (2021), 792–797;
arXiv:2004.09765, submitted April 21, 2020. The abstract specifies a rigorous
interval-arithmetic verification up to height \(3\cdot10^{12}\).
Height is not a count of zeros, and this is not labeled the latest record.

`https://arxiv.org/abs/2004.09765`

DOI: `10.1112/blms.12460`.

### C7 Large values and zero density

Larry Guth and James Maynard, **New large value estimates for Dirichlet
polynomials**, Annals of Mathematics 203 (2026), 623–675;
arXiv:2405.20552. The publication's abstract describes improved large-value
and zero-density estimates. It does not claim a zero-free half-plane or RH.

`https://annals.math.princeton.edu/2026/203-2/p06`

`https://arxiv.org/abs/2405.20552`

### C8 Cubic Gauss dispersion and its conditional inputs

Alexander Dunn and Maksym Radziwiłł, **Bias in cubic Gauss sums: Patterson's
conjecture**, arXiv:2109.07463 (2021). The abstract explicitly describes the
GRH dependence of its bias, sharpness, and key dispersion results. Its theta
summation formulas must be distinguished from those conditional estimates.
No GRH-conditional estimate is used in our deductions.

`https://arxiv.org/abs/2109.07463`

## Evidence labels

- **Repository claim:** a statement and accompanying argument/artifact exist
  in this checkout; this investigation has not independently validated the
  full proof.
- **Derived:** the notes give the deduction from stated assumptions. Exact
  arithmetic checks support the finite algebra, not the analytic assumptions.
- **Research target:** an unproved proposed input. No passing test supplies it.
- **Checked here:** the recorded Python arithmetic tests and static preflight,
  plus twelve explicitly scoped finite/scale lemmas checked by Lean. This does not mean
  the repository's \(7/8\) proof or the analytic research targets were checked
  by the kernel or comparator.
