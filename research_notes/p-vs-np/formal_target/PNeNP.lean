import Mathlib

/-!
# A Comparator-style target statement for P ≠ NP

The definitions follow the trusted challenge files already used by the OpenAI
math release (`ComparatorChallenges/KMedianThreshold.lean` and
`ComparatorChallenges/BinPackingGap.lean`): languages over `List Bool`,
deterministic polynomial-time computation by Mathlib's bundled multi-stack
machines `Turing.FinTM2` with every stack alphabet finite, and NP via
polynomially bounded certificates checked by such a machine.

Nothing below is proved except sanity lemmas about the definitions. The two
target theorems end in `sorry`: a resolution of P vs NP in this model is a
proof of exactly one of them, with only `propext`, `Quot.sound` and
`Classical.choice` as axioms.
-/

namespace PvsNP

abbrev Word := List Bool
abbrev Language := Set Word

/-- Self-delimiting: the bit-length in unary, a separator, then the binary
digits (least significant first). Unlike Mathlib's root `encodeNat`, a prefix
encoded this way can be parsed off a longer word. -/
def encodeNat (n : ℕ) : Word :=
  List.replicate n.bits.length true ++ [false] ++ n.bits

def encodeBit (b : Bool) : Word := [b]

/-- An input together with a certificate, framed by the input's length. -/
def encodePair (x : Word × Word) : Word :=
  encodeNat x.1.length ++ x.1 ++ x.2

/-- Polynomial-time computable with every physical stack alphabet finite.
Without the finiteness clause a single stack symbol could carry unbounded
information. -/
def FinitePolyTime {α β : Type} (ea : α → Word) (eb : β → Word) (f : α → β) : Prop :=
  ∃ M : Turing.TM2ComputableInPolyTime ea eb f, ∀ k : M.tm.K, Finite (M.tm.Γ k)

def P : Set Language :=
  {L | ∃ decide : Word → Bool,
    FinitePolyTime id encodeBit decide ∧ ∀ x, decide x = true ↔ x ∈ L}

def NP : Set Language :=
  {L | ∃ (verify : Word × Word → Bool) (bound : Polynomial ℕ),
    FinitePolyTime encodePair encodeBit verify ∧
    ∀ x, x ∈ L ↔ ∃ w : Word, w.length ≤ bound.eval x.length ∧ verify (x, w) = true}

/-! ## Sanity checks on the definitions -/

theorem bits_injective : Function.Injective Nat.bits := by
  intro m n h
  apply Nat.eq_of_testBit_eq
  intro i
  rw [Nat.testBit_eq_inth, Nat.testBit_eq_inth, h]

/-- A unary run of `true`s terminated by `false` is a self-delimiting prefix. -/
theorem replicate_false_append_inj :
    ∀ {a b : ℕ} {u v : Word},
      List.replicate a true ++ false :: u = List.replicate b true ++ false :: v →
        a = b ∧ u = v
  | 0, 0, u, v, h => by simpa using h
  | 0, b + 1, u, v, h => by simp [List.replicate_succ] at h
  | a + 1, 0, u, v, h => by simp [List.replicate_succ] at h
  | a + 1, b + 1, u, v, h => by
      simp only [List.replicate_succ, List.cons_append, List.cons.injEq, true_and] at h
      obtain ⟨hab, huv⟩ := replicate_false_append_inj h
      exact ⟨by omega, huv⟩

/-- The length prefix really is self-delimiting: equal framings force equal
numbers and equal remainders. -/
theorem encodeNat_append_injective {m n : ℕ} {u v : Word}
    (h : encodeNat m ++ u = encodeNat n ++ v) : m = n ∧ u = v := by
  simp only [encodeNat, List.append_assoc, List.cons_append, List.nil_append] at h
  obtain ⟨hlen, hrest⟩ := replicate_false_append_inj h
  obtain ⟨hbits, huv⟩ := List.append_inj (s₁ := m.bits) (s₂ := n.bits) hrest hlen
  exact ⟨bits_injective hbits, huv⟩

