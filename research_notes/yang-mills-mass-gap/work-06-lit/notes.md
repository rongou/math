# Working notes for dossier 06 (constructive YM literature)
Started 2026-10-09.

## Downloaded primary sources (work-06-lit/downloads-clay/)
- yangmills.pdf -> yangmills.txt  (Jaffe-Witten official description, 6pp... actually 14 pp of text; pdf says 6 pages? check)
  Formal statement: yangmills.txt:277-280. Existence text: :263-271. Mass gap def: :272-276. Footnote 1: :301-304.
  Footnote 2 (weak existence excluded): :618-620. Lattice/RP: :539-549. Balaban 3D: :550-563; 4D: :564-568.
  MRS & continuum reg: :572-573. "New ideas needed ... uniform in volume": :579-581. Perspective T^4: :322-335.
  Clustering eq (2): :283-297. Extensions: :298-311. Further remarks (duality, 1/N): :583-610.
  BFS 2D abelian Higgs "only complete example": :520-525.
- douglas2004.pdf -> douglas2004.txt (April 2004, 4 pages)
- rules.pdf -> rules.txt (Millennium Prize rules, dated 26 Sept 2018)
  yangmills.pdf actually has 14 pages (pdfinfo); created 2006 (MiKTeX). Book version: Carlson-Jaffe-Wiles (eds) The Millennium Prize Problems, CMI/AMS 2006, pp.129-152 (nLab; verify).
- Douglas 2004 report: dated April 2004 (douglas2004.txt:4). Key quotes :69-72 (no significant progress; state of art = Balaban + MRS), :76-83 (2D sigma models "Apparently, even these theories have not yet been constructed to the standards required"; Kopper CMP 202 (1999) 89 mass gap regulated O(N)).
- Douglas 2026: M.R. Douglas, "The Yang-Mills Millennium problem", Nat Rev Phys 8, 86-97 (2026), doi:10.1038/s42254-025-00909-2 (online ~Jan 2026). Paywalled. Cites Cao-Nissim-Sheffield 2505.16585, Ebel-Kennedy-Rychkov 2506.03247 (TRG + computer assistance), Marino 2504.12044.
- Rules PDF: dated 26 September 2018; sections 4 (criteria), 5 (proposed solutions; 5b P vs NP & NS either direction; 5c counterexamples for others), 6 (Qualifying Outlet), 7 (evaluation, 2 years, general acceptance), 8 (award).
- nLab lists: V.P. Nair, "Towards a Proof of Mass Gap in 3d Yang-Mills Theory", arXiv:2608.10133 (VERIFY). Hairer CMI talk Oct 2025; Chatterjee CMSA 15 Oct 2025.
- Search hits on claimed solutions: arXiv:2506.00284 (SU(3) constructive proof claim), preprints.org 202506.2484, 202504.1268 (incompatibility claim), 202506.2241, MDPI 2813-9542/2/1/2, zenodo 15338444, 8076499, Logan Nye book; Frasca blog 2010.
- arXiv:2510.22788 "U(N) lattice Yang-Mills in the 't Hooft regime"; arXiv:2605.16162 "Deconfinement for SO(3) lattice YM at strong coupling"; arXiv:2509.04688 "Dynamical approach to area law for lattice YM" (authors? verify)

## Balaban (verified via Crossref API, DOIs)
- (Higgs)_{2,3} quantum fields in a finite volume I-III: CMP 85 (1982) 603-626 [10.1007/bf01403506]; CMP 86 (1982) 555-594 [bf01214890]; CMP 88 (1983) 411-445 [bf01213217]
- Regularity and decay of lattice Green's functions, CMP 89 (1983) 571-597 [bf01214744]
- Propagators and renormalization transformations for lattice gauge theories I, CMP 95 (1984) 17-40 [bf01215753]; II, CMP 96 (1984) 223-250 [bf01240221]
- Averaging operations for lattice gauge theories, CMP 98 (1985) 17-51 [bf01211042]
- Spaces of regular gauge field configurations on a lattice and gauge fixing conditions, CMP 99 (1985) 75-102 [bf01466594]
- Propagators for lattice gauge theories in a background field, CMP 99 (1985) 389-434 [bf01240355]
- Ultraviolet stability of three-dimensional lattice pure gauge field theories, CMP 102 (1985) 255-275 [bf01229380]
- The variational problem and background fields in renormalization group method for lattice gauge theories, CMP 102 (1985) 277-309 [bf01229381]
- RG approach to lattice gauge field theories I. Generation of effective actions in a small field approximation and a coupling constant renormalization in four dimensions, CMP 109 (1987) 249-301 [bf01215223]
- RG approach to lattice gauge field theories II. Cluster expansions, CMP 116 (1988) 1-22 [bf01239022]
- Convergent renormalization expansions for lattice gauge theories, CMP 119 (1988) 243-285 [bf01217741]
- Large field renormalization I. The basic step of the R operation, CMP 122 (1989) 175-202 [bf01257412]
- Large field renormalization II. Localization, exponentiation, and bounds for the R operation, CMP 122 (1989) 355-392 [bf01238433]
  Received June 5 1987, revised June 10 1988; communicated by A. Jaffe.
  OBTAINED TEXT (downloads-balaban/lfr2.txt). Theorem 1 (p.355): "If the sequence of the effective coupling constants is contained in an interval ]0, γ] with a sufficiently small positive γ, then the effective densities ρ_k have the form, and satisfy all the conditions and bounds, described in Sect. 2 [III]."
  "This is the main result of the whole sequence of papers..." "Theorem 2 of [I] allows us to remove the assumption ... follows from the basic inequality (0.31) [II] ... The proof of Theorem 2, which is based on second order perturbative calculations, is very awkward and long ... and has not been published yet, so we have Theorem 1 with the assumption."
  Consequence (0.1): UV stability bounds "of the same type as for superrenormalizable models in [16]" with constants E_-, E_+ independent of k, T_eta, U_k.
  p.356: "Theorem 1 is the basis for many other applications, for example, for an analysis of expectation values of physical observables, like loop variables, averaged loop variables, etc. These problems are very important for construction of the four-dimensional gauge field theories, and they deserve detailed analysis and further publication. Another important direction ... matter fields, e.g. Fermi fields in QCD."
- Balaban-O'Carroll-Schor, Block renormalization group for Euclidean fermions, CMP 122 (1989) 233-247 [bf01257414]
- Balaban-Brydges-Imbrie-Jaffe, The mass gap for Higgs models on a unit lattice, Ann. Phys. 158 (1984) 281-319 [10.1016/0003-4916(84)90121-0]
- Balaban: Lecture Notes in Physics: The ultraviolet stability bounds for some lattice sigma-models and lattice Higgs-Kibble models (Math Problems in Theor Phys, LNP 116?, 1980) pp 237-240 [10.1007/3-540-09964-6_327]
- Balaban N-vector models: CMP 167 (1995) 103-154; 175 (1996) 607-642; 182 (1996) 33-82; 182 (1996) 675-721; 196 (1998) 485-521; 198 (1998) 493-534; 198 (1998) 1-45; Balaban-O'Carroll CMP 199 (1999) 493-520.
- RG I (CMP 109:249-301, 1987) OBTAINED (downloads-balaban/rg1.txt, page image rg1_p11-11.png = journal p.259):
  Theorem 1 (p.259): "If the sequence of the effective coupling constants is contained in an interval ]0,γ] with a sufficiently small positive γ, then the effective actions for small fields are given by the formulas (0.22)-(0.24), with terms satisfying (0.29)."
  "we do not assume any special asymptotic behavior of the coupling constants, like asymptotic freedom" ... proved for arbitrary semisimple compact G ⊂ U(N), d=4; also covers d=3.
  Theorem 2 (p.259): d=4, G=SU(2): for sufficiently small g there is bare g0=g0(ε,g) s.t. g_k ∈ ]0,γ], g_K = g, and 1/g^2 + β log(L^k ε)^{-1} <= 1/g_k^2 <= 1/g^2 + β' log(L^k ε)^{-1} (0.31). "A proof of this theorem, based on perturbative calculations, will be given in a separate paper" (never published; LFR II p.355 confirms "has not been published yet").
  Also p.260: results valid for 2D nonlinear chiral models (principal chiral) - "will discuss them separately in the future".
  Setting: torus T with sides L^m (L odd >11), lattice spacing ε = L^{-K}; Wilson action with normalized trace.
- UV3D (CMP 102:255-275, 1985) OBTAINED (uv3d.txt): Theorem 1: "The lattice approximations of the three-dimensional pure Yang-Mills theory with a semi-simple compact group Lie G are ultraviolet stable in the sense that the sequence of densities ρ_k ... satisfies the bounds (5)." -> uniform in ε bounds for partition function Z_ε. Proof "very sketchy and we do not discuss many technical details". Mentions Federbush phase cell I, II (preprints) related to stability bound.
- Dimock 2204.07201 (JMP 63, 042305 (2022)) OBTAINED: Thm 1 UV stability QED_3: K_- <= Z_N(e)/Z_N(0) <= K_+, m̄>0, e small, unit volume torus. "The proof should allow one to add local gauge invariant perturbations ... correlation functions ... The continuum limit N -> ∞ ... should also be feasible. The method works equally well for any finite volume ... But the infinite volume limit would pose new difficulties."
  History para: Balaban [1]-[4] scalar ED d=3; BIJ [14],[15],[24] abelian Higgs d=3; Balaban [5]-[13] YM d=3,4; BOS [16],[17].
  BIJ refs: Renormalization of the Higgs model: minimizer, propagators, and the stability of mean field theory, CMP 97 (1985) 299-329; Effective action and cluster properties of the abelian Higgs model, CMP 114 (1988) 257-315. Imbrie, RG methods in gauge field theories, Les Houches 1984 (North-Holland 1986). BOS JMP 32 (1991) 3199-3208.
