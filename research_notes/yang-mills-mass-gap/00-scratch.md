# Yang–Mills existence and mass gap: working notes

Started 2026-10-09. Scratch file, not a finished report.

## The question
What would it take to resolve the Clay problem (Jaffe–Witten): for every compact simple G, construct a
non-trivial quantum YM theory on R^4 satisfying axioms at least as strong as Wightman / Osterwalder–Schrader,
with mass gap Delta > 0.

## Closest analogues in this repo (family 215 and neighbours)
- `preprints/The-canonical-massive-continuum-limit-of-the-two-dimensional-O3-model-October-4-2026/`
  (122 pp). Claims the 2D analogue of the Clay problem for the O(3) sigma model: canonical continuum limit
  along all beta -> infinity, OS axioms, unique vacuum, Hamiltonian gap on the vacuum complement, nonzero
  connected 4-point function. Not Lean-formalized.
- `preprints/Sharp-mass-bounds-for-the-two-dimensional-O4-model-September-23-2026/` (102 pp): full transfer gap
  ~ sqrt(beta) e^{-pi beta}; preliminary mixing length Xi(beta) = exp(pi beta + C sqrt((1+beta) log(2+beta))).
- `preprints/Exact-mass-asymptotics-for-the-two-dimensional-O4-lattice-model-October-5-2026/` (109 pp):
  m_lat ~ 32 e^{pi/4 - 1/2} sqrt(beta) e^{-pi beta}.
- `preprints/Exponential-decay-in-two-dimensional-classical-On-models-September-23-2026/` (20 pp, Lean-formalized
  via `lean/ComparatorChallenges/ClassicalON.lean`): all-temperature exponential decay for n >= 3. Mechanism:
  fourth variation in two noncommuting rotation directions -> annulus twist Z(pi)/Z(0) >= 1 - O(1/log N) ->
  sign-cluster crossing -> exponential decay. Fails for n = 2 (BKT), as it must.
- `preprints/An-Isolated-Particle-Pole-for-the-Two-Dimensional-O3-Spin-Field-October-4-2026/` (26 pp).

## O(3) architecture (from the intro)
1. Preliminary (non-sharp) mixing length X(beta) = C exp((4 pi - eta) beta), uniform under bond weakening.
   True scale is ~ e^{2 pi beta}/beta, so the a priori exponent is strictly below TWICE the truth.
2. Exact blocking (angular integration), carrying sources; kinetic coupling normalized each step.
3. Irrelevant remainder contracts nearly like L^{-2} per step (inversion + tangent reflection cancel the
   next cross term).
4. Effective-density comparison across cutoffs at a fixed physical box of side M: error ~ C_H M^2 L^{-(2-u)K}.
   Mixing length in physical units at reference depth K: a_K X(beta_K) = L^{(1 - eta/(2 pi))K + o(K)}.
   So the box can be much larger than the mixing length while the comparison error -> 0. A finite-box decay
   criterion at one cutoff transfers to all finer cutoffs, which gives a uniform physical mass.
5. Sources -> field normalization B_N; continuum Schwinger functions; OS reconstruction; gap; non-Wick 4-pt.
6. Canonical uniqueness: sensitivity lemma for the marginal kinetic increment; inclined blocking with length
   factor 5 (3-4-5 triangle) gives a rotation by an irrational multiple of pi, which restores rotation invariance.

## First-pass 4D translation of the window condition (to be checked)
- 4D: dimension-6 irrelevant operators contract like L^{-2}. Box volume factor is M^4.
- Wilson action, SU(N), beta = 2N/g^2: xi ~ exp(c* beta) with c* = 1/(4 N b0) = 12 pi^2 / (11 N^2)
  (b0 = 11N/(48 pi^2)). SU(2): c* = 3 pi^2/11 ~ 2.69. SU(3): c* = 4 pi^2/33 ~ 1.20.
- Suppose we had an a priori bound X(beta) = exp((1+delta) c* beta). Then a_K X(beta_K) ~ L^{delta K}.
  We need M >> L^{delta K} and M^4 L^{-(2-u)K} -> 0, so delta < (2-u)/4 ~ 1/2.
  (2D check: M^2 L^{-(2-u)K} with L^{delta K} gives delta < 1, i.e. an a priori exponent < 2x the truth,
  which matches 4 pi - eta < 2 * 2 pi.)
