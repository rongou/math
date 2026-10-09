import Std

/-!
Finite MCSP[0,0] control: m = 3 inner inputs, N = 8 truth-table bits.
Bit a of a table is its value on the inner assignment a (least-significant
inner coordinate first). Free inner wires are the three positive inputs and
constants false/true. Every AND2, OR2, and NOT costs one gate; NOT is not free.

The outer circuit below is an explicit topologically ordered gate list matching
experiments/certificate_controls.py: eight shared NOTs, five left-associated
8-literal AND terms, then a four-gate OR chain. Its interpreter never tests
membership in the specified accepting set.

Scope: finite zero-threshold control, not the growing-beta OPS target, not
circuit-size minimality, and not a formal general-family asymptotic bound.
-/

namespace ZeroGateControl

set_option maxRecDepth 16384
set_option maxHeartbeats 4000000

/-- Structural Fin eliminator; the inequality proofs are definitionally irrelevant. -/
def finCases {n : Nat} {P : Fin (n + 1) → Sort u}
    (h0 : P 0) (hs : (i : Fin n) → P i.succ) : (i : Fin (n + 1)) → P i
  | ⟨0, _⟩ => h0
  | ⟨k + 1, h⟩ => hs ⟨k, Nat.lt_of_succ_lt_succ h⟩

/-- Constructive finite decisions, avoiding library proof-normalization dependencies. -/
def decideAllFin : (n : Nat) → (P : Fin n → Prop) →
    ((i : Fin n) → Decidable (P i)) → Decidable (∀ i, P i)
  | 0, _, _ => .isTrue (fun i => Fin.elim0 i)
  | n + 1, P, d =>
    match d 0 with
    | .isFalse hn => .isFalse (fun h => hn (h 0))
    | .isTrue h0 =>
      match decideAllFin n (fun i => P i.succ) (fun i => d i.succ) with
      | .isTrue hs => .isTrue (finCases h0 hs)
      | .isFalse hn => .isFalse (fun h => hn (fun i => h i.succ))

def decideSomeFin : (n : Nat) → (P : Fin n → Prop) →
    ((i : Fin n) → Decidable (P i)) → Decidable (∃ i, P i)
  | 0, _, _ => .isFalse (fun ⟨i, _⟩ => Fin.elim0 i)
  | n + 1, P, d =>
    match d 0 with
    | .isTrue h0 => .isTrue ⟨0, h0⟩
    | .isFalse hn0 =>
      match decideSomeFin n (fun i => P i.succ) (fun i => d i.succ) with
      | .isTrue h => .isTrue (Exists.elim h (fun i hi => ⟨i.succ, hi⟩))
      | .isFalse hns => .isFalse (fun ⟨i, hi⟩ =>
          finCases (P := fun j => P j → False) hn0
            (fun j hj => hns ⟨j, hj⟩) i hi)

local instance (priority := 2000) {n : Nat} {P : Fin n → Prop}
    [d : DecidablePred P] : Decidable (∀ i, P i) := decideAllFin n P d

local instance (priority := 2000) {n : Nat} {P : Fin n → Prop}
    [d : DecidablePred P] : Decidable (∃ i, P i) := decideSomeFin n P d

abbrev Table := Fin 256
abbrev Address := Fin 8

def bit (x : Table) (a : Address) : Bool := x.val.testBit a.val

/-- All free outputs of a zero-gate inner circuit: inputs 0,1,2; constants 0,1. -/
def innerFreeWire (w : Fin 5) (a : Address) : Bool :=
  if w.val < 3 then a.val.testBit w.val else w.val == 4

abbrev HasZeroGateRealization (x : Table) : Prop :=
  ∃ w : Fin 5, ∀ a : Address, bit x a = innerFreeWire w a

abbrev Accepted (x : Table) : Prop :=
  x.val = 0 ∨ x.val = 255 ∨ x.val = 170 ∨ x.val = 204 ∨ x.val = 240

inductive Gate where
  | and2 (left right : Nat)
  | or2 (left right : Nat)
  | not1 (input : Nat)
  deriving Repr, DecidableEq

def Gate.eval (g : Gate) (values : Array Bool) : Bool :=
  match g with
  | .and2 i j => values[i]?.getD false && values[j]?.getD false
  | .or2 i j => values[i]?.getD false || values[j]?.getD false
  | .not1 i => !(values[i]?.getD false)

def Gate.inBounds (bound : Nat) (g : Gate) : Bool :=
  match g with
  | .and2 i j | .or2 i j => decide (i < bound ∧ j < bound)
  | .not1 i => decide (i < bound)

/-- Outer primary wires 0..7, free constants at 8 and 9, gate wires 10..56. -/
def gates : List Gate := [
    .not1 0,
    .not1 1,
    .not1 2,
    .not1 3,
    .not1 4,
    .not1 5,
    .not1 6,
    .not1 7,
    .and2 10 11,
    .and2 18 12,
    .and2 19 13,
    .and2 20 14,
    .and2 21 15,
    .and2 22 16,
    .and2 23 17,
    .and2 0 1,
    .and2 25 2,
    .and2 26 3,
    .and2 27 4,
    .and2 28 5,
    .and2 29 6,
    .and2 30 7,
    .and2 10 1,
    .and2 32 12,
    .and2 33 3,
    .and2 34 14,
    .and2 35 5,
    .and2 36 16,
    .and2 37 7,
    .and2 10 11,
    .and2 39 2,
    .and2 40 3,
    .and2 41 14,
    .and2 42 15,
    .and2 43 6,
    .and2 44 7,
    .and2 10 11,
    .and2 46 12,
    .and2 47 13,
    .and2 48 4,
    .and2 49 5,
    .and2 50 6,
    .and2 51 7,
    .or2 24 31,
    .or2 53 38,
    .or2 54 45,
    .or2 55 52
  ]

