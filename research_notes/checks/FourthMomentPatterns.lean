import Std

/-!
Finite combinatorial facts used in fourth_moment.md.  This file does NOT
formalize Hecke characters, Poisson summation, the moment estimate, or RH.
It uses only core/Std and can be checked without this repository's .lake.
-/
namespace ResearchNotes.FourthMoment

def bit (mask : Fin 16) (i : Nat) : Int :=
  Int.ofNat ((mask.val / 2 ^ i) % 2)

def plusCount (mask : Fin 16) : Int := bit mask 0 + bit mask 1

def minusCount (mask : Fin 16) : Int := bit mask 2 + bit mask 3

def localExponent (mask : Fin 16) : Int := plusCount mask - minusCount mask

def multiplicity (mask : Fin 16) : Int := plusCount mask + minusCount mask

/-- No nonzero multiple of six can occur at a prime in the fourth moment. -/
theorem principal_iff_balanced :
    ∀ mask : Fin 16, localExponent mask % 6 = 0 ↔
      plusCount mask = minusCount mask := by decide

/-- A nonempty, balanced incidence pattern still contains that prime. -/
theorem balanced_nonempty_has_mask :
    ∀ mask : Fin 16, mask.val ≠ 0 → localExponent mask = 0 →
      multiplicity mask = 2 ∨ multiplicity mask = 4 := by decide

/-- The only nonprincipal local channels are sextic or cubic. -/
theorem active_channels :
    ∀ mask : Fin 16, localExponent mask ≠ 0 →
      localExponent mask = -2 ∨ localExponent mask = -1 ∨
      localExponent mask = 1 ∨ localExponent mask = 2 := by decide

/-- The local Möbius-product parity can be read from the character exponent. -/
theorem mobius_parity :
    ∀ mask : Fin 16, multiplicity mask % 2 = localExponent mask % 2 := by decide

/-- Principal does not mean exponent zero once six columns occur on one side. -/
theorem sixth_order_resonance : (6 : Int) % 6 = 0 ∧ (6 : Int) ≠ 0 := by decide

/-- Multiplication of norm residues 1 mod 6 corresponds to addition mod 6. -/
theorem unit_norm_residue_law :
    ∀ j k : Fin 6,
      (((1 + 6 * j.val) * (1 + 6 * k.val) - 1) / 6) % 6 =
        (j.val + k.val) % 6 := by decide

#print axioms unit_norm_residue_law
#print axioms principal_iff_balanced
#print axioms balanced_nonempty_has_mask
#print axioms active_channels
#print axioms mobius_parity
#print axioms sixth_order_resonance

end ResearchNotes.FourthMoment
