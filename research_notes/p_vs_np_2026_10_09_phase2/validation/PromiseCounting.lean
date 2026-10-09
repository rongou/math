import Mathlib

/-!
Finite Boolean promise/certificate counting, independent of circuit-size definitions.
A partial assignment is a fixed finite set and a total base assignment whose values
outside that set are irrelevant. Intersecting two such subcubes requires explicit
compatibility for the cardinality formula. Certificate cost counts only NEW fixed
coordinates, `C \ F`, not all of `C`. `Low` need only contain every accepted input.
-/

namespace PromiseCounting

universe u
noncomputable section
open scoped Classical
variable {V : Type u} [Fintype V]

/-- The actual Boolean assignments agreeing with `a` on the fixed coordinates `F`. -/
def subcube (F : Finset V) (a : V → Bool) : Finset (V → Bool) :=
  Finset.univ.filter (fun x => ∀ v ∈ F, x v = a v)

@[simp] theorem mem_subcube {F : Finset V} {a x : V → Bool} :
    x ∈ subcube F a ↔ ∀ v ∈ F, x v = a v := by
  simp [subcube]

/-- Completions are exactly arbitrary Boolean functions on the unfixed coordinates. -/
def subcubeEquiv (F : Finset V) (a : V → Bool) :
    {x : V → Bool // x ∈ subcube F a} ≃ (↥(Fᶜ) → Bool) where
  toFun x v := x.val v.val
  invFun g := ⟨fun v => if h : v ∈ F then a v else g ⟨v, Finset.mem_compl.mpr h⟩, by
    apply mem_subcube.mpr
    intro v hv
    simp only [dite_eq_left hv]⟩
  left_inv x := by
    apply Subtype.ext
    funext v
    by_cases hv : v ∈ F
    · simp [hv, mem_subcube.mp x.property v hv]
    · simp [hv]
  right_inv g := by
    funext v
    simp [Finset.mem_compl.mp v.property]

theorem card_subcube (F : Finset V) (a : V → Bool) :
    (subcube F a).card = 2 ^ Fᶜ.card := by
  simpa only [Fintype.card_coe, Fintype.card_fun, Fintype.card_bool]
    using Fintype.card_congr (subcubeEquiv F a)

/-- Two partial assignments agree on their overlapping fixed coordinates. -/
def Compatible (F : Finset V) (a : V → Bool) (C : Finset V) (b : V → Bool) : Prop :=
  ∀ v, v ∈ F → v ∈ C → a v = b v

theorem compatible_of_common_point (F : Finset V) (a : V → Bool)
    (C : Finset V) (b x : V → Bool)
    (hxF : x ∈ subcube F a) (hxC : x ∈ subcube C b) : Compatible F a C b := by
  intro v hvF hvC
  exact (mem_subcube.mp hxF v hvF).symm.trans (mem_subcube.mp hxC v hvC)

theorem subcube_inter_eq (F : Finset V) (a : V → Bool) (C : Finset V) (b : V → Bool)
    (hc : Compatible F a C b) :
    subcube F a ∩ subcube C b =
      subcube (F ∪ C) (fun v => if v ∈ F then a v else b v) := by
  ext x
  simp only [Finset.mem_inter, mem_subcube]
  constructor
  · rintro ⟨hF, hC⟩ v hv
    by_cases hvF : v ∈ F
    · simpa only [ite_eq_left hvF] using hF v hvF
    · simpa only [ite_eq_right hvF] using hC v ((Finset.mem_union.mp hv).resolve_left hvF)
  · intro h
    constructor
    · intro v hv
      simpa only [ite_eq_left hv] using h v (Finset.mem_union.mpr (Or.inl hv))
    · intro v hvC
      have hx := h v (Finset.mem_union.mpr (Or.inr hvC))
      by_cases hvF : v ∈ F
      · simpa only [ite_eq_left hvF, hc v hvF hvC] using hx
      · simpa only [ite_eq_right hvF] using hx

/-- Fixing `C` removes exactly the previously free coordinates `C \ F`. -/
theorem free_after_union (F C : Finset V) :
    (F ∪ C)ᶜ.card = Fᶜ.card - (C \ F).card := by
  have h := Finset.card_sdiff_add_card C F
  rw [Finset.union_comm C F] at h
  simp only [Finset.card_compl]
  omega

theorem card_subcube_inter (F : Finset V) (a : V → Bool) (C : Finset V) (b : V → Bool)
    (hc : Compatible F a C b) :
    (subcube F a ∩ subcube C b).card = 2 ^ (Fᶜ.card - (C \ F).card) := by
  rw [subcube_inter_eq F a C b hc, card_subcube, free_after_union]

theorem card_subcube_inter_lower (F : Finset V) (a : V → Bool)
    (C : Finset V) (b : V → Bool) (hc : Compatible F a C b)
    (q : Nat) (hq : (C \ F).card ≤ q) :
    2 ^ (Fᶜ.card - q) ≤ (subcube F a ∩ subcube C b).card := by
  rw [card_subcube_inter F a C b hc]
  apply Nat.pow_le_pow_right Nat.zero_lt_two
  omega

/-- Only one-way soundness into `Low` is assumed; acceptance need not equal membership in `Low`. -/
theorem accepted_subcube_card_le (A : (V → Bool) → Prop) (Low : Finset (V → Bool))
    (hLow : ∀ x, A x → x ∈ Low) (F : Finset V) (a : V → Bool)
    (haccept : ∀ x ∈ subcube F a, A x) : (subcube F a).card ≤ Low.card := by
  exact Finset.card_le_card (fun x hx => hLow x (haccept x hx))

theorem accepted_inter_card_le (A : (V → Bool) → Prop) (Low : Finset (V → Bool))
    (hLow : ∀ x, A x → x ∈ Low) (F : Finset V) (a : V → Bool)
    (C : Finset V) (b : V → Bool)
    (haccept : ∀ x, x ∈ subcube F a → x ∈ subcube C b → A x) :
    (subcube F a ∩ subcube C b).card ≤ Low.card := by
  apply Finset.card_le_card
  intro x hx
  exact hLow x (haccept x (Finset.mem_inter.mp hx).1 (Finset.mem_inter.mp hx).2)

/-- A counting witness OUTSIDE `Low`; no acceptance or promise condition is used here. -/
theorem outside_low_completion (F : Finset V) (a : V → Bool)
    (C : Finset V) (b : V → Bool) (hc : Compatible F a C b)
    (q : Nat) (hq : (C \ F).card ≤ q) (Low : Finset (V → Bool))
    (hsmall : Low.card < 2 ^ (Fᶜ.card - q)) :
    ∃ x : V → Bool, x ∈ subcube F a ∧ x ∈ subcube C b ∧ x ∉ Low := by
  have hlower := card_subcube_inter_lower F a C b hc q hq
  have hnot : ¬ (subcube F a ∩ subcube C b) ⊆ Low := by
    intro hsub
    exact Nat.not_lt_of_ge (Finset.card_le_card hsub) (hsmall.trans_le hlower)
  obtain ⟨x, hx, hout⟩ := Finset.not_subset.mp hnot
  exact ⟨x, (Finset.mem_inter.mp hx).1, (Finset.mem_inter.mp hx).2, hout⟩

/-- Soundness into `Low` turns the outside witness into a rejected completion. -/
theorem rejected_completion (A : (V → Bool) → Prop) (Low : Finset (V → Bool))
    (hLow : ∀ x, A x → x ∈ Low) (F : Finset V) (a : V → Bool)
    (C : Finset V) (b : V → Bool) (hc : Compatible F a C b)
    (q : Nat) (hq : (C \ F).card ≤ q) (hsmall : Low.card < 2 ^ (Fᶜ.card - q)) :
    ∃ x : V → Bool, x ∈ subcube F a ∧ x ∈ subcube C b ∧ x ∉ Low ∧ ¬ A x := by
  obtain ⟨x, hxF, hxC, hout⟩ := outside_low_completion F a C b hc q hq Low hsmall
  exact ⟨x, hxF, hxC, hout, fun hA => hout (hLow x hA)⟩

/-- A certificate at an accepted point, relative to the initial restriction `(F,a)`.
Its budget charges only coordinates not already fixed by that restriction. -/
structure IsCertificate (A : (V → Bool) → Prop) (F : Finset V) (a : V → Bool)
    (q : Nat) (x : V → Bool) (C : Finset V) (b : V → Bool) : Prop where
  accepted : A x
  in_restriction : x ∈ subcube F a
  agrees : x ∈ subcube C b
  budget : (C \ F).card ≤ q
  forces : ∀ y, y ∈ subcube F a → y ∈ subcube C b → A y

theorem certificate_count_bound (A : (V → Bool) → Prop) (Low : Finset (V → Bool))
    (hLow : ∀ x, A x → x ∈ Low) (F : Finset V) (a : V → Bool)
    (q : Nat) (x : V → Bool) (C : Finset V) (b : V → Bool)
    (hcert : IsCertificate A F a q x C b) : 2 ^ (Fᶜ.card - q) ≤ Low.card := by
  have hc := compatible_of_common_point F a C b x hcert.in_restriction hcert.agrees
  exact (card_subcube_inter_lower F a C b hc q hcert.budget).trans
    (accepted_inter_card_le A Low hLow F a C b hcert.forces)

theorem no_certificate_of_card_lt (A : (V → Bool) → Prop) (Low : Finset (V → Bool))
    (hLow : ∀ x, A x → x ∈ Low) (F : Finset V) (a : V → Bool) (q : Nat)
    (hsmall : Low.card < 2 ^ (Fᶜ.card - q)) :
    ¬ ∃ (x : V → Bool) (C : Finset V) (b : V → Bool), IsCertificate A F a q x C b := by
  rintro ⟨x, C, b, hcert⟩
  exact Nat.not_lt_of_ge (certificate_count_bound A Low hLow F a q x C b hcert) hsmall

/-- Flip exactly coordinate `i`. -/
def flipAt (x : V → Bool) (i : V) : V → Bool :=
  fun j => if j = i then !(x i) else x j

theorem flipAt_mem_subcube (F : Finset V) (x : V → Bool) (i : V) (hi : i ∉ F) :
    flipAt x i ∈ subcube F x := by
  apply mem_subcube.mpr
  intro j hj
  have hji : j ≠ i := by
    intro h
    exact hi (h ▸ hj)
  simp only [flipAt, ite_eq_right hji]

/-- An isolated YES input has no certificate omitting any coordinate.
The explicit YES hypothesis is redundant with forcing at `x`, but records the intended setting. -/
theorem isolated_yes_certificate_full (C : (V → Bool) → Bool) (x : V → Bool)
    (_hyes : C x = true) (hneighbors : ∀ i : V, C (flipAt x i) = false)
    (F : Finset V) (hforces : ∀ y : V → Bool, (∀ i ∈ F, y i = x i) → C y = true) :
    F = Finset.univ := by
  apply Finset.eq_univ_of_forall
  intro i
  by_contra hi
  have htrue := hforces (flipAt x i) (mem_subcube.mp (flipAt_mem_subcube F x i hi))
  cases htrue.symm.trans (hneighbors i)

#print axioms mem_subcube
#print axioms subcubeEquiv
#print axioms card_subcube
#print axioms compatible_of_common_point
#print axioms subcube_inter_eq
#print axioms free_after_union
#print axioms card_subcube_inter
#print axioms card_subcube_inter_lower
#print axioms accepted_subcube_card_le
#print axioms accepted_inter_card_le
#print axioms outside_low_completion
#print axioms rejected_completion
#print axioms certificate_count_bound
#print axioms no_certificate_of_card_lt
#print axioms flipAt_mem_subcube
#print axioms isolated_yes_certificate_full

end
end PromiseCounting