def outputWire : Nat := 56

def initialValues (x : Table) : Array Bool :=
  (Array.ofFn fun a : Address => bit x a) ++ #[false, true]

def evaluate (x : Table) : Bool :=
  let values := gates.foldl (fun values gate => values.push (gate.eval values))
    (initialValues x)
  values[outputWire]?.getD false

def wellFormed : Bool :=
  (gates.zipIdx.all fun p => p.1.inBounds (10 + p.2)) &&
    decide (outputWire < 10 + gates.length)

def numberOfNot : Nat := (gates.filter fun g => match g with
  | .not1 _ => true
  | _ => false).length

def numberOfAnd : Nat := (gates.filter fun g => match g with
  | .and2 _ _ => true
  | _ => false).length

def numberOfOr : Nat := (gates.filter fun g => match g with
  | .or2 _ _ => true
  | _ => false).length

theorem network_well_formed : wellFormed = true := by exact of_decide_eq_true rfl

theorem gate_count_47 : gates.length = 47 := by exact of_decide_eq_true rfl

theorem gate_breakdown :
    numberOfNot = 8 ∧ numberOfAnd = 35 ∧ numberOfOr = 4 := by exact of_decide_eq_true rfl

/-- Closed finite checks use kernel reduction through ordinary `of_decide_eq_true rfl`. -/
theorem zero_gate_tables_exact :
    ∀ x : Table, HasZeroGateRealization x ↔ Accepted x := by exact of_decide_eq_true rfl

theorem classifier_semantics :
    ∀ x : Table, evaluate x = true ↔ Accepted x := by exact of_decide_eq_true rfl

theorem classifier_mcsp_zero (x : Table) :
    evaluate x = true ↔ HasZeroGateRealization x :=
  (classifier_semantics x).trans (zero_gate_tables_exact x).symm

/-- Flip exactly truth-table address i; modulo supplies a total bounded encoding. -/
def flip (x : Table) (i : Address) : Table :=
  ⟨(Nat.xor x.val (2 ^ i.val)) % 256, Nat.mod_lt _ (by exact of_decide_eq_true rfl)⟩

theorem flip_no_wrap : ∀ x : Table, ∀ i : Address,
    (flip x i).val = Nat.xor x.val (2 ^ i.val) := by exact of_decide_eq_true rfl

theorem flip_bit_rule : ∀ x : Table, ∀ i a : Address,
    bit (flip x i) a = (if a = i then !(bit x a) else bit x a) := by exact of_decide_eq_true rfl

theorem accepted_set_isolated : ∀ x : Table, ∀ i : Address,
    Accepted x → ¬ Accepted (flip x i) := by exact of_decide_eq_true rfl

theorem one_bit_neighbors_rejected (x : Table) (hx : evaluate x = true)
    (i : Address) : evaluate (flip x i) = false := by
  have hn := accepted_set_isolated x i ((classifier_semantics x).mp hx)
  cases h : evaluate (flip x i) with
  | false => rfl
  | true => exact False.elim (hn ((classifier_semantics (flip x i)).mp h))

/-- A mask bit true means that address is fixed to its value in x. -/
def AgreesOn (fixed x y : Table) : Prop :=
  ∀ a : Address, bit fixed a = true → bit x a = bit y a

def IsYesCertificate (fixed x : Table) : Prop :=
  ∀ y : Table, AgreesOn fixed x y → evaluate y = true

theorem proper_mask_has_unfixed : ∀ fixed : Table,
    fixed.val ≠ 255 → ∃ i : Address, bit fixed i = false := by exact of_decide_eq_true rfl

theorem flip_preserves_fixed (fixed x : Table) (i : Address)
    (hi : bit fixed i = false) : AgreesOn fixed x (flip x i) := by
  intro a ha
  have hne : a ≠ i := by
    intro h
    subst a
    rw [hi] at ha
    cases ha
  have h := flip_bit_rule x i a
  rw [ite_eq_right hne] at h
  exact h.symm

theorem no_proper_yes_certificate (x fixed : Table)
    (hx : evaluate x = true) (hm : fixed.val ≠ 255) :
    ¬ IsYesCertificate fixed x := by
  intro hcert
  obtain ⟨i, hi⟩ := proper_mask_has_unfixed fixed hm
  have hy := hcert (flip x i) (flip_preserves_fixed fixed x i hi)
  have hn := one_bit_neighbors_rejected x hx i
  rw [hn] at hy
  cases hy

#print axioms network_well_formed
#print axioms gate_count_47
#print axioms gate_breakdown
#print axioms zero_gate_tables_exact
#print axioms classifier_semantics
#print axioms classifier_mcsp_zero
#print axioms flip_no_wrap
#print axioms flip_bit_rule
#print axioms accepted_set_isolated
#print axioms one_bit_neighbors_rejected
#print axioms proper_mask_has_unfixed
#print axioms flip_preserves_fixed
#print axioms no_proper_yes_certificate

end ZeroGateControl
