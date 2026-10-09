import Std

/-!
# A scalar-only, denominator-cleared certificate

This file uses natural numbers, not `Real` or a spectral model. Its intended
external interpretation is delta = p/q, A_i = a_i/q, u_i = v_i/q, with q > 0.
`Inputs` explicitly assumes the scalar recurrences and the conditional local
loss estimate u_i <= 4*A_i^2. No analytic estimate is proved or postulated here.

All declarations below are proved without any axiom dependencies, including
Lean's optional logical axioms. Closed arithmetic uses `decide`, not native
execution. The axiom-audit assertions at the end are part of the checked file.
-/

set_option autoImplicit false

namespace ScalarConstants

/-! Small constructive arithmetic helpers. Reproving these two identities avoids
    the `propext` dependency of the corresponding installed convenience lemmas. -/

private theorem mulAssoc (a b c : Nat) : a * b * c = a * (b * c) := by
  induction c with
  | zero => rfl
  | succ c ih =>
    change a * b * c + a * b = a * (b * c + b)
    rw [Nat.mul_add, ih]

private theorem addMul (a b c : Nat) : (a + b) * c = a * c + b * c := by
  rw [Nat.mul_comm (a + b) c, Nat.mul_add, Nat.mul_comm c a, Nat.mul_comm c b]

private theorem addOneScale (b p : Nat) : b * p + p = (b + 1) * p := by
  rw [addMul, Nat.one_mul]

private theorem scaledSquare (c p : Nat) :
    (c * p) * (c * p) = (c * c) * (p * p) := by
  rw [mulAssoc c p (c * p), ← mulAssoc p c p, Nat.mul_comm p c,
    mulAssoc c p p, ← mulAssoc c c (p * p)]

/-! Exact finite arithmetic. The natural coefficients in each budget are
    nonnegative; the equalities check that none was obtained by truncated
    subtraction or by an approximate floating-point computation. -/

def ConstantChecks : Prop :=
  ([1, 3, 5, 9].map (fun c : Nat => 4 * (c * c)) = [4, 36, 100, 324]) ∧
  ([4, 2 * 4 + 36, 4 * 4 + 2 * 36 + 100] : List Nat) = [4, 44, 188] ∧
  (4 + 2044 = (2048 : Nat) ∧ 44 + 2004 = 2048 ∧ 188 + 1860 = 2048) ∧
  (4 * 1 + 2044 = (2048 : Nat) ∧ 4 * 3 + 2036 = 2048 ∧
    4 * 5 + 2028 = 2048 ∧ 4 * 9 + 2012 = 2048) ∧
  (8 * 4 + 4 * 36 + 2 * 100 + 324 = (700 : Nat)) ∧
  (700 + 324 = (1024 : Nat)) ∧
  (2 * 1024 = (2048 : Nat))

theorem constant_checks : ConstantChecks := by
  unfold ConstantChecks
  decide

/-! Polynomial identities with manifestly nonnegative remainders. Put
    q = 2048*p + s. After division by q^2, s/q is 1 - 2048*delta.
    These are genuine universally quantified Nat identities, not sample tests. -/

private theorem absorptionIdentity (p s k r : Nat) (budget : k + r = 2048) :
    p * (2048 * p + s) = k * (p * p) + r * (p * p) + p * s := by
  calc
    p * (2048 * p + s) = p * (2048 * p) + p * s := Nat.mul_add ..
    _ = 2048 * (p * p) + p * s := by
      rw [← mulAssoc p 2048 p, Nat.mul_comm p 2048, mulAssoc 2048 p p]
    _ = (k + r) * (p * p) + p * s := by rw [budget]
    _ = k * (p * p) + r * (p * p) + p * s := by rw [addMul]

