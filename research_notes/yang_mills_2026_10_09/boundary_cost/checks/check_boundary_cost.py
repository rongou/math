#!/usr/bin/env python3
"""Finite diagnostics for boundary_cost.tex; not a proof of the SU(2) measure.

Standard library only. No downloads, filesystem writes, Monte Carlo probability
estimates, or sibling-script imports. Exact Z2 sums test a different, finite-group
model. Universal analytic quantifiers and the chessboard theorem are NOT certified
by these tests. All assertion checks use unittest and survive python -O.
"""
from collections import Counter, defaultdict, deque
from fractions import Fraction
from itertools import combinations, product
import math
import random
import unittest

SEED = 20261009
ONE = (1.0, 0.0, 0.0, 0.0)
MINUS_ONE = (-1.0, 0.0, 0.0, 0.0)


def mul(a, b):
    w, x, y, z = a
    v, i, j, k = b
    return (w*v-x*i-y*j-z*k, w*i+x*v+y*k-z*j,
            w*j-x*k+y*v+z*i, w*k+x*j-y*i+z*v)


def inv(a):
    return (a[0], -a[1], -a[2], -a[3])


def qdist(a, b=ONE):
    return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))


def random_q(rng):
    q = tuple(rng.gauss(0, 1) for _ in range(4))
    length = math.sqrt(sum(v*v for v in q))
    return tuple(v/length for v in q)


def cap_q(rng, rho):
    axis = [rng.gauss(0, 1) for _ in range(3)]
    length = math.sqrt(sum(v*v for v in axis))
    angle = rng.random()*rho
    return (math.cos(angle), *(math.sin(angle)*v/length for v in axis))


class Lattice:
    def __init__(self, side, dim=4):
        self.side = side
        self.dim = dim
        self.sites = tuple(product(range(side), repeat=dim))
        self.links = tuple((x, mu) for x in self.sites for mu in range(dim))
        self.plaquettes = tuple((x, mu, nu) for x in self.sites
                               for mu, nu in combinations(range(dim), 2))
        self.boundaries = {p: self.boundary(p) for p in self.plaquettes}
        self.incident = {e: [] for e in self.links}
        for p, edges in self.boundaries.items():
            for e, _ in edges:
                self.incident[e].append(p)

    def shift(self, x, mu, step=1):
        y = list(x)
        y[mu] = (y[mu]+step) % self.side
        return tuple(y)

    def boundary(self, p):
        x, mu, nu = p
        return (((x, mu), 1), ((self.shift(x, mu), nu), 1),
                ((self.shift(x, nu), mu), -1), ((x, nu), -1))

    def holonomy(self, field, p):
        value = ONE
        for e, sign in self.boundaries[p]:
            value = mul(value, field[e] if sign == 1 else inv(field[e]))
        return value

    def energies(self, field):
        return {p: 1-self.holonomy(field, p)[0] for p in self.plaquettes}

    def affected(self, links):
        return {p for e in links for p in self.incident[e]}

    def neighbors(self, e):
        return {f for p in self.incident[e] for f, _ in self.boundaries[p]
                if f != e}

    def reflect_site(self, x, axis, plane):
        y = list(x)
        y[axis] = (2*plane-y[axis]) % self.side
        return tuple(y)

    def reflect_link(self, e, axis, plane):
        x, mu = e
        y = self.reflect_site(x, axis, plane)
        if mu == axis:
            return (self.shift(y, mu, -1), mu), -1
        return (y, mu), 1

    def reflect_plaquette(self, p, axis, plane):
        x, mu, nu = p
        y = self.reflect_site(x, axis, plane)
        if axis in (mu, nu):
            y = self.shift(y, axis, -1)
        return (y, mu, nu)

    def reflect_field(self, field, axis, plane):
        result = {}
        for e, value in field.items():
            target, sign = self.reflect_link(e, axis, plane)
            result[target] = value if sign == 1 else inv(value)
        return result

    def half_side(self, e, axis, plane):
        x, mu = e
        doubled_midpoint = 2*x[axis]+int(mu == axis)
        delta = (doubled_midpoint-2*plane) % (2*self.side)
        if delta in (0, self.side):
            return 0
        return 1 if delta < self.side else -1

    def prototype(self, mu, r):
        x = [1]*self.dim
        x[mu] = r
        return (tuple(x), mu)

    def block_link(self, e, block, origin):
        x, mu = e
        y = tuple((origin[j]+2*block[j]+(
            x[j] if block[j] % 2 == 0 else 2-x[j]-int(j == mu)
        )) % self.side for j in range(self.dim))
        return (y, mu), (-1 if block[mu] % 2 else 1)

    def block_plaquette(self, p, block, origin):
        x, mu, nu = p
        y = tuple((origin[j]+2*block[j]+(
            x[j] if block[j] % 2 == 0 else 2-x[j]-int(j in (mu, nu))
        )) % self.side for j in range(self.dim))
        return (y, mu, nu)


