# Route panel (third workflow) — plan

Launch after `pvsnp-repo-audit` and `pvsnp-literature-dossiers` finish; feed both
results in via `args`.

## Advocates (one agent each, independent)

Each writes the strongest honest case that its route is the most plausible path to
resolving P vs NP within ~20 years. It must give a concrete milestone ladder (what to
prove next, then after that), say how the route evades or must evade each known
barrier, name the single hardest step, and say what the 2026 OpenAI results contribute.

1. Algorithmic method (Williams): faster SAT/derandomization for richer circuit
   classes ⇒ NEXP/NQP lower bounds ⇒ … ⇒ NP ⊄ P/poly.
2. Algebraic first: VP ≠ VNP (via constant-depth/chasm, GCT multiplicity
   obstructions, or IPS) and then transfer to the Boolean world (what transfer is
   even known? — Bürgisser, GRH).
3. Proof complexity: superpolynomial lower bounds for Frege/EF ⇒ NP ≠ coNP route;
   lifting and the IPS bridge.
4. Meta-complexity / hardness magnification: tiny lower bounds for MCSP-type problems
   magnify to NP ⊄ P/poly; must beat the locality barrier.
5. Formula lower bounds via KRW / composition ⇒ P ⊄ NC¹ (not P ≠ NP, but the
   recognized next big Boolean milestone) — and how it extends.
6. Descriptive complexity: no logic captures P ⇒ P ≠ NP. Assess honestly whether it
   is a stepping stone or a strictly harder target.
7. The P = NP direction: what a credible algorithmic resolution would look like and
   what currently known evidence (barriers to lower bounds, galactic algorithms,
   Subset Sum 2^{0.49n}, ω ≤ 9/4) says about it.
8. Independence / unprovability: what it would mean for P vs NP to be independent of
   strong theories, and what results exist (Razborov's bounded-arithmetic work, Pich–Santhanam).

## Judges (3 lenses, each scoring every route)

- Barrier lens: does the route have a credible story against relativization, natural
  proofs, algebrization, locality, and rank/GCT no-go results?
- Track-record lens: has the route produced unconditional progress in the last 15
  years, including the 2026 results — and is that progress compounding?
- Formalization/AI-leverage lens: how much would large-scale AI search plus Lean
  verification accelerate this route (e.g., the release's 40K-line proofs), and where
  is human insight still the bottleneck?

## Synthesis

Ranked routes, the minimal milestone ladder, the honest odds, and what an AI-heavy
research program should actually attempt next (concrete theorems, not slogans).
