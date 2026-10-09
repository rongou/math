# Scalar incidence certificate

`IncidenceBounds.lean` checks a small arithmetic component of the replacement proof, not gauge theory or probability.

For any natural-number list `qs` with every entry at most 4 and `total qs <= 6*n`, Lean derives `squareTotal qs <= 24*n`. This is the scalar step used in the Hessian and exactly-flat replacement estimates. The incidence hypotheses are explicit inputs: the file does **not** prove that any particular lattice has those incidences. That geometry is proved in the main note and exercised by the Python checks.

It also verifies the numerical identities producing 18 neighbors, the Hessian-to-energy factor 12, the approximate-compatible output coefficient 48, and 324 in the counting bound. A nonzero list gives a direct test instance.

Run:

```bash
./check.sh
```

This uses the already installed Lean 4.34.1 directly, `--trust=0`, and `Std` only. No dependency download or project configuration change is needed. Every displayed theorem has no axiom dependencies; checked `#guard_msgs` declarations enforce that. [Compiler output](compiler-output.txt) records the successful run. [Mutation output](mutation-output.txt) records rejection of two deliberately corrupted coefficients; the temporary files were removed.

Not formalized: real-valued norms and energies, graph construction, SU(2), Haar measure, cap volume, probability, covariance of the kernel, the replacement theorem, or any continuum or mass-gap assertion.
