import PromiseCounting
import Mathlib.InformationTheory.Hamming

/-!
Boolean certificates in a union of separated Hamming balls.

This imports the Phase 2 Boolean-subcube definitions, not circuit minimization.
The center set is arbitrary. The hypothesis `2*t+1 < distance` is stronger than
unique decoding: it prevents even an EDGE between distinct radius-t balls.
No property of full GapMCSP solvers or of general circuit size is assumed/proved.
-/

namespace SeparatedTubes

universe u
noncomputable section
open scoped Classical
open PromiseCounting
variable {V : Type u} [Fintype V]

/-- A union of closed radius-t Hamming balls around a finite center set. -/
def Tube (centers : Finset (V → Bool)) (t : Nat) (x : V → Bool) : Prop :=
  ∃ c ∈ centers, hammingDist x c ≤ t

/-- Distinct balls neither intersect nor have adjacent vertices. -/
def Separated (centers : Finset (V → Bool)) (t : Nat) : Prop :=
  ∀ c ∈ centers, ∀ d ∈ centers, c ≠ d → 2 * t + 1 < hammingDist c d

/-- Functions that agree away from a single coordinate have distance at most one. -/
theorem hammingDist_le_one (x y : V → Bool) (i : V)
    (h : ∀ j, j ≠ i → x j = y j) : hammingDist x y ≤ 1 := by
  classical
  unfold hammingDist
  calc
    (Finset.univ.filter (fun j => x j ≠ y j)).card ≤ ({i} : Finset V).card := by
      apply Finset.card_le_card
      intro j hj
      have hne := (Finset.mem_filter.mp hj).2
      by_contra hi
      have hji : j ≠ i := by simpa using hi
      exact hne (h j hji)
    _ = 1 := Finset.card_singleton i

/-- A coordinate subcube is connected by single-coordinate steps, in induction form. -/
theorem subcube_step_induction (F : Finset V) (a x y : V → Bool)
    (hx : x ∈ subcube F a) (hy : y ∈ subcube F a)
    (P : (V → Bool) → Prop) (hstart : P x)
    (hstep : ∀ z ∈ subcube F a, ∀ w ∈ subcube F a,
      hammingDist z w ≤ 1 → P z → P w) : P y := by
  classical
  let mix (s : Finset V) : V → Bool := fun i => if i ∈ s then y i else x i
  have hmix (s : Finset V) : mix s ∈ subcube F a := by
    apply mem_subcube.mpr
    intro i hi
    by_cases hs : i ∈ s
    · simpa only [mix, ite_eq_left hs] using mem_subcube.mp hy i hi
    · simpa only [mix, ite_eq_right hs] using mem_subcube.mp hx i hi
  have hall (s : Finset V) : P (mix s) := by
    induction s using Finset.induction_on with
    | empty => simpa [mix] using hstart
    | @insert i s _ ih =>
      apply hstep (mix s) (hmix s) (mix (insert i s)) (hmix (insert i s)) _ ih
      apply hammingDist_le_one _ _ i
      intro j hji
      simp [mix, hji]
  simpa [mix] using hall Finset.univ

/-- Adjacent accepted inputs in separated balls must have the same center. -/
theorem adjacent_centers_eq (centers : Finset (V → Bool)) (t : Nat)
    (hsep : Separated centers t) (c d x y : V → Bool)
    (hc : c ∈ centers) (hd : d ∈ centers)
    (hxc : hammingDist x c ≤ t) (hyd : hammingDist y d ≤ t)
    (hxy : hammingDist x y ≤ 1) : c = d := by
  by_contra hne
  have hfar := hsep c hc d hd hne
  have hcx : hammingDist c x ≤ t := by rw [hammingDist_comm]; exact hxc
  have h₁ := hammingDist_triangle c x d
  have h₂ := hammingDist_triangle x y d
  omega

/-- An accepting coordinate subcube lies entirely in ONE separated ball. -/
theorem accepting_subcube_one_center (centers : Finset (V → Bool)) (t : Nat)
    (hsep : Separated centers t) (F : Finset V) (a : V → Bool)
    (haccept : ∀ x ∈ subcube F a, Tube centers t x) :
    ∃ c ∈ centers, ∀ x ∈ subcube F a, hammingDist x c ≤ t := by
  have ha : a ∈ subcube F a := mem_subcube.mpr (fun _ _ => rfl)
  obtain ⟨c, hc, hac⟩ := haccept a ha
  refine ⟨c, hc, ?_⟩
  intro x hx
  apply subcube_step_induction F a a x ha hx (fun z => hammingDist z c ≤ t) hac
  intro z hz w hw hzw hzc
  obtain ⟨d, hd, hwd⟩ := haccept w hw
  have hcd := adjacent_centers_eq centers t hsep c d z w hc hd hzc hwd hzw
  simpa only [hcd] using hwd

/-- Opposing the center on every free coordinate yields at least that many errors. -/
theorem free_card_le_of_subcube_in_ball (F : Finset V) (a c : V → Bool) (t : Nat)
    (hball : ∀ x ∈ subcube F a, hammingDist x c ≤ t) : Fᶜ.card ≤ t := by
  classical
  let far : V → Bool := fun i => if i ∈ F then a i else !(c i)
  have hfar : far ∈ subcube F a := by
    apply mem_subcube.mpr
    intro i hi
    simp [far, hi]
  have hsubset : Fᶜ ⊆ Finset.univ.filter (fun i => far i ≠ c i) := by
    intro i hi
    have hin : i ∉ F := Finset.mem_compl.mp hi
    apply Finset.mem_filter.mpr
    refine ⟨Finset.mem_univ _, ?_⟩
    cases h : c i <;> simp [far, hin, h]
  exact (Finset.card_le_card hsubset).trans (hball far hfar)