/-- An input and certificate are recoverable from their framing, so a verifier
sees exactly the pair it is asked about. -/
theorem encodePair_injective : Function.Injective encodePair := by
  rintro ⟨x, w⟩ ⟨y, z⟩ h
  simp only [encodePair, List.append_assoc] at h
  obtain ⟨hlen, hrest⟩ := encodeNat_append_injective h
  obtain ⟨hxy, hwz⟩ := List.append_inj hrest hlen
  simp [hxy, hwz]


/-! ## Non-vacuity: an explicit polynomial-time machine

`rejectAll` uses one stack for input and output. It pops until the stack is
empty, then pushes `false` and halts with its state reset, which is what
`Turing.haltList` demands. It runs in `|x| + 1` steps. -/

section NonVacuity

open Turing Turing.TM2 Turing.TM2.Stmt StateTransition


/-- One stack, shared by input and output. The single label pops until the
stack is empty, then pushes `false` and halts with the state reset. -/
def rejectAll : FinTM2 where
  K := Unit
  k₀ := ()
  k₁ := ()
  Γ _ := Bool
  Λ := Unit
  main := ()
  σ := Bool
  initialState := false
  m _ :=
    pop () (fun _ top => top.isSome)
      (branch id
        (load (fun _ => false) (goto fun _ => ()))
        (push () (fun _ => false) halt))

/-- Configurations of `rejectAll`, written with its own index types. -/
def cfg (running : Bool) (l : List Bool) : rejectAll.Cfg :=
  ⟨if running then some (() : rejectAll.Λ) else none, (false : rejectAll.σ),
    fun _ => (l : List (rejectAll.Γ ()))⟩

theorem step_cons (b : Bool) (l : List Bool) :
    rejectAll.step (cfg true (b :: l)) = some (cfg true l) := by
  simp [rejectAll, cfg, FinTM2.step, TM2.step, TM2.stepAux, Function.update]
  rfl

theorem step_nil : rejectAll.step (cfg true []) = some (cfg false [false]) := by
  simp [rejectAll, cfg, FinTM2.step, TM2.step, TM2.stepAux, Function.update]
  rfl

/-- Iterating the machine empties the stack one symbol per step. -/
theorem iterate_drain (l : List Bool) :
    (flip bind rejectAll.step)^[l.length] (some (cfg true l)) = some (cfg true []) := by
  induction l with
  | nil => rfl
  | cons b l ih =>
    rw [List.length_cons, Function.iterate_succ_apply]
    have h : flip bind rejectAll.step (some (cfg true (b :: l))) = some (cfg true l) :=
      step_cons b l
    rw [h, ih]

theorem initList_eq (l : List Bool) : initList rejectAll l = cfg true l := by
  simp [initList, rejectAll, cfg]
  rfl

theorem haltList_false : haltList rejectAll [false] = cfg false [false] := by
  simp [haltList, rejectAll, cfg]
  rfl

/-- `rejectAll` outputs `[false]` on every input, within `|x| + 1` steps. -/
def outputs (l : List Bool) :
    TM2OutputsInTime rejectAll l (some [false]) (l.length + 1) := by
  refine ⟨⟨l.length + 1, ?_⟩, le_refl _⟩
  rw [initList_eq, Option.map_some, haltList_false, Function.iterate_succ_apply',
    iterate_drain]
  exact step_nil

/-- The constant-false decider is polynomial-time computable. -/
noncomputable def rejectAllComputable :
    TM2ComputableInPolyTime (id : List Bool → List Bool) (fun b : Bool => [b])
      (fun _ => false) where
  tm := rejectAll
  inputAlphabet := Equiv.refl Bool
  outputAlphabet := Equiv.refl Bool
  time := Polynomial.X + 1
  outputsFun l := by
    have h : (Polynomial.X + 1 : Polynomial ℕ).eval (id l).length = l.length + 1 := by simp
    rw [h]
    have e : List.map (Equiv.refl Bool).invFun (id l) = l := List.map_id l
    have key := outputs l
    refine ⟨⟨key.steps, ?_⟩, key.steps_le_m⟩
    have k2 := key.evals_in_steps
    have mapId : ∀ w : List Bool,
        List.map (show rejectAll.Γ rejectAll.k₀ ≃ Bool from Equiv.refl Bool).invFun w = w := by
      intro w
      induction w with
      | nil => rfl
      | cons a w ih => exact congrArg (List.cons a) ih
    have mapId' : ∀ w : List Bool,
        List.map (show rejectAll.Γ rejectAll.k₁ ≃ Bool from Equiv.refl Bool).invFun w = w := by
      intro w
      induction w with
      | nil => rfl
      | cons a w ih => exact congrArg (List.cons a) ih
    convert k2 using 3
    · exact congrArg (initList rejectAll) (mapId (id l))
    · exact mapId' [false]


