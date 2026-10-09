import Std

/-!
Scalar incidence certificate only. This does not formalize lattice geometry,
Haar measure, energy, Hessians, a sampling kernel, or a probability theorem.
The bound on the number of occurrences and the bound q <= 4 are explicit inputs;
the four-dimensional link counting that supplies them is proved in the note.
-/
set_option autoImplicit false
namespace RoughRegion

-- Constructive reassociation avoids the optional propext dependency of the
-- convenience lemma in this installed Std version.
private theorem mulAssoc (a b c : Nat) : a * b * c = a * (b * c) := by
  induction c with
  | zero => rfl
  | succ c ih =>
    change a * b * c + a * b = a * (b * c + b)
    rw [Nat.mul_add, ih]

def total : List Nat → Nat
  | [] => 0
  | q :: qs => q + total qs

def squareTotal : List Nat → Nat
  | [] => 0
  | q :: qs => q * q + squareTotal qs

def fourBounded : List Nat → Prop
  | [] => True
  | q :: qs => q ≤ 4 ∧ fourBounded qs

theorem squareTotal_le_four_total (qs : List Nat) (h : fourBounded qs) :
    squareTotal qs ≤ 4 * total qs := by
  induction qs with
  | nil => exact Nat.le_refl 0
  | cons q qs ih =>
    have hq : q ≤ 4 := h.1
    have hr : fourBounded qs := h.2
    calc
      squareTotal (q :: qs) = q * q + squareTotal qs := rfl
      _ ≤ 4 * q + 4 * total qs :=
        Nat.add_le_add (Nat.mul_le_mul_right q hq) (ih hr)
      _ = 4 * (q + total qs) := (Nat.mul_add 4 q (total qs)).symm
      _ = 4 * total (q :: qs) := rfl

theorem four_dimensional_incidence (qs : List Nat) (n : Nat)
    (hq : fourBounded qs) (hi : total qs ≤ 6 * n) :
    squareTotal qs ≤ 24 * n := by
  calc
    squareTotal qs ≤ 4 * total qs := squareTotal_le_four_total qs hq
    _ ≤ 4 * (6 * n) := Nat.mul_le_mul_left 4 hi
    _ = 24 * n := (mulAssoc 4 6 n).symm

theorem constants :
    (6 * 3 = (18 : Nat)) ∧
    (4 * 6 = (24 : Nat)) ∧
    (2 * 12 = (24 : Nat)) ∧
    (6 * (4 * 4) = 2 * (48 : Nat)) ∧
    (18 * 18 = (324 : Nat)) := by
  decide

-- A nonvacuous incidence instance: the full four-dimensional unit-volume
-- counts scaled by four, without asserting a particular periodic geometry.
theorem example_bound : squareTotal [4,4,4,4,4,4] ≤ 24 * 4 :=
  four_dimensional_incidence [4,4,4,4,4,4] 4
    ⟨Nat.le_refl 4, Nat.le_refl 4, Nat.le_refl 4,
     Nat.le_refl 4, Nat.le_refl 4, Nat.le_refl 4, True.intro⟩
    (by decide)

/-- info: 'RoughRegion.squareTotal_le_four_total' does not depend on any axioms -/
#guard_msgs in
#print axioms squareTotal_le_four_total
/-- info: 'RoughRegion.four_dimensional_incidence' does not depend on any axioms -/
#guard_msgs in
#print axioms four_dimensional_incidence
/-- info: 'RoughRegion.constants' does not depend on any axioms -/
#guard_msgs in
#print axioms constants
/-- info: 'RoughRegion.example_bound' does not depend on any axioms -/
#guard_msgs in
#print axioms example_bound

#print axioms squareTotal_le_four_total
#print axioms four_dimensional_incidence
#print axioms constants
#print axioms example_bound
end RoughRegion
