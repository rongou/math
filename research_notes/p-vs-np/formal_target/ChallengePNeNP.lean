import Mathlib

/-!
# A Comparator-style target statement for P ≠ NP

The definitions follow the trusted challenge files already used by the OpenAI
math release (`ComparatorChallenges/KMedianThreshold.lean` and
`ComparatorChallenges/BinPackingGap.lean`): languages over `List Bool`,
deterministic polynomial-time computation by Mathlib's bundled multi-stack
machines `Turing.FinTM2` with every stack alphabet finite, and NP via
polynomially bounded certificates checked by such a machine.

Nothing below is proved except sanity lemmas about the definitions. The two
target theorems end in `sorry`: a resolution of P vs NP in this model is a
proof of exactly one of them, with only `propext`, `Quot.sound` and
`Classical.choice` as axioms.
-/

namespace PvsNP

abbrev Word := List Bool
abbrev Language := Set Word

/-- Self-delimiting: the bit-length in unary, a separator, then the binary
digits (least significant first). Unlike Mathlib's root `encodeNat`, a prefix
encoded this way can be parsed off a longer word. -/
def encodeNat (n : ℕ) : Word :=
  List.replicate n.bits.length true ++ [false] ++ n.bits

def encodeBit (b : Bool) : Word := [b]

/-- An input together with a certificate, framed by the input's length. -/
def encodePair (x : Word × Word) : Word :=
  encodeNat x.1.length ++ x.1 ++ x.2

/-- Polynomial-time computable with every physical stack alphabet finite.
Without the finiteness clause a single stack symbol could carry unbounded
information. -/
def FinitePolyTime {α β : Type} (ea : α → Word) (eb : β → Word) (f : α → β) : Prop :=
  ∃ M : Turing.TM2ComputableInPolyTime ea eb f, ∀ k : M.tm.K, Finite (M.tm.Γ k)

def P : Set Language :=
  {L | ∃ decide : Word → Bool,
    FinitePolyTime id encodeBit decide ∧ ∀ x, decide x = true ↔ x ∈ L}

def NP : Set Language :=
  {L | ∃ (verify : Word × Word → Bool) (bound : Polynomial ℕ),
    FinitePolyTime encodePair encodeBit verify ∧
    ∀ x, x ∈ L ↔ ∃ w : Word, w.length ≤ bound.eval x.length ∧ verify (x, w) = true}

/-- Target A: separation. A Comparator solution proves exactly this, with
permitted axioms `propext`, `Quot.sound`, `Classical.choice`. -/
theorem P_ne_NP : P ≠ NP := by
  sorry

end PvsNP