- So 4D needs an a priori weak-coupling mass-gap bound whose exponent is within a factor ~3/2 of
  asymptotic freedom. Today no exponential a priori bound of any kind is known for 4D non-abelian lattice YM
  at weak coupling. That looks like the crux. (U(1) in 4D has a massless Coulomb phase, so such a bound must
  use non-abelian structure, just as the O(n) argument must fail for n = 2.)

## Plan (ultracode)
- WF1 (research): 4 repo deep-readers + 3 literature/physics agents + 1 quantitative-analysis agent.
  Dossiers go to this directory.
- WF2 (design): independent roadmap proposals from different angles, then a judge panel.
- WF3 (verify): adversarial checks of factual and quantitative claims.
- Final report goes to `reports/`.

## Checks and observations made while WF1 runs (main thread)

### Check: rotation invariance via quaternions (scripts/quaternion_rotations.py)
The 48 Lipschitz quaternions of norm 5 give integer matrices with M^T M = 5I under left and right
multiplication. The isoclinic angle arccos(1/sqrt 5) is an irrational multiple of pi: (1+2i)^k is never
real, because 1+2i and 1-2i are non-associate Gaussian primes. Random words have a Haar-distributed
class-angle histogram, and density in SU(2) follows from Lubotzky–Phillips–Sarnak.
Conclusion: the inclined-blocking rotation trick ports to Z^4 (sublattice qZ^4, index 25, scale sqrt 5,
which is multiplicatively independent of L = 2^k). Gauge caveat: block links on a rotated sublattice must
be parallel transports averaged over lattice staircase paths. Messy but standard (Balaban-type averaging).

### How the O(n) decay proof works (read directly: rotation.tex, annulus.tex)
- W(A) = <exp H(A)> is the spin model in an EXTERNAL SO(3) gauge field A on edges. A change of spin variables
  s -> e^{-F}s maps A -> pure gauge plus the non-abelian remainder B = (1/2)[F_x,F_y] + O(F^3). The twist response
  R = -D^2 W along the commutator generator c is controlled by a 4th variation in the a,b directions,
  summed over a family. The large terms form a positive square, and the rest costs ||T||_HS^2 + cross terms.
- Annulus D_N = {N <= |x|_inf <= 2N}. Test modes f = r^{-3/2} phi(x/N) e^{2 pi i p.x/16N}, shells 1 <= r <= N.
  Commutator: lambda_N >= (1/2) sum 1/r ~ log N. Costs: O(log N). So twist stiffness R <= C_beta/log N, and
  Z(pi)/Z(0) >= 1 - C/log N. Per-shell Dirichlet energy is O(1), i.e. 2D scale invariance gives the log.
- Constants: K_rot = 6 beta^2 + 4 beta^{3/2} + beta. Hence the mixing length from this route alone is roughly
  exp(C beta^2), NOT exp(c beta). The near-sharp a priori bound needs the separate O(4)/O(3) "preliminary
  mixing" machinery.

### STRUCTURAL OBSTRUCTION to a direct 4D port (my analysis; to be adversarially checked)
1. The O(n) mechanism uses a non-abelian GLOBAL symmetry (O(3)) and its background gauge field. In YM the
   only global symmetry is the center 1-form symmetry, and higher-form symmetries are always abelian
   (Gaiotto–Kapustin–Seiberg–Willett 2014). The background for that symmetry is a discrete Z_N 2-form, i.e.
   't Hooft flux. There is no continuous non-abelian background whose commutators can be used.
   Center-free groups (G2, F4, E8) have no 1-form symmetry at all, yet are expected to be gapped.
2. Bulk changes of link variables U -> e^A U preserve Haar measure. They give only Schwinger–Dyson
   (Makeenko–Migdal / Chatterjee master-loop) identities, never a nontrivial "response W(A)".
3. A non-trivial twist must therefore come from BOUNDARY data that is not gauge-trivial: e.g.
   Schrödinger-functional boundary holonomies on T^3 x [0,T]. On T^3, deforming the commuting abelian boundary
   holonomies in non-commuting directions produces boundary curvature ~ [a,b] at second order. That is the
   formal analogue of B = (1/2)[F_x,F_y]. Open: is there a multiscale family whose commutator response grows
   like log N in 4D? (4D YM is classically scale invariant, so each dyadic shell should cost O(1).)
   U(1) must fail (Coulomb phase), which is consistent because all commutators vanish.
