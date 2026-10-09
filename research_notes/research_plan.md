# Research plan toward a critical line theorem

The primary proposed direction is to understand higher moments of the
repository's original Möbius family. A second direction is a genuinely
parameterized continuation bootstrap. Both require new mathematics.

## Current decision after the coprime test

The follow-up `coprime_reflection.md` derives the cubic Gauss conversion and
an exact bilinear unfolding of the divisor weight. The elementary reduction
to the existing canonical family loses a factor \(D\) and is outside its
scale range. Ordinary uncentered mean-square estimates also introduce an
oversized artificial diagonal that must be canceled, not ignored.

The next input should therefore be a **centered bilinear dispersion estimate**,
not a higher moment obtained by an unchanged iteration of the existing
argument. The quantified obstruction applies to those proposed reductions,
not to every possible theta method.

References and status conventions are in `references.md` and `README.md`.

## Fourth moment calculation and its current boundary

The expansion and Poisson calculation described below have now been carried
out in `fourth_moment.md`. That note retains every gcd pattern and proves an
elementary \(D^{5+\varepsilon}\) bound at the pilot scale. It does **not**
prove P4: the remaining off-diagonal target R4 needs a further \(D^{5/3}\)
saving. The next task is a Möbius-sensitive estimate for the explicit sum R.

### The proposed pilot estimate

Use \(A_u(D)\), \(K\), \(S\), and \(W\) from `exponent_analysis.md`.
A precise ambitious pilot target is

\[
 \sum_{0<Nu\le D^{4/3}}|A_u(D)|^4
     \ll_{\nu,S,W,\varepsilon}D^{10/3+\varepsilon}.
 \tag{P4}
\]

**P4 is unproved.** If it held for all smooth tests for the required fixed
character, the replica argument would give
\(A_1(D)\ll D^{7/9+\varepsilon}\). This would already be a substantial
new result, not a routine preliminary exercise. P4 alone would not prove RH.

### An exact expansion to begin with

Put
\(a_{\mathfrak n}=\mu_K(\mathfrak n)\nu(\mathfrak n)W(N\mathfrak n/D)\),
with the exclusions understood. Then

\[
\begin{aligned}
\sum_{0<Nu\le H}|A_u(D)|^4
={}&\sum_{\mathfrak n_1,\ldots,\mathfrak n_4}
 a_{\mathfrak n_1}a_{\mathfrak n_2}
 \overline{a_{\mathfrak n_3}a_{\mathfrak n_4}}\\
 &\quad\times\sum_{0<Nu\le H}
 \chi_{\mathfrak n_1}(u)\chi_{\mathfrak n_2}(u)
 \overline{\chi_{\mathfrak n_3}(u)\chi_{\mathfrak n_4}(u)}.
\end{aligned}
\]

This finite identity does not require any conjecture. It is the correct place
to start a Poisson calculation, with all common prime factors retained.

### A small diagonal lemma

**Derived.** On the squarefree column support, the exponent of a given local
sextic character in the inner product is

\[
 v_{\mathfrak p}(\mathfrak n_1)+v_{\mathfrak p}(\mathfrak n_2)
 -v_{\mathfrak p}(\mathfrak n_3)-v_{\mathfrak p}(\mathfrak n_4)
 \in\{-2,-1,0,1,2\}.
\]

Away from the excluded primes, the local character has order six. By CRT the
product induces a principal character exactly when every such exponent is
0 modulo 6, which here means 0. Thus the principal-character tuples satisfy

\[
 \mathfrak n_1\mathfrak n_2=\mathfrak n_3\mathfrak n_4.
\]

This diagonal includes more than the two pairwise permutations. For each
\((\mathfrak n_1,\mathfrak n_2)\) there are at most
\(\tau_K(\mathfrak n_1\mathfrak n_2)\ll_\varepsilon D^\varepsilon\)
possible divisor choices for \(\mathfrak n_3\), with \(\mathfrak n_4\)
then determined. There are \(O_W(D^2)\) first pairs. The sum of the absolute
values of these diagonal contributions is therefore
\(O_{S,W,\varepsilon}(HD^{2+\varepsilon})\), the size sought in P4.
The remaining coprimality masks only reduce this bound; they must still be
kept in any exact transformation.

