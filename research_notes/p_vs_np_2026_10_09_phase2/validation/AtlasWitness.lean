import Std

/-!
# Finite atlas witness, NOT a general circuit-encoding or analytic theorem

The checked finite grammar has initial wires [0,1,x0,x1,x2], encoded by their
8-bit truth tables [0,255,170,204,240]. Row a means xi=(a/2^i)%2.
Two topological gate slots are used. Slot one has 55 choices over 5 wires;
slot two has 78 choices over the resulting 6 wires. At k available wires:
  codes 0..k-1: NOT of wire code;
  next k^2 codes: AND2(a,b), row-major ordered (a,b);
  last k^2 codes: OR2(a,b), row-major ordered (a,b).
Fanins may repeat; earlier gates may be reused; outputs are any of all 7 wires.
Unused gate slots are permitted, and a zero/one-slot witness is padded by NOT 0.
This checks precisely this 55*78*7 finite grammar, not an arbitrary-DAG encoding
or normalization theorem. Python separately exhausts the stated <=2 grammar.

Low is the explicit 40-table list below. The forward check covers every output
of every pair of slot codes. Explicit in-range codes witness all Low entries.
Zero-table certificate checks concern the MAXIMAL separator 1_Low. Its accepting
subcubes need not be accepted by a fixed solver, which may reject GAP tables.
All 256 masks are checked using recorded NO completions, with the <=6 condition;
mask 127 fixes seven positions and its completions are exactly [0,128] in Low.
Eight checked YES/NO edges force all eight raw inputs of every valid separator
to be essential. The arbitrary-DAG support lemma and resulting >=7 binary-gate
bound are external, supplied by the parent. No attainable size or exact outer
minimum is asserted here. No real-valued analysis is formalized.
-/

namespace AtlasWitness
set_option debug.skipKernelTC false
set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

/-- Explicit bounded Boolean bit operations avoid an extra library axiom dependency. -/
def bitwise : Nat → (Bool → Bool → Bool) → Nat → Nat → Nat
  | 0 => fun _ _ _ => 0
  | n + 1 => fun op a b =>
      (if op (a % 2 == 1) (b % 2 == 1) then 1 else 0) +
        2 * bitwise n op (a / 2) (b / 2)

def and8 (a b : Nat) : Nat := bitwise 8 Bool.and a b
def or8 (a b : Nat) : Nat := bitwise 8 Bool.or a b
def xor8 (a b : Nat) : Nat := bitwise 8 Bool.xor a b

def initial : List Nat := [0, 255, 170, 204, 240]

/-- Total lookup, used only on in-range wires in the finite checks. -/
def lookup : List Nat → Nat → Nat
  | [] => fun _ => 0
  | x :: xs => fun index => match index with
      | 0 => x
      | i + 1 => lookup xs i

def gateValue (k code : Nat) (wires : List Nat) : Nat :=
  if code < k then 255 - lookup wires code
  else if code < k + k * k then
    and8 (lookup wires ((code - k) / k)) (lookup wires ((code - k) % k))
  else
    or8 (lookup wires ((code - k - k * k) / k))
      (lookup wires ((code - k - k * k) % k))

def paddedValues (first second : Nat) : List Nat :=
  let g1 := gateValue 5 first initial
  let g2 := gateValue 6 second [0, 255, 170, 204, 240, g1]
  [0, 255, 170, 204, 240, g1, g2]

structure Code where
  first : Nat
  second : Nat
  output : Nat

def validCode (c : Code) : Bool :=
  decide (c.first < 55) && decide (c.second < 78) && decide (c.output < 7)
def output (c : Code) : Nat := lookup (paddedValues c.first c.second) c.output

def lowTables : List Nat := [
  0, 3, 5, 10, 12, 15, 17, 34, 48, 51,
  63, 68, 80, 85, 95, 119, 128, 136, 160, 168,
  170, 175, 187, 192, 200, 204, 207, 221, 224, 234,
  236, 238, 240, 243, 245, 248, 250, 252, 254, 255]

def lowBitmap : Nat := 96415657254914957901423304087409861422800801310844973125464174589087425139753
def inLow (t : Nat) : Bool := decide (t < 256) && (lowBitmap / 2 ^ t % 2 == 1)

def lowWitnesses : List Code := [
  ⟨0, 0, 0⟩,
  ⟨49, 5, 6⟩,
  ⟨44, 5, 6⟩,
  ⟨4, 23, 6⟩,
  ⟨4, 29, 6⟩,
  ⟨4, 0, 5⟩,
  ⟨43, 5, 6⟩,
  ⟨3, 23, 6⟩,
  ⟨3, 35, 6⟩,
  ⟨3, 0, 5⟩,
  ⟨24, 5, 6⟩,
  ⟨2, 29, 6⟩,
  ⟨2, 35, 6⟩,
  ⟨2, 0, 5⟩,
  ⟨19, 5, 6⟩,
  ⟨18, 5, 6⟩,
  ⟨18, 35, 6⟩,
  ⟨18, 0, 5⟩,
  ⟨19, 0, 5⟩,
  ⟨49, 23, 6⟩,
  ⟨0, 0, 2⟩,
  ⟨4, 59, 6⟩,
  ⟨3, 59, 6⟩,
  ⟨24, 0, 5⟩,
  ⟨44, 29, 6⟩,
  ⟨0, 0, 3⟩,
  ⟨4, 65, 6⟩,
  ⟨2, 65, 6⟩,
  ⟨43, 35, 6⟩,
  ⟨24, 59, 6⟩,
  ⟨19, 65, 6⟩,
  ⟨43, 0, 5⟩,
  ⟨0, 0, 4⟩,
  ⟨3, 71, 6⟩,
  ⟨2, 71, 6⟩,
  ⟨18, 71, 6⟩,
  ⟨44, 0, 5⟩,
  ⟨49, 0, 5⟩,
  ⟨43, 71, 6⟩,
  ⟨0, 0, 1⟩]