4. The 2D "sign cluster" step is analogous to the SU(2) -> Z_2 center decomposition (Mack–Petkova,
   Tomboulis–Yaffe vortex free energy). This parallels Tomboulis's 2007 claimed confinement proof, which
   was critiqued by Ito–Seiler. It is not available for center-free G.

### Where the crux sits in the O(3) architecture (main-thread derivation; WF1 'quant' will verify)
- The RG only runs in the WEAK-coupling regime (terminal kinetic coupling H at the physical block scale). Mass
  generation (strong coupling) is handled entirely by the a priori lattice bound at a reference depth K,
  transferred to all finer cutoffs by the density comparison. The comparison window needs
  a/a* < 1 + p/d.
  2D: p=2, d=2 gives < 2 (the paper has 4pi - eta vs 2pi). 4D: p=2, d=4 gives < 3/2.
  Improvement (O(a^2) removed at tree level) leaves O(g^2 a^2) ~ L^{-2K}/K, so p stays 2 up to logs.
- So the IR crux is a purely lattice statement:
  (A) 4D SU(N) Wilson LGT at large beta has a full transfer gap m(beta) >= exp(-a beta) with
      a < (3/2) c*, where c* = 12 pi^2/(11 N^2), robust under the perturbations the comparison needs.
  Currently no exponential bound of ANY kind is known at weak coupling, and even "mass gap at every beta"
  for 4D lattice SU(2) is open.
- Robustness plus RG would self-improve: an a priori bound applied to the RG-effective theory at the scale
  where the effective coupling is H gives sharp exponents (compare the O(4) "sharp" paper). Robustness to
  Balaban-type effective actions is the catch.

### The a priori bound in the repo is a ONE-SIDED, NON-PERTURBATIVE, ONE-LOOP RG FOR THE STIFFNESS
(read directly: O(3) preliminary.tex lines 60-720; O(4) preliminary.tex lines 805-880)
- The stiffness H_Q of a pinned square is (contact term) - Var(current), uniformly over ALL boundary pins and
  bond weakenings. Trivially H <= b.
