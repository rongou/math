#!/usr/bin/env python3
"""Reproducible finite SU(2) transfer-interface diagnostics (standard library).

Preserves and strengthens the temporary check_interface.py described in
../audits/su2_transfer_interface.md, Validation record (2026-10-09).
Original parameters are retained: seed 20261009, periods (4, 5, 4, 5),
beta 3/8 for lattice checks, character truncation 100, and 4096-panel
class-Haar quadrature at beta = 0, 1/8, 1, 3, 10.

Run from the repository root, with Python 3.9 or newer:
    python3 -B research_notes/yang_mills_2026_10_09/checks/check_su2_interface.py

Capture both streams by appending:
    > research_notes/yang_mills_2026_10_09/checks/check_su2_interface_output.txt 2>&1

No dependencies, downloads, sibling-check imports, or filesystem writes.
Assertions below use require(), so python -O does not disable the checks.
The seed and grids are fixed; last-bit float errors may vary by Python/libm.

IMPORTANT: finite matrix samples, finite character sums, and finite quadrature
are DIAGNOSTICS, NOT PROOFS. No full-lattice partition function or physical
transfer spectrum is computed. The exact-rational beta-zero matrix is a
finite constant-kernel model, not a replacement for the Haar Hilbert space.
The mathematical proofs, scope, and primary bibliography remain in the audit.
"""

from fractions import Fraction
from itertools import combinations, product
from math import cos, exp, fsum, pi, sin, sqrt
import random
import sys


SEED = 20261009
PERIODS = (4, 5, 4, 5)
LATTICE_BETA = Fraction(3, 8)
CHARACTER_CUTOFF = 100
QUADRATURE_PANELS = 4096
IDENTITY = (1 + 0j, 0j, 0j, 1 + 0j)
MATRIX_TOL = 1e-11
ACTION_TOL = 1e-10
PAIRS = tuple(combinations(range(4), 2))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def close(actual, expected, tolerance, context):
    error = abs(actual - expected)
    require(error <= tolerance, f"{context}: error {error!r} > {tolerance!r}")
    return error


def mul(a, b):
    """Multiply two row-major 2-by-2 complex matrices."""
    return (
        a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
        a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
    )


def inv(a):
    """Conjugate transpose; an inverse for the SU(2) matrices checked below."""
    return (a[0].conjugate(), a[2].conjugate(),
            a[1].conjugate(), a[3].conjugate())


def chain(*matrices):
    result = IDENTITY
    for matrix in matrices:
        result = mul(result, matrix)
    return result