- Dimock CV (Feb 2024): items 54-67 incl. Covariant axial gauge LMP 105 (2015) 959-987; Nonperturbative renormalization of scalar QED in d=3 JMP 56 102304 (2015); UV regularity QED d=3 JMP 59 012301 (2018); Multiscale block averaging QED d=3 JMP 61 032302 (2020); UV stability QED d=3 AHP 23 (2022) 2113-2205 (arXiv 2009.01156); Dimock-Yuan Gross-Neveu AHP 25 (2024) 5113-5186 (arXiv 2303.07916); Correlation functions GN arXiv 2406.16799.
  Dimock RG according to Balaban: I RMP 25 1330010 (2013) arXiv 1108.1335; II JMP 54 092301 (2013) arXiv 1212.5562; III AHP 15 (2014) 2133-2175 arXiv 1304.0705. phi^4_3 on toroidal lattice.
- Convergent renormalization expansions (CMP 119:243-285, 1988) OBTAINED (cre.txt). Abstract: "In this paper we introduce an inductive description of the complete effective densities including large field domains, and we show that the renormalization transformations preserve the form of the densities. This completes the renormalization group analysis for superrenormalizable models and yields convergent expansions in this case."
  Intro p.244: for d=4 the bare coupling ~ (a + b log ε^{-1})^{-1/2}; large-field small factor does not give a positive power of ε; "it controls a large number of steps, but this number is a small fraction of the total number of steps" -> need operation R to "renormalize the expression corresponding to the large field region".
- RG II (CMP 116:1-22, 1988): abstract (via search, paraphrase) - fluctuation integral of Part I written as exponentiated cluster expansion; every term satisfies inductive assumptions; "completes the construction of the sequence of effective actions in the small field approximation."
- LFR I (CMP 122:175-202, 1989): abstract (via search) "constructs the renormalization operation of the expressions connected with the large field regions. This operation, denoted by R, removes the main obstacle to prove the ultraviolet stability of four-dimensional gauge field theories."
- INSPIRE abstracts (verbatim):
  * Propagators & RT I (CMP 95): "Lattice gauge theories may be looked at as perturbations of the theory of a vector field with a Gaussian action. We study this theory here and in following papers obtaining crucial results for understanding the renormalization group method in more complicated non-Abelian gauge field theories."
  * Propagators & RT II (CMP 96): "We continue the studies of the Paper I and extend the results of this paper to operators defined by restrictions on different scales, or by renormalization transformations of different orders."
  * Averaging operations (CMP 98): "...we study such operations for lattice gauge fields and for gauge transformations ... characterizing some classes of field configurations on which the averaging operations are regular (e.g., analytic)."
  * Spaces of regular gauge field configs & gauge fixing (CMP 99:75): "...if these conditions are chosen properly then configurations belonging to the intersection are small and regular."
  * Propagators in background field (CMP 99:389): "We prove regularity and decay properties for propagators connected with the RG method in lattice gauge theories. These propagators depend on an external gauge field configuration, called a background field."
  * Variational problem & background fields (CMP 102:277): "...action ... on a space of regular gauge field configurations with fixed averages, and we prove that there exists a minimum of this action. The minimum is unique up to gauge transformations. This minimal configuration is called a background field..."
  * LFR I (CMP 122:175): "We construct the renormalization operation of the expressions connected with the large field regions. This operation, denoted by R, removes the main obstacle to prove the ultraviolet stability of four-dimensional gauge field theories. The proof will be completed in the second part of this paper."
- MRS (CMP 155 (1993) 325-383 [INSPIRE says 325-384], doi 10.1007/BF02097397). Abstract verbatim (INSPIRE): "We provide the basis for a rigorous construction of the Schwinger functions of the pure SU(2) Yang-Mills field theory in four dimensions (in the trivial topological sector) with a fixed infrared cutoff but no ultraviolet cutoff, in a regularized axial gauge. ... We prove that this combined effect is stabilizing if we use cutoffs of a certain type in momentum space. We check the validity of the construction by showing that Slavnov identities ... do hold non-perturbatively."
  Search summary says paper itself states they don't claim to prove convergence in full detail (VERIFY from PDF).
- MRS PDF OBTAINED (downloads-other/mrs.txt). Received Feb 17 1992; revised Sept 8 1992. Key quotes (pp.325-327):
  * On Balaban: "This program defines a sequence of block-spin transformations for the pure Yang-Mills theory in a finite volume on the lattice and shows that, as the lattice spacing tends to 0 and these transformations are iterated many times, the resulting effective action on the unit lattice remains bounded. From this result the existence of an ultraviolet limit for gauge invariant observables such as 'smoothed Wilson loops' should follow, at least through a compactness argument using a subsequence of approximations; but the limit is not necessarily unique. Clearly this is a point which requires further work."
  * "Balaban's work is not easily accessible ... results are scattered over many publications; hence to check the consistency of all the arguments is very difficult. Also it does not address the problem of constructing ... Schwinger functions [in a gauge], because these are not gauge invariant observables."
  * "A related program was also undertaken by Federbush [F]."
  * "We do not claim to provide here the proofs of convergence of our expansion in all detail. However ... provides a detailed outline of these proofs"
  * "We do not investigate invariance under large gauge transformations and non-trivial topological effects such as instantons; also we do not try to remove the infrared cutoff, since this would lead to large values of the coupling constant, and presumably to so-called non-perturbative effects corresponding to confinement."
  * "we cannot study the complete set of Osterwalder-Schrader axioms, also because we do not remove our fixed infrared cutoff. However we think that the main axiom, the OS positivity, could be shown to hold with some additional work"
  * Statement: "The ultraviolet limit as ρ -> ∞ of the Schwinger functions which are the moments of the bare measure defined below in (II.77) exists; furthermore these functions in the ultraviolet limit satisfy the Slavnov identities (VIII.6) adapted to the particular infrared cutoff chosen. In this paper we do not provide a detailed proof of this statement but we give all the elements necessary ... writing up of such a detailed self-contained proof, which would presumably be several hundred pages long, remains an extremely valuable task."
  * SU(2), axial gauge at large field, background-dependent gauge for small fields; momentum cutoffs that break gauge invariance + gauge-restoring counterterms; trivial topological sector.

## Federbush phase cell (INSPIRE verified)
- 0. Introductory exposition (preprint 1984; also in Proc? unknown)
- I. Small field modes, CMP 107 (1986) 319-329 [10.1007/BF01209397] (abelian: 1-1 correspondence continuum potentials <-> compatible lattice configs on finer lattices via block spin)
- II. Analysis of a mode (with C. Williamson), JMP 28 (1987) 1416-1419 [10.1063/1.527495]
- III. Stability, modified RG transformation, CMP 110 (1987) 293-309 [10.1007/BF01207369] ("basic local stability result ... valid in both small field and large field regions"; modifications of action and RG transformation)
- IV. The choice of variables, CMP 114 (1988) 317-343 [10.1007/BF01225039] (modes, averaging correction modes, chunks; pi_3(G) obstructions)
- V. Analysis of a chunk, CMP 127 (1990) 433-457 [10.1007/BF02104497]
- VI. Nonabelian lattice-continuum duality, Ann. IHP Phys. Theor. 47 (1987) 17-23
- (VII?) MRS ref [F] says "I-VII"; need check. Also Battle-Federbush phase cell cluster expansion Ann Phys 142 (1982) 95-139; "Ondelettes and phase cell cluster expansions, a vindication" CMP 109 (1987) 417-419.
- Federbush's program never completed (no final construction paper). (standard knowledge; verify if any statement)

## Classic lattice gauge (INSPIRE verified)
- Osterwalder-Seiler, Gauge field theories on the lattice, Ann. Phys. 110 (1978) 440-471 [10.1016/0003-4916(78)90039-8]. Abstract: "...verify physical positivity for the Schwinger functions ... positive self-adjoint transfer matrix. We then prove existence and analyticity of the infinite volume limit of strongly coupled Yang-Mills theories on the lattice and we verify Wilson's confinement bound. Finally ... Higgs mechanism in lattice gauge theories."
- Seiler, Gauge Theories as a Problem of Constructive QFT and Statistical Mechanics, Lect. Notes Phys. 159, Springer 1982 (pp. 1-192).
- Frohlich-Spencer, Massless phases and symmetry restoration in abelian gauge theories and spin systems, CMP 83 (1982) 411-454 [10.1007/BF01213610]. Abstract: "new, elementary proof for the existence of a deconfining transition to a massless (QED) phase in the 4D U(1) LGT and of an intermediate QED phase ... in the 4D Z_N models, with N large..."
- Guth, Existence proof of a nonconfining phase in four-dimensional U(1) lattice gauge theory, PRD 21 (1980) 2291 [10.1103/PhysRevD.21.2291]: Villain action, g^2<0.168, Coulomb lower bound on Wilson loop.
- BFS: I. General results, Ann. Phys. 121 (1979) 227-284 [10.1016/0003-4916(79)90098-8]; II. Convergence of the lattice approximation, CMP 71 (1980) 159-205 [10.1007/BF01197918]; III. The two-dimensional abelian Higgs model without cutoffs, CMP 79 (1981) 353-399 [10.1007/BF01208500].
- Luscher, Construction of a self-adjoint strictly positive transfer matrix for Euclidean lattice gauge theories, CMP 54 (1977) 283.