theorem empty_mem_P : (∅ : Language) ∈ P :=
  ⟨fun _ => false, ⟨rejectAllComputable, fun _ => inferInstanceAs (Finite Bool)⟩,
    fun x => by simp⟩

/-- The same machine, read as a verifier on framed pairs, rejects every
certificate. -/
noncomputable def rejectAllVerifier :
    TM2ComputableInPolyTime encodePair encodeBit (fun _ : Word × Word => false) where
  toTM2ComputableAux := rejectAllComputable.toTM2ComputableAux
  time := rejectAllComputable.time
  outputsFun xw := rejectAllComputable.outputsFun (encodePair xw)

theorem empty_mem_NP : (∅ : Language) ∈ NP :=
  ⟨fun _ => false, 0, ⟨rejectAllVerifier, fun _ => inferInstanceAs (Finite Bool)⟩,
    fun x => by simp⟩

end NonVacuity

/-! ## P ⊆ NP

`stripTM` wraps a polynomial-time decider `D` with a two-label prelude that
consumes the `encodeNat |x|` header (unary bit-length, separator, then that many
digits) using a fresh unit counter stack, and then runs `D` unchanged. With
certificate bound `0` the only admissible certificate is `[]`, so the verifier
`fun (x, w) => d (x ++ w)` decides exactly `L`. -/

section PSubsetNP

open Turing StateTransition

variable (D : FinTM2)

/-- Stack alphabets of the wrapper: `none` is a fresh unary counter stack,
`some k` is stack `k` of the wrapped machine. -/
abbrev StripΓ : Option D.K → Type
  | none => Unit
  | some k => D.Γ k

/-- Statements of `D`, run inside the wrapper. The extra scratch bit is untouched. -/
def stripTr : TM2.Stmt D.Γ D.Λ D.σ → TM2.Stmt (StripΓ D) (Bool ⊕ D.Λ) (D.σ × Bool)
  | .push k f q => .push (some k) (fun s => f s.1) (stripTr q)
  | .peek k f q => .peek (some k) (fun s a => (f s.1 a, s.2)) (stripTr q)
  | .pop k f q => .pop (some k) (fun s a => (f s.1 a, s.2)) (stripTr q)
  | .load f q => .load (fun s => (f s.1, s.2)) (stripTr q)
  | .branch f q₁ q₂ => .branch (fun s => f s.1) (stripTr q₁) (stripTr q₂)
  | .goto f => .goto (fun s => .inr (f s.1))
  | .halt => .halt

/-- The wrapper program. Label `inl true` moves the leading `true`s of the input
to the counter stack and consumes the separating `false`. Label `inl false` drops
one input symbol per counter token. Control then passes to `D`'s main label. -/
def stripProg (e : D.Γ D.k₀ ≃ Bool) :
    Bool ⊕ D.Λ → TM2.Stmt (StripΓ D) (Bool ⊕ D.Λ) (D.σ × Bool)
  | .inl true =>
      .pop (some D.k₀) (fun s a => (s.1, a.elim false (fun g => e g)))
        (.branch (fun s => s.2)
          (.push none (fun _ => ()) (.load (fun s => (s.1, false)) (.goto fun _ => .inl true)))
          (.goto fun _ => .inl false))
  | .inl false =>
      .pop none (fun s a => (s.1, a.isSome))
        (.branch (fun s => s.2)
          (.pop (some D.k₀) (fun s _ => (s.1, false)) (.goto fun _ => .inl false))
          (.goto fun _ => .inr D.main))
  | .inr l => stripTr D (D.m l)