private theorem stageIdentity (p s b k r : Nat) (budget : k + r = 2048) :
    (b + 1) * (p * (2048 * p + s)) =
      (b * (p * (2048 * p + s)) + k * (p * p)) +
        (r * (p * p) + p * s) := by
  calc
    (b + 1) * (p * (2048 * p + s)) =
        b * (p * (2048 * p + s)) + p * (2048 * p + s) := by
      rw [addMul, Nat.one_mul]
    _ = b * (p * (2048 * p + s)) +
        (k * (p * p) + r * (p * p) + p * s) :=
      congrArg (fun x => b * (p * (2048 * p + s)) + x)
        (absorptionIdentity p s k r budget)
    _ = (b * (p * (2048 * p + s)) + k * (p * p)) +
        (r * (p * p) + p * s) := by
      rw [Nat.add_assoc (k * (p * p)) (r * (p * p)) (p * s),
        Nat.add_assoc (b * (p * (2048 * p + s))) (k * (p * p))
          (r * (p * p) + p * s)]

private theorem cutoffIdentity (p s c r : Nat) (budget : 4 * c + r = 2048) :
    2048 * p + s = 4 * (c * p) + (r * p + s) := by
  calc
    2048 * p + s = (4 * c + r) * p + s := by rw [budget]
    _ = (4 * c) * p + r * p + s := by rw [addMul]
    _ = 4 * (c * p) + (r * p + s) := by rw [mulAssoc, Nat.add_assoc]

structure PolynomialChecks (p s : Nat) : Prop where
  square1 : 4 * ((1 * p) * (1 * p)) = 4 * (p * p)
  square2 : 4 * ((3 * p) * (3 * p)) = 36 * (p * p)
  square3 : 4 * ((5 * p) * (5 * p)) = 100 * (p * p)
  square4 : 4 * ((9 * p) * (9 * p)) = 324 * (p * p)
  stage2 : 3 * (p * (2048 * p + s)) =
    (2 * (p * (2048 * p + s)) + 4 * (p * p)) + (2044 * (p * p) + p * s)
  stage3 : 5 * (p * (2048 * p + s)) =
    (4 * (p * (2048 * p + s)) + 44 * (p * p)) + (2004 * (p * p) + p * s)
  stage4 : 9 * (p * (2048 * p + s)) =
    (8 * (p * (2048 * p + s)) + 188 * (p * p)) + (1860 * (p * p) + p * s)
  cutoff1 : 2048 * p + s = 4 * (1 * p) + (2044 * p + s)
  cutoff2 : 2048 * p + s = 4 * (3 * p) + (2036 * p + s)
  cutoff3 : 2048 * p + s = 4 * (5 * p) + (2028 * p + s)
  cutoff4 : 2048 * p + s = 4 * (9 * p) + (2012 * p + s)
  weighted : 8 * (4 * (p * p)) + 4 * (36 * (p * p)) +
    2 * (100 * (p * p)) + 324 * (p * p) = 700 * (p * p)
  reserve : 1024 * (p * p) = 700 * (p * p) + 324 * (p * p)
  contraction : 2048 * p + s = 2 * (1024 * p) + s

theorem polynomial_checks (p s : Nat) : PolynomialChecks p s := by
  constructor
  · rw [scaledSquare, ← mulAssoc]
  · rw [scaledSquare, ← mulAssoc]
  · rw [scaledSquare, ← mulAssoc]
  · rw [scaledSquare, ← mulAssoc]
  · exact stageIdentity p s 2 4 2044 (by decide)
  · exact stageIdentity p s 4 44 2004 (by decide)
  · exact stageIdentity p s 8 188 1860 (by decide)
  · exact cutoffIdentity p s 1 2044 (by decide)
  · exact cutoffIdentity p s 3 2036 (by decide)
  · exact cutoffIdentity p s 5 2028 (by decide)
  · exact cutoffIdentity p s 9 2012 (by decide)
  · rw [← mulAssoc 8 4 (p * p), ← mulAssoc 4 36 (p * p),
      ← mulAssoc 2 100 (p * p), ← addMul, ← addMul, ← addMul]
  · exact addMul 700 324 (p * p)
  · rw [← mulAssoc]

/-! The three nonnegative-coefficient gap certificates imply actual inequalities
    in the formalized domain. No abstract order facts are assumed. -/

