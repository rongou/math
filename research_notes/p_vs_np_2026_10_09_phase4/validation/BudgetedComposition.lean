import SeparatedTubes

/-!
Glue for the one-round composition control, not a full GapMCSP theorem.
The center set is a finite set of actual Boolean tables; all 16 binary
Boolean operations are allowed. Hamming errors add under composition.
The separate gate-set identity counts distinct node IDs and does not by
itself assert that an arbitrary finite set is a well-formed circuit.
-/

namespace BudgetedComposition

universe u
noncomputable section
open scoped Classical
open SeparatedTubes
variable {V : Type u} [Fintype V]

/-- All pointwise binary Boolean combinations of two centers. -/
def binaryCenters (C : Finset (V → Bool)) : Finset (V → Bool) :=
  C.biUnion fun x => C.biUnion fun y =>
    Finset.univ.image (fun op : Bool → Bool → Bool => fun i => op (x i) (y i))

theorem mem_binaryCenters (C : Finset (V → Bool)) (x y : V → Bool)
    (hx : x ∈ C) (hy : y ∈ C) (op : Bool → Bool → Bool) :
    (fun i => op (x i) (y i)) ∈ binaryCenters C := by
  classical
  apply Finset.mem_biUnion.mpr
  refine ⟨x, hx, ?_⟩
  apply Finset.mem_biUnion.mpr
  refine ⟨y, hy, ?_⟩
  exact Finset.mem_image.mpr ⟨op, Finset.mem_univ _, rfl⟩

/-- An output can change only where at least one argument changes. -/
theorem binary_hamming_bound (op : Bool → Bool → Bool) (x y c d : V → Bool) :
    hammingDist (fun i => op (x i) (y i)) (fun i => op (c i) (d i)) ≤
      hammingDist x c + hammingDist y d := by
  have hleft : hammingDist (fun i => op (x i) (y i)) (fun i => op (c i) (y i)) ≤
      hammingDist x c := hammingDist_comp_le_hammingDist (fun i b => op b (y i))
  have hright : hammingDist (fun i => op (c i) (y i)) (fun i => op (c i) (d i)) ≤
      hammingDist y d := hammingDist_comp_le_hammingDist (fun i b => op (c i) b)
  exact (hammingDist_triangle (fun i => op (x i) (y i))
    (fun i => op (c i) (y i)) (fun i => op (c i) (d i))).trans
    (Nat.add_le_add hleft hright)

/-- One noisy composition round is contained in the tube with summed radii. -/
theorem binary_tube_closure (C : Finset (V → Bool)) (r s : Nat) (x y : V → Bool)
    (hx : Tube C r x) (hy : Tube C s y) (op : Bool → Bool → Bool) :
    Tube (binaryCenters C) (r + s) (fun i => op (x i) (y i)) := by
  obtain ⟨c, hc, hxc⟩ := hx
  obtain ⟨d, hd, hyd⟩ := hy
  refine ⟨(fun i => op (c i) (d i)), mem_binaryCenters C c d hc hd op, ?_⟩
  exact (binary_hamming_bound op x y c d).trans (Nat.add_le_add hxc hyd)

/-- The new family includes the old one, not just its unperturbed centers. -/
theorem original_tube_subset_binary_double (C : Finset (V → Bool)) (r : Nat)
    (x : V → Bool) (hx : Tube C r x) : Tube (binaryCenters C) (r + r) x := by
  simpa using binary_tube_closure C r r x x hx hx (fun a _ => a)

/-- Shared reachable gates are charged once, with genuinely fresh top gates. -/
theorem distinct_gate_union_cost (A B New : Finset Nat)
    (hnew : Disjoint (A ∪ B) New) :
    ((A ∪ B) ∪ New).card + (A ∩ B).card = A.card + B.card + New.card := by
  rw [Finset.card_union_of_disjoint hnew]
  have h := Finset.card_union_add_card_inter A B
  omega

#print axioms mem_binaryCenters
#print axioms binary_hamming_bound
#print axioms binary_tube_closure
#print axioms original_tube_subset_binary_double
#print axioms distinct_gate_union_cost

end
end BudgetedComposition