def matrix_error(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def tr(a):
    trace = a[0] + a[3]
    close(trace.imag, 0, MATRIX_TOL, "SU(2) trace must be real")
    return trace.real


def haar_sample(rng):
    """Normalized Gaussian quaternion; used only for finite test inputs."""
    q = [rng.gauss(0, 1) for _ in range(4)]
    norm = sqrt(sum(x * x for x in q))
    a, b, c, d = [x / norm for x in q]
    return (complex(a, b), complex(c, d), complex(-c, d), complex(a, -b))


def shift(x, direction):
    y = list(x)
    y[direction] = (y[direction] + 1) % PERIODS[direction]
    return tuple(y)


def base_at_zero(x, direction):
    y = list(x)
    y[direction] = 0
    return tuple(y)


def plaquette(links, x, mu, nu):
    return chain(links[x, mu], links[shift(x, mu), nu],
                 inv(links[shift(x, nu), mu]), inv(links[x, nu]))


def electric_argument(links, x, time, spatial):
    """Argument X_i v_end Y_i^{-1} v_start^{-1} in audit (4.7)."""
    return chain(links[x, spatial], links[shift(x, spatial), time],
                 inv(links[shift(x, time), spatial]), inv(links[x, time]))


def wilson_terms(links, sites, beta):
    return {
        (x, mu, nu): float(beta) * tr(plaquette(links, x, mu, nu)) / 2
        for x in sites for mu, nu in PAIRS
    }


def gauge_transform(links, gauge, sites):
    return {
        (x, mu): chain(gauge[x], links[x, mu], inv(gauge[shift(x, mu)]))
        for x in sites for mu in range(4)
    }


def holonomy(links, base, time):
    require(base[time] == 0, "holonomy base must be on slice zero")
    x, result = base, IDENTITY
    for _ in range(PERIODS[time]):
        result = mul(result, links[x, time])
        x = shift(x, time)
    require(x == base, "Polyakov loop failed to close periodically")
    return result


def check_input_matrices(links, gauge):
    worst = 0.0
    for matrix in (*links.values(), *gauge.values()):
        determinant = matrix[0] * matrix[3] - matrix[1] * matrix[2]
        worst = max(worst, abs(determinant - 1),
                    matrix_error(mul(matrix, inv(matrix)), IDENTITY))
        close(tr(matrix), tr(inv(matrix)), MATRIX_TOL, "trace under inversion")
    require(worst <= MATRIX_TOL, "sampled matrices are not numerically SU(2)")
    print(f"SU(2) inputs: determinant/unitarity error={worst:.3g}")


def check_lattice_decompositions(links, sites, beta):
    terms = wilson_terms(links, sites, beta)
    full_log = fsum(terms.values())
    require(len(links) == 4 * len(sites), "independent link count")
    require(len(terms) == 6 * len(sites), "unoriented plaquette count")
    for x, mu, nu in terms:
        support = {(x, mu), (shift(x, mu), nu), (shift(x, nu), mu), (x, nu)}
        require(len(support) == 4, "plaquette has repeated independent links")
    print(f"Lattice counts: sites={len(sites)}, links={len(links)}, plaquettes={len(terms)}")

    for time, period in enumerate(PERIODS):
        spatial = [mu for mu in range(4) if mu != time]
        magnetic = [[] for _ in range(period)]
        electric = [[] for _ in range(period)]
        inverse_error = seam_inverse_error = wrong_seam_error = 0.0
        for x in sites:
            t = x[time]
            for i, j in combinations(spatial, 2):
                magnetic[t].append(float(beta) * tr(plaquette(links, x, i, j)) / 2)
            for i in spatial:
                q = electric_argument(links, x, time, i)
                target = inv(plaquette(links, x, time, i))
                error = matrix_error(q, target)
                inverse_error = max(inverse_error, error)
                electric[t].append(float(beta) * tr(q) / 2)
                if t == period - 1:
                    require(shift(x, time)[time] == 0, "seam did not wrap to zero")
                    seam_inverse_error = max(seam_inverse_error, error)
                    # Negative control: reuse X_last instead of the actual X_0.
                    wrong = chain(links[x, i], links[shift(x, i), time],
                                  inv(links[x, i]), inv(links[x, time]))
                    wrong_seam_error = max(wrong_seam_error, matrix_error(q, wrong))
        transverse = len(sites) // period
        require(all(len(row) == 3 * transverse for row in magnetic), "spatial slice count")
        require(all(len(row) == 3 * transverse for row in electric), "electric slice count")
        require(inverse_error <= MATRIX_TOL, "electric orientation mismatch")
        require(wrong_seam_error > 1e-3, "fixed-seed wrong-seam control was not detected")
        multiplicity = [Fraction(0) for _ in range(period)]
        pieces = []
        for t in range(period):
            following = (t + 1) % period
            multiplicity[t] += Fraction(1, 2)
            multiplicity[following] += Fraction(1, 2)
            pieces.extend((fsum(magnetic[t]) / 2, fsum(electric[t]),
                           fsum(magnetic[following]) / 2))
        require(all(value == 1 for value in multiplicity), "half magnetic weights did not glue")
        error = close(fsum(pieces), full_log, ACTION_TOL, f"direction {time} cyclic action")
        print(
            f"Direction {time}: period={period}, N={transverse}, seam_plaquettes={3 * transverse}, "
            f"action_error={error:.3g}, inverse_error={inverse_error:.3g}, "
            f"seam_inverse_error={seam_inverse_error:.3g}, wrong_seam_control={wrong_seam_error:.3g}"
        )
    return full_log


def check_gauge_covariance(links, gauge, sites, beta, full_log):
    transformed = gauge_transform(links, gauge, sites)
    plaquette_error = electric_error = holonomy_error = 0.0
    for x in sites:
        for mu, nu in PAIRS:
            expected = chain(gauge[x], plaquette(links, x, mu, nu), inv(gauge[x]))
            plaquette_error = max(plaquette_error,
                                  matrix_error(plaquette(transformed, x, mu, nu), expected))
        for time in range(4):
            for spatial in range(4):
                if spatial == time:
                    continue
                # g_t and g_{t+1} are independent endpoint gauge functions,
                # including g_last and g_0 across the periodic seam.
                expected = chain(gauge[x], electric_argument(links, x, time, spatial),
                                 inv(gauge[x]))
                electric_error = max(electric_error,
                                     matrix_error(electric_argument(transformed, x, time, spatial),
                                                  expected))
            if x[time] == 0:
                expected = chain(gauge[x], holonomy(links, x, time), inv(gauge[x]))
                holonomy_error = max(holonomy_error,
                                     matrix_error(holonomy(transformed, x, time), expected))
    require(max(plaquette_error, electric_error, holonomy_error) <= MATRIX_TOL,
            "local/endpoint/periodic-holonomy gauge covariance failed")
    action_error = close(fsum(wilson_terms(transformed, sites, beta).values()), full_log,
                         ACTION_TOL, "gauge-invariant Wilson action")
    print(f"Gauge covariance: plaquette_error={plaquette_error:.3g}, "
          f"independent_endpoint_error={electric_error:.3g}, "
          f"holonomy_error={holonomy_error:.3g}, action_error={action_error:.3g}")


def check_temporal_gauge_and_seams(links, sites, beta, full_log):
    for time, period in enumerate(PERIODS):
        gauge, retained = {}, {}
        for base in sites:
            if base[time] != 0:
                continue
            x, cumulative = base, IDENTITY
            for _ in range(period):
                gauge[x] = cumulative
                cumulative = mul(cumulative, links[x, time])
                x = shift(x, time)
            retained[base] = cumulative
        transformed = gauge_transform(links, gauge, sites)
        open_error = closing_error = 0.0
        for x in sites:
            if x[time] == period - 1:
                expected = retained[base_at_zero(x, time)]
                closing_error = max(closing_error, matrix_error(transformed[x, time], expected))
            else:
                open_error = max(open_error, matrix_error(transformed[x, time], IDENTITY))
        require(max(open_error, closing_error) <= MATRIX_TOL, "partial temporal gauge failed")
        require(max(matrix_error(h, IDENTITY) for h in retained.values()) > 1e-3,
                "fixed-seed closing holonomies unexpectedly all trivial")
        action_error = close(fsum(wilson_terms(transformed, sites, beta).values()), full_log,
                             ACTION_TOL, "partial temporal gauge action")
        print(f"Temporal gauge {time}: nonclosing_identity_error={open_error:.3g}, "
              f"retained_holonomy_error={closing_error:.3g}, action_error={action_error:.3g}")

        # Deterministic negative control, independent of random cancellations.
        # All links are I except one CLOSING temporal link H=diag(i,-i).
        # Six seam plaquettes have trace 0 instead of 2. Erasing H changes the
        # exponent by exactly 6*beta and changes its Polyakov trace from 0 to 2.
        witness = {key: IDENTITY for key in links}
        endpoint = [0] * 4
        endpoint[time] = period - 1
        endpoint = tuple(endpoint)
        h = (1j, 0j, 0j, -1j)
        witness[endpoint, time] = h
        witness_terms = wilson_terms(witness, sites, beta)
        changed = [key for key, value in witness_terms.items() if value != float(beta)]
        require(len(changed) == 6, "closing-link witness must affect six plaquettes")
        require(all(x[time] == period - 1 and time in (mu, nu) for x, mu, nu in changed),
                "closing-link witness affected a non-seam plaquette")
        require(holonomy(witness, (0, 0, 0, 0), time) == h, "closing holonomy lost")
        close(tr(h), 0, 0, "nontrivial closing holonomy trace")
        before = fsum(witness_terms.values())
        witness[endpoint, time] = IDENTITY  # Deliberately incorrect periodic gauge fixing.
        after = fsum(wilson_terms(witness, sites, beta).values())
        close(after - before, float(6 * beta), 0, "erasing closing holonomy action change")
        close(tr(holonomy(witness, (0, 0, 0, 0), time)), 2, 0, "erased holonomy trace")
        print(f"Seam witness {time}: six wrapping plaquettes; erasing holonomy changes "
              f"log_weight by {after - before:g} (negative control detected)")


def rational_matrix_product(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def check_beta_zero(links, sites):
    # Evaluate the actual plaquette and one-step magnetic/electric integrands
    # at zero, before any gauge integration. They must be identically one.
    require(all(exp(value) == 1 for value in wilson_terms(links, sites, 0).values()),
            "beta-zero plaquette weight is not one")
    for time in range(4):
        spatial = [mu for mu in range(4) if mu != time]
        for x in sites:
            for i, j in combinations(spatial, 2):
                require(exp(0.0 * tr(plaquette(links, x, i, j)) / 4) == 1,
                        "beta-zero magnetic half weight")
            for i in spatial:
                require(exp(0.0 * tr(electric_argument(links, x, time, i)) / 2) == 1,
                        "beta-zero electric factor")

    # EXACT finite constant-kernel algebra, not quadrature of a nonconstant
    # function and not a computation of the physical infinite-dimensional K.
    # Nonuniform probability weights catch dropped normalization factors.
    weights = [Fraction(1, 8), Fraction(1, 4), Fraction(3, 8), Fraction(1, 4)]
    require(sum(weights) == 1, "probability measure not normalized")
    gauge_average_of_one = sum(weights)  # The beta-zero gauge integrand is 1.
    k = [[gauge_average_of_one * weight for weight in weights] for _ in weights]
    require(rational_matrix_product(k, k) == k, "beta-zero constant-kernel idempotence")
    require(all(sum(row) == 1 for row in k), "beta-zero vacuum is not fixed")
    require(all(weights[i] * k[i][j] == weights[j] * k[j][i]
                for i in range(4) for j in range(4)), "weighted selfadjointness")
    zero_mean = [Fraction(0), Fraction(1), Fraction(-2), Fraction(2)]
    require(any(zero_mean) and sum(p * f for p, f in zip(weights, zero_mean)) == 0,
            "beta-zero null-vector fixture")
    require(all(sum(a * f for a, f in zip(row, zero_mean)) == 0 for row in k),
            "constant kernel failed to annihilate a nonzero mean-zero vector")
    for n in (1, 2, 4, 5, 8, 16):
        power = k
        for _ in range(n - 1):
            power = rational_matrix_product(power, k)
        require(sum(power[i][i] for i in range(4)) == 1, "beta-zero trace power")
    print("Beta=0: sampled plaquette/magnetic/electric integrands all equal 1 in all directions")
    print("Beta=0 exact finite constant-kernel model: K1=1, K^2=K, weighted K*=K, "
          "nonzero mean-zero null vector; Tr K^n=1 for n=1,2,4,5,8,16")
    print("Beta=0 limitation: rank-one propagation gives D_0(n)=0; the criterion alone "
          "cannot establish nontriviality (proof in audit)")


def coefficients(beta, cutoff=CHARACTER_CUTOFF):
    """Finite tensor-character expansion, with exact multiplicity checks."""
    multiplicities = [1] + [0] * (cutoff + 1)
    b = [0.0] * (cutoff + 1)
    weight = 1.0
    for r in range(cutoff + 1):
        require(sum((ell + 1) * m for ell, m in enumerate(multiplicities)) == 2 ** r,
                f"tensor dimension identity at r={r}")
        require(multiplicities[r] == 1 and all(m >= 0 for m in multiplicities),
                f"tensor multiplicity identity at r={r}")
        if r:
            weight *= beta / (2 * r)
        for ell in range(r + 1):
            b[ell] += weight * multiplicities[ell]
        following = [0] * (cutoff + 2)
        for ell, m in enumerate(multiplicities[:-1]):
            following[ell + 1] += m
            if ell:
                following[ell - 1] += m
        multiplicities = following
    return b


def chi(ell, theta):
    """SU(2) character via recurrence, avoiding sin(theta) division at endpoints."""
    if ell == 0:
        return 1.0
    previous, current = 1.0, 2 * cos(theta)
    for _ in range(1, ell):
        previous, current = current, 2 * cos(theta) * current - previous
    return current


def class_haar_quadrature(beta, ell, panels):
    """FINITE composite Simpson approximation, NOT an exact Haar integral.

    Integrand: (2/pi) sin(theta)^2 exp(beta*cos(theta)) chi_ell(theta).
    No certified quadrature-error or infinite-series-tail bound is supplied.
    """
    require(panels > 0 and panels % 2 == 0, "Simpson panels must be positive and even")
    h = pi / panels
    samples = []
    for i in range(panels + 1):
        theta = i * h
        value = (2 / pi) * sin(theta) ** 2 * exp(beta * cos(theta)) * chi(ell, theta)
        weight = 1 if i in (0, panels) else (4 if i % 2 else 2)
        samples.append(weight * value)
    return fsum(samples) * h / 3


def check_characters():
    print("Finite character/quadrature diagnostics ONLY: not proofs of positivity, "
          "Haar identities, convergence, or trace class")
    for beta in (0.0, 0.125, 1.0, 3.0, 10.0):
        b = coefficients(beta)
        trace_sum = fsum((ell + 1) * value for ell, value in enumerate(b))
        relative_error = abs(trace_sum - exp(beta)) / exp(beta)
        require(relative_error < 1e-13, "finite one-link trace-sum diagnostic")
        if beta == 0:
            require(b[0] == 1 and all(value == 0 for value in b[1:]),
                    "beta-zero character spectrum must have only its constant coefficient")
        else:
            require(all(value > 0 for value in b), "positive beta: tested coefficients not positive")
        worst_error = worst_grid_difference = 0.0
        for ell in range(7):
            fine = class_haar_quadrature(beta, ell, QUADRATURE_PANELS)
            coarse = class_haar_quadrature(beta, ell, QUADRATURE_PANELS // 2)
            tolerance = 5e-12 * max(1, exp(beta))
            worst_error = max(worst_error, close(fine, b[ell], tolerance,
                                                f"finite quadrature beta={beta}, ell={ell}"))
            worst_grid_difference = max(worst_grid_difference,
                                        close(fine, coarse, tolerance, "quadrature grid comparison"))
        print(f"  beta={beta:g}: truncated_trace_rel_error={relative_error:.3g}, "
              f"coefficient_quad_error={worst_error:.3g}, grid_difference={worst_grid_difference:.3g}")


def check_parent_arithmetic():
    coefficient = 16 * 6 * 4 ** 4
    value = coefficient * Fraction(1, 2 ** 26)
    threshold = Fraction(1, 2048)
    require(coefficient == 24576 and value == Fraction(3, 8192) and value < threshold,
            "parent small-beta constant check")
    for n in range(4, 11):
        require(16 * 6 * n ** 4 == 6 * (2 * n) ** 4, "Wilson action-constant cancellation")
    print(f"Exact parent arithmetic: {coefficient}*2^-26={value}<{threshold}; "
          "volume-constant cancellation checked at n=4,...,10")
    print("This checks constants only, not the parent's conditional spectral implication.")


def main():
    require(all(period >= 4 for period in PERIODS), "scope requires all periods >= 4")
    print("SU(2) Wilson transfer interface: reproducible standard-library diagnostics")
    print(f"Python {sys.version.split()[0]}; seed={SEED}; periods={PERIODS}; lattice beta={LATTICE_BETA}")
    print(f"Character cutoff={CHARACTER_CUTOFF}; Simpson panels={QUADRATURE_PANELS} "
          f"and {QUADRATURE_PANELS // 2}; labels=0,...,6")
    print("WARNING: finite samples/truncations/quadrature are DIAGNOSTICS, NOT PROOFS.")
    print("No full-lattice partition-function integration or physical spectrum is computed.")
    rng = random.Random(SEED)
    sites = list(product(*(range(period) for period in PERIODS)))
    links = {(x, mu): haar_sample(rng) for x in sites for mu in range(4)}
    gauge = {x: haar_sample(rng) for x in sites}
    check_input_matrices(links, gauge)
    full_log = check_lattice_decompositions(links, sites, LATTICE_BETA)
    check_gauge_covariance(links, gauge, sites, LATTICE_BETA, full_log)
    check_temporal_gauge_and_seams(links, sites, LATTICE_BETA, full_log)
    check_beta_zero(links, sites)
    check_characters()
    check_parent_arithmetic()
    print("ALL DIAGNOSTIC CHECKS PASSED. Mathematical proofs and caveats are in the audit.")


if __name__ == "__main__":
    main()
