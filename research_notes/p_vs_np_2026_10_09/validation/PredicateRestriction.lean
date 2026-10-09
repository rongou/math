import LocalPredicateCNF
import OAI.Computability.DepthThree.Restriction

/-!
Restriction-lemma corollary for finite conjunctions of arbitrary scoped Boolean predicates.
Inputs may repeat: clauses are finite sets of literals, and width counts distinct variables.
The CNF translation is a truth-table expansion, not a polynomial-size/time construction.
-/

namespace OAI.DepthThreeLowerBound.PredicateRestriction

universe u
noncomputable section
open scoped Classical

/-- A local predicate with an arbitrary (not necessarily injective) input map. -/
structure ScopedPredicate (V : Type u) where
  arity : Nat
  inputs : Fin arity → V
  Q : (Fin arity → Bool) → Bool

variable {V : Type u}

namespace ScopedPredicate

def eval (P : ScopedPredicate V) (x : Cube V) : Bool := P.Q (x ∘ P.inputs)

/-- The clause falsified by the local bit pattern `a`, before identifying repeated inputs. -/
def rejectedClause (P : ScopedPredicate V) (a : Fin P.arity → Bool) : Clause V :=
  Finset.univ.image (fun i => (P.inputs i, !(a i)))

theorem rejectedClause_eval (P : ScopedPredicate V) (a : Fin P.arity → Bool)
    (x : Cube V) :
    (P.rejectedClause a).eval x = true ↔
      ∃ i : Fin P.arity, x (P.inputs i) ≠ a i := by
  simp [rejectedClause, Clause.eval_eq_true, Bool.eq_not_iff]

theorem rejectedClause_width_le (P : ScopedPredicate V) (a : Fin P.arity → Bool) :
    (P.rejectedClause a).width ≤ P.arity := by
  calc
    (P.rejectedClause a).width ≤ (P.rejectedClause a).card := Finset.card_image_le
    _ ≤ (Finset.univ : Finset (Fin P.arity)).card := Finset.card_image_le
    _ = P.arity := by simp

/-- One encoded clause for each rejected truth-table row. -/
def compile (P : ScopedPredicate V) : CNF V :=
  (LocalPredicateCNF.truthTableCNF P.arity P.Q).map P.rejectedClause

theorem compile_eval (P : ScopedPredicate V) (x : Cube V) :
    P.compile.eval x = P.eval x := by
  apply Bool.eq_iff_iff.mpr
  simpa only [CNF.eval_eq_true, compile, List.forall_mem_map, rejectedClause_eval, eval,
    Function.comp_apply]
    using (LocalPredicateCNF.truthTableCNF_correct P.arity P.Q (x ∘ P.inputs)).symm

theorem compile_width (P : ScopedPredicate V) : P.compile.WidthAtMost P.arity := by
  intro C hC
  obtain ⟨a, _, rfl⟩ := List.mem_map.mp hC
  exact P.rejectedClause_width_le a

theorem compile_length_le (P : ScopedPredicate V) : P.compile.length ≤ 2 ^ P.arity := by
  simpa only [compile, List.length_map]
    using LocalPredicateCNF.truthTableCNF_length_le P.arity P.Q

end ScopedPredicate

/-- Boolean conjunction, including the empty list (true). -/
def conjunction (Ps : List (ScopedPredicate V)) (x : Cube V) : Bool :=
  Ps.all (fun P => P.eval x)

/-- Concatenate the truth-table CNFs of the predicates. -/
def compileConjunction (Ps : List (ScopedPredicate V)) : CNF V :=
  Ps.flatMap ScopedPredicate.compile

theorem conjunction_eq_true (Ps : List (ScopedPredicate V)) (x : Cube V) :
    conjunction Ps x = true ↔ ∀ P ∈ Ps, P.Q (x ∘ P.inputs) = true := by
  simp [conjunction, ScopedPredicate.eval]

theorem compileConjunction_eval (Ps : List (ScopedPredicate V)) (x : Cube V) :
    (compileConjunction Ps).eval x = conjunction Ps x := by
  induction Ps with
  | nil => simp [compileConjunction, conjunction]
  | cons P Ps ih =>
    change (P.compile ++ compileConjunction Ps).eval x = (P.eval x && conjunction Ps x)
    rw [CNF.eval_append, ScopedPredicate.compile_eval, ih]

theorem compileConjunction_width (Ps : List (ScopedPredicate V)) (k : Nat)
    (hPs : ∀ P ∈ Ps, P.arity ≤ k) : (compileConjunction Ps).WidthAtMost k := by
  intro C hC
  obtain ⟨P, hP, hC⟩ := List.mem_flatMap.mp hC
  exact (P.compile_width C hC).trans (hPs P hP)

/-- The repository's exact theta/expectation/all-test-function bound for these predicates. -/
theorem predicate_restriction_bound [Fintype V]
    (Ps : List (ScopedPredicate V)) (b k : Nat) (hb : 1 ≤ b)
    (hPs : ∀ P ∈ Ps, P.arity ≤ k) (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1)
    (hθ : restrictionTheta k b p < 1) :
    ∃ W : Restriction V → ℝ,
      (∀ σ, 0 ≤ W σ) ∧
      restrictionAvg p W ≤ 1 / (1 - restrictionTheta k b p) ∧
      ∀ (σ : Restriction V) (G : Cube (Live σ) → ℝ),
        |finiteAvg (fun x => G x * indicator (conjunction Ps (fill σ x)))| ≤
          W σ * corr b G := by
  simpa only [compileConjunction_eval] using
    (OAI.DepthThreeLowerBound.cnf_restriction_bound
      (compileConjunction Ps) b k hb (compileConjunction_width Ps k hPs) p hp0 hp1 hθ)

#print axioms ScopedPredicate.rejectedClause_eval
#print axioms ScopedPredicate.rejectedClause_width_le
#print axioms ScopedPredicate.compile_eval
#print axioms ScopedPredicate.compile_width
#print axioms ScopedPredicate.compile_length_le
#print axioms conjunction_eq_true
#print axioms compileConjunction_eval
#print axioms compileConjunction_width
#print axioms predicate_restriction_bound

end
end OAI.DepthThreeLowerBound.PredicateRestriction