theorem nonnegative_gap_checks (p s : Nat) :
    (2 * (p * (2048 * p + s)) + 4 * (p * p) ≤ 3 * (p * (2048 * p + s))) ∧
    (4 * (p * (2048 * p + s)) + 44 * (p * p) ≤ 5 * (p * (2048 * p + s))) ∧
    (8 * (p * (2048 * p + s)) + 188 * (p * p) ≤ 9 * (p * (2048 * p + s))) := by
  have cert := polynomial_checks p s
  constructor
  · rw [cert.stage2]; exact Nat.le_add_right ..
  constructor
  · rw [cert.stage3]; exact Nat.le_add_right ..
  · rw [cert.stage4]; exact Nat.le_add_right ..

/-! Denominator-cleared scalar induction. In particular, the quarter cutoffs
    are conclusions, not hypotheses of the induction. Only the local loss law
    is conditional on each cutoff. All numerators are nonnegative by type. -/

structure Inputs (p q a1 a2 a3 a4 v1 v2 v3 v4 : Nat) : Prop where
  denominator_pos : 0 < q
  delta_small : 2048 * p ≤ q
  input1 : a1 ≤ p
  input2 : a2 ≤ 2 * p + v1
  input3 : a3 ≤ 4 * p + 2 * v1 + v2
  input4 : a4 ≤ 8 * p + 4 * v1 + 2 * v2 + v3
  loss1 : 4 * a1 ≤ q → v1 * q ≤ 4 * (a1 * a1)
  loss2 : 4 * a2 ≤ q → v2 * q ≤ 4 * (a2 * a2)
  loss3 : 4 * a3 ≤ q → v3 * q ≤ 4 * (a3 * a3)
  loss4 : 4 * a4 ≤ q → v4 * q ≤ 4 * (a4 * a4)

structure Bounds (p q a1 a2 a3 a4 v1 v2 v3 v4 : Nat) : Prop where
  amplitude1 : a1 ≤ p
  input2_bound : 2 * p + v1 ≤ 3 * p
  amplitude2 : a2 ≤ 3 * p
  input3_bound : 4 * p + 2 * v1 + v2 ≤ 5 * p
  amplitude3 : a3 ≤ 5 * p
  input4_bound : 8 * p + 4 * v1 + 2 * v2 + v3 ≤ 9 * p
  amplitude4 : a4 ≤ 9 * p
  loss1_bound : v1 * q ≤ 4 * (p * p)
  loss2_bound : v2 * q ≤ 36 * (p * p)
  loss3_bound : v3 * q ≤ 100 * (p * p)
  loss4_bound : v4 * q ≤ 324 * (p * p)
  quarter1 : 4 * a1 ≤ q
  quarter2 : 4 * a2 ≤ q
  quarter3 : 4 * a3 ≤ q
  quarter4 : 4 * a4 ≤ q
  weighted700 : (8 * v1 + 4 * v2 + 2 * v3 + v4) * q ≤ 700 * (p * p)
  relaxation : 700 * (p * p) ≤ 1024 * (p * p)
  weighted1024 : (8 * v1 + 4 * v2 + 2 * v3 + v4) * q ≤ 1024 * (p * p)
  contraction : 2 * (1024 * p) ≤ q

private theorem quarterOfCap {a c p q : Nat}
    (cap : a ≤ c * p) (hc : 4 * c ≤ 2048) (small : 2048 * p ≤ q) : 4 * a ≤ q := by
  calc
    4 * a ≤ 4 * (c * p) := Nat.mul_le_mul_left 4 cap
    _ = (4 * c) * p := (mulAssoc ..).symm
    _ ≤ 2048 * p := Nat.mul_le_mul_right p hc
    _ ≤ q := small

