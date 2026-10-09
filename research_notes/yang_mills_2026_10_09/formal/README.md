# Scalar constants only: an axiom-free Lean certificate

This is **not a formalization of Yang–Mills or of the real/spectral finite-size
criterion**. It checks the stated constants and proves the full
**denominator-cleared natural-number scalar induction**, conditional on explicit
scalar input inequalities.

## Files and reproduction

- `ScalarConstants.lean`: the certificate, induction, boundary tests, and axiom
  audit assertions; its only explicit import is the installed `Std`.
- `check.sh`: standalone checker; no Lake, configuration changes, or downloads.
- `compiler-output.txt`: the actual successful compiler output.
- `validation-output.txt`: dependency and deliberately failing mutation tests.

From `/home/rou/src/math/research_notes/yang_mills_2026_10_09/formal`, the exact
compiler command is:

```sh
env -u LEAN_PATH -u LEAN_SRC_PATH \
  /home/rou/.elan/toolchains/leanprover--lean4---v4.34.1/bin/lean \
  --trust=0 ScalarConstants.lean
```

Equivalently, run `./check.sh`. To regenerate the compiler transcript:

```sh
./check.sh > compiler-output.txt 2>&1
```

Verified with:

```text
Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)
```

The command exits **0**, without warnings. It does not invoke the separate rc4
toolchain. `--trust=0` requests checking imported modules too. Clearing the Lean
search-path environment variables prevents use of project-local dependency
paths; the main project's Lean configuration is untouched.

## Precise formal domain and assumptions

Every variable is a `Nat`. The intended **external** rational interpretation is

```text
delta = p/q,  A_i = a_i/q,  u_i = v_i/q.
```

All these quantities are nonnegative in that interpretation. `Inputs` requires:

```text
0 < q                    2048*p <= q

a1 <= p
a2 <= 2*p + v1
a3 <= 4*p + 2*v1 + v2
a4 <= 8*p + 4*v1 + 2*v2 + v3

for each i: 4*a_i <= q -> v_i*q <= 4*(a_i*a_i).
```

The last four implications are the denominator-cleared **local loss law**
`A_i <= 1/4 -> u_i <= 4*A_i^2`. They are explicit hypotheses, not proved analytic
facts. No final bounds `u_i <= K_i*delta^2`, no weighted bound, and no quarter
cutoffs are smuggled into the hypotheses. The proof establishes each quarter
cutoff before using its local loss law. Positivity of `q` is used to cancel a
factor of `q`; it is not omitted at the zero boundary.

## What Lean proves

`scalar_induction : Inputs ... -> Bounds ...` proves:

| Statement under the rational interpretation | Actual Nat conclusion |
|---|---|
| `A_i <= (1,3,5,9)_i * delta` | `a_i <= (1,3,5,9)_i * p` |
| All three intermediate recurrence RHS caps | `2*p+v1 <= 3*p`, `4*p+2*v1+v2 <= 5*p`, `8*p+4*v1+2*v2+v3 <= 9*p` |
| `u_i <= (4,36,100,324)_i * delta^2` | `v_i*q <= (4,36,100,324)_i * (p*p)` |
| Every `A_i <= 1/4` | Every `4*a_i <= q` |
| `8*u1+4*u2+2*u3+u4 <= 700*delta^2` | `(8*v1+4*v2+2*v3+v4)*q <= 700*(p*p)` |
| Relaxation to `1024*delta^2` | Both `700*(p*p) <= 1024*(p*p)` and the relaxed weighted bound |
| `1024*delta <= 1/2` | `2*(1024*p) <= q` |

`constant_checks`, proved with ordinary `decide`, checks:

- `4*(1,3,5,9)^2 = (4,36,100,324)` componentwise;
- corrections `4`, `2*4+36 = 44`, and `4*4+2*36+100 = 188`;
- all absorption and quarter-cutoff coefficient budgets below;
- `8*4+4*36+2*100+324 = 700`, `700+324 = 1024`, and `2*1024 = 2048`.

`polynomial_checks p s` proves universal polynomial identities over `Nat`, with
`q` replaced by `2048*p+s`. It covers all four square scalings, all three stage
gaps, all four quarter cutoffs, the weighted identity, the reserve, and the
contraction identity. These are not evaluations at a finite set of sample
points. Every remainder is a sum of monomials with **natural, hence nonnegative,
coefficients**. `nonnegative_gap_checks p s` derives the three stage inequalities
from those identities using Nat order, without abstract order assumptions.

For orientation only, dividing these identities by positive denominators gives
the following familiar formulas. This rational reading is not a separate Lean
theorem. Write `sigma = 1 - 2048*delta`:

```text
3*delta - (2*delta +   4*delta^2) = delta*sigma + 2044*delta^2
5*delta - (4*delta +  44*delta^2) = delta*sigma + 2004*delta^2
9*delta - (8*delta + 188*delta^2) = delta*sigma + 1860*delta^2

1 - 4*c*delta = sigma + r*delta
(c,r) = (1,2044), (3,2036), (5,2028), (9,2012)

1024*delta^2 - 700*delta^2 = 324*delta^2
1 - 2*1024*delta = sigma.
```

The independently checked boundary examples are `delta = 0` and
`delta = 1/2048`. The latter uses `p=2048`, `q=4194304`,
`(a1,a2,a3,a4)=(2048,4097,8195,16391)`, and all `v_i=1`, so the assumptions
have an explicit nonzero-loss instance.

## Trust and limitations

The six visible axiom audits all report **no axiom dependencies**. Matching
`#guard_msgs` assertions make an unexpected dependency a compilation error.
There are no proof placeholders, added axioms, native-decision tactics,
Mathlib imports, or external solvers. Two elementary Nat identities are
reproved constructively to avoid the `propext` dependency of convenience lemmas
in this installed library. Ordinary `decide` and symbolic proof terms are
checked by Lean's kernel.

**Not formalized:** the existence of a common denominator for arbitrary rational
inputs; a `Rat`/`Real` interpretation or transfer theorem; arbitrary real scalar
inputs; the local loss law itself; operator/spectral estimates; the parent's
finite-size theorem or any Yang–Mills/mass-gap conclusion. The explanatory
rational interpretation and the correspondence to the parent's mathematics
remain outside this Lean development. No optimality of these constants is
claimed.