/-- Every accepting certificate leaves at most t coordinates free. -/
theorem accepting_subcube_free_card_le (centers : Finset (V → Bool)) (t : Nat)
    (hsep : Separated centers t) (F : Finset V) (a : V → Bool)
    (haccept : ∀ x ∈ subcube F a, Tube centers t x) : Fᶜ.card ≤ t := by
  obtain ⟨c, _, hball⟩ := accepting_subcube_one_center centers t hsep F a haccept
  exact free_card_le_of_subcube_in_ball F a c t hball

/-- The obstruction survives arbitrary initial restrictions and overlapping certificates. -/
theorem relative_certificate_free_budget (centers : Finset (V → Bool)) (t : Nat)
    (hsep : Separated centers t) (F : Finset V) (a : V → Bool)
    (q : Nat) (x : V → Bool) (C : Finset V) (b : V → Bool)
    (hcert : IsCertificate (Tube centers t) F a q x C b) : Fᶜ.card - q ≤ t := by
  classical
  have hc := compatible_of_common_point F a C b x hcert.in_restriction hcert.agrees
  have haccept : ∀ y ∈ subcube (F ∪ C) (fun i => if i ∈ F then a i else b i),
      Tube centers t y := by
    intro y hy
    rw [← subcube_inter_eq F a C b hc] at hy
    exact hcert.forces y (Finset.mem_inter.mp hy).1 (Finset.mem_inter.mp hy).2
  have hbound := accepting_subcube_free_card_le centers t hsep (F ∪ C)
    (fun i => if i ∈ F then a i else b i) haccept
  rw [free_after_union] at hbound
  have hbudget := hcert.budget
  omega

/-- The radius bound is achievable at a center for any free set of size at most t. -/
theorem center_subcube_accepted (centers : Finset (V → Bool)) (t : Nat)
    (c : V → Bool) (hc : c ∈ centers) (F : Finset V) (hfree : Fᶜ.card ≤ t) :
    ∀ x ∈ subcube F c, Tube centers t x := by
  classical
  intro x hx
  refine ⟨c, hc, ?_⟩
  have hsubset : Finset.univ.filter (fun i => x i ≠ c i) ⊆ Fᶜ := by
    intro i hi
    apply Finset.mem_compl.mpr
    intro hF
    exact (Finset.mem_filter.mp hi).2 (mem_subcube.mp hx i hF)
  exact (Finset.card_le_card hsubset).trans hfree

/-- An INNER Boolean function depends only on a declared set of address coordinates. -/
def DependsOn (F : Finset V) (f : (V → Bool) → Bool) : Prop :=
  ∀ x y, (∀ i ∈ F, x i = y i) → f x = f y

/-- One disagreement of locally supported functions repeats on an address subcube. -/
theorem disagreement_contains_subcube (F G : Finset V) (f g : (V → Bool) → Bool)
    (hf : DependsOn F f) (hg : DependsOn G g) (a : V → Bool) (hne : f a ≠ g a) :
    subcube (F ∪ G) a ⊆ Finset.univ.filter (fun x => f x ≠ g x) := by
  intro x hx
  apply Finset.mem_filter.mpr
  refine ⟨Finset.mem_univ _, ?_⟩
  have hfx : f x = f a := hf x a (fun i hi =>
    mem_subcube.mp hx i (Finset.mem_union.mpr (Or.inl hi)))
  have hgx : g x = g a := hg x a (fun i hi =>
    mem_subcube.mp hx i (Finset.mem_union.mpr (Or.inr hi)))
  simpa only [hfx, hgx] using hne

/-- Actual truth-table Hamming distance, not distance between circuit descriptions. -/
theorem supported_distance_lower_bound (F G : Finset V) (f g : (V → Bool) → Bool)
    (hf : DependsOn F f) (hg : DependsOn G g) (hne : f ≠ g) :
    2 ^ (F ∪ G)ᶜ.card ≤ hammingDist f g := by
  classical
  have hex : ∃ a, f a ≠ g a := by
    by_contra h
    push Not at h
    exact hne (funext h)
  obtain ⟨a, ha⟩ := hex
  have hcard := Finset.card_le_card (disagreement_contains_subcube F G f g hf hg a ha)
  rw [card_subcube] at hcard
  exact hcard

/-- Distinct k-juntas are separated by at least 2^(m-2k), with Nat subtraction. -/
theorem junta_distance_lower_bound (F G : Finset V) (f g : (V → Bool) → Bool)
    (hf : DependsOn F f) (hg : DependsOn G g) (hne : f ≠ g)
    (k : Nat) (hF : F.card ≤ k) (hG : G.card ≤ k) :
    2 ^ (Fintype.card V - 2 * k) ≤ hammingDist f g := by
  classical
  have hu := Finset.card_union_le F G
  have hexp : Fintype.card V - 2 * k ≤ (F ∪ G)ᶜ.card := by
    rw [Finset.card_compl]
    omega
  exact (Nat.pow_le_pow_right Nat.zero_lt_two hexp).trans
    (supported_distance_lower_bound F G f g hf hg hne)

#print axioms disagreement_contains_subcube
#print axioms supported_distance_lower_bound
#print axioms junta_distance_lower_bound

#print axioms hammingDist_le_one
#print axioms subcube_step_induction
#print axioms adjacent_centers_eq
#print axioms accepting_subcube_one_center
#print axioms free_card_le_of_subcube_in_ball
#print axioms accepting_subcube_free_card_le
#print axioms relative_certificate_free_budget
#print axioms center_subcube_accepted

end
end SeparatedTubes