private theorem lossOfCap {a v c k p q : Nat}
    (cap : a ≤ c * p) (loss : v * q ≤ 4 * (a * a)) (hk : 4 * (c * c) = k) :
    v * q ≤ k * (p * p) := by
  calc
    v * q ≤ 4 * (a * a) := loss
    _ ≤ 4 * ((c * p) * (c * p)) := Nat.mul_le_mul_left 4 (Nat.mul_le_mul cap cap)
    _ = (4 * (c * c)) * (p * p) := by rw [scaledSquare, mulAssoc 4 (c * c) (p * p)]
    _ = k * (p * p) := by rw [hk]

private theorem absorb {k p q : Nat} (hk : k ≤ 2048) (small : 2048 * p ≤ q) :
    k * (p * p) ≤ p * q := by
  calc
    k * (p * p) = (k * p) * p := (mulAssoc ..).symm
    _ ≤ q * p := Nat.mul_le_mul_right p (Nat.le_trans (Nat.mul_le_mul_right p hk) small)
    _ = p * q := Nat.mul_comm ..

private theorem correctionLe {v k p q : Nat}
    (bound : v * q ≤ k * (p * p)) (hk : k ≤ 2048)
    (small : 2048 * p ≤ q) (positive : 0 < q) : v ≤ p :=
  Nat.le_of_mul_le_mul_right (Nat.le_trans bound (absorb hk small)) positive

private theorem scaleBound {v q k t : Nat} (bound : v * q ≤ k * t) (c : Nat) :
    (c * v) * q ≤ (c * k) * t := by
  calc
    (c * v) * q = c * (v * q) := mulAssoc ..
    _ ≤ c * (k * t) := Nat.mul_le_mul_left c bound
    _ = (c * k) * t := (mulAssoc ..).symm

private theorem addBounds {v w q k l t : Nat}
    (hv : v * q ≤ k * t) (hw : w * q ≤ l * t) : (v + w) * q ≤ (k + l) * t := by
  calc
    (v + w) * q = v * q + w * q := addMul ..
    _ ≤ k * t + l * t := Nat.add_le_add hv hw
    _ = (k + l) * t := (addMul ..).symm