This elementary diagonal estimate does **not** control the off-diagonal.
It isolates the missing part instead of assuming it is negligible.

### Transformation tasks and remaining work

1. **Done:** all 15 prime-incidence patterns and their zero masks are tabulated
   in `fourth_moment.md`.
2. **Done as a written derivation:** smoothed lattice Poisson, including exact
   conductor, CRT phase, and Ramanujan mask factors. Finite factors are checked
   separately; the analytic theorem is not Lean-formalized.
3. **Coprime test completed:** the exact cubic conversion and bilinear
   unfolding are in `coprime_reflection.md`. A direct canonical reduction loses
   a power and misses the scale hypothesis. A new centered bilinear bound,
   including the reintroduced gcd corrections, remains necessary.
4. Bound the nonprincipal contribution with Möbius-sensitive cancellation.
   A bound for arbitrary bounded coefficients is impossible at the desired
   scale; see the counterexample in `exponent_analysis.md`.
5. **Recorded:** elementary completion gives
   \(\mathcal E_4\ll HD^3+D^{5+\varepsilon}\), not P4. The extra term is not
   suppressed, and no improved zero-free region is claimed.

In the generic coprime four-column configuration the conductor norm can be of
order \(D^4\). The naive dual row scale is then \(D^4/H\), namely
\(D^{8/3}\) at P4, before exploiting further structure. This scale calculation
explains why merely repeating the second-moment proof is not an argument.

The fourth moment in [R7, `lem:plain`] is for **plain** polynomials, with
specific exclusions of principal/finite-family inducing characters and
constraints on marked prime factors. P4 instead concerns Möbius coefficients
and includes the sixth-power replica rows essential for extraction. These
statements are not interchangeable.

## What would turn the pilot into RH

One sufficient endpoint is HM from `exponent_analysis.md`: every fixed even
moment at \(H=D^3\), with square-root-sized moments for the original sums.
There are at least three new obligations beyond a finite-moment result:

- A recursion that closes for arbitrarily large fixed moment order without
  an exponent loss bounded away from zero.
- Control of all new principal configurations. Starting at order \(2m\) with
  \(m\ge6\), local exponent differences can be nonzero multiples of six;
  principal products need no longer have equal numerator and denominator
  ideals. Those resonances must be classified, not replaced by pairings.
- Fixed-order control of transformed weights, character twists, common masks,
  and principal residues. Constants can deteriorate with the chosen moment
  order, but must be independent of the growing scale.

An estimate proved only after assuming GRH would verify consistency, not
resolve the problem. The ultimate Möbius bound must be unconditional.

## Alternative a true bootstrap for the zero free boundary

Let \(\mathcal Z(b)\) mean that all primitive finite-order Hecke L-functions
in the relevant family are zero-free for \(\Re s>b\), with poles excluded.
A sufficient new theorem would be, for one fixed \(0<r<1\),

\[
 \mathcal Z(b)\Longrightarrow
 \mathcal Z\bigl(\tfrac12+r(b-\tfrac12)\bigr),
 \qquad \tfrac12<b\le\tfrac78.
 \tag{B}
\]

Once the repository's initial \(\mathcal Z(7/8)\) is independently validated,
iteration gives boundaries tending to \(1/2\). Any hypothetical zero to the
right would eventually be excluded. No bound uniform in the iteration count
is needed for this logical conclusion; each application must be justified.

**B is unproved.** The existing common-signal lemma is flexible enough to
state the continuation step, but the supplied probe estimates do not prove B:

- The current low bound crosses the signal at \(7/8\).
- The plain marked-moment input only covers \(\kappa\ge3/4\); approaching the
  critical line would force \(\kappa=2\beta_*-1\to0\).
- Euler-factor holomorphy, detector floors, prime supply, and all contour and
  approximation errors must survive the new parameter regime.