def simpson(f, lo, hi, panels=2048):
    if lo == hi:
        return 0.0
    dx = (hi-lo)/panels
    value = f(lo)+f(hi)
    for j in range(1, panels):
        value += (4 if j % 2 else 2)*f(lo+j*dx)
    return value*dx/3


def constants(h):
    a = 1.5+math.log(24)+1.5*math.log(8*h)
    return a, a/2+math.log(2)/64


def gf2_rank(rows):
    pivots = {}
    for row in rows:
        while row:
            pivot = row.bit_length()-1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return len(pivots)


class GeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lattices = (Lattice(4), Lattice(8))

    def test_incidence_and_reflection_half_split(self):
        for lat in self.lattices:
            self.assertEqual(len(lat.links), 4*lat.side**4)
            self.assertEqual(len(lat.plaquettes), 6*lat.side**4)
            self.assertEqual({len(v) for v in lat.incident.values()}, {6})
            for axis in range(4):
                for plane in range(lat.side):
                    for p, edges in lat.boundaries.items():
                        sides = {lat.half_side(e, axis, plane) for e, _ in edges}
                        self.assertFalse({-1, 1}.issubset(sides), (lat.side, p))
                    for e in lat.links:
                        other, sign = lat.reflect_link(e, axis, plane)
                        original, sign2 = lat.reflect_link(other, axis, plane)
                        self.assertEqual((original, sign*sign2), (e, 1))
                        if lat.half_side(e, axis, plane) == 0:
                            self.assertEqual((other, sign), (e, 1))

    def test_reflected_stars_have_no_shared_plaquettes(self):
        for lat in self.lattices:
            blocks = tuple(product(range(lat.side//2), repeat=4))
            for mu, r in product(range(4), range(2)):
                prototype = lat.prototype(mu, r)
                local = lat.incident[prototype]
                for p in local:
                    vertices = {x for (x, _), _ in lat.boundaries[p]}
                    vertices |= {lat.shift(x, direction)
                                 for (x, direction), _ in lat.boundaries[p]}
                    self.assertTrue(all(0 <= v <= 2 for x in vertices for v in x))
                    for j in range(4):
                        self.assertNotEqual({x[j] for x in vertices}, {0})
                        self.assertNotEqual({x[j] for x in vertices}, {2})
                for origin in ((0, 0, 0, 0), (1, 0, 1, 0)):
                    used = set()
                    for block in blocks:
                        images = {lat.block_plaquette(p, block, origin) for p in local}
                        target, _ = lat.block_link(prototype, block, origin)
                        self.assertEqual(images, set(lat.incident[target]))
                        self.assertTrue(used.isdisjoint(images))
                        used |= images
                    self.assertEqual(len(used), 6*len(blocks))

    def test_64_classes_distinct_blocks_and_reflected_pullback(self):
        for lat in self.lattices:
            classes = defaultdict(list)
            for e in lat.links:
                x, mu = e
                classes[(mu, tuple(v % 2 for v in x))].append(e)
            self.assertEqual(len(classes), 64)
            self.assertEqual({len(v) for v in classes.values()}, {lat.side**4//16})
            for (mu, parity), links in classes.items():
                origin = tuple(parity[j] if j == mu else (parity[j]-1) % 2
                               for j in range(4))
                occupied = set()
                for e in links:
                    x, _ = e
                    delta = tuple((x[j]-origin[j]) % lat.side for j in range(4))
                    block = tuple(v//2 for v in delta)
                    local = tuple(v % 2 for v in delta)
                    self.assertEqual(local, tuple(0 if j == mu else 1 for j in range(4)))
                    self.assertNotIn(block, occupied)
                    occupied.add(block)
                    prototype = lat.prototype(mu, block[mu] % 2)
                    target, _ = lat.block_link(prototype, block, origin)
                    self.assertEqual(target, e)

    def test_all_star_energies_cannot_be_called_disjoint(self):
        lat = self.lattices[0]
        counts = Counter(p for e in lat.links for p in lat.incident[e])
        self.assertEqual(set(counts.values()), {4})
        # An uncolored sum over every link counts total energy FOUR times.
        self.assertEqual(sum(counts.values()), 4*len(lat.plaquettes))
        self.assertEqual(len(lat.neighbors(lat.links[0])), 18)


class QuaternionAndScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lat = Lattice(4)

    def test_su2_reflection_energy_and_probability_haar_maps(self):
        lat = self.lat
        rng = random.Random(SEED)
        field = {e: random_q(rng) for e in lat.links}
        original = lat.energies(field)
        for axis, plane in product(range(4), (0, 1)):
            reflected = lat.reflect_field(field, axis, plane)
            back = lat.reflect_field(reflected, axis, plane)
            self.assertEqual(back, field)
            energies = lat.energies(reflected)
            for p in lat.plaquettes:
                rp = lat.reflect_plaquette(p, axis, plane)
                self.assertAlmostEqual(original[p], energies[rp], places=12)
            self.assertAlmostEqual(sum(original.values()), sum(energies.values()), places=10)

    def test_product_cap_energy_and_haar_constant(self):
        lat = self.lat
        rng = random.Random(SEED+1)
        for h in (1, 4, 64, 10000, 100000000):
            rho = 1/math.sqrt(8*h)
            # Stable scaled quadrature, not a cancellation-prone rho-sin(rho)cos(rho).
            cap_over_rho3 = 2/math.pi*simpson(
                lambda x: (math.sin(rho*x)/rho)**2, 0, 1)
            self.assertGreater(cap_over_rho3, 1/24)
            a, _ = constants(h)
            self.assertAlmostEqual(12*h*rho*rho+math.log(24)-3*math.log(rho), a)
            if h <= 64:
                field = {e: cap_q(rng, rho) for e in lat.links}
                energies = lat.energies(field)
                self.assertLessEqual(sum(energies.values()), 48*len(lat.sites)*rho*rho+1e-10)
                self.assertLessEqual(max(qdist(lat.holonomy(field, p))
                                         for p in lat.plaquettes), 4*rho+1e-12)

    def test_frustrated_exterior_is_not_a_conditional_tail(self):
        lat = self.lat
        root = ((0, 0, 0, 0), 0)
        field = {e: ONE for e in lat.links}
        for nu in (1, 2, 3):
            field[(lat.shift(root[0], nu), 0)] = MINUS_ONE
        staples = [ONE]*3+[MINUS_ONE]*3
        b = tuple(sum(s[j] for s in staples) for j in range(4))
        defect = sum(qdist(a, c)**2 for a, c in combinations(staples, 2))
        self.assertEqual(b, (0.0, 0.0, 0.0, 0.0))
        self.assertEqual(defect, 36)
        rng = random.Random(SEED+2)
        for value in [ONE, MINUS_ONE]+[random_q(rng) for _ in range(64)]:
            field[root] = value
            energy = sum(1-lat.holonomy(field, p)[0] for p in lat.incident[root])
            self.assertAlmostEqual(energy, 6, places=12)
        # Conditional P(E_star>=5)=1, but the NEW MARGINAL bound would be tiny.
        # The test detects the invalid conditional reinterpretation, not the theorem.
        _, b_h = constants(1000000)
        self.assertLess(-1000000*5/128+b_h, -1000)

    def test_padding_has_no_volume_proportional_energy_gain(self):
        lat = self.lat
        root = lat.links[0]
        field = {e: ONE for e in lat.links}
        field[root] = MINUS_ONE
        energies = lat.energies(field)
        for n in (1, 8, 64, 256):
            j = set(lat.links[:n])
            self.assertIn(root, j)
            self.assertEqual(sum(energies[p] for p in lat.affected(j)), 12)
            # Setting the edited links to identity gives a zero-energy witness.
            output = {e: ONE if e in j else value for e, value in field.items()}
            self.assertEqual(sum(lat.energies(output)[p] for p in lat.affected(j)), 0)
        self.assertLess(12, 256)

    def test_overlapping_edits_need_declared_losses(self):
        lat = self.lat
        x = (0, 0, 0, 0)
        e1, e2 = (x, 0), (lat.shift(x, 0), 1)
        g = (0.0, 0.0, 0.0, 1.0)
        field = {e: ONE for e in lat.links}
        field[e1] = field[e2] = g
        totals = []
        for edits in ((), (e1,), (e2,), (e1, e2)):
            output = dict(field)
            for e in edits:
                output[e] = inv(g)
            totals.append(sum(lat.energies(output).values()))
        self.assertEqual(totals, [12, 10, 10, 12])
        p1, p2 = lat.affected({e1}), lat.affected({e2})
        self.assertTrue(p1 & p2)
        self.assertEqual(max(Counter(list(p1)+list(p2)).values()), 2)
        energies = lat.energies(field)
        self.assertLessEqual(sum(energies[p] for p in p1)+sum(energies[p] for p in p2),
                             2*sum(energies[p] for p in p1 | p2))

    def test_zero_minimum_does_not_remove_frozen_winding_holonomy(self):
        lat = self.lat
        phi = math.pi/3
        v = (math.cos(phi/lat.side), 0.0, 0.0, math.sin(phi/lat.side))
        field = {e: v if e[1] == 0 else ONE for e in lat.links}
        energies = lat.energies(field)
        self.assertLess(max(abs(value) for value in energies.values()), 1e-12)
        j = {((x, 0, 0, 0), 1) for x in range(lat.side)}
        frozen = {e for p in lat.affected(j) for e, _ in lat.boundaries[p]}-j
        loop = [((x, 0, 0, 0), 0) for x in range(lat.side)]
        self.assertTrue(set(loop) <= frozen)
        holonomy = ONE
        for e in loop:
            holonomy = mul(holonomy, field[e])
        self.assertAlmostEqual(holonomy[0], math.cos(phi), places=12)
        self.assertGreater(qdist(holonomy), 0.9)
        # Current flat field witnesses e_* = 0; no numerical minimizer is asserted.
        self.assertLess(abs(sum(energies[p] for p in lat.affected(j))), 1e-11)

    def test_one_link_sublevel_band_volume_and_covariance(self):
        rng = random.Random(SEED+4)
        families = [[ONE]*6, [ONE]*3+[MINUS_ONE]*3]
        families += [[random_q(rng) for _ in range(6)] for _ in range(6)]
        for staples in families:
            total = tuple(sum(s[j] for s in staples) for j in range(4))
            length = math.sqrt(sum(v*v for v in total))
            minimum = 6-length
            center = tuple(v/length for v in total) if length else ONE
            left, right = random_q(rng), random_q(rng)
            transformed = [mul(mul(left, s), inv(right)) for s in staples]
            total2 = tuple(sum(s[j] for s in transformed) for j in range(4))
            self.assertAlmostEqual(sum(v*v for v in total2), length*length, places=11)
            for h in (1, 64, 1000000):
                # Exact one-link sublevel: b(1-cos(angle)) <= 12/H.
                ratio = min(2, 12/(h*length)) if length else 2
                angle = 2*math.asin(math.sqrt(ratio/2))
                if angle <= 1:
                    volume = angle**3*2/math.pi*simpson(
                        lambda x: (math.sin(angle*x)/angle)**2, 0, 1)
                else:
                    volume = (angle-math.sin(angle)*math.cos(angle))/math.pi
                self.assertGreaterEqual(volume+1e-15, h**(-1.5)/24)
                for _ in range(12):
                    # Support witnesses, NOT claimed Haar-uniform kernel samples.
                    u = mul(center, cap_q(rng, angle))
                    energy = sum(1-sum(a*b for a, b in zip(u, s)) for s in staples)
                    self.assertLessEqual(energy, minimum+12/h+1e-12)
                    gu = mul(mul(left, u), inv(right))
                    energy2 = sum(1-sum(a*b for a, b in zip(gu, s)) for s in transformed)
                    self.assertAlmostEqual(energy, energy2, places=11)

    def test_source_components_have_paid_witness_density(self):
        lat = self.lat
        field = {e: ONE for e in lat.links}
        for e in (lat.links[0], ((1, 0, 0, 0), 1), ((3, 3, 3, 3), 2)):
            field[e] = MINUS_ONE
        energies = lat.energies(field)
        rough = {p for p, energy in energies.items() if energy > 1}
        rough_links = {e for p in rough for e, _ in lat.boundaries[p]}
        remaining = set(rough_links)
        while remaining:
            root = min(remaining)
            seen, queue, order = {root}, deque([root]), []
            while queue:
                e = queue.popleft()
                order.append(e)
                for neighbor in sorted(lat.neighbors(e) & rough_links):
                    if neighbor not in seen:
                        seen.add(neighbor)
                        queue.append(neighbor)
            remaining -= seen
            for n in range(1, len(order)+1):
                chosen = set(order[:n])
                witnesses = lat.affected(chosen) & rough
                self.assertGreaterEqual(4*len(witnesses), n)
                reached = {root}
                for e in order[1:n]:
                    self.assertTrue(lat.neighbors(e) & reached)
                    reached.add(e)


class ScalarTests(unittest.TestCase):
    def test_exact_constant_chain(self):
        self.assertEqual(4*2**4, 64)
        self.assertEqual(Fraction(1, 2)/64, Fraction(1, 128))
        self.assertEqual(Fraction(1, 128)/2, Fraction(1, 256))
        self.assertEqual(Fraction(1, 256)/4, Fraction(1, 1024))
        self.assertEqual(Fraction(12, 8), Fraction(3, 2))
        self.assertEqual(Fraction(3, 2)/2, Fraction(3, 4))
        self.assertEqual(6*3, 18)
        self.assertEqual(18**2, 324)

    def test_joint_tail_layer_cake_integral(self):
        for theta, k in product((0.125, 0.5, 0.875), (0.0, math.log(4), 3.0)):
            first = simpson(lambda v: theta*math.exp(theta*v), 0, k, 4096)
            # v=k+w in the exponentially decaying tail.
            second = simpson(lambda w: theta*math.exp(theta*k-(1-theta)*w),
                             0, 40/(1-theta), 4096)
            expected = math.exp(theta*k)/(1-theta)
            self.assertAlmostEqual((1+first+second)/expected, 1, places=9)

    def test_partial_cooling_and_exception_budgets_exactly(self):
        for n, k in product((1, 4, 9, 64), (1, 3, 16)):
            ell, b_h = Fraction(7, 2), Fraction(8, 3)
            p2 = max(Fraction(96*n, k), 16*n*ell/k, 1024*n*b_h/k)
            baseline = k*p2/4  # H times the retained minimum.
            output_energy = baseline+12*n
            output_count = 2*output_energy/p2
            gain = k*p2/2-output_energy
            self.assertLessEqual(output_count, Fraction(3*k, 4))
            self.assertGreaterEqual(gain, k*p2/8)
            self.assertLessEqual(-gain+n*ell, -k*p2/16)
            self.assertLessEqual(-k*p2/512+b_h*n, -k*p2/1024)

    def test_counted_tail_and_nonvacuous_large_h_example(self):
        lam = 2*math.log(18)+1.25
        for n in (1, 2, 10):
            explicit = sum(18**(2*(j-1))*math.exp(-lam*j) for j in range(n, n+100))
            formula = 18**(2*(n-1))*math.exp(-lam*n)/(1-324*math.exp(-lam))
            self.assertAlmostEqual(explicit, formula, places=14)
        # A finite arithmetic example, not a numerical Yang--Mills probability.
        h = math.exp(20)
        p = 40*math.sqrt(math.log(h))
        _, b_h = constants(h)
        self.assertLess(p/math.sqrt(h), 2)
        self.assertGreater(p*p/1024-b_h, 2*math.log(18))


class ExactZ2ChessboardTests(unittest.TestCase):
    """Exact 4x4 two-dimensional Z2 gauge law at exp(-2H)=1/4.

    The GF(2) incidence map has image all even-parity plaquette patterns.
    Fibers have equal size, so no link integrations or gauge fixing are guessed.
    """
    @classmethod
    def setUpClass(cls):
        cls.lat = Lattice(4, dim=2)
        lat = cls.lat
        cls.index = {p: j for j, p in enumerate(lat.plaquettes)}
        cls.blocks = tuple(product(range(2), repeat=2))
        cls.states = [(bits, 4**(16-bits.bit_count())) for bits in range(1 << 16)
                      if bits.bit_count() % 2 == 0]
        cls.z = sum(weight for _, weight in cls.states)
        cls.cache = {}

    @classmethod
    def star_mask(cls, mu, r, block):
        lat = cls.lat
        star = lat.incident[lat.prototype(mu, r)]
        return sum(1 << cls.index[lat.block_plaquette(p, block, (0, 0))] for p in star)

    @classmethod
    def numerator(cls, requirements):
        key = tuple(sorted(set(requirements)))
        if key not in cls.cache:
            cls.cache[key] = sum(weight for bits, weight in cls.states
                                 if all((bits & mask).bit_count() >= count
                                        for mask, count in key))
        return cls.cache[key]

    def test_exact_gauge_image_and_partition(self):
        rows = [sum(1 << self.index[p] for p in self.lat.incident[e])
                for e in self.lat.links]
        self.assertTrue(all(row.bit_count() % 2 == 0 for row in rows))
        self.assertEqual(gf2_rank(rows), 15)
        self.assertEqual(len(self.states), 1 << 15)
        # Sum_even binomial(16,k) 4^(16-k) = (5^16+3^16)/2.
        self.assertEqual(2*self.z, 5**16+3**16)

    def test_event_chessboard_for_distinct_blocks_exactly(self):
        rng = random.Random(SEED+3)
        cases = []
        for size in range(1, 5):
            for _ in range(6):
                selected = rng.sample(list(self.blocks), size)
                events = [(block, rng.randrange(2), rng.randrange(2), rng.randrange(1, 3))
                          for block in selected]
                cases.append(events)
        for events in cases:
            local = [(self.star_mask(mu, r, block), count)
                     for block, mu, r, count in events]
            numerator = self.numerator(local)
            right = self.z**(4-len(events))
            for _, mu, r, count in events:
                disseminated = [(self.star_mask(mu, r, block), count) for block in self.blocks]
                right *= self.numerator(disseminated)
            self.assertLessEqual(numerator**4, right, events)

    def test_duplicate_block_negative_control(self):
        local = [(self.star_mask(0, 0, (0, 0)), 2)]
        disseminated = [(self.star_mask(0, 0, block), 2) for block in self.blocks]
        a = self.numerator(local)
        d = self.numerator(disseminated)
        # Counting the SAME event twice on the SAME block violates the bound.
        self.assertGreater(a**4, d*d*self.z**2)

    def test_arbitrary_reweighting_cancels_the_wilson_suppression(self):
        # Multiplication by Q=4^number_bad cancels the integer Wilson weights.
        weighted_total = sum(weight*4**bits.bit_count() for bits, weight in self.states)
        weighted_bad = sum(weight*4**bits.bit_count() for bits, weight in self.states if bits & 1)
        self.assertEqual(2*weighted_bad, weighted_total)
        raw_bad = sum(weight for bits, weight in self.states if bits & 1)
        self.assertLess(2*raw_bad, self.z)


if __name__ == '__main__':
    print('Boundary-cost diagnostics: Python standard library; seed', SEED, flush=True)
    print('4D SU(2) geometry/algebra, scalar controls, and EXACT 2D Z2 comparison checks.', flush=True)
    print('NOT a SU(2) partition-function calculation, analytic proof, RG estimate, or mass-gap claim.', flush=True)
    unittest.main(verbosity=2)