theorem scalar_induction {p q a1 a2 a3 a4 v1 v2 v3 v4 : Nat}
    (h : Inputs p q a1 a2 a3 a4 v1 v2 v3 v4) :
    Bounds p q a1 a2 a3 a4 v1 v2 v3 v4 := by
  have a1cap : a1 ≤ 1 * p := by rw [Nat.one_mul]; exact h.input1
  have q1 := quarterOfCap a1cap (by decide) h.delta_small
  have u1 : v1 * q ≤ 4 * (p * p) := lossOfCap a1cap (h.loss1 q1) (by decide)
  have correction2 : v1 ≤ p := correctionLe u1 (by decide) h.delta_small h.denominator_pos
  have rhs2 : 2 * p + v1 ≤ 3 * p := by
    calc
      2 * p + v1 ≤ 2 * p + p := Nat.add_le_add_left correction2 (2 * p)
      _ = 3 * p := addOneScale 2 p
  have a2cap := Nat.le_trans h.input2 rhs2
  have q2 := quarterOfCap a2cap (by decide) h.delta_small
  have u2 : v2 * q ≤ 36 * (p * p) := lossOfCap a2cap (h.loss2 q2) (by decide)
  have correction3q : (2 * v1 + v2) * q ≤ 44 * (p * p) :=
    addBounds (scaleBound u1 2) u2
  have correction3 := correctionLe correction3q (by decide) h.delta_small h.denominator_pos
  have rhs3 : 4 * p + 2 * v1 + v2 ≤ 5 * p := by
    calc
      4 * p + 2 * v1 + v2 = 4 * p + (2 * v1 + v2) := Nat.add_assoc ..
      _ ≤ 4 * p + p := Nat.add_le_add_left correction3 (4 * p)
      _ = 5 * p := addOneScale 4 p
  have a3cap := Nat.le_trans h.input3 rhs3
  have q3 := quarterOfCap a3cap (by decide) h.delta_small
  have u3 : v3 * q ≤ 100 * (p * p) := lossOfCap a3cap (h.loss3 q3) (by decide)
  have correction4q : (4 * v1 + 2 * v2 + v3) * q ≤ 188 * (p * p) :=
    addBounds (addBounds (scaleBound u1 4) (scaleBound u2 2)) u3
  have correction4 := correctionLe correction4q (by decide) h.delta_small h.denominator_pos
  have rhs4 : 8 * p + 4 * v1 + 2 * v2 + v3 ≤ 9 * p := by
    calc
      8 * p + 4 * v1 + 2 * v2 + v3 = 8 * p + (4 * v1 + 2 * v2 + v3) := by
        rw [Nat.add_assoc (8 * p) (4 * v1) (2 * v2),
          Nat.add_assoc (8 * p) (4 * v1 + 2 * v2) v3]
      _ ≤ 8 * p + p := Nat.add_le_add_left correction4 (8 * p)
      _ = 9 * p := addOneScale 8 p
  have a4cap := Nat.le_trans h.input4 rhs4
  have q4 := quarterOfCap a4cap (by decide) h.delta_small
  have u4 : v4 * q ≤ 324 * (p * p) := lossOfCap a4cap (h.loss4 q4) (by decide)
  have weighted : (8 * v1 + 4 * v2 + 2 * v3 + v4) * q ≤ 700 * (p * p) :=
    addBounds (addBounds (addBounds (scaleBound u1 8) (scaleBound u2 4))
      (scaleBound u3 2)) u4
  have relax : 700 * (p * p) ≤ 1024 * (p * p) :=
    Nat.mul_le_mul_right (p * p) (by decide)
  have contract : 2 * (1024 * p) ≤ q := by
    rw [← mulAssoc]
    exact h.delta_small
  exact {
    amplitude1 := h.input1, input2_bound := rhs2, amplitude2 := a2cap,
    input3_bound := rhs3, amplitude3 := a3cap,
    input4_bound := rhs4, amplitude4 := a4cap,
    loss1_bound := u1, loss2_bound := u2, loss3_bound := u3, loss4_bound := u4,
    quarter1 := q1, quarter2 := q2, quarter3 := q3, quarter4 := q4,
    weighted700 := weighted, relaxation := relax,
    weighted1024 := Nat.le_trans weighted relax, contraction := contract }

/-! Nonvacuity and boundary regressions. First delta = 0, then delta = 1/2048
    with all four losses strictly positive (v_i = 1). Neither test is used
    to prove the induction. -/

theorem zero_bounds : Bounds 0 1 0 0 0 0 0 0 0 0 :=
  scalar_induction (by constructor <;> decide)

theorem endpoint_inputs : Inputs 2048 4194304 2048 4097 8195 16391 1 1 1 1 := by
  constructor <;> decide

theorem endpoint_bounds : Bounds 2048 4194304 2048 4097 8195 16391 1 1 1 1 :=
  scalar_induction endpoint_inputs

/-! These guard assertions fail compilation if any audited theorem acquires an
    axiom dependency. The final prints make the successful audit visible. -/

/-- info: 'ScalarConstants.constant_checks' does not depend on any axioms -/
#guard_msgs in
#print axioms constant_checks
/-- info: 'ScalarConstants.polynomial_checks' does not depend on any axioms -/
#guard_msgs in
#print axioms polynomial_checks
/-- info: 'ScalarConstants.nonnegative_gap_checks' does not depend on any axioms -/
#guard_msgs in
#print axioms nonnegative_gap_checks
/-- info: 'ScalarConstants.scalar_induction' does not depend on any axioms -/
#guard_msgs in
#print axioms scalar_induction
/-- info: 'ScalarConstants.zero_bounds' does not depend on any axioms -/
#guard_msgs in
#print axioms zero_bounds
/-- info: 'ScalarConstants.endpoint_bounds' does not depend on any axioms -/
#guard_msgs in
#print axioms endpoint_bounds

#print axioms constant_checks
#print axioms polynomial_checks
#print axioms nonnegative_gap_checks
#print axioms scalar_induction
#print axioms zero_bounds
#print axioms endpoint_bounds

end ScalarConstants