/-- Exactly the 55 by 78 code pairs, with every one of their seven outputs. -/
def allPaddedOutputsInLow : Bool :=
  (List.range 55).all fun first =>
    (List.range 78).all fun second => (paddedValues first second).all inLow

def noDuplicates : List Nat → Bool
  | [] => true
  | t :: ts => !(ts.contains t) && noDuplicates ts

def popcount : Nat → Nat → Nat
  | 0 => fun _ => 0
  | n + 1 => fun value => value % 2 + popcount n (value / 2)

def zeroNOCompletions : List Nat := [
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 16,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 32,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 16,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 64,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 16,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 32,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 16,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 0,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 16,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 32,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 16,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 64,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 16,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 32,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 16,
  1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 0]

/-- Witness at each mask is explicit data, not existential search in the proof. -/
def smallZeroMaskChecks : Bool :=
  (List.range 256).all fun mask =>
    if popcount 8 mask ≤ 6 then
      let t := lookup zeroNOCompletions mask
      decide (t < 256) && (and8 mask t == 0) && !(inLow t)
    else true

def zeroCompletions (mask : Nat) : List Nat :=
  (List.range 256).filter fun t => and8 mask t == 0

structure PromiseEdge where
  coordinate : Nat
  yesTable : Nat
  noTable : Nat
  yesInitialWire : Nat

def promiseEdges : List PromiseEdge := [
  ⟨0, 0, 1, 0⟩,
  ⟨1, 0, 2, 0⟩,
  ⟨2, 0, 4, 0⟩,
  ⟨3, 0, 8, 0⟩,
  ⟨4, 0, 16, 0⟩,
  ⟨5, 0, 32, 0⟩,
  ⟨6, 0, 64, 0⟩,
  ⟨7, 255, 127, 1⟩]

/-- Each YES endpoint is an initial wire, hence a zero-gate YES witness. -/
def edgeChecks : Bool := promiseEdges.all fun e =>
  decide (e.coordinate < 8) && decide (e.yesInitialWire < 5) &&
  (lookup initial e.yesInitialWire == e.yesTable) &&
  (xor8 e.yesTable e.noTable == 2 ^ e.coordinate) &&
  decide (e.noTable < 256) && !(inLow e.noTable)

theorem first_gate_choice_count : (5 : Nat) + 2 * 5 * 5 = 55 := by decide
theorem second_gate_choice_count : (6 : Nat) + 2 * 6 * 6 = 78 := by decide
theorem padded_output_count : (55 : Nat) * 78 * 7 = 30030 := by decide
theorem paddedValues_length (first second : Nat) :
    (paddedValues first second).length = 7 := rfl

theorem low_length : lowTables.length = 40 := by decide
theorem low_distinct : noDuplicates lowTables = true := by decide
theorem low_bitmap_exact : (List.range 256).filter inLow = lowTables := by decide
theorem every_padded_output_in_low : allPaddedOutputsInLow = true := by decide

theorem low_witness_codes_valid : lowWitnesses.all validCode = true := by decide
theorem low_witnesses_exact : lowWitnesses.map output = lowTables := by decide

theorem zero_no_witness_count : zeroNOCompletions.length = 256 := by decide
theorem all_small_zero_masks_have_recorded_NO_completion : smallZeroMaskChecks = true := by decide
theorem mask127_fixed_count : popcount 8 127 = 7 := by decide
theorem mask127_completions : zeroCompletions 127 = [0, 128] := by decide
theorem mask127_is_low_compatible : (zeroCompletions 127).all inLow = true := by decide

theorem all_eight_coordinates : promiseEdges.map PromiseEdge.coordinate = List.range 8 := by decide
theorem all_eight_promise_edges_valid : edgeChecks = true := by decide

theorem atlas_finite_certificate :
    allPaddedOutputsInLow = true ∧
    lowWitnesses.all validCode = true ∧ lowWitnesses.map output = lowTables ∧
    smallZeroMaskChecks = true ∧ zeroCompletions 127 = [0, 128] ∧
    (zeroCompletions 127).all inLow = true ∧ edgeChecks = true :=
  ⟨every_padded_output_in_low, low_witness_codes_valid, low_witnesses_exact,
    all_small_zero_masks_have_recorded_NO_completion, mask127_completions,
    mask127_is_low_compatible, all_eight_promise_edges_valid⟩

#print axioms first_gate_choice_count
#print axioms second_gate_choice_count
#print axioms padded_output_count
#print axioms paddedValues_length
#print axioms low_length
#print axioms low_distinct
#print axioms low_bitmap_exact
#print axioms every_padded_output_in_low
#print axioms low_witness_codes_valid
#print axioms low_witnesses_exact
#print axioms zero_no_witness_count
#print axioms all_small_zero_masks_have_recorded_NO_completion
#print axioms mask127_fixed_count
#print axioms mask127_completions
#print axioms mask127_is_low_compatible
#print axioms all_eight_coordinates
#print axioms all_eight_promise_edges_valid
#print axioms atlas_finite_certificate

end AtlasWitness
