# Source ledger and analytic dependencies

**Inspected October 9, 2026.** The only imported analytic inequality is the standard event chessboard theorem. Hölder transfer, output domination, the counterexamples, and the cell-interaction estimates are derived in [the proof](weighted_boundary.tex). The primary PDFs were inspected through temporary local copies; they are not bundled into this dossier.

## Standard chessboard estimate

Marek Biskup and Roman Kotecký, *Forbidden gap argument for phase transitions proved by means of chessboard estimates*, Communications in Mathematical Physics **264** (2006), 631–656, arXiv `math-ph/0505011`.

Inspected the author manuscript, §2.2, Definition 2.2 and Theorem 2.4, equation (2.10), pages 4–5. The authors allow a reflection involution respecting support and use closed blocks with distinct placements. This pass retains the power-of-two factor-torus restriction. The link-variable application checks the needed reflection algebras explicitly instead of treating links at their tails as independent site spins.

```text
https://www.cts.cuni.cz/~kotecky/publ/BK-CMP06.pdf
```

## Designated reflections and shared block faces

Marek Biskup, *Reflection Positivity and Phase Transitions in Lattice Spin Models*, author lecture notes.

Inspected §5.1 for reflection positivity and the Cauchy–Schwarz consequence, and §5.3, Definition 5.7 and Theorem 5.8, equations (5.34)–(5.35), pages 43–46. The theorem states positivity for the reflections between neighboring blocks; the blocks share boundary sites. This is used to clarify the geometrically encoded edge-algebra application. Only the event version is used; the moment estimate is derived by layer-cake integration.

```text
https://www.math.ucla.edu/~biskup/PDFs/papers/Biskup-Prague-notes.pdf
```

These sources do not certify the Wilson-specific cell perturbation class, its quantitative constants, or an RG closure assertion. Those are local derivations with the stated scope.

## Local dependencies and comparison target

- [Second-pass proof](../rough_region/rough_region_replacement.tex): the robust frustrated boundary, Haar cap, minimizer Hessian bound, and distinction between output-weighted integrals and probabilities.
- [Third-pass proof](../boundary_cost/boundary_cost.tex): raw energy moments, actual-component counts, and the uniform sublevel kernel. The [audit](audit_third_pass.md) records the exact unchanged source hash.
- Supplied Family 215 O(3) manuscript, `preprints/The-canonical-massive-continuum-limit-of-the-two-dimensional-O3-model-October-4-2026/build/sections/comparison.tex`, lines 1–92 and 467–507: the actual comparison requires a positive complete endpoint density, mandatory inventories, signed or complex covering activities, and an output-evaluated complete covering factor. Those requirements are read as a target, not imported as gauge-theory estimates.

No older reported plaquette-concentration theorem, continuum theorem, or independent literature novelty assessment is required for this pass. The existing notes' caveats about external expert acceptance and continuum reconstruction remain in force.