- Iteration: tile S = l*R into l^2 cells and condition on the cell boundary "rings". The variance identity
  H_Q(A,A) = v|A|^2 - Var J(A) holds, with auxiliary Gaussian noise of covariance v - H_c. Var J(A) is
  bounded below by Cauchy–Schwarz against the divergence of a test array. The test array uses commuting
  "potential directions" (rotation profiles u_i = chi phi_i/|k_i|), and the NON-ABELIAN derivative
  d_i J(F) ~ J(u_i F'), with F' = -a x F, supplies the signal.
- Gains: O(3) gives Var J >= log(l)/(4 pi), so log xi <= 4 pi b, against the truth 2 pi b; the coefficient 1/2
  in the Ward identity costs a factor 2. O(4) gives Var J >= log(l)/pi, so log xi <= pi b + C sqrt(b log b),
  which is SHARP in the exponent (= one-loop rate 2/(2 pi)). A strict saving eta for O(3) comes from the
  first square: the one-site Fisher-information bound gives M = E z^2 >= 7u/8, so the contact is
  <= 1 - 7u/8.
- So the bound proves "stiffness decreases at least at rate kappa per unit log scale", with
  kappa = (fraction of the one-loop rate). The 2D window needs kappa > 1/2 of the one-loop rate
  (O(3): exactly 1/2, plus the strict saving). The 4D window (a/a* < 3/2) would need kappa > 2/3 of b0.

### Candidate 4D analogue: "magnetic stiffness iteration" (my proposal; needs adversarial check)
- 2D rotation profile u          <-> 4D background gauge potential delta A (amplitude ~1/|k|)
- 2D Dirichlet energy ||grad u||^2 <-> 4D YM energy ||d delta A||^2 (scale-invariant in 4D)
- 2D pinned-square stiffness H <= b <-> 4D response of a hypercube with fixed boundary links to a background
  field strength: a worst-case-over-boundary-data Schrödinger-functional coupling, 1/g^2_eff <= beta
- 2D non-abelian derivative (current colour F -> a x F) <-> 4D adjoint action [delta A, .] in the covariant
  derivative
- Physics check: 4D YM is marginal, and the one-loop vacuum polarisation is log-divergent, coming from the
  second moment of a ~1/r^6 current correlator. U(1) gives zero signal, which is consistent with the Coulomb phase.
- Problems already visible:
  (P1) The 2D potential directions are background fields for a GLOBAL symmetry. 4D gauge theory has no such
       symmetry, so the directions must be non-pure-gauge background shifts. The first variation is then the
       YM equation-of-motion current, and the structure of the Ward identities changes.
  (P2) Naive 4D mode sums: T = sum |k|^{-2} ~ K^2 (a power). Then Var >= vT/(v + C T) ~ v/C, i.e. a
       geometric stiffness decrease, which is impossible physically. So the crossed-array and weighted-current
       estimates (which rely on 2D convolution bounds) must fail or be re-weighted. One needs the |k|^{-4}
       weighting so that each dyadic shell is O(1), and must redo all the convolution estimates in 4D.
  (P3) b0 = (N/16pi^2)(4 - 1/3): paramagnetic (spin) minus diamagnetic (orbital), per Nielsen–Hughes.
       A variance-only lower bound sees the paramagnetic side. Must check that the diamagnetic -1/3 does not
       enter with the wrong sign through the contact term, which 2D simply bounds by its max.
  (P4) "Small stiffness => decay": 2D uses the global symmetry (rotating the interior against the boundary)
       plus FERROMAGNETIC (Ginibre/FKG) decompositions to pass from centred one-site observables to all local
       observables. Neither exists for non-abelian LGT. The 4D replacement must show that small magnetic
       stiffness implies an effective strong-coupling regime at the coarse scale with ALL effective couplings
       controlled, followed by an Osterwalder–Seiler cluster expansion.

### Sharper obstruction: why the 2D stiffness induction cannot even START for a gauge field (main-thread analysis)
- 2D: rotating site spins by a fixed profile R_a(f_x) changes a bond by q_x . R_a(f_y - f_x) q_y. This is exact and
  independent of the configuration, because the global rotation cancels. So the trivial contact bound is
  b * sum_e (f_y - f_x)^2, i.e. b times the classical Dirichlet energy, uniformly over all pins. That makes
  "H_Q <= b" a valid induction START.
- 4D gauge: the variables live ON links. The analogue of a site rotation is a gauge transformation, which is an
  exact symmetry with zero response. The analogue of a background field is a fixed smooth Lie-algebra 1-form u
  acting by U_e -> e^{u_e} U_e. To first order the plaquette changes by
  u_1 + Ad(U_1) u_2 - Ad(U_1 U_2 U_3^{-1}) u_3 - Ad(U_p) u_4.
  For ROUGH U there is no cancellation, so |delta U_p| ~ |u| rather than |du|. Over a box of side R with
  |u| ~ eps/R:
    contact ~ beta * R^4 * (eps/R)^2 = beta * R^2 * eps^2,  versus classical energy beta * eps^2.
  The trivial bound is worse by a factor R^2. Shifting only the boundary links gives a factor R. Haar invariance
  makes any shift of interior-only links trivial. The pure-gauge cancellation happens only after subtracting
  the current variance, i.e. only through the fluctuations, which is circular.
- Hence the gauge analogue of "stiffness" must use a CONFIGURATION-DEPENDENT covariant transport of u (a
  background-field gauge, axial gauge in blocks, or a covariant harmonic extension). Such changes of variables have
  Jacobians, are ill-defined at large fields (Gribov, Singer), and need a small-field/large-field split. That is
  exactly Balaban's machinery.
  CONCLUSION: the repo's non-perturbative a priori bound has no gauge analogue "for free". Any 4D version will be
  a Balaban-type gauge-covariant RG statement, not a soft Ward-identity argument.
- Remaining candidate soft observables (which ARE gauge-invariant monotone-ish quantities):
  (i) 't Hooft-flux / center-vortex free energies F_v(L) (Tomboulis–Yaffe inequalities; not for center-free G);
  (ii) the Schrödinger-functional coupling with FLAT abelian boundary data (smooth, not arbitrary pins);
  (iii) Wilson-loop/Creutz-ratio monotonicity (no known general inequalities for non-abelian G);
  (iv) gradient-flow coupling g_GF^2(t) (Lüscher 2010), defined via E(t) = <t^2 E> on flowed fields.
  None has a known uniform-over-boundary-data induction.

### The finite-volume gap criterion (purity bootstrap) DOES port to 4D LGT (scripts/purity_bootstrap_4d.py)
- 4D test: Delta(n) = 16 log Z(n;n,n,n) - log Z(2n;2n,2n,2n). The factor 2^4 cancels the 4-volume free energy.
  Telescoping: Delta = 8p + 4q_1 + 2q_2 + q_3, with all terms >= 0, given RP/positive transfer in all 4 directions.
  The rectangle identity p(n; w with w_i doubled) = 2p - 2q_i + q_i(2n) holds in each direction (checked on random data).
- Recursion: bound p(r; 2r,2r,2r) <= C Delta via the 3 rectangle identities, square (dimension-free lemma),
  and likewise for the q_i, using the transfer operator in direction i. Result: Delta(2r) <= C' Delta(r)^2 with some
  C' ~ 10^2-10^3. Not computed; it is mechanical.
- Gauge specifics: Z = Tr_{gauge-inv} K^n. Integrating the temporal links projects onto Gauss-law states, the
  Lüscher 1977 transfer matrix is positive self-adjoint, and the Wilson action is RP (Osterwalder–Seiler 1978).
  So "finite box with small Delta at bounded physical size => full gap in infinite volume" is NOT the obstacle.
- The obstacle is making Delta small on a box of physical size O(1/Lambda), i.e. lattice side ~ xi(beta),
  uniformly as beta -> infinity. Feasible ways in: (a) the a priori bound (missing); (b) RG + comparison
  (needs (a)); (c) a direct non-perturbative small-volume-to-large-volume step-scaling argument (Lüscher
  finite-size "step scaling", as an analytic statement, is open).

### Two regimes for the "a priori bound + comparison" architecture (from the O(4) intro, lines 400-470)
- O(4): the a priori exponent is SHARP (pi*beta, plus a subleading sqrt(beta log beta)), so Xi(beta_K)/L^K = exp(O(sqrt(K log K))).
  The comparison only needs |D_N - D_K| <= C e^{-dK} for coarse sides with (2M)^2 <= e^{cK} and arbitrary small c > 0.
  Choosing log M_K = K^{3/4} works. A WEAK, non-quantitative contraction suffices.
- O(3): the a priori exponent is 2x too large minus eta, so the comparison must be QUANTITATIVE:
  delta_K = L^{-(2-u)K} with M^2 delta_K -> 0 and M >> X(beta_K)/L^K = L^{(1-eta/2pi)K}.
- General: for a priori exponent a and true exponent a*, the window is a/a* < 1 + p/d, where p is the
  contraction exponent. If a = a* (up to subexponential terms), any p > 0 works.
- 4D: an a priori bound with a < 1.5 c* plus O(a^2)-quality contraction, OR a sharp bound plus any contraction.

### Core reason the 2D twist mechanism has no 4D analogue (main-thread; to be stress-tested in WF3)
- 2D O(n): the "stiffness" is the response to twists of a non-abelian GLOBAL symmetry, through an external field
  A for that symmetry. The identity W(dF) = W(B), with B = (1/2)[F_x,F_y] + ..., says that abelian-gradient twists
  cost only through commutators. Mass gap there = disordering of the global symmetry.
- 4D lattice YM: an external field for the gauge symmetry is absorbed by Haar invariance except on pinned boundary
  links. The boundary gauge group acts on boundary data, and Z is invariant. A constant gauge rotation of the inner
  boundary relative to the outer is undone by an interior gauge transformation AT ZERO COST, since G is connected.
  So there is NO twist stiffness for gauge rotations.
- Gauge-invariant "twists" are FLUX data (holonomies): SF electric flux, 't Hooft magnetic/center flux. These
  are not symmetries, so there are no exact Ward identities and no commutator identity of W(dF) = W(B) type.
- The 1-form (center) symmetry is the only global symmetry, and it is discrete and abelian (Z_N). Disordering it
  = confinement (Tomboulis–Yaffe vortex free energy). The O(n) proof needs a CONTINUOUS non-abelian symmetry, and
  it must fail for discrete symmetries (2D Ising orders). Center-free G (G2, F4, E8) have no 1-form symmetry
  but are still gapped.
- So the mass gap in 4D is NOT a symmetry-disordering statement. The only known all-coupling non-perturbative
  confinement proof in d >= 3 is Göpfert–Mack (3D U(1), monopole Coulomb gas, CMP 1982). That mechanism is abelian.

### The fixed-theory reformulation (useful framing)
- With complete-density RG control down to a FIXED terminal coupling H, plus convergence of terminal effective
  densities as depth N -> infinity (the "renormalized trajectory"/perfect action at coupling H), the purity
  test Delta(M_0) is an open condition stable under small perturbations of the density.
- So, modulo the UV program, the Clay gap reduces to: "ONE fixed lattice theory (the limiting terminal effective
  density at coupling H) has Delta(M_0) <= 2^{-10} for some box M_0", i.e. a mass gap for a single fixed,
  non-local, intermediate-coupling lattice gauge theory.
