import SeparatedTubes

/-!
Finite prefix-splicing and counting glue for the connected-family control.
This does not formalize the arbitrary-size weighted 2-SAT circuit compiler.
-/
namespace PrefixSplicing

noncomputable section
open scoped Classical
open PromiseCounting
variable {N : Nat}

/-- A thresholded min/max update is exactly a Boolean reachability update. -/
theorem minmax_threshold (a b c t : Nat) :
    min a (max b c) ≤ t ↔ a ≤ t ∨ (b ≤ t ∧ c ≤ t) := by
  simp only [min_le_iff, max_le_iff]

/-- The first j truth-table coordinates come from f and the rest from g. -/
def splice (j : Nat) (f g : Fin N → Bool) : Fin N → Bool :=
  fun i => if i.val < j then f i else g i

theorem splice_zero (f g : Fin N → Bool) : splice 0 f g = g := by
  funext i
  simp [splice]

theorem splice_last (f g : Fin N → Bool) : splice N f g = f := by
  funext i
  simp [splice, i.isLt]

/-- Increasing the cut by one changes at most that single coordinate. -/
theorem splice_adjacent (f g : Fin N → Bool) (j : Nat) (hj : j < N) :
    hammingDist (splice j f g) (splice (j+1) f g) ≤ 1 := by
  apply SeparatedTubes.hammingDist_le_one _ _ ⟨j, hj⟩
  intro i hne
  have hij : i.val ≠ j := by
    intro h
    exact hne (Fin.ext h)
  have hiff : i.val < j ↔ i.val < j+1 := by omega
  simp only [splice, hiff]

/-- All bounded cuts and ordered pairs of finite centers. -/
def spliceSet (C : Finset (Fin N → Bool)) : Finset (Fin N → Bool) :=
  (((Finset.univ : Finset (Fin (N+1))).product (C.product C)).image
    (fun x => splice x.1.val x.2.1 x.2.2))

theorem mem_spliceSet (C : Finset (Fin N → Bool)) (j : Fin (N+1))
    (f g : Fin N → Bool) (hf : f ∈ C) (hg : g ∈ C) :
    splice j.val f g ∈ spliceSet C := by
  apply Finset.mem_image.mpr
  refine ⟨(j, (f, g)), ?_, rfl⟩
  exact Finset.mem_product.mpr ⟨Finset.mem_univ _, Finset.mem_product.mpr ⟨hf, hg⟩⟩

theorem card_spliceSet_le (C : Finset (Fin N → Bool)) :
    (spliceSet C).card ≤ (N+1) * C.card ^ 2 := by
  have h := Finset.card_image_le (s := (Finset.univ : Finset (Fin (N+1))).product (C.product C))
    (f := fun x => splice x.1.val x.2.1 x.2.2)
  simpa [spliceSet, Finset.card_product, Nat.pow_two] using h

/-- The prefix/suffix coverage condition produces an actual exact splice. -/
theorem splice_of_matching_prefix_suffix (p q : Nat) (_hp : p ≤ N) (_hq : q ≤ N)
    (hcover : N ≤ p+q) (t f g : Fin N → Bool)
    (hprefix : ∀ i, i.val < p → t i = f i)
    (hsuffix : ∀ i, N-q ≤ i.val → t i = g i) : t = splice p f g := by
  funext i
  by_cases hi : i.val < p
  · simpa only [splice, ite_eq_left hi] using hprefix i hi
  · simpa only [splice, ite_eq_right hi] using hsuffix i (by omega)

/-- Count any accepting coordinate subcube inside an old set plus the splice set. -/
theorem accepted_subcube_count_bound (C T : Finset (Fin N → Bool))
    (F : Finset (Fin N)) (a : Fin N → Bool)
    (hacc : ∀ x ∈ subcube F a, x ∈ T ∨ x ∈ spliceSet C) :
    2 ^ Fᶜ.card ≤ T.card + (N+1) * C.card ^ 2 := by
  have hsub : subcube F a ⊆ T ∪ spliceSet C := by
    intro x hx
    exact Finset.mem_union.mpr (hacc x hx)
  calc
    2 ^ Fᶜ.card = (subcube F a).card := by
      simpa only [Finset.card_compl] using (card_subcube F a).symm
    _ ≤ (T ∪ spliceSet C).card := Finset.card_le_card hsub
    _ ≤ T.card + (spliceSet C).card := Finset.card_union_le _ _
    _ ≤ T.card + (N+1) * C.card ^ 2 := Nat.add_le_add_left (card_spliceSet_le C) _

#print axioms minmax_threshold
#print axioms splice_zero
#print axioms splice_last
#print axioms splice_adjacent
#print axioms mem_spliceSet
#print axioms card_spliceSet_le
#print axioms splice_of_matching_prefix_suffix
#print axioms accepted_subcube_count_bound

end
end PrefixSplicing