## 2D YM
- L. Gross, C. King, A. Sengupta, Two dimensional Yang-Mills theory via stochastic differential equations, Ann. Phys. 194 (1989) 65-112 [10.1016/0003-4916(89)90032-8]. Complete axial gauge; parallel transport as SDE; Wilson loop expectations; Euclidean invariance proven.
- B.K. Driver, YM2: continuum expectations, lattice convergence, and lassos, CMP 123 (1989) 575-616 [10.1007/BF01218586].
- A. Sengupta, The Yang-Mills measure for S^2, J. Funct. Anal. 108 (1992) 231-273; Quantum gauge theory on compact surfaces, Ann. Phys. 221 (1993) 17-52; Gauge theory on compact surfaces, Mem. AMS 126 (600) (1997).
- T. Levy, Yang-Mills measure on compact surfaces, Mem. AMS 166 (790) (2003). Also Levy, The master field on the plane, Astérisque 388 (2017) (verify).
- arXiv:2607.24640 (July 2026) Chhaibi, Dang, Guedes Bonthonneau, Riviere, To: "The Yang-Mills measure on surfaces via Morse theory" (verify).
## King U(1) Higgs (INSPIRE + Crossref)
- C. King, The U(1) Higgs model I. The continuum limit, CMP 102 (1986) 649-677 [10.1007/BF01221651]: "By using rigorous renormalization group methods we construct the continuum limit of the finite-volume lattice U(1) Higgs model in two and three dimensions. The method relies on a proof of the convergence of the effective action."
- C. King, The U(1) Higgs model II. The infinite volume limit, CMP 103 (1986) 323-349 [10.1007/BF01206942]: "We construct the infinite volume limit of the U(1) Higgs model in two and three dimensions, and verify some of the Osterwalder-Schrader axioms. The proof uses a combination of RG techniques and correlation inequalities."
- Kennedy-King, Spontaneous symmetry breakdown in the abelian Higgs model, CMP 104 (1986) 327-347; PRL 55 (1985) 776.
## Balaban-Imbrie-Jaffe (INSPIRE)
- BBIJ (Balaban, Brydges, Imbrie, Jaffe), The mass gap for Higgs models on a unit lattice, Ann. Phys. 158 (1984) 281-319: "isomorphism ... compact and noncompact formulations of Abelian gauge theory on a lattice. For weak coupling, the mass gap predicted by the Higgs mechanism is then established."
- BIJ, Renormalization of the Higgs model: minimizers, propagators and the stability of mean field theory, CMP 97 (1985) 299-329 [10.1007/BF01206191]: U(1) Higgs d=2,3; "essential step toward proving the existence of a gap in the mass spectrum and exponential decay of gauge invariant correlations."
- BIJ, Effective action and cluster properties of the abelian Higgs model, CMP 114 (1988) 257-315 [10.1007/BF01225038]: "We continue our program to establish the Higgs mechanism and mass gap for the abelian Higgs model in two and three dimensions ... multiscale cluster expansion ... decoupling properties needed for a proof of exponential decay of correlations. The result ... gauge invariant unit lattice theory with a deep Higgs potential..."
  -> Note: continuum mass gap for 3D abelian Higgs not announced as complete in these abstracts (program).
