#!/usr/bin/env python3
"""Fifth-pass finite diagnostics, not a 4D SU(2) partition-function calculation.

Standard library only; no downloads, filesystem writes or sibling imports.
Q8 tests use exact integer quaternions; Z2 marginalization uses exact Fractions.
Finite-group integrals are NOT identified with the continuous SU(2) Bessel integral.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import math
import random
import unittest

SEED = 20261009
ONE = (1, 0, 0, 0)
Q8 = tuple(tuple(sign if j == i else 0 for j in range(4))
           for i in range(4) for sign in (-1, 1))


def qmul(a, b):
    w, x, y, z = a
    v, i, j, k = b
    return (w*v-x*i-y*j-z*k, w*i+x*v+y*k-z*j,
            w*j-x*k+y*v+z*i, w*k+x*j-y*i+z*v)


def qinv(a):
    return (a[0], -a[1], -a[2], -a[3])


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def qsum(qs):
    return tuple(sum(q[j] for q in qs) for j in range(4))


def qnorm(q):
    return math.sqrt(dot(q, q))


def qcap(rng, rho):
    v = [rng.gauss(0, 1) for _ in range(3)]
    length = math.sqrt(sum(x*x for x in v))
    theta = rho*rng.random()
    return (math.cos(theta), *(math.sin(theta)*x/length for x in v))


def phase(theta):
    return (math.cos(theta), 0.0, 0.0, math.sin(theta))


def simpson(fun, lo, hi, panels=4096):
    dx = (hi-lo)/panels
    result = fun(lo)+fun(hi)
    result += sum((4 if i % 2 else 2)*fun(lo+i*dx) for i in range(1, panels))
    return result*dx/3


def F_series(t):
    """Positive defining series, bounded arguments only in these diagnostics."""
    term, total = 1.0, 1.0
    for j in range(1, 2000):
        term *= t*t/(4*j*(j+1))
        total += term
        if term <= total*2e-17:
            return total
    raise RuntimeError('series did not converge')


def Fprime_over_F(t):
    if t == 0:
        return 0.0
    term, total, derivative = 1.0, 1.0, 0.0
    for j in range(1, 2000):
        term *= t*t/(4*j*(j+1))
        total += term
        derivative += 2*j*term/t
        if term <= total*2e-17:
            return derivative/total
    raise RuntimeError('derivative series did not converge')


@lru_cache(maxsize=512)
def remainder(t):
    """Stable scaled angular quadrature for -log(exp(-t)*F(t)).

    For large t the transformed Gaussian tail beyond w=16 is omitted;
    this is a numerical diagnostic, not a certified quadrature bound.
    """
    if t == 0:
        return 0.0
    if t < 1e-3:
        return t-math.log(F_series(t))
    scale = math.sqrt(1+t)
    upper = min(math.pi*scale, 16)
    def integrand(w):
        theta = w/scale
        return math.exp(-2*t*math.sin(theta/2)**2)*(scale*math.sin(theta))**2
    integral = simpson(integrand, 0, upper)
    return 1.5*math.log1p(t)-math.log(2/math.pi*integral)


def remainder_bound(t):
    return 0.5+math.log(24)+1.5*math.log1p(t)


def loop_energy(field, word):
    value = ONE
    for e, sign in word:
        value = qmul(value, field[e] if sign == 1 else qinv(field[e]))
    return 1-value[0]


class Lattice:
    def __init__(self, side):
        self.side = side
        self.sites = tuple(product(range(side), repeat=4))
        self.links = tuple((x, mu) for x in self.sites for mu in range(4))
        self.plaquettes = tuple((x, mu, nu) for x in self.sites
                               for mu, nu in combinations(range(4), 2))
        self.words = {p: self.word(p) for p in self.plaquettes}
        self.stars = {e: set() for e in self.links}
        for p, word in self.words.items():
            for e, _ in word:
                self.stars[e].add(p)

    def shift(self, x, axis, amount=1):
        return tuple((v+amount*int(j == axis)) % self.side for j, v in enumerate(x))

    def word(self, p):
        x, mu, nu = p
        return (((x, mu), 1), ((self.shift(x, mu), nu), 1),
                ((self.shift(x, nu), mu), -1), ((x, nu), -1))

    def path_step(self, x, axis, sign):
        return ((x, axis), 1) if sign == 1 else ((self.shift(x, axis, -1), axis), -1)

    def staple_words(self, e):
        x, mu = e
        y = self.shift(x, mu)
        words = []
        for nu in range(4):
            if nu == mu:
                continue
            for sign in (-1, 1):
                words.append((self.path_step(x, nu, sign),
                              ((self.shift(x, nu, sign), mu), 1),
                              self.path_step(self.shift(y, nu, sign), nu, -sign)))
        return words

    def staples(self, field, e):
        values = []
        for word in self.staple_words(e):
            q = ONE
            for f, sign in word:
                q = qmul(q, field[f] if sign == 1 else qinv(field[f]))
            values.append(q)
        return values

    def frozen(self, e):
        return {f for word in self.staple_words(e) for f, _ in word}

    def energies(self, field):
        return {p: loop_energy(field, word) for p, word in self.words.items()}

    def independent(self, removed):
        return all(sum(e in removed for e, _ in word) <= 1 for word in self.words.values())

    def pattern(self):
        return {e for e in self.links if e[1] == 0 and all(v % 2 == 0 for v in e[0][1:])}

    def affected(self, links):
        return {p for e in links for p in self.stars[e]}

    def closure(self, removed, edited):
        neighbors = {d for d in removed if self.frozen(d) & edited}
        return neighbors, edited | neighbors

    def base_plaquettes(self, removed):
        return {p for p, word in self.words.items() if all(e not in removed for e, _ in word)}

    def leading_local(self, field, removed, edited):
        neighbors, _ = self.closure(removed, edited)
        retained_ps = self.base_plaquettes(removed) & self.affected(edited)
        return (sum(loop_energy(field, self.words[p]) for p in retained_ps)
                +sum(6-qnorm(qsum(self.staples(field, e))) for e in neighbors))

    def reflect_vertex(self, x, axis, plane):
        return tuple((2*plane-v) % self.side if j == axis else v for j, v in enumerate(x))

    def reflect_link(self, e, axis, plane):
        x, mu = e
        y = self.reflect_vertex(x, axis, plane)
        return ((self.shift(y, axis, -1), mu), -1) if mu == axis else ((y, mu), 1)

    def reflect_field(self, field, axis, plane):
        output = {}
        for e, q in field.items():
            target, sign = self.reflect_link(e, axis, plane)
            output[target] = q if sign == 1 else qinv(q)
        return output

    def cell_edges(self, x):
        return {(tuple((v+w) % self.side for v, w in zip(x, offset)), mu)
                for mu in range(4) for offset in product((0, 1), repeat=4) if offset[mu] == 0}


class IntegralTests(unittest.TestCase):
    def test_F_zero_and_sphere_normalization(self):
        self.assertEqual(F_series(0), 1)
        self.assertEqual(remainder(0), 0)
        angular_mass = 2/math.pi*simpson(lambda th: math.sin(th)**2, 0, math.pi)
        self.assertAlmostEqual(angular_mass, 1, places=13)
        self.assertAlmostEqual((F_series(0.001)-1)/0.001**2, 1/8, places=7)

    def test_series_and_independent_angular_integral(self):
        for t in (0, 0.01, 0.25, 1, 3, 6, 16, 40, 96):
            value = F_series(t)
            # Normalize integrand at its maximum to avoid large exponentials.
            angular = 2/math.pi*simpson(lambda th: math.exp(t*(math.cos(th)-1))*math.sin(th)**2,
                                      0, math.pi)
            self.assertAlmostEqual(angular/(math.exp(-t)*value), 1, places=10)
            if t:
                ratio = Fprime_over_F(t)
                self.assertTrue(0 < ratio < 1)

    def test_log_remainder_bound_small_and_large_arguments(self):
        for t in (0, 1e-8, 0.01, 1, 6, 40, 100, 10000, 100000000):
            value = remainder(t)
            self.assertGreaterEqual(value, -1e-12)
            self.assertLessEqual(value, remainder_bound(t)+1e-12)
            if 0 < t <= 40:
                self.assertAlmostEqual(value, t-math.log(F_series(t)), places=10)
        h = 1e6
        self.assertGreater(6*h-remainder(6*h), 5*h)
        self.assertLess(remainder_bound(6*h), 100)

    def test_exact_factor_and_leading_remainder_identity(self):
        for h, b in product((1, 3, 10), (0, 0.25, 1, 4, 6)):
            log_integral = -6*h+math.log(F_series(h*b))
            extracted = -h*(6-b)-remainder(h*b)
            self.assertAlmostEqual(log_integral, extracted, places=10)
        self.assertEqual(F_series(0), 1)  # Never divide the Bessel expression by 0.

    def test_zero_staple_cusp_cancels_only_in_the_complete_action(self):
        h = 3
        for angle in (0.01, 0.001):
            # Rotate one +I staple in a 3+ / 3- balanced star: |B|=2sin(|a|/2).
            b = 2*math.sin(angle/2)
            right_minimum_slope = ((6-b)-6)/angle
            left_minimum_slope = ((6-b)-6)/(-angle)
            self.assertLess(right_minimum_slope, -0.99)
            self.assertGreater(left_minimum_slope, 0.99)
            full_change = math.log(F_series(h*b))
            self.assertLess(abs(full_change/angle), 2*h*h*angle)
            self.assertAlmostEqual(-h*(6-b)-remainder(h*b), -6*h+full_change, places=12)

    def test_opposite_staple_mixed_derivative_and_cell_additivity_failure(self):
        step = 0.001
        for h in (1, 3, 10):
            def logfactor(a, b):
                total = qsum([ONE]*4+[phase(a), phase(b)])
                return math.log(F_series(h*qnorm(total)))
            mixed = (logfactor(step, step)-logfactor(step, -step)
                     -logfactor(-step, step)+logfactor(-step, -step))/(4*step*step)
            expected = h/6*Fprime_over_F(6*h)
            self.assertGreater(mixed, 0)
            self.assertAlmostEqual(mixed/expected, 1, places=5)
            four_point = logfactor(step, step)-logfactor(step, 0)-logfactor(0, step)+logfactor(0, 0)
            self.assertGreater(four_point, 0)


class GeometryAndLiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lat = Lattice(4)

    def test_periodic_sparse_pattern_and_all_site_reflections(self):
        for lat in (self.lat, Lattice(8)):
            removed = lat.pattern()
            self.assertEqual(len(removed), lat.side**4//8)
            self.assertTrue(lat.independent(removed))
            for axis, plane in product(range(4), range(lat.side)):
                self.assertEqual({lat.reflect_link(e, axis, plane)[0] for e in removed}, removed)
            for e in removed:
                self.assertTrue(lat.frozen(e).isdisjoint(removed))

    def test_empty_removed_set_recovers_the_original_local_energy(self):
        lat = self.lat
        rng = random.Random(SEED+7)
        field = {e: rng.choice(Q8) for e in lat.links}
        removed = set()
        self.assertTrue(lat.independent(removed))
        self.assertEqual(lat.base_plaquettes(removed), set(lat.plaquettes))
        for n in (1, 5, 20):
            edited = set(rng.sample(list(lat.links), n))
            neighbors, lifted = lat.closure(removed, edited)
            self.assertEqual(neighbors, set())
            self.assertEqual(lifted, edited)
            expected = sum(loop_energy(field, lat.words[p]) for p in lat.affected(edited))
            self.assertEqual(lat.leading_local(field, removed, edited), expected)

    def test_actual_balanced_and_aligned_staple_endpoints(self):
        lat = self.lat
        root = ((0, 0, 0, 0), 0)
        field = {e: ONE for e in lat.links}
        self.assertEqual(qsum(lat.staples(field, root)), (6, 0, 0, 0))
        for axis in (1, 2, 3):
            field[(lat.shift(root[0], axis), 0)] = (-1, 0, 0, 0)
        self.assertEqual(qsum(lat.staples(field, root)), (0, 0, 0, 0))
        for u in Q8:
            field[root] = u
            self.assertEqual(sum(loop_energy(field, lat.words[p]) for p in lat.stars[root]), 6)

    def test_full_parity_class_would_fail_normal_reflection_invariance(self):
        lat = self.lat
        removed = {e for e in lat.pattern() if e[0][0] % 2 == 0}
        self.assertTrue(lat.independent(removed))
        reflected = {lat.reflect_link(e, 0, 0)[0] for e in removed}
        self.assertNotEqual(removed, reflected)
        self.assertTrue(removed.isdisjoint(reflected))

    def test_six_distinct_staples_have_exactly_18_frozen_links(self):
        lat = self.lat
        for e in lat.links:
            self.assertEqual(len(lat.staple_words(e)), 6)
            self.assertEqual(len(lat.frozen(e)), 18)
            self.assertNotIn(e, lat.frozen(e))
            geometric = {f for p in lat.stars[e] for f, _ in lat.words[p]}-{e}
            self.assertEqual(lat.frozen(e), geometric)

    def test_exact_Q8_staple_energy_and_gauge_covariance(self):
        lat = self.lat
        rng = random.Random(SEED)
        field = {e: rng.choice(Q8) for e in lat.links}
        gauges = {x: rng.choice(Q8) for x in lat.sites}
        transformed = {e: qmul(qmul(gauges[e[0]], q), qinv(gauges[lat.shift(e[0], e[1])]))
                       for e, q in field.items()}
        energies = lat.energies(field)
        for e in rng.sample(list(lat.links), 80):
            total = qsum(lat.staples(field, e))
            self.assertEqual(sum(energies[p] for p in lat.stars[e]), 6-dot(field[e], total))
            transformed_staples = lat.staples(transformed, e)
            expected = [qmul(qmul(gauges[e[0]], s), qinv(gauges[lat.shift(e[0], e[1])]))
                        for s in lat.staples(field, e)]
            self.assertEqual(transformed_staples, expected)
            self.assertEqual(dot(qsum(transformed_staples), qsum(transformed_staples)), dot(total, total))

    def test_fine_decomposition_and_leading_local_lift(self):
        lat = self.lat
        removed = lat.pattern()
        rng = random.Random(SEED+1)
        field = {e: rng.choice(Q8) for e in lat.links}
        energies = lat.energies(field)
        base = lat.base_plaquettes(removed)
        self.assertEqual(sum(energies.values()),
                         sum(energies[p] for p in base)+sum(sum(energies[p] for p in lat.stars[e]) for e in removed))
        retained = sorted(set(lat.links)-removed)
        for n in (1, 3, 10, 40):
            edited = set(rng.sample(retained, n))
            neighbors, lifted = lat.closure(removed, edited)
            self.assertLessEqual(len(neighbors), 6*n)
            self.assertLessEqual(len(lifted), 7*n)
            expected_ps = (base & lat.affected(edited)) | lat.affected(neighbors)
            self.assertEqual(lat.affected(lifted), expected_ps)
            self.assertTrue(all(not ((set(e for e, _ in lat.words[p])) & (removed-neighbors)) for p in expected_ps))
            g = lat.leading_local(field, removed, edited)
            self.assertLessEqual(g, sum(energies[p] for p in expected_ps)+1e-10)
            # Choose each continuous SU(2) minimizer B/|B|; this is NOT Q8 Haar.
            minimizing = dict(field)
            for e in neighbors:
                total = qsum(lat.staples(field, e))
                length = qnorm(total)
                minimizing[e] = tuple(v/length for v in total) if length else ONE
            achieved = sum(loop_energy(minimizing, lat.words[p]) for p in expected_ps)
            self.assertAlmostEqual(achieved, g, places=10)

    def test_local_closure_bound_six_is_attained(self):
        lat = self.lat
        root = ((0, 0, 0, 0), 0)
        removed = {(lat.shift(root[0], axis, sign), 0) for axis in (1, 2, 3) for sign in (-1, 1)}
        self.assertTrue(lat.independent(removed))
        neighbors, lifted = lat.closure(removed, {root})
        self.assertEqual(neighbors, removed)
        self.assertLessEqual(len(neighbors), 6*len({root}))
        self.assertEqual(len(lifted), 7)

    def test_entire_affected_star_must_be_kept_in_the_lift(self):
        lat = self.lat
        root = ((0, 0, 0, 0), 0)
        removed = {(lat.shift(root[0], 1), 0)}
        neighbors, lifted = lat.closure(removed, {root})
        self.assertEqual(len(neighbors), 1)
        self.assertGreater(len(lat.affected(lifted)), len(lat.affected({root})))
        field = {e: ONE for e in lat.links}
        field[next(iter(removed))] = (-1, 0, 0, 0)
        energies = lat.energies(field)
        whole_lift = sum(energies[p] for p in lat.affected(lifted))
        original_J_only = sum(energies[p] for p in lat.affected({root}))
        self.assertEqual(whole_lift, 12)
        self.assertEqual(original_J_only, 2)
        self.assertNotEqual(whole_lift, original_J_only)

    def test_local_remainder_cost_depends_on_affected_removed_stars_only(self):
        lat = self.lat
        removed = lat.pattern()
        retained = sorted(set(lat.links)-removed)
        rng = random.Random(SEED+2)
        old = {e: rng.choice(Q8) for e in lat.links}
        for n in (1, 3, 9):
            edited = set(rng.sample(retained, n))
            new = {e: rng.choice(Q8) if e in edited else q for e, q in old.items()}
            neighbors, _ = lat.closure(removed, edited)
            for e in removed-neighbors:
                self.assertEqual(lat.staples(old, e), lat.staples(new, e))
            for h in (1, 1000):
                delta = sum(remainder(h*qnorm(qsum(lat.staples(new, e))))
                            -remainder(h*qnorm(qsum(lat.staples(old, e)))) for e in removed)
                local_delta = sum(remainder(h*qnorm(qsum(lat.staples(new, e))))
                                  -remainder(h*qnorm(qsum(lat.staples(old, e)))) for e in neighbors)
                self.assertAlmostEqual(delta, local_delta, places=11)
                self.assertLessEqual(abs(delta), len(neighbors)*remainder_bound(6*h)+1e-10)

    def test_retained_sublevel_has_caps_with_n_not_lift_size_in_flat_case(self):
        lat = self.lat
        removed = lat.pattern()
        retained = sorted(set(lat.links)-removed)
        rng = random.Random(SEED+3)
        for n, h in product((1, 4, 12), (4, 1024)):
            edited = set(rng.sample(retained, n))
            # Identity supplies a JOINT fine minimizer, with all frozen data flat.
            field = {e: qcap(rng, 1/math.sqrt(h)) if e in edited else ONE for e in lat.links}
            leading = lat.leading_local(field, removed, edited)
            self.assertLessEqual(leading, 12*n/h+1e-10)
            self.assertGreaterEqual(leading, -1e-10)

    def test_effective_support_incidence_and_component_witness_factor(self):
        lat = self.lat
        removed = lat.pattern()
        retained = set(lat.links)-removed
        supports = [frozenset(e for e, _ in lat.words[p]) for p in lat.base_plaquettes(removed)]
        supports += [frozenset(lat.frozen(e)) for e in removed]
        hits = Counter(e for support in supports for e in support)
        self.assertEqual(set(hits), retained)
        self.assertLessEqual(max(hits.values()), 6)
        self.assertEqual(max(map(len, supports)), 18)
        neighbors = {e: set() for e in retained}
        for support in supports:
            for e in support:
                neighbors[e].update(support-{e})
        self.assertLessEqual(max(map(len, neighbors.values())), 102)
        rng = random.Random(SEED+4)
        for _ in range(24):
            rough_supports = rng.sample(supports, 7)
            rough_links = set().union(*rough_supports)
            chosen = set(rng.sample(sorted(rough_links), min(17, len(rough_links))))
            witnesses = [support for support in rough_supports if support & chosen]
            self.assertGreaterEqual(18*len(witnesses), len(chosen))

    def test_opposite_staples_share_no_original_elementary_cell(self):
        for side in (4, 8):
            lat = self.lat if side == 4 else Lattice(side)
            pair = {((0, 1, 0, 0), 0), ((0, side-1, 0, 0), 0)}
            self.assertTrue(all(not pair <= lat.cell_edges(x) for x in lat.sites))

    def test_exact_marginal_factors_are_reflection_invariant_for_pattern(self):
        lat = self.lat
        removed = lat.pattern()
        base = lat.base_plaquettes(removed)
        rng = random.Random(SEED+5)
        field = {e: rng.choice(Q8) for e in lat.links}
        energies = lat.energies(field)
        original = (sum(energies[p] for p in base),
                    sorted(dot(qsum(lat.staples(field, e)), qsum(lat.staples(field, e))) for e in removed))
        for axis in range(4):
            transformed = lat.reflect_field(field, axis, 0)
            new_energies = lat.energies(transformed)
            actual = (sum(new_energies[p] for p in base),
                      sorted(dot(qsum(lat.staples(transformed, e)), qsum(lat.staples(transformed, e))) for e in removed))
            self.assertEqual(original, actual)

    def test_exact_Q8_integration_factorizes_only_in_removed_variables(self):
        lat = self.lat
        rng = random.Random(SEED+6)
        field = {e: rng.choice(Q8) for e in lat.links}
        removed = set(sorted(lat.pattern())[:3])
        self.assertTrue(lat.independent(removed))
        removed_list = sorted(removed)
        totals = {e: qsum(lat.staples(field, e)) for e in removed}
        star_ps = lat.affected(removed)
        q = F(1, 4)
        joint = F(0)
        for values in product(Q8, repeat=3):
            output = dict(field)
            output.update(zip(removed_list, values))
            exponent = sum(loop_energy(output, lat.words[p]) for p in star_ps)
            self.assertEqual(exponent, sum(6-dot(output[e], totals[e]) for e in removed))
            joint += q**exponent/8**3
        factor = F(1)
        for e in removed:
            factor *= sum(q**(6-dot(u, totals[e])) for u in Q8)/8
        self.assertEqual(joint, factor)
        # This discrete factor depends on the Q8 orbit, not only |B|.
        b1, b2 = (2, 0, 0, 0), (1, 1, 1, 1)
        self.assertEqual(dot(b1, b1), dot(b2, b2))
        f1 = sum(q**(-dot(u, b1)) for u in Q8)/8
        f2 = sum(q**(-dot(u, b2)) for u in Q8)/8
        self.assertNotEqual(f1, f2)


class OpenZ2:
    """Actual 2x2 open plaquette lattice with 12 Z2 links and 4 plaquettes."""
    def __init__(self):
        self.links = tuple(((x, y), d) for x, y in product(range(3), repeat=2)
                           for d in (0, 1) if (x if d == 0 else y) < 2)
        self.index = {e: i for i, e in enumerate(self.links)}
        self.plaquettes = []
        for x, y in product(range(2), repeat=2):
            edges = [((x, y), 0), ((x+1, y), 1), ((x, y+1), 0), ((x, y), 1)]
            self.plaquettes.append(sum(1 << self.index[e] for e in edges))
        self.removed = (self.index[((1, 0), 1)], self.index[((1, 1), 1)])
        self.retained = tuple(i for i in range(12) if i not in self.removed)
        self.stars = {e: tuple(j for j, p in enumerate(self.plaquettes) if (p >> e) & 1) for e in range(12)}
        self.q = F(1, 4)

    def fine(self, z, u=0):
        value = sum(((z >> j) & 1) << e for j, e in enumerate(self.retained))
        value |= sum(((u >> j) & 1) << e for j, e in enumerate(self.removed))
        return value

    def energy(self, fine, ps=None):
        if ps is None:
            ps = range(4)
        return sum(2*((fine & self.plaquettes[j]).bit_count() % 2) for j in ps)

    def factors(self, z):
        fine = self.fine(z)
        entries = {}
        for e in self.removed:
            e0 = self.energy(fine, self.stars[e])
            e1 = self.energy(fine ^ (1 << e), self.stars[e])
            minimum = min(e0, e1)
            integral = (self.q**e0+self.q**e1)/2
            entries[e] = (minimum, integral, integral/self.q**minimum)
        return entries

    def density(self, z):
        entries = self.factors(z)
        return math.prod(value[1] for value in entries.values())

    def closure(self, retained_position):
        e = self.retained[retained_position]
        a = {d for d in self.removed if set(self.stars[d]) & set(self.stars[e])}
        k = a | {e}
        ps = set().union(*(set(self.stars[x]) for x in k))
        return a, k, ps

    def leading_local(self, z, retained_position):
        a, _, _ = self.closure(retained_position)
        # Here every fine plaquette touches exactly one removed link, so E0=0.
        entries = self.factors(z)
        return sum(entries[e][0] for e in a)


class ExactFiniteMarginalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = OpenZ2()
        cls.weights = [cls.model.density(z) for z in range(1024)]
        cls.total = sum(cls.weights)
        cls.nu = [w/cls.total for w in cls.weights]

    def test_exact_joint_marginal_normalization_and_Haar_factors(self):
        model = self.model
        for z in range(1024):
            direct = sum(model.q**model.energy(model.fine(z, u)) for u in range(4))/4
            self.assertEqual(direct, self.weights[z])
        z_fine = sum(model.q**model.energy(x) for x in range(4096))/4096
        z_marginal = sum(self.weights)/1024
        self.assertEqual(z_fine, z_marginal)
        self.assertEqual(z_fine, ((1+model.q**2)/2)**4)
        self.assertEqual(sum(self.nu), 1)

    def test_exact_minimum_and_remainder_decomposition(self):
        model = self.model
        for z in range(1024):
            values = model.factors(z)
            minimum = sum(v[0] for v in values.values())
            direct_min = min(model.energy(model.fine(z, u)) for u in range(4))
            self.assertEqual(minimum, direct_min)
            residual = math.prod(v[2] for v in values.values())
            self.assertEqual(model.q**minimum*residual, self.weights[z])
            self.assertTrue(all(F(1, 2) <= v[2] <= 1 for v in values.values()))
        self.assertGreater(len(set(self.weights)), 1)

    def test_local_lift_and_boundary_minimum_are_exact(self):
        model = self.model
        for position in range(10):
            affected, lifted, ps = model.closure(position)
            self.assertLessEqual(len(lifted), 3)
            for z in range(1024):
                g = model.leading_local(z, position)
                direct = min(model.energy(model.fine(z, u), ps) for u in range(4))
                self.assertEqual(g, direct)
                if z & (1 << position):
                    continue
                other = z ^ (1 << position)
                boundary_min = min(g, model.leading_local(other, position))
                direct_joint = min(model.energy(model.fine(zz, u), ps)
                                   for zz in (z, other) for u in range(4))
                self.assertEqual(boundary_min, direct_joint)

    def test_exact_sublevel_accepted_output_domination(self):
        model = self.model
        successful = 0
        for position in range(10):
            affected, _, _ = model.closure(position)
            output = [F(0)]*1024
            input_mass = F(0)
            for z in range(1024):
                other = z ^ (1 << position)
                g0 = model.leading_local(z, position)
                g1 = model.leading_local(other, position)
                if g0-min(g0, g1) < 2:
                    continue
                # Source is accepted only with the actual current energy drop.
                output[other] += self.nu[z]
                input_mass += self.nu[z]
            self.assertEqual(sum(output), input_mass)
            # Finite Z2 analogue: output Haar-density <=2, residual ratio <=2^a.
            c = 2*2**len(affected)*model.q**2
            self.assertLess(c, 1)
            self.assertTrue(all(value <= c*mass for value, mass in zip(output, self.nu)))
            if input_mass:
                successful += 1
        self.assertGreater(successful, 0)

    def test_shared_removed_plaquette_does_not_factorize(self):
        q = F(1, 4)
        # One actual Z2 plaquette with two removed links and the other two fixed +1.
        joint = sum(q**(0 if u == v else 2) for u, v in product((-1, 1), repeat=2))/4
        one_link_frozen_other = (1+q**2)/2
        self.assertEqual(joint, one_link_frozen_other)
        self.assertNotEqual(joint, one_link_frozen_other**2)

    def test_factorization_does_not_license_independence_or_duplicate_labels(self):
        model = self.model
        bad0 = {z for z in range(1024) if model.factors(z)[model.removed[0]][0] == 2}
        # A duplicate of the SAME retained label cannot be paid twice.
        probability = sum(self.nu[z] for z in bad0)
        self.assertTrue(0 < probability < 1)
        self.assertNotEqual(probability, probability**2)
        # Supports of the two factors share retained links even though plaquettes do not.
        supports = []
        for e in model.removed:
            supports.append({i for p in model.stars[e] for i in range(12)
                             if (model.plaquettes[p] >> i) & 1 and i not in model.removed})
        self.assertTrue(supports[0] & supports[1])


class BudgetAndScopeTests(unittest.TestCase):
    def test_exact_one_step_absorption_budgets(self):
        ell, r_h, b_h = F(17, 3), F(23, 4), F(11, 2)
        for n, a, k in ((1, 6, 1), (7, 3, 2), (20, 100, 3)):
            p2 = max(F(96*n, k), 16*(ell*n+a*r_h)/k, 1024*b_h*(n+a)/k)
            self.assertLessEqual(-k*p2/8+ell*n+a*r_h, -k*p2/16)
            self.assertLessEqual(-k*p2/512+b_h*(n+a), -k*p2/1024)
            self.assertLessEqual(F(k, 2)+24*n/p2, F(3*k, 4))

    def test_effective_label_constants_and_nonempty_star_regime(self):
        self.assertEqual(6*17, 102)
        self.assertEqual(256*18, 4608)
        self.assertEqual(96*18, 1728)
        self.assertEqual(8*18, 144)
        self.assertEqual(102**2+1, 10405)
        # A star at m=6 can be rough with threshold between 2 and 6, although
        # no individual retained plaquette (max energy 2) can then be rough.
        threshold = F(5, 2)
        self.assertFalse(2 > threshold)
        self.assertTrue(6 > threshold)
        self.assertFalse(6 > 6)

    def test_adaptive_accepted_kernel_count_and_overlap_budget(self):
        w = F(1, 20000)
        geometric = w/(1-10404*w)
        partial = sum(F(10404)**(n-1)*w**n for n in range(1, 30))
        tail = w*(10404*w)**29/(1-10404*w)
        self.assertEqual(partial+tail, geometric)
        self.assertLess(geometric, 1)
        self.assertEqual(F(1, 10405)/(1-F(10404, 10405)), 1)
        for n in range(1, 100):
            k = (n+17)//18
            self.assertGreaterEqual(k*1728, 96*n)
            self.assertGreaterEqual(F(k, 8), F(n, 144))

    def test_large_H_budgets_can_hold_without_empty_labels(self):
        h = math.exp(24)
        ell = math.log(24)+1.5*math.log(h)
        r_h = remainder_bound(6*h)
        a_h = 1.5+math.log(24)+1.5*math.log(8*h)
        b_h = a_h/2+math.log(2)/64
        p2 = 2e8
        self.assertLess(p2, 4*h)  # Even original-plaquette rough events need not be empty.
        self.assertGreater(p2, 1728)
        self.assertGreater(p2, 18*16*(ell+6*r_h))
        self.assertGreater(p2, 18*1024*7*b_h)
        self.assertGreater(p2/144-ell-6*r_h, math.log(10405))
        self.assertGreater(p2/4608-7*b_h, 2*math.log(102))


if __name__ == '__main__':
    print('Exact sparse marginal diagnostics; Python standard library; seed', SEED, flush=True)
    print('Continuous one-link quadrature, exact Q8 link algebra and separate finite Z2 marginals.', flush=True)
    print('NOT a 4D SU(2) partition-function calculation, RG closure proof, or continuum construction.', flush=True)
    unittest.main(verbosity=2)