A useful optimization experiment would expose **all** these constraints as
variables and derive a certified feasible region. Optimizing just the final
endpoint polynomial would be misleading. If a barrier appears, identify the
specific analytic lemma that fixes it.

## Other proof interfaces worth keeping distinct

These are alternate ways to finish, not additional premises that can simply
be combined with a zero-free half-plane.

| Direction | What would suffice | Main missing requirement |
| --- | --- | --- |
| Li positivity | For \(\xi(s)=\tfrac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)\), prove \(\lambda_n=\left.\frac1{(n-1)!}\frac{d^n}{ds^n}[s^{n-1}\log\xi(s)]\right|_{s=1}\ge0\) for every \(n\ge1\) [C3] | An unconditional all-index positivity mechanism, not a finite list of positive coefficients |
| Hilbert–Pólya | Construct a self-adjoint operator whose spectral determinant agrees with \(\xi(1/2+it)\) up to an entire zero-free factor [C2] | An actual domain, self-adjointness, and a complete spectral identity covering every zero; matching statistics is insufficient |
| Heat deformation | Prove the de Bruijn–Newman constant \(\Lambda\le0\); Rodgers–Tao prove \(\Lambda\ge0\), so the target is exactly 0 [C4] | All-zero control down to zero deformation; a positive upper bound cannot be rounded to zero |
| Jensen polynomials | Prove hyperbolicity for every required degree and shift [C5] | Fixed-degree eventual results leave infinitely many degree-dependent exceptional cases |

For an infinite-dimensional positivity or spectral proposal, finite matrix
checks need a proved convergence theorem and tail control. Those are part of
the proof, not implementation details.

## What does not count as resolving RH

- Checking more zeros alone. Platt–Trudgian rigorously verified all zeros up to
  ordinate \(3\cdot10^{12}\) using interval arithmetic; this is a benchmark,
  not a claim here about the latest record. A finite check can finish a proof
  only after a theorem reduces all remaining cases to that finite range. [C6]
- A zero-density bound that still permits any exceptional zeros. Guth–Maynard's
  large-value work provides important density estimates, not an exclusion of
  every zero. [C7]
- Treating \(\forall d\,\exists N(d)\,\forall n\ge N(d)\) as though only
  finitely many pairs \((d,n)\) remain. This is the quantifier trap in using
  fixed-degree eventual Jensen hyperbolicity. [C5]
- Discarding residue terms, assuming the Mellin numerator is nonzero without
  proof, or shifting a reciprocal contour through unknown zeros.
- Proving an RH-equivalent condition under another unproved RH-strength
  assumption and calling the result unconditional.

A disproof is also a resolution: it would require a rigorously certified zero
in the critical strip with real part different from \(1/2\), for example a
validated zero count in a small rectangle disjoint from the line. A numerical
root finder's approximate output is not such a certificate.

## Milestones and stopping rules

1. **Baseline verification:** the isolated comparator attempt completed setup
   but timed out during solution compilation. Resume the retained warm build
   and review the target definitions; until a verdict is obtained, keep uses
   of the seven-eighths baseline conditional.
2. **Fourth-moment identity:** the local-factor and Poisson calculation is
   written in `fourth_moment.md` and its finite factors are tested. Independent
   review and any desired analytic formalization remain.
3. **A stronger estimate:** the elementary replacement bound W4 is proved in
   the notes. Improve it toward P4 with all ranges and losses retained. Stop any
   derivation that would also prove the false arbitrary-coefficient bound.
4. **Critical-line mechanism:** prove a moment hierarchy or bootstrap with an
   actual limit at \(1/2\). A sequence converging to a larger boundary is not RH.
5. **Independent validation:** translate the successful analytic argument into
   a minimal formal target, check axioms and definitions, and obtain specialist
   review of the analytic number theory and its formal translation.

The work calls for analytic number theory, metaplectic/theta and large-sieve
expertise, and proof-assistant verification. Hardware and coding help with
local arithmetic, exact inequalities, dependency management, and certified
numerics. None supplies a known substitute for the missing uniform estimate.