/-- The header-stripping wrapper around `D`. -/
def stripTM (e : D.Γ D.k₀ ≃ Bool) : FinTM2 where
  K := Option D.K
  kFin := by letI := D.kFin; infer_instance
  k₀ := some D.k₀
  k₁ := some D.k₁
  Γ := StripΓ D
  Λ := Bool ⊕ D.Λ
  main := .inl true
  ΛFin := by letI := D.ΛFin; infer_instance
  σ := D.σ × Bool
  initialState := (D.initialState, false)
  σFin := by letI := D.σFin; infer_instance
  Γk₀Fin := D.Γk₀Fin
  m := stripProg D e

variable {D}

/-- Stacks of the wrapper, from a counter stack and the stacks of `D`. -/
def combine (c : List Unit) (S : ∀ k, List (D.Γ k)) : ∀ k : Option D.K, List (StripΓ D k)
  | none => c
  | some k => S k

@[simp] theorem combine_none (c : List Unit) (S : ∀ k, List (D.Γ k)) :
    combine c S none = c := rfl

@[simp] theorem combine_some (c : List Unit) (S : ∀ k, List (D.Γ k)) (k : D.K) :
    combine c S (some k) = S k := rfl

theorem update_combine_some (c : List Unit) (S : ∀ k, List (D.Γ k)) (k : D.K)
    (v : List (D.Γ k)) :
    Function.update (combine c S) (some k) v = combine c (Function.update S k v) := by
  funext j
  cases j with
  | none => rfl
  | some j =>
    by_cases h : j = k
    · subst h
      rw [Function.update_self]
      show v = Function.update S j v j
      rw [Function.update_self]
    · rw [Function.update_of_ne (by simpa using h)]
      show S j = Function.update S k v j
      rw [Function.update_of_ne h]

