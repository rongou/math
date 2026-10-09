import Std

/-!
Linear arithmetic of proposed length transformations only.  These maps do not
assert that theta reflection applies to the new divisor-weighted coefficients.
Coordinates may represent log_D lengths in any common denominator.
-/
namespace ResearchNotes.CoprimeScales

def poisson (p : Int × Int) : Int × Int := (2 * p.2 - p.1, p.2)

def theta (p : Int × Int) : Int × Int := (p.1, 2 * p.1 - p.2)

theorem poisson_involution (u x : Int) : poisson (poisson (u, x)) = (u, x) := by
  apply Prod.ext <;> simp [poisson] <;> omega

theorem theta_involution (u x : Int) : theta (theta (u, x)) = (u, x) := by
  apply Prod.ext <;> simp [theta] <;> omega

theorem cycle_formula (u x : Int) :
    theta (poisson (u, x)) = (u + 2 * (x - u), x + 2 * (x - u)) := by
  apply Prod.ext <;> simp [theta, poisson] <;> omega

theorem short_row_cycle_grows (u x : Int) (h : u < x) :
    u < (theta (poisson (u, x))).1 ∧ x < (theta (poisson (u, x))).2 := by
  simp [theta, poisson]
  omega

/-- Pilot exponents in units of one third: (4/3,2) -> (8/3,2). -/
theorem pilot_outside_canonical_range :
    ¬ (poisson (4, 6)).1 ≤ (poisson (4, 6)).2 := by decide

/-- Even the counterfactually transferred completed bound has exponent 14/3. -/
theorem pilot_completed_budget_exceeds_target : max (4 + 8) (4 + 2 * 8 - 6) > (10 : Int) := by decide

#print axioms poisson_involution
#print axioms theta_involution
#print axioms cycle_formula
#print axioms short_row_cycle_grows
#print axioms pilot_outside_canonical_range
#print axioms pilot_completed_budget_exceeds_target

end ResearchNotes.CoprimeScales
