# A machine-checkable target for P vs NP

These files pin down, in Lean 4 with Mathlib, exactly what a formal resolution of
P vs NP must prove. They follow the conventions of the trusted challenge files already
used by the OpenAI math release (`lean/ComparatorChallenges/KMedianThreshold.lean`,
`BinPackingGap.lean`).

| File | Contents |
|---|---|
| `ChallengePNeNP.lean` / `.json` | Comparator challenge: definitions plus `theorem P_ne_NP : P ≠ NP := by sorry` |
| `ChallengePEqNP.lean` / `.json` | Comparator challenge: the same definitions plus `theorem P_eq_NP : P = NP := by sorry` |
| `PNeNP.lean` | The definitions, the sanity theorems below (all proved), and both targets as `sorry` |
| `PSubsetNP.lean` | The standalone proof of `P_subset_NP`, as delivered (now also merged into `PNeNP.lean`) |

## The model

- Languages are sets of `List Bool`.
- `P`: decided by a `Turing.TM2ComputableInPolyTime` machine (Mathlib's bundled
  multi-stack machine with a `Polynomial ℕ` clock on the input length) whose stack
  alphabets are all finite.
- `NP`: a certificate of length at most `bound.eval |x|` is accepted by such a
  machine reading `encodePair (x, w)`. The pair is framed by `encodeNat |x|`, which
  is self-delimiting: the bit-length in unary, a separator, then the binary digits.

## Sanity theorems (proved, axioms `propext`, `Quot.sound`, `Classical.choice` at most)

- `encodePair_injective`: the framing is unambiguous.
- `empty_mem_P`, `empty_mem_NP`: via an explicit one-stack machine `rejectAll`,
  verified to halt in `|x| + 1` steps.
- `P_subset_NP`: a wrapper machine strips the `encodeNat |x|` header in
  `2(b + 1)` steps using a unit counter stack, then runs the decider unchanged;
  the certificate bound is `0`.

These rule out the two cheapest ways a target statement goes wrong: classes that
are empty for definitional reasons, and an NP definition that fails to contain P.

## Checking

The files import only Mathlib. Compile against the release's pinned toolchain
(Lean 4.34.1, Mathlib `d13f23b`) from any built copy of the release's `lean/`
directory:

```sh
lake env lean "research_notes/P vs NP roadmap/formal_target/PNeNP.lean"
```

Each file checks in about 7 seconds. A solution to either challenge would be
checked with `comparator` exactly as the release's own results are.

## What this does not settle

- Whether this model matches every other reasonable formalization (one-tape
  machines, other encodings). Robustness of P and NP is a theorem on paper, but it
  is not formalized here, and the release itself uses three slightly different
  NP definitions (unary versus binary length prefix; `Finite` versus `Fintype`
  alphabets) that are nowhere proved equivalent.
- Anything about which of the two targets is true.