- Balaban-Imbrie-Jaffe, "Exact renormalization group for gauge theories" (1983 preprint, in Progress in Gauge Field Theory, Cargese 1983, Plenum 1984).
## Tomboulis / Ito-Seiler (INSPIRE)
- Tomboulis, Confinement for all values of the coupling in four-dimensional SU(2) gauge theory, arXiv:0707.2179 (July 2007) - not journal-published per INSPIRE (no pub info). Potential-moving (Migdal-Kadanoff-type) decimations giving upper & lower bounds on Z; vortex free energy -> area law for any coupling; d<=4.
- Tomboulis, Deriving confinement via RG decimations, PoS LATTICE2007 336, arXiv:0710.1894.
- Ito-Seiler, On the recent paper on quark confinement by Tomboulis, arXiv:0711.4930 ("missing links").
- Tomboulis, Reply to arXiv:0711.4930 by Ito and Seiler, arXiv:0712.2620 (claims inequality invoked only at strong coupling).
- Ito-Seiler, Further discussion of Tomboulis' approach to the confinement problem, arXiv:0803.3019 ("certain gaps and open problems ... what would be needed to fill the gaps").
- Ito-Seiler, Critical discussion of Tomboulis's approach..., PoS CONFINEMENT8 (2008) 034, arXiv:0901.4246.
- Tomboulis-Yaffe: Nonconfinement at high temperatures, PRD 29 (1984) 780; Absence of chiral symmetry breaking at high temperatures PRL 52 (1984) 2115; Finite temperature SU(2) lattice gauge theory, CMP 100 (1985) 313-? [10.1007/BF01206134].
- Kovacs-Tomboulis, Computation of the vortex free energy in SU(2) gauge theory, PRL 85 (2000) 704, hep-lat/0002004.
- NEED: Tomboulis-Yaffe vortex free energy inequalities: "Thermodynamics of the deconfinement transition" ? Actually: E.T. Tomboulis & L.G. Yaffe, "Finite temperature SU(2) lattice gauge theory" CMP 100 (1985) — contains vortex free energy / 't Hooft loop inequalities? Also Tomboulis "Center vortices and the area law" ? Also Kovacs-Tomboulis "Vortex free energy and the deconfinement" ; Tomboulis-Yaffe "Wilson loop bound by vortex free energy" ? search.
## TY inequality (via Kanazawa 0808.3442, Ann Phys 324 (2009) 1634-1665) OBTAINED downloads-arxiv/kanazawa_0808.3442.txt
- Theorem 1 (TY, SU(2), [Tomboulis-Yaffe CMP 100 (1985) 313-341]; also Kovacs-Tomboulis PRD 65 (2002) 074501): <W(C)> <= 2 { (1/2)(1 - Z^(-)/Z) }^{A_C/(L_mu L_nu)}, C rectangle in mu-nu plane, periodic lattice, V vortex winding d-2 directions. Uses site-reflection positivity (any one-plaquette action).
- implication: area law if 1 - Z^(-)/Z ~ e^{-rho L_mu L_nu} in thermodynamic limit ('t Hooft criterion); verified at strong coupling by Munster NPB 180 (1981) 23 via convergent strong coupling expansion.
- Kanazawa abstract: "Basically the inequalities guarantee that a system in a box that is sufficiently insensitive to boundary conditions has a non-zero mass gap."  <-- RELEVANT to finite-box criteria in repo O(3) work.
- Kanazawa PLB 670 (2009) 421-427 (0805.2742): appendix "carefully examine the proof of quark confinement by Tomboulis and summarize its loopholes."
- Mack-Petkova: Annals Phys. 125 (1980) 117 ("Comparison of lattice gauge theories with gauge groups Z_2 and SU(2)"); also Mack-Petkova Ann Phys 123 (1979) 442 "Sufficient condition for confinement of static quarks by a vortex condensation mechanism". VERIFY.
- 't Hooft NPB 138 (1978) 1; NPB 153 (1979) 141.
- Mack-Petkova (INSPIRE verified): "Comparison of lattice gauge theories with gauge groups Z_2 and SU(2)", Ann. Phys. 123 (1979) 442 [10.1016/0003-4916(79)90346-4]: inequality relating Wilson loops: SU(2) confinement whenever Z_2 model confines; 't Hooft disorder parameter. "Sufficient condition for confinement of static quarks by a vortex condensation mechanism", Ann. Phys. 125 (1980) 117 [10.1016/0003-4916(80)90121-9]. "Z_2 monopoles in the standard SU(2) lattice gauge theory model", Z. Phys. C 12 (1982) 177.

## Kopper et al. (flow equations)
- Keller-Kopper, Renormalizability proof for QED based on flow equations, CMP 176 (1996) 193-226 [10.1007/BF02099368]; PLB 273 (1991) 323.
- Kopper-Muller, Renormalization proof for spontaneously broken YM theory with flow equations, CMP 209 (2000) 477-516, hep-th/9902114 (INSPIRE abstract now says: "The proof given in the paper was incomplete due to an omission in the proof of Lemma 2. A corrected and improved version ... arXiv:0902.2486.")
- Kopper-Muller, Renormalization of spontaneously broken SU(2) YM theory with flow equations, RMP 21 (2009) 781-820, arXiv:0902.2486 (corrected version).
- Efremov-Guida-Kopper, Renormalization of SU(2) Yang-Mills theory with flow equations, JMP 58 (2017) 093503, arXiv:1704.06799. Perturbative (all-orders) renormalizability of pure SU(2) YM_4 in Euclidean space, flow equations, physical renormalization conditions, bounds on massless correlation functions; STI restored in renormalized theory.
- Kopper, Mass generation in the large N nonlinear sigma model, CMP 202 (1999) 89-126, math-ph/9902020 (UV cutoff, N large finite -> massive). Kopper-Magnen-Rivasseau, Mass generation in the large N Gross-Neveu model, CMP 169 (1995) 121-180.
- Frob-Holland-Hollands, All-order bounds for correlation functions of gauge-invariant operators in Yang-Mills theory, JMP 57 (2016) 122301 (arXiv:1511.09425? verify).
- Kopper: arXiv:2610.06165 (Oct 5 2026) Asymptotically free solutions of the scalar flow equations (verify). Also "Asymptotically free solutions of the scalar mean field flow equations" AHP (2022) [10.1007/s00023-022-01194-w], arXiv:1912.08183 (Gurau? Kopper?).

## Chatterjee (arXiv API verified)
- 1502.07719 Rigorous solution of strongly coupled SO(N) LGT in the large N limit (CMP 370 (2019) 1-? per Springer link s00220-019-03353-3; verify pages)
- 1604.04777 Chatterjee-Jafarov, The 1/N expansion for SO(N) LGT at strong coupling (pub? verify)
- 1602.01222 The leading term of the Yang-Mills free energy (JFA? verify) - 3D U(N) leading term of free energy as lattice spacing -> 0; "avoids phase cell renormalization"; 4D only in weak coupling limit.
- 1803.01950 Yang-Mills for probabilists (in Probability and Analysis in Interacting Physical Systems, Springer PROMS 283 (2019))
- 1811.09770 Wilson loops in Ising lattice gauge theory (CMP 377 (2020) 307-340? verify): 4D Z_2 Wilson loop to leading order at weak coupling.
- 2006.16229 A probabilistic mechanism for quark confinement, CMP 385 (2021) 1007-1039 [10.1007/s00220-021-04086-y]: unbroken center symmetry => confinement; nontrivial center + exponential correlation decay under arbitrary boundary conditions => center symmetry unbroken.
- 2111.10652 Cao-Chatterjee, YM heat flow with random distributional initial data (Comm. PDE? verify)
- 2111.12813 Cao-Chatterjee, A state space for 3D Euclidean Yang-Mills theories (CMP 405 (2024)? verify): random distributional gauge orbits on 3D unit torus, under GFF-like assumption; regularized Wilson loops; proposal of Charalambous-Gross.
- 2401.10507 A scaling limit of SU(2) lattice Yang-Mills-Higgs theory, Prob. Math. Phys. 7 (2026) 339-381 [10.2140/pmp.2026.7.339]: any d>=2; unitary gauge; eps->0, g->0, alpha->inf with alpha g = c eps, g = O(eps^{50d}); converges to massive Gaussian field. "The question of constructing a non-Gaussian scaling limit remains open."
- 2509.19176 Chatterjee-Yakir, Correlation decay for U(1) lattice Higgs theory: the case of small mass (2025): alpha = m beta, beta large -> exp decay; extends Osterwalder-Seiler 1978; Fradkin-Shenker phase diagram; GJS cluster expansion following BBIJ 1984.
- 2602.00436 A short proof of confinement in 3D LGT with a central U(1) (Jan 2026): |<W>| <= n exp{-c(1+n beta)^{-1} T log(R+1)} (log potential); Gopfert-Mack 3D U(1) Villain; Frohlich comparison + Glimm-Jaffe.

## Cao et al. (arXiv API verified)
- 2001.05627 Cao, Wilson loop expectations in LGT with finite gauge groups, CMP (2020) [10.1007/s00220-020-03912-z] (vol 380? verify): 4D finite groups weak coupling first order; Poisson approx + Stein.
- 2202.10375 Adhikari-Cao, Correlation decay for finite LGT at weak coupling (Ann. Probab.? verify): exp decay for gauge-invariant functions incl. arbitrary functions of Wilson loops; finite (possibly non-abelian) groups, weak coupling.
- 2307.06790 Cao-Park-Sheffield, Random surfaces and lattice Yang-Mills: Wilson loops as sums over embedded planar maps, any N, any beta, any d>=2; Weingarten weights.
- 2411.11676 Borga-Cao-Shogren-Knaak, Surface sums for lattice YM in the large-N limit (strong coupling; signed Catalan; peeling).
- 2508.13827 Borga-Cao-Shogren-Knaak, Surface sums in 2D large-N lattice YM: cancellations and explicit computations for general loops.
- 2505.16585 Cao-Nissim-Sheffield, Expanded regimes of area law for lattice YM theories: U(N), large N; improves Osterwalder-Seiler 1978; master loop equation as linear inhomogeneous equation; truncated model for merger term.
- 2509.04688 Cao-Nissim-Sheffield, Dynamical approach to area law for lattice YM: uses SZZ23 dynamical approach to prove area law in 't Hooft regime; verifies mass gap condition of [DF80] (Durhuus-Frohlich 1980) from which area law follows; G in {U(N), SU(N), SO(2N)}.
- 2406.19321 Cao-Sheffield, Fractional Gaussian forms and gauge theory: an overview.
- 2305.07197 Bringmann-Cao, para-controlled approach to stochastic YM equation in 2D; 2403.16878 global well-posedness stochastic abelian Higgs 2D.

## Shen-Zhu-Zhu & co (arXiv API verified)
- 2204.12737 Shen-Zhu-Zhu, A stochastic analysis approach to lattice Yang-Mills at strong coupling, CMP (2023) [10.1007/s00220-022-04609-1] (vol 400, 805-851? verify). 't Hooft scaling beta N; |beta| < (N-2)/(32(d-1)N) for SO(N), |beta| < 1/(16(d-1)) for SU(N): unique invariant measure; exponential ergodicity; infinite-volume limit; LSI & Poincare; large N factorization; strictly positive mass gap.
- 2401.13299 Shen-Zhu-Zhu, Langevin dynamics of lattice YMH and applications: small (beta,kappa) or (beta,kappa/m): mass gap.
- 2202.00880 Shen-Smith-Zhu, new derivation of finite N master loop equation (Langevin + Ito).
- 2512.00570 Shen-Smith-Zhu, Makeenko-Migdal equations for lattice YMH.
- Note: Bakry-Emery criterion; regime is strong coupling (small beta in 't Hooft scaling).
- CNS 2509.04688 OBTAINED: Theorem 1.6 (Area law in 't Hooft regime): d>=2, N>=2, G in {U(N), SU(N), SO(2(N-1))}; beta < beta*_G with beta*_SU(N)=beta*_U(N)=1/(8(d-1)), beta*_SO(N)=1/(16(d-1)) - 1/(8N(d-1)); |<W_l>| <= C exp(-c area(l)) for rectangular loops with side <= L/2, uniform in L. Action S = N beta sum Re Tr(Q_p). Threshold is 2x SZZ23's (Bakry-Emery on a vertex spin system).
  Key mechanism: Durhuus-Frohlich [DF80] "A connection between nu-dimensional Yang-Mills theory and (nu-1)-dimensional, non-linear sigma-models", CMP 75 (1980) 103-151: split lattice into height-1 slabs; conditional law of crossing edges is a variable-environment sigma-model; if these sigma models have exp decay uniform in boundary conditions, then area law. Requires nontrivial center.
  SZZ23 = CMP 400(2):805-851 (2023). Cha19a = CMP 366(1):203-268 (2019). BG18 = CPAM 71(10):2016-2064 (2018). CPS23 to appear in Comm. AMS. Orland: Z2 confinement for all couplings J Phys A 53 (2020) 13LT01; (2+1)D anisotropic works.

## 2023-2026 lattice YM / probability (arXiv API verified)
- 2305.02306 Park-Pfeffer-Sheffield-Yu, Wilson loop expectations as sums over surfaces on the plane, Prob. Math. Phys. 7 (2026) 37-121 [10.2140/pmp.2026.7.37]: d=2; surface sums; new proof of Makeenko-Migdal; combinatorial master field.
- 2309.07399 Abdelghani-Nissim, Geometric derivation of the finite N master loop equation.
- 2510.22788 Nissim, U(N) lattice YM in the 't Hooft regime: mass gap, unique infinite volume limit, large N, for U(N) (Bakry-Emery fails since Ricci curvature of U(N) not uniformly positive; random-environment SU(N) + U(1) field; cluster expansion + Langevin).
- 2511.07297 Brennecke, On the leading order term of the lattice YM free energy (computes K_d in Chatterjee's formula).
- 2603.24555 Rajasekaran-Yakir-Zhou, Gaussian limits of lattice Higgs models with complete symmetry breaking: any compact connected G, d>=2, massive Gaussian scaling limit (generalizes Chatterjee 2401.10507).
- 2604.16252 Lemoine, Universal dualities for Wilson loops in lattice YM (U(N), arbitrary smooth central plaquette actions; companion: heat-kernel master field at strong coupling + area law bound).
- 2605.16162 Nissim, Deconfinement for SO(3) lattice YM at strong coupling: SO(3) (trivial center) does not satisfy Wilson's criterion at strong coupling.
- 2608.27828 Chevyrev-Qu-Shen, Scaling limit of the 3D abelian YM Langevin dynamics: U(1), 3D torus, weak coupling scaling, DeTurck gauge; converges to one-form stochastic heat equation; universal.
- UCSD seminar (Sept 11 2025, Ron Nissim): before CNS, finite-N area law only for beta < c_d/N (with beta N scaling? -> in 't Hooft normalization) ; CNS 2505.16585 extends to beta < c_d uniformly in N; dynamical approach reaches beta < c_d N ... [careful with normalizations].
- Forsstrom-Lenells-Viklund 2001.07453, Wilson loops in finite abelian LGT (Z_n, Z^4, Wilson action, leading order weak coupling, no duality/cluster) [Ann. Inst. Henri Poincare Probab. Stat.? verify]
- Forsstrom 2104.03752 Decay of correlations in finite abelian LGT (Z^4)
- Forsstrom-Viklund 2304.08286 Free energy and quark potential in Ising LGT via cluster expansion; 2502.19942 current expansion & couplings Ising LGT
- Forsstrom 2409.20085 Pure perimeter laws for Wilson lines (lattice Higgs)
- Forsstrom 2111.06620 Wilson lines in abelian lattice Higgs model
- Garban-Sepulveda 2107.04021 Improved spin-wave estimate for Wilson loops in U(1) LGT: Villain, 4D, |<W>| <= exp(-(C_GFF/(2beta))(1 + C beta e^{-2 pi^2 beta})(|gamma| + o(|gamma|))) - perimeter law w/ correction from topological defects; complement Guth & Frohlich-Spencer.
- Chevyrev-Garban 2404.09928 Villain action in LGT, J Stat Phys 192 (2025) 38.
- Chevyrev-Shen 2302.12160 Invariant measure and universality of the 2D YM Langevin dynamic, CPAM (2026) [10.1002/cpa.70043]
- Dang-Nohra 2602.08591 YM measure on compact surfaces as universal scaling limit of lattice gauge models (Wilson, Manton, Villain)
- Lemoine-Nohra 2608.15923 Universality of 2D Markovian holonomy fields
- Duncan-Schweinhart: Potts LGT topological phases 2207.08339; sharp deconfinement transition codim 2 (2308.07534); topological formula 2607.02434

## Stochastic quantization (arXiv API verified)
- Chevyrev 1808.09196 YM measure on 2D torus as a random distribution, CMP 372 (2019) 1027-1058 [10.1007/s00220-019-03567-5]
- CCHS 2006.04987 Langevin dynamic for the 2D YM measure, Publ. Math. IHES 136 (2022) 1-147 [10.1007/s10240-022-00132-0]: state space, Markov process on orbits (local in time? -- 2D: global? check), DeTurck trick, regularity structures.
- CCHS 2201.03487 Stochastic quantisation of Yang-Mills-Higgs in 3D, Invent. Math. 237 (2024) 541-696 [10.1007/s00222-024-01264-2]: state space S; local in time solutions; unique renormalisation counterterms giving gauge covariance in law; canonical Markov process on gauge orbits "up to a potential finite time blow-up". NOT construction of the 3D YM measure.
- Chevyrev 2202.13359 Stochastic quantisation of Yang-Mills (review), JMP 63 (2022) [10.1063/5.0089431] - open problems.
- Chevyrev-Shen 2302.12160 invariant measure & universality 2D YM Langevin, CPAM (2026).
- Chevyrev-Shen 2503.03060 uniqueness of gauge covariant renormalisation of stochastic 3D YMH, ARMA 250 (2026) no.1 paper 11.
- Chevyrev-Klose-Mohamed 2607.22236 A PDE approach to the 2D YM measure (rough Uhlenbeck compactness).
- Barashkov-Chandra-Chevyrev-Koller-Mohamed 2609.21972 variational approach 2D abelian YMH measure.
- Chevyrev-Qu-Shen 2608.27828 scaling limit of 3D abelian YM Langevin dynamics.
- Shen 1801.04596 Stochastic quantization of an abelian gauge theory (2D abelian Higgs).

## Claimed / partial / heuristic (arXiv API verified texts)
- Jacobsen 2506.00284 (physics.gen-ph, May 2025) "A constructive proof of existence and mass gap for pure SU(3) YM in 4D": 5D orbifold regulator, polymer expansion, OS reconstruction... claims "leaving no remaining gap" — no expert acceptance found.
- Lim 2307.00788 (math-ph, 2023-2025, v7) "Positive mass gap of quantum Yang-Mills fields": Hilbert space as countable sum of non-separable Hilbert spaces; Casimir eigenvalues; not accepted. (Lim also 1701.01529 abstract Wiener measure abelian YM R^4)
- Mondal 2301.06996 "A geometric approach to the YM mass gap" JHEP 12 (2023) 191: Bakry-Emery Ricci curvature of orbit space; self-described "at least as a heuristic one"; assumes existence of quantized YM.
- Dynin 0903.4727, 1005.3779, 1110.4682, 1205.3187, 1308.6571 (Russ. J. Math. Phys. 24 (2017) 26): Hamiltonian canonical claims; not accepted.
- Frasca 1509.05292 EPJ Plus 132 (2017) 38 (+erratum 242): DS equations "exactly solved"; not accepted as proof.
- Sevostyanov math-ph/0407004: conditional statement about quadratic principal term; not a solution.
- Kholodenko 1001.0029 "Gravity assisted solution of the mass gap problem for pure YM fields".
- Faddeev 0911.1013 "Mass in quantum YM theory (comment on a Clay Millennium problem)" - commentary (Bull Braz Math Soc 33 (2002) 201-212; Perspectives in Analysis 2005).
- Faria da Veiga-O'Carroll 2509.03513 (2025-26) charge conjugation, Elitzur, "towards solving the mass gap problem" (partial, not a claim).
- Nair 2608.10133 "Towards a proof of mass gap in 3d YM" (VERIFY)
- web: preprints.org 202506.2484 "Complete Resolution to YM Existence and Mass Gap"; 202504.1268 "Fundamental Incompatibility of the YM Mass Gap and Asymptotic Freedom within Continuum QFT"; 202506.2241 "Motion is the solution"; MDPI 2813-9542/2/1/2 "Existence and Mass Gap in Quantum YM Theory"; zenodo 15338444 (2025-05-01), 8076499 (2023); Logan Nye book "Solving the Mass Gap" (2024); SSRN 5709002 Blackshear 2025; ai.vixra 2602.0069 "The Balaban-Dimock Structural Package"; GitHub lluiseriksson/THE-ERIKSSON-PROGRAMME; grandchallenge/MATHFORGE PR #240.
- !! "Adhikari-Suzuki-Zhou-Zhuang (dynamical approach to the area law)" NOT FOUND on arXiv API, INSPIRE, or web search (several queries). Closest: Cao-Nissim-Sheffield 2509.04688 "Dynamical approach to area law for lattice Yang-Mills". Flag in dossier as unverified attribution.
- Adhikari-Cao: Ann. Probab. 53 (2025) 140-174 [10.1214/24-AOP1702] (INSPIRE).
## Journal refs (INSPIRE)
- Chatterjee Ising LGT: CMP 377 (2020) 307-340 [10.1007/s00220-020-03738-9]
- Chatterjee SO(N) large N: CMP 366 (2019) 203-268 [10.1007/s00220-019-03353-3]
- Cao-Chatterjee state space: CMP 405 (2024) 3 [10.1007/s00220-023-04870-y]
- Cao-Chatterjee heat flow: Comm PDE 48 (2023) 209-251
- Cao finite groups: CMP 380 (2020) 1439-1505
- FLV: AIHP Prob Stat 58 (2022) 2129-2164
- SZZ: CMP 400 (2023) 805-851; SZZ YMH: CMP 407 (2026) 27 [10.1007/s00220-025-05528-7]
- Garban-Sepulveda: IMRN 2023 18142-18198
- Chevyrev-Shen 2D invariant: CPAM 79 (2026) 1973-2102
- Leading term YM free energy (1602.01222): published? Chatterjee, "The leading term of the Yang-Mills free energy", J. Funct. Anal. 271 (2016) 2944-3005 (verify)
- Chatterjee-Jafarov 1/N: unpublished? ; Jafarov SU(N): unpublished?
- Chatterjee leading term YM free energy: JFA 271 (2016) 2944-3005 [10.1016/j.jfa.2016.04.032] (Crossref)
- Brennecke 2511.07297: J. Stat. Phys. 193 (2026) [10.1007/s10955-026-03649-4] (Crossref)
- CCHS 2D: Publ. Math. IHES 136 (2022) 1-147; CCHS 3D: Invent. Math. 237 (2024) 541-696
- Basu-Ganguly: CPAM 71 (2018) 2016-2064
- Shen-Smith-Zhu master loop: EJP 29 (2024?) [10.1214/24-EJP1090]
- PPSY: PMP 7 (2026) 37-121; Chatterjee YMH scaling limit: PMP 7 (2026) 339-381
- Chevyrev-Shen uniqueness: ARMA 250 (2026) 11
## More classics (INSPIRE)
- Durhuus-Frohlich, A connection between nu-dimensional YM theory and (nu-1)-dimensional nonlinear sigma models, CMP 75 (1980) 103-151 [10.1007/BF01222514]: YM on Z^nu = integral of product over one coordinate of sigma models on Z^{nu-1} in random external gauge fields; clustering of certain two-point functions of those sigma models implies confinement. Clustering proven for 1D sigma models, U(n)xU(n) sigma models in 2D, SU(2)xSU(2) for g^2 >~ O(nu). Random surface representation.  ** KEY BRIDGE: 2D sigma models <-> YM area law. ** (Repo O(n) relevance!)
- Gopfert-Mack, Proof of confinement of static quarks in 3D U(1) LGT for all values of the coupling constant, CMP 82 (1981) 545-606? [10.1007/BF01961240]: Villain action; string tension nonzero for all g^2; continuum limit = free scalar field of mass m_D (string tension in physical units -> inf).
- Driver, Convergence of the U(1)_4 lattice gauge theory to its continuum limit, CMP 110 (1987) 479-501 [10.1007/BF01212424]: converges to renormalized free EM field.
- Brydges-Durhuus-Frohlich-Giffen? Surface representations of Wilson loop expectations in LGT, NPB 275 (1986) 459-487.
## More 2024-2026 (arXiv API)
- Goswami 2204.08252, variational problem & background field in Balaban RG for nonlinear sigma models (d=2), AHP 25 (2024) 2065-2085 [10.1007/s00023-023-01353-7] -- Dimock student; adapts Balaban's variational problem from YM d=3,4 to 2D NLSM.
- Sevostyanov 2605.14616 tree-free approach to 3D YM Langevin dynamic (model for regularity structure via multi-index approach).
- Chhaibi-Dang-Guedes Bonthonneau-Riviere-To 2607.24640 YM measure on surfaces via Morse theory.
- Dang-Nohra 2607.19037 semiclassical analysis for YM random connections on compact surfaces.
- Lemoine 2508.16162 review 2D YM via integrable probability; Dahlqvist-Lemoine large N 2D (2201.05882, 2201.05886); Levy 1912.06246 MM equations; Dahlqvist-Norris sphere master field 1703.10578; Hall 1705.07808.
- Shen-Smith-Zhu 2412.15422 MM equations 2D YM lattice -> continuum.
- Sauzedde 2412.16781 Symanzik representation 2D abelian YMH.
- Chatterjee-Frasca-Ghoshal-Groote 2608.05415 "Exact lattice identities and continuum-limit DS equations for YM" (physics; not rigorous construction?)
- 2506.00284 Jacobsen: WITHDRAWN by arXiv Admin (v2 June 13 2025): "withdrawn because it does not meet arXiv's research content quality standards" (verified via arxiv.org/abs page).
- 2026 web: Toupin (PhilPapers, Jan 2026, celestial holography); Croft Adams (Medium Feb 2026); GitHub Shariq81 Coq repo (assumes lattice->continuum convergence); Zenodo 19372339 (Watt, April 2026, fuzzy CP^2, AI co-authors); Zenodo 19699784 / 19424275 ("dissolution", explicitly not claiming prize); Rietz (PhilArchive RIECYM, 2025, 1.710 GeV); ai.viXra 2505.0198 (Loiseau, prime matrix); viXra 2504.0192 (Fesembeck energy minimization); viXra 2407.0176; 2006.0155; merfijang/yang-mills-gap Lean blueprint; yangmills.xyz Lean project (states not solved).
- Press: OpenAI Oct 6 2026 release (722 papers) includes O(3) sigma model papers; Douglas quoted (Scientific American) calling sigma model "warm-up" for YM; Quanta 2026-09-08 "AI has solved one of math's $1M Millennium Prize problems" (Navier-Stokes claim by OpenAI). NOT YM.
- Scientific American (Oct 8 2026, Peter Hall & Joseph Howlett), "The most exciting claims from OpenAI's heap of new proofs": section "Baby Yang-Mills": OpenAI released multiple papers "claiming to completely resolve the equivalent of the Yang-Mills problem for this simpler model" (nonlinear sigma model). Douglas: "This goes back 50 years, much like Yang-Mills, and is widely considered the 'warm-up' for Yang-Mills". Bauerschmidt (NYU): first sigma-model paper "seems very reasonable" ("I haven't digested it or understood all the details"); others "incomprehensible slop"; "The second paper is horrible". Not all proofs Lean-certified; some retracted (general).
## Douglas 2026 Nat Rev Phys 8, 86-97 (published online 2026-01-12, Crossref). 74 references incl.:
- Chatterjee CMSA talk "Yang-Mills existence and mass gap" (Oct 14/15 2025, cmsa.fas.harvard.edu/event/clay_101425/)
- Chevyrev JMP 63, 091101 (2022) [SQ review]
- Mastropietro Non-Perturbative Renormalization (2008)
- Cao-Nissim-Sheffield 2505.16585
- Gubinelli-Hofmanova PDE construction of Phi^4_3 (CMP 2021); Albeverio-Kusuoka Phi^4_3 Mem AMS; Duch-Hairer-Yi-Zhao ergodicity infinite volume Phi^4_3 high temperature arXiv 2508.07776 (2025); Moinat-Weber; Hairer-Steele
- Bauerschmidt-Brydges-Slade Intro to RG method (Springer 2019); Brydges lectures
- Balaban RG I (CMP 109); Dimock RG according to Balaban I
- CCHS 3D YMH Invent 2024; Cao-Chatterjee CMP 405 (2024)
- Makeenko-Migdal PLB 88 (1979) 135
- Kupiainen RG and SPDEs AHP 17 (2016); Duch flow equation approach SPDE PMP 6 (2025)
- Chatterjee SO(N) CMP 366; PPSY PMP 7 (2025 per Douglas; 2026 per INSPIRE)
- 't Hooft NPB 138 (1978) 1-25
- Chatterjee probabilistic mechanism CMP 385
- MRS CMP 155, 325-384 (1993)
- Rai et al. spectral gap certificates frustration-free (arXiv 2411.03680)
- Singer orbit space; Feynman 2+1
- Dybalski-Stottmeister-Tanimoto, The Balaban variational problem in the non-linear sigma model, Rev. Math. Phys. (2024) [10.1142/s0129055x24610038]  <-- VERIFY
- Dunne-Unsal resurgence; Marino renormalon 2504.12044; Unsal magnetic bion PRD 80 (2009) 065001
- Meurice-Sakai-Unmuth-Yockey tensor lattice RMP 94 (2022); Ebel-Kennedy-Rychkov 2506.03247; Kennedy-Rychkov JSP 187 (2022) 33; Giuliani-Mastropietro-Rychkov JHEP 2021
- Athenodorou-Teper glueball spectrum JHEP 2021 82; Athenodorou-Dubovsky-Luo-Teper confining strings IJMPA 40 (2025)
- Computer-assisted proofs refs (Buckmaster-Cao-Labora-Gomez-Serrano; Nakao-Plum-Watanabe)
=> Douglas 2026 emphasizes: computational RG methods, computer-assisted proofs, tensor RG, as promising directions (per secondary summary). 
- Dybalski-Stottmeister-Tanimoto, The Balaban variational problem in the non-linear sigma model, Rev. Math. Phys. 38(08) 2461003 (online 2024-10-30) [10.1142/s0129055x24610038], arXiv 2403.09800. O(N)? NLSM 2D; Banach contraction; random walk expansions. Also "Lattice Green functions for pedestrians: Exponential decay" RMP 36 (2024) arXiv 2303.10754.
  -> Balaban-RG tooling being revived for 2D sigma models (Goswami AHP 2024; DST RMP 2024).
## Rivasseau-Wang (web search)
- LVE: Rivasseau-Wang, LVE for Phi^2k in zero dimension, JMP 51 (2010) 092304 (1003.1037); Constructive renormalization for Phi^4_2 with LVE, JMP 53 (2012) 042302 (1104.3443) -- ERROR found, corrected in "Corrected LVE for Phi^4_2", JMP 56 (2015) 062301 (1406.7428); How to resum Feynman graphs, AHP 15 (2014) 2069-2083 (1304.5913). Gurau-Rivasseau multiscale LVE AHP 16 (2015) 1869 (1312.7226). Rivasseau, constructive matrix theory JHEP 0709 (2007) 008; Magnen-Rivasseau constructive phi^4 without tears AHP 9 (2008) 403.
- NO LVE application to gauge theories found.
- MRS, Rigorous results on the UV limit of non-Abelian gauge theories, PLB 283 (1992) 90-96 (announcement). Rivasseau, Construction of the continuum limit of non-Abelian gauge theory in a finite volume, proceedings (1994) pp 432-439.
- Lemoine 2606.28945 The heat-kernel master field on Z^d at strong coupling (area law bound; companion to 2604.16252).
## Chatterjee, Yang-Mills for probabilists (1803.01950) OBTAINED downloads-arxiv/chatterjee_1803.01950.txt
- Problem 4.1 (Area law) [line ~374]: any compact non-abelian G ⊂ U(N), N>=2, any infinite volume limit of 4D LGT at inverse coupling beta: |<W_{R,T}>| <= C(beta) e^{-c(beta) R T}.
- "For non-Abelian theories, this is currently known only in dimension two ... For U(1) theory ... Gopfert and Mack ... area law at arbitrary beta in dimension three. The solution of Problem 4.1 for four-dimensional non-Abelian lattice gauge theories at large beta remains elusive."
- Problem 5.1 (Mass gap): plaquette-plaquette correlation f_beta(x); show for any beta>0 exists xi(beta) in (0,inf) with lim log f_beta(x)/|x| = -1/xi(beta), and lim_{beta->inf} xi(beta) = inf.
- Problem 5.2 (Continuum limit): as beta->inf, eps(beta)->0, c(beta)->inf, nonzero d: log<W_{R/eps,T/eps}> = -c(R+T) - dRT + o(1).
- Sec 6: "Usually, convergence is hard to prove, so one settles for subsequential convergence by a compactness argument. The existence of a convergent subsequence is known as ultraviolet stability"
- "In spite of the remarkable achievements surveyed above, there is yet no construction of a continuum limit of a lattice gauge theory in any dimension higher than two where Wilson loop variables have been shown to have nontrivial behavior."
- King [56,57] continuum limit of 3D Higgs; Gross [49] continuum limit of pure U(1) YM (3D) with different notion of convergence; Driver [29] 4D U(1); Borgs [17] confinement/deconfinement 3D/4D weak coupling; Borgs-Seiler 2D Higgs; Charalambous-Gross YM heat flow regularization.
- MRS description: "regularize the continuum theory by introducing a quadratic term..."(mass term breaking gauge invariance)
- CNS 2505.16585 v3 OBTAINED. Theorem 1.2 (Area law): G=U(N), all d>=2, exists beta_0(d)>0 s.t. for beta <= beta_0(d) and all N>=1, rectangular loops: |<W_l>| <= C_{1,d} C_N^{|l|} exp(-C_{2,d} area(l)). (Normalization: action presumably N beta Re Tr in 't Hooft form? Figure: OS78 needs beta << 1/N; theirs beta << 1; in tilde-beta = N beta: OS78 tilde-beta << 1 vs theirs tilde-beta << N.)
  Quote: "it remains a major open problem to show area law for large beta and d = 4 for arbitrary N > 1 (e.g. N = 2 or N = 3) and to control the corresponding string tension constants in the large beta limit. Area law is known not to hold for large beta and d = 4 when N = 1, so any proof will have to use N > 1 in a crucial way."
  "In dimension three, area law is known to hold for the U(1) theory at all beta [GM81], and then by a general result of [Fro79], this implies that the same is true for U(N) Yang-Mills theory for any N >= 1." [Fro79 = Frohlich, Confining forces... comparison? verify: J. Frohlich, "Confining Coulomb forces? / Phys. Lett. B 83 (1979) 195"?]
- [Fro79] Frohlich, "Confinement in Z_n lattice gauge theories implies confinement in SU(n) lattice Higgs theories", Phys. Lett. B 83 (1979) 195-198 (per CNS refs; verify page).
- Kazakov-Zheng bootstrap for lattice YM PRD 107 (2023) L051501; finite N JHEP 03 (2025) 099 (numerical-rigorous bounds; relevant to "intermediate coupling").
- Bootstrap: Kazakov-Zheng 2203.11360 (PRD 107 L051501, 2023); 2404.16925 (JHEP 03 (2025) 099); Guo-Li-Yang-Zhu 2502.14421 Bootstrapping SU(3) lattice YM (JHEP 12 (2025) 033); Liu-Yang 2601.04316 direct & indirect loop equations. Rigorous two-sided bounds on plaquette average etc. from loop equations + positivity (numerical, computer-assisted SDP; not a proof of mass gap).
- Faizal & Shabir, "Reflection-Positive Construction of a Four-Dimensional SU(N) Yang-Mills Theory With Mass Gap and Confinement", Fortschr. Phys. 74(4) (2026) e70097 [10.1002/prop.70097] (online 2026-04-20; Crossref verified); arXiv 2606.19362 (June 2026). Parts 1 & 2 in Int. J. Geom. Methods Mod. Phys. (Jan/Feb 2026) ("Reflection positivity and a finite-a strong-coupling gap in lattice SU(N) YM: Part (1)"; "Reflection-positive renormalization and the persistence of the mass gap in lattice SU(N) YM: Part (2)", INSPIRE 3124506). No expert endorsement found; abstract-level claims. Treat as claimed, unverified; peer-reviewed in a physics journal but not accepted by the community.

## Repo cross-links (family 215)
- O(3) paper build/sections/history.tex:60-95 cites Balaban gauge RG I (CMP 109) and gauge variational (CMP 102:277) as part of RG tradition; N-vector low-temp series (CMP 167, 175); Goswami 2024 (SU(n) chiral models incl O(4)); DST variational (O(4), one block averaging); Kupiainen large N; Kopper large N; Gawedzki-Kupiainen hierarchical sigma model; Mitter-Ramadas renormalized trajectory (perturbative); Aru-Garban-Sepulveda (local GFF limit).
- O(4) sharp mass bounds introduction.tex:191 and renormalization.tex:6 cite Balaban flow/variational, DST.
- No repo paper treats Yang-Mills directly (grep for yang-mills/lattice gauge in TeX: only these citations).
- Balaban N-vector I (CMP 167, 1995) abstract: "low temperature lattice classical spin models with a symmetry group O(N) ... RG approach in a small field approximation ... goal to prove the so-called 'spin wave picture' displaying massless behavior of the models" -> d>=3 (massless, Goldstone). (Balaban N-vector program is for d>=3 low temperature, not 2D.)
- Dimock ETH Zurich slides (May 28 2013, "The renormalization group according to Balaban") OBTAINED downloads-balaban/dimock_eth_slides.txt:
  "Balaban projects: 1. Scalar electrodynamics in d=2,3 (UV problem, 5 papers, 1982-83); 2. Yang-Mills in d=3,4 (UV problem, 11 papers, 1984-89); 3. Linear sigma-model in d>=3 (IR problem, 8 papers, 1995-99). (Also with J. Imbrie, A. Jaffe: partial results on abelian Higgs model in d=2,3 (UV and IR, 1988))"
  YM d=3,4: "Results (after renormalization): bounds on effective densities for RG flow; upper stability bound. Caveat: paper on coupling constant flow in second order perturbation theory missing"
  Scalar ED: stability bound exp(-c Vol) <= Z/Z(0) <= exp(c Vol), massive photons.
  Note "upper stability bound" for YM (lower bound not claimed in summary for 4D!). (3D paper says lower bound easier; 4D LFR II eq (0.1) gives two-sided? The text: "ultraviolet stability bounds of the same type as for superrenormalizable models in [16]: χ exp(-1/g^2 A - E_-|T_η|) <= ρ_k <= exp(E_+|T_η|)" -> upper & lower in some form; Dimock summarizes "upper stability bound". Flag nuance.)
- LFR II page image confirms (0.1): chi_k exp[-(1/g_k^2) A(U_k) - E_-|T_eta|] <= rho_k <= exp(E_+ |T_eta|) (two-sided; lower bound only on small-field domain via chi_k).
## Crossref-verified classics
- Seiler LNP 159 (1982): chapters "Lattice gauge theories" pp 3-98 [10.1007/3-540-11559-5_2]; "Continuum gauge quantum field theories" pp 99-181 [10.1007/3-540-11559-5_3].
- Borgs, Confinement, deconfinement and freezing in lattice YM theories with continuous time, CMP 116 (1988) 309-342 [10.1007/bf01225259].
- Borgs-Seiler, Lattice YM theory at nonzero temperature and the confinement problem, CMP 91 (1983) 329-380 [10.1007/bf01208780].
- L. Gross, Convergence of U(1)_3 lattice gauge theory to its continuum limit, CMP 92 (1983) 137-162 [10.1007/bf01210842].
- Munster, Strong coupling expansions for the mass gap in lattice gauge theories, NPB 190 (1981) 439-453.
- Federbush series: published I-VI (I CMP 107 1986; II JMP 28 1987 w/ Williamson; III CMP 110 1987 (title on Euclid "III. Local stability, modified renormalization group transformation"); IV CMP 114 1988; V CMP 127 1990; VI AIHP 47 1987). No published VII found (MRS 1993 ref list says "I-VII" listing those journals). Part V: point gauge singularities inevitable; gauge-invariant loop expectations future work. Program not completed (no final construction).
- Frontiers in Appl Math Stat 2026 "The pure Yang-Mills field, I: fixed time existence" (10.3389/fams.2026.1811439) claims Clay requirements fulfilled -- treat as claimed (verify author).
- !! James Glimm (Stony Brook / GlimmAnalytics LLC), "The pure Yang-Mills field, I: fixed time existence", Front. Appl. Math. Stat. 12:1811439 (published 21 Aug 2026; received 6 Apr 2026; accepted 30 Jul 2026; corrected 3 Sep 2026) [10.3389/fams.2026.1811439] (Crossref + page verified).
  Abstract: "The convergence of renormalized perturbation theory to all finite orders is defined and shown to be valid for the fixed time perturbation theory of a pure Yang-Mills field. Two pure YM quantum gauge field theories are constructed, one based on short distance asymptotics and the other based on long distance asymptotics. The construction depends on an assumed principle of a maximum rate of entropy production."
  Sec 1.1.3: "All requirements for the Clay Foundation Yang-Mills Millennium Prize are fulfilled at this point." Mass gap deferred to companion "The Yang-Mills Field, II: The Mass Gap" (2026, Stony Brook Academic Commons). "The theory remains perturbative". Convergence "order by order to all finite orders".
  -> Claimed; relies on an extra physical postulate (max entropy production) and order-by-order perturbative convergence; does not meet the Clay bar as stated. No community acceptance found.
- Glimm-Petrillo-Lee 2107.05981 (2021, v2 Feb 2025) "Construction of nontrivial quantum gauge theories: the continuum limit in a finite volume" (math-ph, unpublished per arXiv): claims 4D abelian & non-abelian in finite volume, UV limit, RPT summed to all orders. Not accepted.
## Perturbative YM rigorous (INSPIRE)
- Frob-Holland-Hollands, All-order bounds for correlation functions of gauge-invariant operators in YM theory, JMP 57 (2016) 122301? [10.1063/1.4967747], arXiv 1511.09425: perturbative renormalisability of Euclidean YM; all correlation functions of composite local operators satisfy Ward identities; UV and IR; Wilson-Wegner-Polchinski-Wetterich flow.
- Hollands, Renormalized quantum Yang-Mills fields in curved spacetime, RMP 20 (2008) 1033-1172, arXiv 0705.3340: perturbative YM on globally hyperbolic spacetimes; algebra of gauge-invariant renormalized interacting fields (polynomials in F and derivatives), OPE; formal power series. -> RELEVANT to Clay's "local operators ↔ gauge-invariant polynomials in F" and OPE requirement, at perturbative level.
- Hollands & collaborators: OPE convergence in perturbation theory (Hollands-Kopper, "The operator product expansion converges in perturbative field theory", CMP 313 (2012) 257-290) -- scalar phi^4; Holland-Hollands for YM? (verify if needed).
## Clay web page (downloaded 2026-10-09: downloads-clay/clay_ym_page.html)
- Status: "Unsolved". Summary: "Experiment and computer simulations suggest the existence of a 'mass gap' in the solution to the quantum versions of the Yang-Mills equations. But no proof of this property is known."
- "...Progress in establishing the existence of the Yang-Mills theory and a mass gap will require the introduction of fundamental new ideas both in physics and in mathematics."
- Links: official description PDF (wp-content/uploads/2022/06/yangmills.pdf) and rules page. Douglas report not linked from page (lives at claymath.org/library/annual_report/douglas_quantum_yang_mills.pdf).
- Faria da Veiga-O'Carroll 1903.09829 "On thermodynamic and ultraviolet stability of Yang-Mills" (2019, unpublished per arXiv): U(N), SU(N), d=2,3,4, free b.c., axial-tree gauge; e^{c_l d(N) Λ_r} <= (a^{d-4}/g^2)^{d(N)Λ_r/2} Z <= e^{c_u d(N) Λ_r} uniform in L, a, g^2 — i.e., extracts the leading (Gaussian-scale) singular behavior of the free energy only; "at least in the sense of subsequences" limits. Much weaker than Balaban (no RG, no asymptotic freedom; analogous to Chatterjee's leading-term free energy).
- Farinelli 1406.4177 (math.GM, v17) and 2406.16881 (math.GM): claimed Wightman construction + mass gap; and "mass gap implies quark confinement" conditional. Not accepted.
- Lim 2211.07064 "Wilson area law formula on R^4" (math-ph, v8) - claimed.
- Wikipedia (rev. last edited 6 Aug 2026): no Balaban; claims "It was proved in this way that Yang-Mills theory develops a mass gap on a lattice" citing lattice NUMERICS (Lucini-Teper-Wenger 2004; Chen et al 2006) -> misleading; flag.
- Chatterjee CMSA Millennium Prize Problems Lecture "Yang-Mills and the foundations of quantum field theory", Oct 15 2025 (Harvard CMSA, event clay_101425) (Douglas 2026 cites it as "Yang-Mills existence and mass gap").
- lluiseriksson/THE-ERIKSSON-PROGRAMME (GitHub, Lean 4): lattice strong-coupling (OS regime) area law/correlation decay machine-checked; lattice mass-gap theorem conditional on Balaban UV estimate hypothesis; explicitly "No four-dimensional continuum mass gap is claimed"; earlier headline theorem `clay_millennium_yangMills` was vacuous (corrected). ai.viXra 2602.0033 "The Yang-Mills mass gap on the lattice" & 2602.0069 "The Balaban-Dimock structural package" (Eriksson) -- cite Balaban Theorem 1 w/o the coupling assumption (per search snippet).
- Logan Nye, "Existence and Mass Gap in Quantum Yang-Mills Theory", International Journal of Topology (MDPI) 2(1) (2025) 2 [10.3390/ijt2010002] (Crossref; published 25 Feb 2025); also SSRN 4997374 (2024) and a self-published book "Solving the Mass Gap" (Amazon B0DP2BH7GJ). Not accepted.
- SSRN 6141826 De Miguel Bueno (2026) "Existence and Mass Gap for 4D Yang-Mills Theory"; SSRN 5836022 / preprints-3113970 Borom (2025-26) "Constructive Existence of Quantum YM on R^4 with strictly positive mass gap for each compact simple G". Not accepted.
- Faria da Veiga, "On the Mass Gap Problem for the Yang-Mills Model of QFT", Matemática Contemporânea 61 (2025) [10.1007/s44425-025-00006-7] (survey/partial? verify).
## Crossref page ranges (verified)
- Guth PRD 21 (1980) 2291-2307; Mack-Petkova AP 123 (1979) 442-467; AP 125 (1980) 117-134; Gopfert-Mack CMP 82 (1981/82) 545-606 [issued 1982-01]; Tomboulis-Yaffe CMP 100 (1985) 313-341; Durhuus-Frohlich CMP 75 (1980) 103-151; OS AP 110 (1978) 440-471; FS CMP 83 (1982) 411-454; Rivasseau JMP 41 (2000) 3764-3775 "Constructive field theory and applications: perspectives and open problems" (math-ph/0006017).
- SZZ 2204.12737 OBTAINED (downloads-arxiv/szz_2204.12737.txt:67-92): OS78 "showed that ... when the coupling is sufficiently strong, the cluster expansion ... for expectation values of local observables ... is convergent, uniformly in volume. The proof ... was sketched in [OS78] ... follows similarly as [GJS73] ... Moreover, as explained in [OS78], the existence of a mass gap (exponential clustering) follows from convergence of the cluster expansion, so do existence of the infinite volume limit and analyticity of Schwinger functions in the inverse coupling." ; OS78 condition in 't Hooft scaling amounts to beta N small; SZZ uniqueness uniform in N.
- Adhikari-Cao 2202.10375 OBTAINED: "main result ... can be interpreted as showing the existence of a mass gap in the setting of finite (non-Abelian) gauge groups at large beta. In general, it is more difficult to prove exponential decay of correlations at large beta compared to small beta". Footnote: Seiler monograph claims cluster expansions extend from finite abelian to general finite groups, "However, as pointed out by Borgs [22, Section 7], this is not the case." Method: swapping/percolation argument (Forsstrom) + algebraic topology (homomorphisms of pi_1).
  Key structural point (my analysis): finite gauge group at weak coupling = low temperature of a discrete spin system -> gapped (no continuous symmetry, no asymptotic freedom); NOT the continuum regime of SU(N).
- CCHS 3D (2201.03487) OBTAINED: open problems (p.7-8): "One of the main questions is whether the Markov process on O constructed in this paper admits an invariant measure, which should then be unique due to the strong Feller [HM18] and full support [HS22a] properties ... We do conjecture that such an invariant measure exists, which then yields a reasonable candidate for the YMH measure on T^3. Unfortunately, we do not even know how to show the weaker statement that the Markov process survives for all times. For the pure YM measure and Langevin dynamic on T^2, this question was recently answered in [CS23]."
- Chatterjee 2401.10507 OBTAINED (PMP 7 (2026) 339-381): limit is massive Gaussian (Euclidean Proca field); "None of these approaches have yet reached their ultimate goal of constructing non-Abelian Euclidean Yang-Mills theories in d >= 3, but the case looks promising." "Proving mass gap in Yang-Mills theories is a fundamental open question in d >= 3." "The problem with holding αg larger than a constant ... the correlation length does not diverge to infinity [39] and therefore one cannot pass to a continuum limit." Also: "construction of Yang-Mills-Higgs theories in the continuum remains open even in 2D" (as of v4 April 2026; cites Bringmann-Cao global well-posedness of abelian YMH heat flow 2D). Giuliani-Ott [27] Gaussian limits O(N) 2D. Gross [31] (3D U(1)) & Driver [22] (4D U(1)): convergence of curvature forms to massless Euclidean Proca fields.
- Adhikari, Wilson loop expectations for non-abelian finite gauge fields coupled to a Higgs boson at low and high disorder, CMP 405 (2024) [10.1007/s00220-024-04998-5] (arXiv 2111.07540).
- Brydges-Giffen-Durhuus-Frohlich, Surface representations of Wilson loop expectations in LGT, NPB 275 (1986) 459-487.
- Jafarov SU(N) 1610.03821 & Chatterjee-Jafarov 1604.04777: no journal version found (arXiv only).
- Hairer, "Yang-Mills and the Mass Gap", 2025 Clay Research Conference (Oct 2025; claymath.org/lectures/yang-mills-and-the-mass-gap/; YouTube qJOV8NZDUQw): "introduction to the probabilistic formulation of the Yang-Mills problem ... reasons why it is so hard ... progress made in this direction over the past five years or so."
- Dimock RG-Balaban I (1108.1335v2) OBTAINED: "after each RG transformation a split is introduced into regions where the fields are large and regions where the fields are small ... sums over all possible splittings"; "These are all very difficult problems and for each problem the analysis extends over many papers. As a result others have been slow to adopt the approach"; avoids perturbation theory entirely ("dynamical systems approach"); phi^4_3 finite volume UV stability (known result, new proof).
- Douglas-Hoback-Mei-Nissim 2603.15770 "Formalization of QFT" (Mar 2026): Lean 4 formalization of free bosonic QFT in 4D Euclidean satisfying Glimm-Jaffe (OS variant) axioms; assumptions (Minlos, nuclearity of Schwartz space, Goursat) later proven/avoided -> OS/GJ axioms for free field proven in Lean+Mathlib. RELEVANT to "formalizing the target" for the Clay problem.
- Douglas 2607.06379 "Axioms for physical reasoning: codifying the Seiberg-Witten solution in Lean" (Jul 2026).
- BOS: CMP 122 (1989) 233-247; JMP 32 (1991) 3199-3208 "Properties of block renormalization group operators for Euclidean fermions in an external gauge field" (Crossref).
- Jaffe-Witten book version: in J. Carlson, A. Jaffe, A. Wiles (eds.), The Millennium Prize Problems, CMI/AMS 2006, pp. 129-152 (CNS refs: "The millennium prize problems, 1:129-152, 2006"). Online PDF (yangmills.pdf) 14 pp, metadata creation date 2006.
- Faddeev, Mass in quantum YM theory (comment on a Clay Millennium problem), Perspectives in Analysis (Math. Phys. Studies 27), Springer 2005, 63-72; arXiv 0911.1013.
- Ito-Seiler 0803.3019 OBTAINED: central objection "this cannot possibly be correct, however, since there exists a deconfining transition in 4D lattice gauge theory based on abelian gauge groups" (the argument seems to work even for U(1)); "The previous proof may look perfect, but there must be something missing since this proof seems to work even for G = U(1)". Problems 1-3: existence of t_m, t*, extension of implicit-function branch t(λ) from 0 to 1 not established. "MK RG recursion formulae cannot distinguish non-abelian groups from abelian ones". "We are skeptical about the idea that the problem of quark confinement can be solved by soft analysis like this".
  -> LESSON (relevant to repo O(n) analogue): any argument must fail for U(1) in 4D (cf. O(2)/BKT in 2D).
## Douglas 2026 Nat Rev Phys KEY POINTS (verbatim from nature.com page HTML, downloaded downloads-other/douglas2026.html)
- "Yang–Mills theory is the basis of the standard model of particle physics and describes the strong and weak forces."
- "The Yang–Mills Millennium problem is to show that Yang–Mills theory is mathematically well defined and that it has the mass gap property."
- "The issue of definition is to prove that the theory has a continuum limit, which is well defined at arbitrarily high energies. This requires renormalization, which has never been made rigorous in the needed generality."
- "The mass gap property (no massless particles) is expected because it is true of real-world quantum chromodynamics and it is seen in numerical simulations. It is widely felt that no clear path is known towards proving it."
- "Recent mathematical approaches include rigorous stochastic quantization and the rigorous strong coupling expansion. They are part of probability theory, and mathematicians are making significant advances."
- "Numerical and computational methods are important in the physical study of Yang–Mills and likely to be used in any rigorous proof. Physicists could contribute significantly by developing more powerful computational renormalization group methods."
- Abstract: "The Yang–Mills Millennium Prize problem is one of the great challenges of mathematical physics. In the quarter century since it was set, what progress has been made? This Review outlines the problem from a physics point of view, gives its physical background, explains its nature and significance as a problem in mathematics and surveys promising approaches from recent years."
## 2D YM (Crossref verified)
- Sengupta, The YM measure for S^2, JFA 108 (1992) 231-273; Quantum gauge theory on compact surfaces, Ann Phys 221 (1993) 17-52; Gauge theory on compact surfaces Mem AMS 126 (600) (1997).
- Levy, YM measure on compact surfaces, Mem AMS 166 (790) (2003) [10.1090/memo/0790]; Discrete and continuous YM measure for non-trivial bundles, PTRF 136 (2006) 171-202; The master field on the plane, Asterisque 388 (2017/2018) [10.24033/ast.1016].
- Witten, On quantum gauge theories in two dimensions, CMP 141 (1991) 153-209.
- Driver-Hall-Kemp, Three proofs of the Makeenko-Migdal equation for YM on the plane, CMP 351 (2017) 741-774; Driver-Gabriel-Hall-Kemp, MM equation on compact surfaces, CMP 352 (2017) 967-978.
- Chatterjee 2602.00436v2 OBTAINED: Theorem 3.1 (3D, G ⊆ U(n) containing central U(1), free b.c.): |<W_l>| <= n exp(-C(1+n beta)^{-1} T log(R+1)). Expository; result = Frohlich [1] Corollary 2 + Glimm-Jaffe 3D U(1) log potential (McBryan-Spencer complex rotation). Notes: whether Frohlich comparison + Gopfert-Mack gives area law for 3D U(n) Wilson action "We do not pursue this here". (Contrast CNS 2505.16585 which states area law at all beta holds for 3D U(N) via GM81+Fro79 -- possible discrepancy in formulations (Villain vs Wilson); flag.)
- Frohlich 1979: "Confinement in Z_n lattice gauge theories implies confinement in SU(n) lattice Higgs theories", PLB 83 (1979) 195-198. (Chatterjee [1] is Frohlich -- check if same paper.)
