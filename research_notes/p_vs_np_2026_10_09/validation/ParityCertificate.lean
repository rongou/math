import Std

/-!
# Finite parity certificate for a NAIVE gate-fanin generalization

This is a standalone finite arithmetic/semantic certificate, NOT a Lean proof
of family112, of any real-valued analytic inequality, or of a counterexample to
the original paper. The external analytic argument turns the correlations
checked here into a lower bound on a proposed restriction-dependent multiplier.

`none` in a restriction means live; `some false` / `some true` means fixed.
Assignments and restrictions are explicitly enumerated lists, not samples.
For width-one CNFs, a consistent conjunction of unit literals is a subcube;
an inconsistent conjunction is the separately included false subcube.
All sums are UNNORMALIZED. Integer absolute values are returned as naturals.

The distribution p = 1/4 gives a restriction with m live coordinates and d-m
fixed coordinates probability 2^m * 3^(d-m) / 8^d. This file checks the integer
weights and their total, not a measure-theoretic probability construction.
-/

namespace ParityCertificate

set_option debug.skipKernelTC false
set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

/-- Every Boolean word of length n, each exactly once. -/
def assignments : Nat → List (List Bool)
  | 0 => [[]]
  | n + 1 => (assignments n).flatMap fun z => [false :: z, true :: z]

/-- Every restriction of length n, each exactly once. -/
def restrictions : Nat → List (List (Option Bool))
  | 0 => [[]]
  | n + 1 => (restrictions n).flatMap fun s =>
      [none :: s, some false :: s, some true :: s]

/-- Odd parity; each recursive combining gate has fanin two. -/
def parity : List Bool → Bool
  | [] => false
  | b :: z => Bool.xor b (parity z)

/-- The even-parity Boolean function on the raw input bits. -/
def H (x : List Bool) : Bool := !(parity x)

/-- G(z) = (-1)^(parity z). -/
def G (z : List Bool) : Int := if parity z then -1 else 1

def liveCount : List (Option Bool) → Nat
  | [] => 0
  | none :: s => 1 + liveCount s
  | some _ :: s => liveCount s

/-- Fill live coordinates left to right. The fallback on missing live bits is
irrelevant below: every use takes z from assignments (liveCount s). -/
def fill : List (Option Bool) → List Bool → List Bool
  | [], _ => []
  | some b :: s, z => b :: fill s z
  | none :: s, b :: z => b :: fill s z
  | none :: s, [] => false :: fill s []

/-- A subcube indicator, false also on words of the wrong length. -/
def matchesSubcube : List (Option Bool) → List Bool → Bool
  | [] => fun z => match z with
      | [] => true
      | _ :: _ => false
  | entry :: s => fun z => match z with
      | [] => false
      | c :: z =>
          (match entry with | none => true | some b => b == c) &&
            matchesSubcube s z

/-- Outer none denotes the identically false subcube. Inner none is a free bit. -/
abbrev Subcube := Option (List (Option Bool))

def subcubes (m : Nat) : List Subcube :=
  none :: (restrictions m).map some

def subcubeIndicator : Subcube → List Bool → Bool
  | none, _ => false
  | some s, z => matchesSubcube s z

def subcubeSignedSum (m : Nat) (j : Subcube) : Int :=
  ((assignments m).map fun z => if subcubeIndicator j z then G z else 0).sum

def maxSubcubeSignedSum (m : Nat) : Nat :=
  ((subcubes m).map fun j => (subcubeSignedSum m j).natAbs).foldl Nat.max 0

/-- v(sigma) = |sum_z G(z) H(fill sigma z)|, with H interpreted as 0/1. -/
def correlationValue (s : List (Option Bool)) : Nat :=
  (((assignments (liveCount s)).map fun z =>
    if H (fill s z) then G z else 0).sum).natAbs

def restrictionWeight (s : List (Option Bool)) : Nat :=
  2 ^ liveCount s * 3 ^ (s.length - liveCount s)

def weightedSum (d : Nat) : Nat :=
  ((restrictions d).map fun s => restrictionWeight s * correlationValue s).sum

def weightedSum6 : Nat := weightedSum 6

/-- Separate closed computations, one for each requested dimension. -/
theorem maxSubcubeSignedSum_0 : maxSubcubeSignedSum 0 = 1 := by decide
theorem maxSubcubeSignedSum_1 : maxSubcubeSignedSum 1 = 1 := by decide
theorem maxSubcubeSignedSum_2 : maxSubcubeSignedSum 2 = 1 := by decide
theorem maxSubcubeSignedSum_3 : maxSubcubeSignedSum 3 = 1 := by decide
theorem maxSubcubeSignedSum_4 : maxSubcubeSignedSum 4 = 1 := by decide
theorem maxSubcubeSignedSum_5 : maxSubcubeSignedSum 5 = 1 := by decide
theorem maxSubcubeSignedSum_6 : maxSubcubeSignedSum 6 = 1 := by decide