- The obstruction is then the classic intermediate-coupling gap: strong-coupling expansions converge only for
  small beta, and Balaban-type RG needs small g at every scale. Bridging options: (a) a new non-perturbative a
  priori bound; (b) computer-assisted bridging (rigorous interval-arithmetic RG/cluster expansions at
  intermediate coupling; cf. repo family 268 seeding the bootstrap by certificates). That is plausible in principle
  but enormous, since the effective-action space is infinite-dimensional; (c) a new mechanism.

### CRUX REFORMULATION (main thread, 14:30)
Taking the O(3)/O(4) architecture as the template, the Clay problem splits into:
(UV) Balaban-type gauge-covariant exact RG with complete-density control to a fixed weak terminal coupling H, endpoint
     comparison across depths with contraction delta_K ~ L^{-(2-u)K}, sources/composite operators (Tr F^2), OS,
     rotation restoration (quaternion inclined blocking), canonical normalization, and AF at short distances.
     Huge (Balaban's UV stability alone was ~14 CMP papers) but "conventional": no new non-perturbative idea visible.
(IR) A purely LATTICE statement about the Wilson action:
  (Q) exists a < (3/2)c*, c* = 12 pi^2/(11 N^2) [SU(N)], with Delta_beta(n) <= C beta^p n^p exp(-c n/X(beta)) for
      n >= C X(beta), X(beta) = exp(a beta), for all large beta. Uniform under plaquette weakening.
      (A sharp a = c* + o(1) would let any contraction rate suffice.)
  Even the qualitative "gap > 0 for all beta" is OPEN for 4D SU(2). Nothing is known at weak coupling.
A natural way to get (Q) would mirror the 2D stiffness iteration:
  (Q1) Non-perturbative one-sided step scaling: for a gauge-invariant finite-volume coupling g(L) (worst case
       over a boundary-data class), 1/g^2(lL) <= 1/g^2(L) - kappa log l + errors at weak coupling, with
       kappa > (2/3)(2 b0). It must also continue to decrease at intermediate coupling (2D "short steps").
  (Q2) Small 1/g^2(L) => Delta small on boxes of side ~L (coarse links nearly Haar => cluster expansion).
The 2D proof of the (Q1)-analogue uses a CONTINUOUS NON-ABELIAN GLOBAL SYMMETRY (spreadable twists, contact <= b,
commutator Ward identity). 4D YM has none. Its only global symmetry is the discrete abelian center 1-form
symmetry, and U(1) (the only continuous 1-form case) is gapless. So (Q1) needs a non-symmetry mechanism. That is
the genuinely missing idea.

### Why "small coarse coupling => gap" fails without a non-abelian mechanism: the free-photon test
- 3D non-compact U(1): coarse block links e^{i Phi} have Var Phi ~ e^2 l -> infinity, so they are nearly Haar and
  nearly independent (covariances ~ e^{-e^2 l} r^{-3}). Yet the theory is massless: power-law tails in r.
  In 2D, the O(n) proof turns near-Haar coarse orientations into decay of CHARGED observables by randomizing the
  global symmetry. It then reaches neutral observables via Ginibre/FKG. Gauge theory has only neutral observables
  and no such inequalities. So any IR argument must use non-abelian structure at the level of NEUTRAL dynamics
  (e.g. orbit-space curvature, Singer 1981; KKN Jacobian in 2+1D; center vortices; ...).

### 3D YM as a milestone (main thread)
- 3D: g^2 has mass dimension 1, beta = 2N/(g^2 a), xi/a ~ beta (power law). Dimension-6 operators give contraction
  p = 2. Window for an a priori bound X(beta) = beta^a: need M >> L^{(a-1)K} and M^3 L^{-(2-u)K} -> 0, so a < 5/3.
- Balaban proved UV stability for 3D lattice pure gauge (CMP 102, 1985). Continuum limit (correlations, uniqueness),
  OS and the mass gap are open. The 3D IR crux is "gap >= c beta^{-a}, a < 5/3, robust" (a power law). Classical
  scaling makes the dimensionless coupling grow like l/beta for free, but the free-photon test shows that this
  alone does not give a gap.
- 3D compact U(1): Göpfert–Mack proved a gap at all beta (monopoles), but with exponentially small mass. The
  mechanism is abelian and specific.
