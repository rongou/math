# Sources and proof dependencies

**Inspected October 9, 2026.** The only imported analytic inequality is the standard event chessboard estimate. The Wilson-specific reflection, star geometry, moment conversion, sublevel replacement, and counting are derived in [the proof](boundary_cost.tex).

## Chessboard input

Marek Biskup and Roman Kotecký, *Forbidden gap argument for phase transitions proved by means of chessboard estimates*, Communications in Mathematical Physics **264** (2006), 631–656; arXiv `math-ph/0505011`.

Inspected the author manuscript, §2.2, Definition 2.2 and Theorem 2.4, equation (2.10), manuscript pages 4–5. The proof retains its power-of-two factor-torus restriction. The application to geometrically supported link variables checks the closed-half reflection algebras directly; it does not treat shared block-face links as independent.

```text
https://www.cts.cuni.cz/~kotecky/publ/BK-CMP06.pdf
```

The event form suffices: joint tails are converted to exponential moments by an explicit finite-product layer-cake argument. No functional chessboard strengthening is required.

## Earlier plaquette concentration context

O. Borisenko, S. Voloshin and M. Faber, *Plaquette representation for 3D lattice gauge models: I. Formulation and perturbation theory*, arXiv `hep-lat/0508003`.

Inspected §1.1, equation (4), manuscript page 3, and reference [20]. The authors report earlier volume-uniform plaquette concentration, citing G. Mack and V. Petkova, Annals of Physics **125** (1980), 117. This is context against any novelty inference. Neither that reported bound nor its constants are used, and the Mack–Petkova original was not inspected.

```text
https://arxiv.org/pdf/hep-lat/0508003
```

The cited paper concerns its own gauge-model formulation and perturbation program; it is not a certificate of the present four-dimensional argument or the continuum problem.

## Local proof dependencies

The [second-pass proof](../rough_region/rough_region_replacement.tex) supplies the elementary SU(2) energy identity, probability-Haar cap bound, minimizer-cap Hessian bound, and the exact one-link staple defect identity. The present note restates the necessary estimates and proves the kernel and integrated application.

No source supplies compatibility or reweighted rarity by assumption. The raw Wilson exceptional-label bound and the output-weighted replacement integral have different scopes. No external continuum or RG theorem is imported.