theorem update_combine_none (c c' : List Unit) (S : ∀ k, List (D.Γ k)) :
    Function.update (combine c S) none c' = combine c' S := by
  funext j
  cases j with
  | none => simp only [Function.update_self]; rfl
  | some j => rw [Function.update_of_ne (by simp)]; rfl

/-- Configurations of `D`, viewed inside the wrapper. -/
def liftCfg (c : TM2.Cfg D.Γ D.Λ D.σ) : TM2.Cfg (StripΓ D) (Bool ⊕ D.Λ) (D.σ × Bool) :=
  ⟨c.l.map Sum.inr, (c.var, false), combine [] c.stk⟩

theorem stepAux_stripTr (q : TM2.Stmt D.Γ D.Λ D.σ) (v : D.σ) (S : ∀ k, List (D.Γ k)) :
    TM2.stepAux (stripTr D q) (v, false) (combine [] S) = liftCfg (TM2.stepAux q v S) := by
  induction q generalizing v S with
  | push k f q ih =>
    simp only [stripTr, TM2.stepAux]
    rw [← ih]
    congr 1
    exact update_combine_some _ _ _ _
  | peek k f q ih =>
    simp only [stripTr, TM2.stepAux]
    exact ih _ _
  | pop k f q ih =>
    simp only [stripTr, TM2.stepAux]
    rw [← ih]
    congr 1
    exact update_combine_some _ _ _ _
  | load f q ih =>
    simp only [stripTr, TM2.stepAux]
    exact ih _ _
  | branch f q₁ q₂ ih₁ ih₂ =>
    simp only [stripTr, TM2.stepAux]
    cases f v
    · exact ih₂ _ _
    · exact ih₁ _ _
  | goto f => rfl
  | halt => rfl

variable (e : D.Γ D.k₀ ≃ Bool)

theorem step_lift (c : TM2.Cfg D.Γ D.Λ D.σ) :
    TM2.step (stripProg D e) (liftCfg c) = (TM2.step D.m c).map liftCfg := by
  rcases c with ⟨_ | l, v, S⟩
  · rfl
  · show some (TM2.stepAux (stripTr D (D.m l)) (v, false) (combine [] S)) =
      some (liftCfg (TM2.stepAux (D.m l) v S))
    rw [stepAux_stripTr]

theorem iterate_lift (n : ℕ) (c : TM2.Cfg D.Γ D.Λ D.σ) :
    (flip bind (TM2.step (stripProg D e)))^[n] (some (liftCfg c)) =
      ((flip bind (TM2.step D.m))^[n] (some c)).map liftCfg := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [Function.iterate_succ_apply', Function.iterate_succ_apply', ih]
    cases (flip bind (TM2.step D.m))^[n] (some c) with
    | none => rfl
    | some c' => exact step_lift e c'

/-! ### The header phase -/

theorem initStk_k₀ (l : List (D.Γ D.k₀)) : (initList D l).stk D.k₀ = l := by
  simp [initList]

theorem update_initStk (l l' : List (D.Γ D.k₀)) :
    Function.update (initList D l).stk D.k₀ l' = (initList D l').stk := by
  funext j
  by_cases h : j = D.k₀
  · subst h
    rw [Function.update_self, initStk_k₀]
  · rw [Function.update_of_ne h]
    simp [initList, h]

/-- Header-phase configurations: label `inl lbl`, counter `c`, input stack `l`. -/
def hdr (lbl : Bool) (c : List Unit) (l : List (D.Γ D.k₀)) :
    TM2.Cfg (StripΓ D) (Bool ⊕ D.Λ) (D.σ × Bool) :=
  ⟨some (.inl lbl), (D.initialState, false), combine c (initList D l).stk⟩

theorem count_step (g : D.Γ D.k₀) (hg : e g = true) (c : List Unit) (l : List (D.Γ D.k₀)) :
    TM2.step (stripProg D e) (hdr true c (g :: l)) = some (hdr true (() :: c) l) := by
  show some (TM2.stepAux (stripProg D e (.inl true)) (D.initialState, false)
    (combine c (initList D (g :: l)).stk)) = _
  simp only [stripProg, TM2.stepAux, update_combine_some, combine_some, initStk_k₀,
    List.head?_cons, List.tail_cons, Option.elim, hg, Bool.cond_true, update_initStk,
    update_combine_none, combine_none]
  rfl

theorem count_end (g : D.Γ D.k₀) (hg : e g = false) (c : List Unit) (l : List (D.Γ D.k₀)) :
    TM2.step (stripProg D e) (hdr true c (g :: l)) = some (hdr false c l) := by
  show some (TM2.stepAux (stripProg D e (.inl true)) (D.initialState, false)
    (combine c (initList D (g :: l)).stk)) = _
  simp only [stripProg, TM2.stepAux, update_combine_some, combine_some, initStk_k₀,
    List.head?_cons, List.tail_cons, Option.elim, hg, Bool.cond_false, update_initStk]
  rfl

theorem skip_step (c : List Unit) (g : D.Γ D.k₀) (l : List (D.Γ D.k₀)) :
    TM2.step (stripProg D e) (hdr false (() :: c) (g :: l)) = some (hdr false c l) := by
  show some (TM2.stepAux (stripProg D e (.inl false)) (D.initialState, false)
    (combine (() :: c) (initList D (g :: l)).stk)) = _
  simp only [stripProg, TM2.stepAux, update_combine_none, combine_none, combine_some,
    List.head?_cons, List.tail_cons, Option.isSome_some, Bool.cond_true, update_combine_some,
    initStk_k₀, update_initStk]
  rfl

theorem skip_end (l : List (D.Γ D.k₀)) :
    TM2.step (stripProg D e) (hdr false [] l) = some (liftCfg (initList D l)) := by
  show some (TM2.stepAux (stripProg D e (.inl false)) (D.initialState, false)
    (combine [] (initList D l).stk)) = _
  simp only [stripProg, TM2.stepAux, update_combine_none, combine_none,
    List.head?_nil, List.tail_nil, Option.isSome_none, Bool.cond_false]
  rfl

/-- Phase 1: count the unary run onto the counter stack and drop the separator. -/
theorem count_trace (n m : ℕ) (rest : List (D.Γ D.k₀)) :
    (flip bind (TM2.step (stripProg D e)))^[n + 1]
        (some (hdr true (List.replicate m ()) ((List.replicate n true).map e.symm ++
          e.symm false :: rest))) =
      some (hdr false (List.replicate (n + m) ()) rest) := by
  induction n generalizing m with
  | zero =>
    simp only [Nat.zero_add, List.replicate_zero, List.map_nil, List.nil_append]
    exact count_end e (e.symm false) (by simp) (List.replicate m ()) rest
  | succ n ih =>
    rw [Function.iterate_succ_apply]
    have h1 : flip bind (TM2.step (stripProg D e))
        (some (hdr true (List.replicate m ()) ((List.replicate (n + 1) true).map e.symm ++
          e.symm false :: rest))) =
        some (hdr true (List.replicate (m + 1) ()) ((List.replicate n true).map e.symm ++
          e.symm false :: rest)) :=
      count_step e (e.symm true) (by simp) _ _
    rw [h1, ih (m + 1), Nat.add_right_comm, Nat.add_assoc]

/-- Phase 2: drop one input symbol per counter token, then enter `D`. -/
theorem skip_trace (l rest : List (D.Γ D.k₀)) :
    (flip bind (TM2.step (stripProg D e)))^[l.length + 1]
        (some (hdr false (List.replicate l.length ()) (l ++ rest))) =
      some (liftCfg (initList D rest)) := by
  induction l with
  | nil => exact skip_end e rest
  | cons g l ih =>
    rw [List.length_cons, Function.iterate_succ_apply]
    have h1 : flip bind (TM2.step (stripProg D e))
        (some (hdr false (List.replicate (l.length + 1) ()) (g :: l ++ rest))) =
        some (hdr false (List.replicate l.length ()) (l ++ rest)) :=
      skip_step e _ g (l ++ rest)
    rw [h1, ih]

theorem initList_stripTM (l : List (D.Γ D.k₀)) :
    initList (stripTM D e) l = hdr true [] l := by
  unfold initList hdr
  congr 1
  funext k
  cases k with
  | none => simp [stripTM]
  | some j =>
    by_cases h : j = D.k₀
    · subst h
      simp [stripTM, initList]
      rfl
    · simp [stripTM, initList, h]

theorem haltList_stripTM (l : List (D.Γ D.k₁)) :
    haltList (stripTM D e) l = liftCfg (haltList D l) := by
  unfold haltList liftCfg
  congr 1
  funext k
  cases k with
  | none => simp [stripTM]
  | some j =>
    by_cases h : j = D.k₁
    · subst h
      simp [stripTM]
      rfl
    · simp [stripTM, h]

theorem map_encodePair (x w : Word) :
    (encodePair (x, w)).map e.symm =
      (List.replicate x.length.bits.length true).map e.symm ++ e.symm false ::
        (x.length.bits.map e.symm ++ (x ++ w).map e.symm) := by
  simp [encodePair, encodeNat, List.map_append, List.append_assoc]

/-- Phases 1 and 2 together: the header `encodeNat x.length` is consumed in
`2 * (b + 1)` steps, leaving `D`'s initial configuration on `x ++ w`. -/
theorem strip_header (x w : Word) :
    (flip bind (TM2.step (stripProg D e)))^[(x.length.bits.length + 1) +
        (x.length.bits.length + 1)]
      (some (hdr true [] ((encodePair (x, w)).map e.symm))) =
      some (liftCfg (initList D ((x ++ w).map e.symm))) := by
  rw [Function.iterate_add_apply, map_encodePair]
  have h1 := count_trace e x.length.bits.length 0
    (x.length.bits.map e.symm ++ (x ++ w).map e.symm)
  simp only [List.replicate_zero, Nat.add_zero] at h1
  rw [h1]
  have h2 := skip_trace e (x.length.bits.map e.symm) ((x ++ w).map e.symm)
  simp only [List.length_map] at h2
  exact h2

/-- The wrapper on `encodePair (x, w)` produces what `D` produces on `x ++ w`. -/
def stripOutputs (x w : Word) {out : List (D.Γ D.k₁)} {m : ℕ}
    (h : TM2OutputsInTime D ((x ++ w).map e.symm) (some out) m) :
    TM2OutputsInTime (stripTM D e) ((encodePair (x, w)).map e.symm) (some out)
      (m + ((x.length.bits.length + 1) + (x.length.bits.length + 1))) := by
  obtain ⟨⟨n, hD⟩, hn⟩ := h
  replace hn : n ≤ m := hn
  replace hD : (flip bind (TM2.step D.m))^[n] (some (initList D ((x ++ w).map e.symm))) =
      some (haltList D out) := hD
  refine ⟨⟨n + ((x.length.bits.length + 1) + (x.length.bits.length + 1)), ?_⟩, ?_⟩
  · have h1 := congrArg (fun c => (flip bind (TM2.step (stripProg D e)))^[n] c)
      (strip_header e x w)
    have h2 := iterate_lift e n (initList D ((x ++ w).map e.symm))
    rw [hD] at h2
    have h3 := haltList_stripTM e out
    have h4 := initList_stripTM e ((encodePair (x, w)).map e.symm)
    refine (Function.iterate_add_apply _ _ _ _).trans ?_
    refine (congrArg (fun c => (flip bind (TM2.step (stripProg D e)))^[n]
      ((flip bind (TM2.step (stripProg D e)))^[(x.length.bits.length + 1) +
        (x.length.bits.length + 1)] (some c))) h4).trans ?_
    refine h1.trans (h2.trans ?_)
    exact congrArg some h3.symm
  · show n + _ ≤ _
    omega

end PSubsetNP

theorem poly_eval_mono (p : Polynomial ℕ) {a b : ℕ} (h : a ≤ b) : p.eval a ≤ p.eval b := by
  induction p using Polynomial.induction_on' with
  | add p q hp hq =>
    rw [Polynomial.eval_add, Polynomial.eval_add]
    exact Nat.add_le_add hp hq
  | monomial n c =>
    rw [Polynomial.eval_monomial, Polynomial.eval_monomial]
    exact Nat.mul_le_mul_left _ (Nat.pow_le_pow_left h n)

theorem encodePair_length (x w : Word) :
    (encodePair (x, w)).length =
      x.length.bits.length + 1 + x.length.bits.length + x.length + w.length := by
  simp only [encodePair, encodeNat, List.length_append, List.length_replicate,
    List.length_cons, List.length_nil]

open Turing in
/-- A decider for `L`, composed with header stripping, is a verifier on framed
pairs that ignores the frame. -/
noncomputable def stripComputable {d : Word → Bool}
    (M : TM2ComputableInPolyTime id encodeBit d) :
    TM2ComputableInPolyTime encodePair encodeBit
      (fun xw : Word × Word => d (xw.1 ++ xw.2)) where
  tm := stripTM M.tm M.inputAlphabet
  inputAlphabet := M.inputAlphabet
  outputAlphabet := M.outputAlphabet
  time := M.time + Polynomial.X + 1
  outputsFun := fun xw => by
    obtain ⟨x, w⟩ := xw
    have h := M.outputsFun (x ++ w)
    have run := stripOutputs M.inputAlphabet x w h
    refine ⟨run.toEvalsTo, run.steps_le_m.trans ?_⟩
    have hmono := poly_eval_mono M.time
      (show (x ++ w).length ≤ (encodePair (x, w)).length by
        rw [encodePair_length, List.length_append]; omega)
    have hlen := encodePair_length x w
    simp only [Polynomial.eval_add, Polynomial.eval_X, Polynomial.eval_one, id]
    omega

theorem P_subset_NP : P ⊆ NP := by
  rintro L ⟨d, ⟨M, hfin⟩, hd⟩
  refine ⟨fun xw => d (xw.1 ++ xw.2), 0, ⟨stripComputable M, ?_⟩, ?_⟩
  · intro k
    cases k with
    | none => exact inferInstanceAs (Finite Unit)
    | some k => exact hfin k
  · intro x
    constructor
    · intro hx
      exact ⟨[], by simp, by simpa using (hd x).mpr hx⟩
    · rintro ⟨w, hw, hv⟩
      have hw0 : w = [] := by simpa using hw
      subst hw0
      exact (hd x).mp (by simpa using hv)

/-! ## The two possible resolutions -/

theorem P_ne_NP : P ≠ NP := by
  sorry

theorem P_eq_NP : P = NP := by
  sorry

end PvsNP