/-- Natural-number formulation, including the zero-dimensional subcube. -/
theorem maxSubcubeSignedSum_of_le_six :
    (m : Nat) → m ≤ 6 → maxSubcubeSignedSum m = 1
  | 0, _ => maxSubcubeSignedSum_0
  | 1, _ => maxSubcubeSignedSum_1
  | 2, _ => maxSubcubeSignedSum_2
  | 3, _ => maxSubcubeSignedSum_3
  | 4, _ => maxSubcubeSignedSum_4
  | 5, _ => maxSubcubeSignedSum_5
  | 6, _ => maxSubcubeSignedSum_6
  | n + 7, h => False.elim (Nat.not_succ_le_zero n
      (Nat.le_of_succ_le_succ (Nat.le_of_succ_le_succ
        (Nat.le_of_succ_le_succ (Nat.le_of_succ_le_succ
          (Nat.le_of_succ_le_succ (Nat.le_of_succ_le_succ h)))))))

/-- This finite universal theorem includes m = 0, ..., 6. -/
theorem maxSubcubeSignedSum_zero_through_six (m : Fin 7) :
    maxSubcubeSignedSum m.val = 1 :=
  maxSubcubeSignedSum_of_le_six m.val (Nat.le_of_lt_succ m.isLt)

/-- The false indicator is included and contributes zero in every dimension. -/
theorem falseSubcubeSignedSum_zero (m : Nat) : subcubeSignedSum m none = 0 := by
  have h : ∀ zs : List (List Bool),
      (zs.map fun z => if subcubeIndicator none z then G z else 0).sum = 0 := by
    intro zs
    induction zs with
    | nil => rfl
    | cons z zs ih => exact congrArg (fun t : Int => 0 + t) ih
  exact h (assignments m)

theorem weightedSum6_exact : weightedSum6 = 500000 := by decide

/-- Normalization of all 3^6 integer restriction weights. -/
theorem restrictionWeights6_total :
    ((restrictions 6).map restrictionWeight).sum = 8 ^ 6 := by decide

/-- An auditable breakdown of the numerator by the number of live bits. -/
def weightedByLiveCount6 (m : Nat) : Nat :=
  (((restrictions 6).filter fun s => liveCount s == m).map fun s =>
    restrictionWeight s * correlationValue s).sum

theorem weightedProfile6_exact :
    (List.range 7).map weightedByLiveCount6 =
      [23328, 93312, 155520, 138240, 69120, 18432, 2048] := by decide

theorem denominator6_exact : (8 : Nat) ^ 6 = 262144 := by decide

/-- Equality of the unreduced and reduced positive-denominator fractions. -/
theorem fraction_reduction_cross_product :
    (500000 : Nat) * 8192 = 15625 * 262144 := by decide

theorem strict_separation : (5 : Nat) * 500000 > 9 * 8 ^ 6 := by decide

theorem weighted_strict_separation : 5 * weightedSum6 > 9 * 8 ^ 6 := by
  rw [weightedSum6_exact]
  exact strict_separation

/-- An explicit binary-XOR circuit followed by a unary NOT. -/
def H6fanin2 (a b c d e f : Bool) : Bool :=
  !(Bool.xor (Bool.xor (Bool.xor a b) (Bool.xor c d)) (Bool.xor e f))

theorem H6fanin2_correct :
    ∀ a b c d e f : Bool, H [a, b, c, d, e, f] = H6fanin2 a b c d e f := by
  decide

/-- The principal finite certificate, with no real-valued analytic claim. -/
theorem finite_certificate :
    (∀ m : Fin 7, maxSubcubeSignedSum m.val = 1) ∧
    weightedSum6 = 500000 ∧
    ((restrictions 6).map restrictionWeight).sum = 8 ^ 6 ∧
    (5 : Nat) * 500000 > 9 * 8 ^ 6 :=
  ⟨maxSubcubeSignedSum_zero_through_six, weightedSum6_exact,
    restrictionWeights6_total, strict_separation⟩

#print axioms maxSubcubeSignedSum_0
#print axioms maxSubcubeSignedSum_1
#print axioms maxSubcubeSignedSum_2
#print axioms maxSubcubeSignedSum_3
#print axioms maxSubcubeSignedSum_4
#print axioms maxSubcubeSignedSum_5
#print axioms maxSubcubeSignedSum_6
#print axioms maxSubcubeSignedSum_zero_through_six
#print axioms maxSubcubeSignedSum_of_le_six
#print axioms falseSubcubeSignedSum_zero
#print axioms weightedSum6_exact
#print axioms restrictionWeights6_total
#print axioms weightedProfile6_exact
#print axioms denominator6_exact
#print axioms fraction_reduction_cross_product
#print axioms strict_separation
#print axioms weighted_strict_separation
#print axioms H6fanin2_correct
#print axioms finite_certificate

end ParityCertificate
