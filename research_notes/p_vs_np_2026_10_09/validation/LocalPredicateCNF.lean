import Std

/-!
Standalone local-predicate-to-CNF transfer; no project or Mathlib imports.
An assignment `a` encodes the width-`k` clause `∃ i : Fin k, x i ≠ a i`:
its literal at `i` is positive when `a i = false` and negative otherwise.
The quantifiers allow `k = 0`, constant predicates, and empty index types.
This file does not check family112 or assert a polynomial-size bound.
-/

namespace LocalPredicateCNF

/-- One clause for every rejected local assignment. -/
theorem predicate_iff_rejected_clauses (k : Nat)
    (Q : (Fin k → Bool) → Bool) (x : Fin k → Bool) :
    Q x = true ↔
      ∀ a : Fin k → Bool, Q a = false → ∃ i : Fin k, x i ≠ a i := by
  constructor
  · intro hx a ha
    by_cases h : ∃ i : Fin k, x i ≠ a i
    · exact h
    · have hxa : x = a := funext fun i => by
        by_cases hi : x i = a i
        · exact hi
        · exact False.elim (h ⟨i, hi⟩)
      have hfalse : Q x = false := (congrArg Q hxa).trans ha
      cases hx.symm.trans hfalse
  · intro h
    cases hx : Q x with
    | false =>
      obtain ⟨i, hi⟩ := h x hx
      exact False.elim (hi rfl)
    | true => rfl

/-- Conjunction lifting, allowing a different arity at each index. -/
theorem conjunction_iff_rejected_clauses {J : Type u}
    (k : J → Nat)
    (Q : (j : J) → (Fin (k j) → Bool) → Bool)
    (x : (j : J) → Fin (k j) → Bool) :
    (∀ j : J, Q j (x j) = true) ↔
      (∀ (j : J) (a : Fin (k j) → Bool),
        Q j a = false → ∃ i : Fin (k j), x j i ≠ a i) := by
  constructor
  · intro h j
    exact (predicate_iff_rejected_clauses (k j) (Q j) (x j)).mp (h j)
  · intro h j
    exact (predicate_iff_rejected_clauses (k j) (Q j) (x j)).mpr (h j)

/-- Disjunction of conjunctions lifting; this does not flatten the result into CNF. -/
theorem disjunction_of_conjunctions_iff_rejected_clauses
    {T : Type u} {J : T → Type v}
    (k : (t : T) → J t → Nat)
    (Q : (t : T) → (j : J t) → (Fin (k t j) → Bool) → Bool)
    (x : (t : T) → (j : J t) → Fin (k t j) → Bool) :
    (∃ t : T, ∀ j : J t, Q t j (x t j) = true) ↔
      (∃ t : T, ∀ (j : J t) (a : Fin (k t j) → Bool),
        Q t j a = false → ∃ i : Fin (k t j), x t j i ≠ a i) := by
  constructor
  · intro ⟨t, ht⟩
    exact ⟨t, (conjunction_iff_rejected_clauses (k t) (Q t) (x t)).mp ht⟩
  · intro ⟨t, ht⟩
    exact ⟨t, (conjunction_iff_rejected_clauses (k t) (Q t) (x t)).mpr ht⟩

/-- All local assignments, recursively listed with the first bit false, then true. -/
def assignments : (k : Nat) → List (Fin k → Bool)
  | 0 => [fun i => Fin.elim0 i]
  | k + 1 =>
    (assignments k).map (fun a => Fin.cases false a) ++
    (assignments k).map (fun a => Fin.cases true a)

theorem assignments_complete : ∀ (k : Nat) (a : Fin k → Bool),
    a ∈ assignments k := by
  intro k
  induction k with
  | zero =>
    intro a
    have ha : a = (fun i : Fin 0 => Fin.elim0 i) := funext fun i => Fin.elim0 i
    simp [assignments, ha]
  | succ k ih =>
    intro a
    have ha : Fin.cases (a 0) (fun i => a i.succ) = a := by
      funext i
      exact Fin.cases rfl (fun _ => rfl) i
    simp only [assignments, List.mem_append, List.mem_map]
    cases hb : a 0 with
    | false => exact Or.inl ⟨_, ih _, by simpa only [hb] using ha⟩
    | true => exact Or.inr ⟨_, ih _, by simpa only [hb] using ha⟩

theorem assignments_length (k : Nat) : (assignments k).length = 2 ^ k := by
  induction k with
  | zero => rfl
  | succ k ih => simp [assignments, ih, Nat.pow_succ, Nat.mul_two]

/-- A CNF list whose elements encode clauses as described above (not satisfied assignments). -/
def truthTableCNF (k : Nat) (Q : (Fin k → Bool) → Bool) : List (Fin k → Bool) :=
  (assignments k).filter (fun a => !(Q a))

theorem mem_truthTableCNF (k : Nat) (Q : (Fin k → Bool) → Bool)
    (a : Fin k → Bool) : a ∈ truthTableCNF k Q ↔ Q a = false := by
  simp [truthTableCNF, assignments_complete]

/-- List membership supplies the conjunction; the existential supplies each clause. -/
theorem truthTableCNF_correct (k : Nat)
    (Q : (Fin k → Bool) → Bool) (x : Fin k → Bool) :
    Q x = true ↔
      ∀ a : Fin k → Bool, a ∈ truthTableCNF k Q → ∃ i : Fin k, x i ≠ a i := by
  simpa only [mem_truthTableCNF] using predicate_iff_rejected_clauses k Q x

theorem truthTableCNF_length_le (k : Nat) (Q : (Fin k → Bool) → Bool) :
    (truthTableCNF k Q).length ≤ 2 ^ k := by
  calc
    (truthTableCNF k Q).length ≤ (assignments k).length := List.length_filter_le _ _
    _ = 2 ^ k := assignments_length k

/-- The true predicate gives the empty conjunction. -/
theorem truthTableCNF_true (k : Nat) : truthTableCNF k (fun _ => true) = [] := by
  unfold truthTableCNF
  induction assignments k with
  | nil => rfl
  | cons _ _ ih => exact ih

/-- The false predicate rejects every assignment, including the empty assignment at arity zero. -/
theorem truthTableCNF_false (k : Nat) :
    truthTableCNF k (fun _ => false) = assignments k := by
  unfold truthTableCNF
  induction assignments k with
  | nil => rfl
  | cons a _ ih => exact congrArg (List.cons a) ih

/-- At arity zero the result is either no clauses or one empty (unsatisfiable) clause. -/
theorem truthTableCNF_zero (Q : (Fin 0 → Bool) → Bool) :
    truthTableCNF 0 Q =
      if Q (fun i : Fin 0 => Fin.elim0 i) then [] else [fun i : Fin 0 => Fin.elim0 i] := by
  cases h : Q (fun i : Fin 0 => Fin.elim0 i) <;> simp [truthTableCNF, assignments, h]

#print axioms predicate_iff_rejected_clauses
#print axioms conjunction_iff_rejected_clauses
#print axioms disjunction_of_conjunctions_iff_rejected_clauses

#print axioms assignments_complete
#print axioms assignments_length
#print axioms mem_truthTableCNF
#print axioms truthTableCNF_correct
#print axioms truthTableCNF_length_le
#print axioms truthTableCNF_true
#print axioms truthTableCNF_false
#print axioms truthTableCNF_zero

end LocalPredicateCNF
