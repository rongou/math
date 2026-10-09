#!/usr/bin/env python3
"""Reproducible diagnostics for the fourth-pass weighted boundary note.

No downloads, filesystem writes, sibling imports, or external dependencies.
Finite probability calculations use Fraction; Q8 link algebra is integer exact.
The Z2 checks are in a DIFFERENT 2D gauge model, not 4D SU(2) integration.
Tests do not prove chessboard, continuum results, or RG closure.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
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


def normalized(masses):
    total = sum(masses, F(0))
    if total <= 0:
        raise ValueError('nonpositive normalizer')
    return [value/total for value in masses]


def push(mass, kernel):
    size = len(mass)
    return [sum((mass[i]*kernel[i][j] for i in range(size)), F(0))
            for j in range(size)]


def zero_kernel(size):
    return [[F(0) for _ in range(size)] for _ in range(size)]


def accepted(kernel, event):
    return [row[:] if i in event else [F(0)]*len(row)
            for i, row in enumerate(kernel)]


class FiniteConditionalModel:
    """Abstract product-Haar analogue, not a continuous lattice calculation."""
    def __init__(self):
        self.states = tuple(product(range(4), range(4)))  # (edited x, frozen z)
        self.energy_by_z = ((0, 2, 4, 6), (2, 4, 2, 6),
                            (6, 6, 6, 6), (5, 7, 5, 9))
        self.energy = [self.energy_by_z[z][x] for x, z in self.states]
        self.minimum = [min(self.energy_by_z[z]) for x, z in self.states]
        self.mu = normalized([F(1, 4)**e for e in self.energy])  # H=log(4)
        self.kernel = zero_kernel(len(self.states))
        for i, (x, z) in enumerate(self.states):
            outputs = [j for j, (y, zz) in enumerate(self.states)
                       if zz == z and self.energy[j] == self.minimum[i]]
            for j in outputs:
                self.kernel[i][j] = F(1, len(outputs))
        self.good = {i for i in range(16)
                     if self.minimum[i] <= 2 and self.energy[i] >= self.minimum[i]+2}
        self.bad = {i for i in range(16) if self.minimum[i] > 3}

    def tilt(self, weight):
        return normalized([m*q for m, q in zip(self.mu, weight)])

    def projection(self, weight):
        mean = sum((m*q for m, q in zip(self.mu, weight)), F(0))
        marginal = [sum(self.mu[i] for i, (_, zz) in enumerate(self.states) if zz == z)
                    for z in range(4)]
        numerator = [sum(self.mu[i]*weight[i] for i, (_, zz) in enumerate(self.states) if zz == z)
                     for z in range(4)]
        ratio = [num/(mass*mean) for num, mass in zip(numerator, marginal)]
        return marginal, ratio

    def edit_ratio(self, weight, event):
        return max([F(1)]+[weight[i]/weight[j] for i in event
                          for j, value in enumerate(self.kernel[i]) if value])


class MarginalAndComparisonTests(unittest.TestCase):
    def setUp(self):
        self.model = FiniteConditionalModel()

    def test_local_projection_has_full_normalizer_and_mean_one(self):
        model = self.model
        rng = random.Random(SEED)
        for _ in range(16):
            weight = [F(rng.randrange(1, 19), rng.randrange(1, 8)) for _ in model.states]
            nu = model.tilt(weight)
            mz, r = model.projection(weight)
            self.assertEqual(sum(m*v for m, v in zip(mz, r)), 1)
            for z in range(4):
                actual = sum(nu[i] for i, (_, zz) in enumerate(model.states) if zz == z)
                self.assertEqual(actual, mz[z]*r[z])
            # Replacing the full normalizer by a conditional one would give r=1.
            self.assertTrue(any(value != 1 for value in r))

    def test_exterior_tilt_defeats_edit_stability_exactly(self):
        model = self.model
        t = sum(model.mu[i] for i in model.bad)
        self.assertTrue(0 < t < F(1, 100))
        for desired in (F(1, 2), F(9, 10), F(99, 100)):
            q = desired*(1-t)/((1-desired)*t)
            weight = [q if i in model.bad else F(1) for i in range(16)]
            nu = model.tilt(weight)
            self.assertEqual(sum(nu[i] for i in model.bad), desired)
            for i in range(16):
                for j, mass in enumerate(model.kernel[i]):
                    if mass:
                        self.assertEqual(weight[i], weight[j])
            mz, density = model.projection(weight)
            for exponent in (2, 3, 4):
                norm_power = sum(m*r**exponent for m, r in zip(mz, density))
                expected = desired**exponent*t**(1-exponent)
                expected += (1-desired)**exponent*(1-t)**(1-exponent)
                self.assertEqual(norm_power, expected)
                self.assertGreater(norm_power, 1)
            self.assertGreater(desired, t)

    def test_holder_marginal_transfer_with_finite_and_infinite_exponents(self):
        model = self.model
        rng = random.Random(SEED+1)
        raw_bad = sum(model.mu[i] for i in model.bad)
        for _ in range(24):
            weight = [F(rng.randrange(1, 30), 7) for _ in model.states]
            nu = model.tilt(weight)
            mz, density = model.projection(weight)
            actual = sum(nu[i] for i in model.bad)
            for r in (2, 3, 4):
                norm_r = sum(m*q**r for m, q in zip(mz, density))
                self.assertLessEqual(actual**r, norm_r*raw_bad**(r-1))
            self.assertLessEqual(actual, max(density)*raw_bad)

    def test_bounded_oscillation_tilt_verifies_both_requirements(self):
        model = self.model
        weight = [F(8+(3*x+z) % 7, 8) for x, z in model.states]
        ratio = max(weight)/min(weight)
        mz, density = model.projection(weight)
        self.assertLessEqual(max(density), ratio)
        self.assertLessEqual(model.edit_ratio(weight, set(range(16))), ratio)
        nu = model.tilt(weight)
        for subset in (model.bad, model.good, {0, 5, 10}, set(range(16))):
            self.assertLessEqual(sum(nu[i] for i in subset),
                                 ratio*sum(model.mu[i] for i in subset))
        # Multiplying by a scalar changes neither normalized law nor projection.
        self.assertEqual(nu, model.tilt([12345*q for q in weight]))
        self.assertEqual((mz, density), model.projection([12345*q for q in weight]))

    def test_local_projection_avoids_irrelevant_global_norm_in_product_toy(self):
        # For independent fair bits and Q=product q_i, q_i in {1,3}, all far
        # factors cancel from the projection on the first bit. NOT Wilson independence.
        local_second_moment = (F(1, 2)**2+F(3, 2)**2)/2
        self.assertEqual(local_second_moment, F(5, 4))
        for count in (1, 4, 16, 64):
            conditional_means = [q*2**(count-1) for q in (1, 3)]
            ratios = [F(q, 2**count) for q in conditional_means]
            self.assertEqual(sum(q*q for q in ratios)/2, local_second_moment)
            global_second_moment = F(5, 4)**count
            self.assertGreaterEqual(global_second_moment, local_second_moment)

    def test_weighted_accepted_output_domination_pointwise(self):
        model = self.model
        rng = random.Random(SEED+2)
        for _ in range(16):
            outside = [F(rng.randrange(1, 101)) for _ in range(4)]
            weight = [outside[z]*F(rng.randrange(4, 9), 4) for x, z in model.states]
            nu = model.tilt(weight)
            operator = accepted(model.kernel, model.good)
            output = push(nu, operator)
            # density M=4 relative to edited uniform probability measure;
            # minimum accepted energy drop 2, exp(-H*2)=1/16.
            bound = 4*F(1, 16)*model.edit_ratio(weight, model.good)
            self.assertLess(bound, 1)
            self.assertEqual(sum(output), sum(nu[i] for i in model.good))
            self.assertTrue(all(v <= bound*m for v, m in zip(output, nu)))
            f = [F((i % 5)-2) for i in range(16)]
            self.assertLessEqual(sum(abs(v)*m for v, m in zip(f, output)),
                                 bound*sum(abs(v)*m for v, m in zip(f, nu)))

    def test_two_branches_are_controlled_in_the_same_weighted_measure(self):
        model = self.model
        weight = [F(1+z*3)*F(4+x, 4) for x, z in model.states]
        nu = model.tilt(weight)
        good_mass = sum(nu[i] for i in model.good)
        bad_mass = sum(nu[i] for i in model.bad)
        union_mass = sum(nu[i] for i in model.good | model.bad)
        self.assertEqual(union_mass, good_mass+bad_mass)
        low_bound = F(1, 4)*model.edit_ratio(weight, model.good)
        self.assertLessEqual(good_mass, low_bound)
        mz, density = model.projection(weight)
        raw_bad = sum(model.mu[i] for i in model.bad)
        square_bound = sum(m*r*r for m, r in zip(mz, density))*raw_bad
        self.assertLessEqual(bad_mass*bad_mass, square_bound)
        if union_mass > low_bound:
            self.assertLessEqual((union_mass-low_bound)**2, square_bound)

    def test_output_weighted_integral_is_not_a_weighted_probability(self):
        model = self.model
        weight = [F(4)**e for e in model.energy]  # cancels raw energy exactly
        nu = model.tilt(weight)
        self.assertEqual(set(nu), {F(1, 16)})
        actual = sum(nu[i] for i in model.good)
        mean_q = sum(m*q for m, q in zip(model.mu, weight))
        literal = sum(model.mu[i]*sum(k*q for k, q in zip(model.kernel[i], weight))
                      for i in model.good)/mean_q
        self.assertLessEqual(literal, F(1, 4))
        self.assertGreater(actual, F(1, 4))
        self.assertNotEqual(actual, literal)

    def test_positive_weight_replacement_integral_can_exceed_one(self):
        mass_a, mass_b, boltzmann, q_a, q_b = F(99, 100), F(1, 100), F(1, 10), F(1), F(10000)
        z = mass_a*boltzmann*q_a+mass_b*q_b
        literal = mass_a*boltzmann*q_b/z
        probability = mass_a*boltzmann*q_a/z
        self.assertGreater(literal, 1)
        self.assertLessEqual(literal, boltzmann/mass_b)
        self.assertLess(probability, 1)


class CompositionTests(unittest.TestCase):
    def test_two_successful_repairs_compose_by_measure_domination(self):
        states = tuple(product(range(3), repeat=2))
        mu = normalized([F(1, 4)**(2*sum(x)) for x in states])
        q = [1+F(sum(x), 4) for x in states]
        nu = normalized([m*w for m, w in zip(mu, q)])
        transitions = []
        constants = []
        for axis in (0, 1):
            kernel = zero_kernel(9)
            ratios = []
            for i, x in enumerate(states):
                if x[axis] == 0:
                    continue
                y = list(x)
                y[axis] = 0
                j = states.index(tuple(y))
                kernel[i][j] = 1
                ratios.append(q[i]/q[j])
            c = 3*F(1, 16)*max(ratios)
            self.assertLess(c, 1)
            output = push(nu, kernel)
            self.assertTrue(all(v <= c*m for v, m in zip(output, nu)))
            transitions.append(kernel)
            constants.append(c)
        actual = push(push(nu, transitions[0]), transitions[1])
        bound = constants[0]*constants[1]
        self.assertTrue(all(v <= bound*m for v, m in zip(actual, nu)))
        self.assertGreater(sum(actual), 0)  # Nonvacuous accepted paths.

    def test_adaptive_geometry_count_cannot_be_omitted(self):
        states = tuple(product((0, 1), repeat=4))
        nu = normalized([F(1, 16)**sum(x) for x in states])
        kernel = zero_kernel(16)
        for i, x in enumerate(states):
            if not any(x):
                continue
            axis = x.index(1)  # source-dependent support choice
            y = list(x)
            y[axis] = 0
            kernel[i][states.index(tuple(y))] = 1
        output = push(nu, kernel)
        fixed_support_bound = F(2, 16)
        self.assertGreater(sum(output), fixed_support_bound)
        self.assertLessEqual(sum(output), 4*fixed_support_bound)
        self.assertTrue(all(v <= 4*fixed_support_bound*m for v, m in zip(output, nu)))
        self.assertGreater(output[0], fixed_support_bound*nu[0])

    def test_retained_exception_is_not_a_small_operator_or_independent_label(self):
        nu = [F(99, 100), F(1, 100)]
        operator = [[F(0), F(0)], [F(0), F(1)]]
        once = push(nu, operator)
        twice = push(once, operator)
        self.assertEqual(once, twice)
        self.assertEqual(sum(twice), F(1, 100))
        self.assertGreater(sum(twice), F(1, 100)**2)
        self.assertGreater(once[1], F(1, 100)*nu[1])

    def test_ungated_near_minimum_output_is_not_the_original_law(self):
        model = FiniteConditionalModel()
        output = push(model.mu, model.kernel)
        minima = {i for i in range(16) if model.energy[i] == model.minimum[i]}
        self.assertEqual(sum(output[i] for i in minima), 1)
        self.assertLess(sum(model.mu[i] for i in minima), 1)
        # Here the finite kernel is nonincreasing in energy and M<=4.
        self.assertTrue(all(v <= 4*m for v, m in zip(output, model.mu)))
        self.assertNotEqual(output, model.mu)


class Cube:
    def __init__(self, side=4, dim=4):
        self.side, self.dim = side, dim
        self.sites = tuple(product(range(side), repeat=dim))
        self.links = tuple((x, d) for x in self.sites for d in range(dim))
        self.plaquettes = tuple((x, a, b) for x in self.sites
                               for a, b in combinations(range(dim), 2))
        self.boundaries = {p: self.boundary(p) for p in self.plaquettes}
        self.stars = {e: [] for e in self.links}
        for p, edges in self.boundaries.items():
            for e, _ in edges:
                self.stars[e].append(p)
        self.cell_edges = {x: self.edges_of_cell(x) for x in self.sites}
        self.cell_plaquettes = {x: self.faces_of_cell(x) for x in self.sites}

    def offset(self, x, v):
        return tuple((a+b) % self.side for a, b in zip(x, v))

    def step(self, x, axis, direction=1):
        return tuple((v+direction*int(j == axis)) % self.side for j, v in enumerate(x))

    def boundary(self, p):
        x, a, b = p
        return (((x, a), 1), ((self.step(x, a), b), 1),
                ((self.step(x, b), a), -1), ((x, b), -1))

    def edges_of_cell(self, x):
        return frozenset((self.offset(x, v), a)
                         for a in range(self.dim)
                         for v in product((0, 1), repeat=self.dim) if v[a] == 0)

    def faces_of_cell(self, x):
        return frozenset((self.offset(x, v), a, b)
                         for a, b in combinations(range(self.dim), 2)
                         for v in product((0, 1), repeat=self.dim) if v[a] == v[b] == 0)

    def reflect_vertex(self, x, axis, plane):
        return tuple((2*plane-v) % self.side if j == axis else v
                     for j, v in enumerate(x))

    def reflect_edge(self, e, axis, plane):
        x, direction = e
        y = self.reflect_vertex(x, axis, plane)
        if direction == axis:
            return (self.step(y, axis, -1), direction), -1
        return (y, direction), 1

    def reflect_cell(self, x, axis, plane):
        return self.step(self.reflect_vertex(x, axis, plane), axis, -1)

    def reflect_field(self, field, axis, plane, invert=True):
        output = {}
        for e, value in field.items():
            target, sign = self.reflect_edge(e, axis, plane)
            output[target] = qinv(value) if sign == -1 and invert else value
        return output

    def half(self, e, axis, plane):
        x, direction = e
        v = (2*x[axis]+int(direction == axis)-2*plane) % (2*self.side)
        return 0 if v in (0, self.side) else (1 if v < self.side else -1)

    def energy(self, field):
        energies = {}
        for p, edges in self.boundaries.items():
            value = ONE
            for e, sign in edges:
                value = qmul(value, field[e] if sign == 1 else qinv(field[e]))
            energies[p] = 1-value[0]
        return energies

    def gauge_transform(self, field, gauges):
        return {e: qmul(qmul(gauges[e[0]], value),
                        qinv(gauges[self.step(e[0], e[1])]))
                for e, value in field.items()}

    def cell_potential(self, field):
        energies = self.energy(field)
        # A genuinely coupled, bounded gauge-invariant cell potential in [0,1].
        max_energy = 2*len(next(iter(self.cell_plaquettes.values())))
        return {c: F(sum(energies[p] for p in faces)**2, max_energy**2)
                for c, faces in self.cell_plaquettes.items()}


class CellGeometryAndNonabelianTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lat = Cube()

    def test_cell_incidence_constants_32_24_8_4(self):
        lat = self.lat
        self.assertEqual(set(map(len, lat.cell_edges.values())), {32})
        self.assertEqual(set(map(len, lat.cell_plaquettes.values())), {24})
        edge_counts = Counter(e for edges in lat.cell_edges.values() for e in edges)
        face_counts = Counter(p for faces in lat.cell_plaquettes.values() for p in faces)
        self.assertEqual(set(edge_counts), set(lat.links))
        self.assertEqual(set(face_counts), set(lat.plaquettes))
        self.assertEqual(set(edge_counts.values()), {8})
        self.assertEqual(set(face_counts.values()), {4})

    def test_cells_do_not_cross_both_strict_reflection_halves(self):
        lat = self.lat
        for axis, plane in product(range(4), range(4)):
            for cell, edges in lat.cell_edges.items():
                sides = {lat.half(e, axis, plane) for e in edges}
                self.assertFalse({-1, 1}.issubset(sides), (axis, plane, cell))
                reflected = {lat.reflect_edge(e, axis, plane)[0] for e in edges}
                self.assertEqual(reflected, lat.cell_edges[lat.reflect_cell(cell, axis, plane)])

    def test_refined_midpoint_encoding_and_orthogonal_commutation(self):
        lat = self.lat
        for e in lat.links:
            x, direction = e
            v = tuple(2*x[j]+int(j == direction) for j in range(4))
            self.assertEqual(sum(z % 2 for z in v), 1)
            for axis in range(4):
                target, sign = lat.reflect_edge(e, axis, 1)
                y, mu = target
                encoded = tuple(2*y[j]+int(j == mu) for j in range(4))
                expected = tuple((4-z) % 8 if j == axis else z for j, z in enumerate(v))
                self.assertEqual(encoded, expected)
                self.assertEqual(sign, -1 if direction == axis else 1)
            for a, b in combinations(range(4), 2):
                ae, sa = lat.reflect_edge(e, a, 0)
                ab, sb = lat.reflect_edge(ae, b, 1)
                be, tb = lat.reflect_edge(e, b, 1)
                ba, ta = lat.reflect_edge(be, a, 0)
                self.assertEqual((ab, sa*sb), (ba, ta*tb))

    def test_exact_noncommuting_Q8_reflections_and_wrong_orientation_control(self):
        lat = self.lat
        rng = random.Random(SEED+3)
        self.assertNotEqual(qmul((0, 1, 0, 0), (0, 0, 1, 0)),
                            qmul((0, 0, 1, 0), (0, 1, 0, 0)))
        field = {e: rng.choice(Q8) for e in lat.links}
        original_energy = sum(lat.energy(field).values())
        original_potentials = lat.cell_potential(field)
        detected = False
        for axis, plane in product(range(4), (0, 1)):
            output = lat.reflect_field(field, axis, plane)
            self.assertEqual(lat.reflect_field(output, axis, plane), field)
            self.assertEqual(sum(lat.energy(output).values()), original_energy)
            potentials = lat.cell_potential(output)
            for cell, value in original_potentials.items():
                self.assertEqual(potentials[lat.reflect_cell(cell, axis, plane)], value)
            wrong = lat.reflect_field(field, axis, plane, invert=False)
            detected |= sum(lat.energy(wrong).values()) != original_energy
        self.assertTrue(detected, 'wrong normal-link inversion was not caught')

    def test_gauge_invariance_and_bounded_cell_edit_cost(self):
        lat = self.lat
        rng = random.Random(SEED+4)
        field = {e: rng.choice(Q8) for e in lat.links}
        original = lat.cell_potential(field)
        gauges = {x: rng.choice(Q8) for x in lat.sites}
        self.assertEqual(original, lat.cell_potential(lat.gauge_transform(field, gauges)))
        self.assertTrue(all(0 <= v <= 1 for v in original.values()))
        for n in (1, 4, 16, 64):
            edited = set(rng.sample(list(lat.links), n))
            output = {e: rng.choice(Q8) if e in edited else value for e, value in field.items()}
            new = lat.cell_potential(output)
            touched = {c for c, edges in lat.cell_edges.items() if edges & edited}
            self.assertLessEqual(len(touched), 8*n)
            for c in set(lat.sites)-touched:
                self.assertEqual(original[c], new[c])
            self.assertLessEqual(abs(sum(new.values())-sum(original.values())), len(touched))
            self.assertLessEqual(abs(sum(new.values())-sum(original.values())), 8*n)

    def test_squared_plaquette_example_cell_decomposition_and_sharper_cost(self):
        lat = self.lat
        rng = random.Random(SEED+5)
        field = {e: rng.choice(Q8) for e in lat.links}
        original = lat.energy(field)
        for gamma in (F(-3, 7), F(0), F(2, 5)):
            cells = {c: gamma/4*sum(original[p]**2 for p in faces)
                     for c, faces in lat.cell_plaquettes.items()}
            self.assertEqual(sum(cells.values()), gamma*sum(v*v for v in original.values()))
            for n in (1, 8, 32):
                edited = set(rng.sample(list(lat.links), n))
                output = {e: rng.choice(Q8) if e in edited else v for e, v in field.items()}
                new = lat.energy(output)
                delta = abs(gamma*(sum(v*v for v in new.values())-sum(v*v for v in original.values())))
                self.assertLessEqual(delta, 24*abs(gamma)*n)
            self.assertEqual(F(24, 8)*abs(gamma), 3*abs(gamma))

    def test_frustrated_boundary_label_uses_only_frozen_staples(self):
        lat = self.lat
        root = ((0, 0, 0, 0), 0)
        field = {e: ONE for e in lat.links}
        for axis in (1, 2, 3):
            field[(lat.step(root[0], axis), 0)] = (-1, 0, 0, 0)
        frozen = {e for p in lat.stars[root] for e, _ in lat.boundaries[p]}-{root}
        self.assertEqual(len(frozen), 18)
        for q in Q8:
            field[root] = q
            energies = lat.energy(field)
            self.assertEqual(sum(energies[p] for p in lat.stars[root]), 6)
        # Exact algebra witnesses m_*=6; neighborhood/measure claims are analytic.

    def test_longer_support_breaks_the_cell_split_and_symmetry_is_not_RP(self):
        lat = self.lat
        left = ((0, 0, 0, 0), 0)
        right = ((1, 0, 0, 0), 0)
        self.assertEqual({lat.half(e, 0, 1) for e in (left, right)}, {-1, 1})
        # Positive reflection-symmetric two-spin antiferromagnetic weight.
        states = tuple(product((-1, 1), repeat=2))
        nu = normalized([F(1, 4) if a == b else F(1) for a, b in states])
        correlation = sum(m*a*b for m, (a, b) in zip(nu, states))
        self.assertEqual(correlation, F(-3, 5))
        self.assertLess(correlation, 0)


class BudgetTests(unittest.TestCase):
    def test_chessboard_volume_loss_becomes_local_constant(self):
        for side in (4, 8, 16, 32):
            v = side**4
            blocks = (side//2)**4
            self.assertEqual(F(4*v, blocks), 64)
            self.assertEqual(F(v, blocks), 16)
            for theta in (F(1, 8), F(1, 2), F(7, 8)):
                a, epsilon = F(13, 3), F(7, 5)
                self.assertEqual(theta*(64*a+16*epsilon)/64, theta*(a+epsilon/4))
        self.assertEqual(F(1, 2)*F(1, 4), F(1, 8))

    def test_weighted_split_absorption_constants(self):
        ell, b, epsilon = F(9, 2), F(17, 3), F(3, 7)
        b_hat = b+epsilon/8
        for n, k in product((1, 4, 17), (1, 3, 11)):
            p2 = max(F(96*n, k), 16*n*(ell+8*epsilon)/k, 1024*n*b_hat/k)
            low = -k*p2/8+(ell+8*epsilon)*n
            high = -k*p2/512+b_hat*n
            self.assertLessEqual(low, -k*p2/16)
            self.assertLessEqual(high, -k*p2/1024)
            output_count = F(k, 2)+24*n/p2
            self.assertLessEqual(output_count, F(3*k, 4))

    def test_rooted_adaptive_kernel_sum_and_acceptance_budget(self):
        w = F(1, 1000)  # w=exp(-d_H), with 324w<1 and 325w<1.
        partial = sum(F(324)**(n-1)*w**n for n in range(1, 41))
        tail = w*(324*w)**40/(1-324*w)
        total = w/(1-324*w)
        self.assertEqual(partial+tail, total)
        self.assertLess(total, 1)
        self.assertEqual(F(1, 325)/(1-F(324, 325)), 1)
        for n in range(1, 100):
            k = (n+3)//4
            self.assertGreaterEqual(k*384, 96*n)
            self.assertGreaterEqual(F(k, 8), F(n, 32))

    def test_energy_cancelling_weight_makes_bound_vacuous_not_false(self):
        for h in (1, 100, 1000000):
            epsilon = 12*h
            # Drop b_H>=0 to give the MOST favorable possible exponent.
            largest_kappa = F(4*h, 1024)-F(epsilon, 8)
            self.assertLess(largest_kappa, 0)

    def test_no_spurious_whole_volume_factor_in_local_budget(self):
        n, epsilon, a = 5, F(2, 3), F(9, 2)
        values = []
        for side in (4, 8, 16):
            v, m = side**4, (side//2)**4
            star_cost = F(4*v, m)*a+F(v, m)*epsilon
            local_moment_cost = F(n, 128)*star_cost  # theta=1/2, apart from log(2)
            values.append(local_moment_cost)
        self.assertEqual(len(set(values)), 1)
        self.assertEqual(values[0], n*(a/2+epsilon/8))

    def test_nonempty_rough_regime_has_a_nonvacuous_example(self):
        h = math.exp(24)
        epsilon = math.log(h)/10
        ell = math.log(24)+1.5*math.log(h)
        a = 1.5+math.log(24)+1.5*math.log(8*h)
        b_hat = a/2+math.log(2)/64+epsilon/8
        p = 150*math.sqrt(math.log(h))
        self.assertLess(p/math.sqrt(h), 2)
        # k>=n/4, so these sufficient n-independent budgets imply both branches.
        self.assertGreater(p*p, 384)
        self.assertGreater(p*p, 64*(ell+8*epsilon))
        self.assertGreater(p*p, 4096*b_hat)
        self.assertGreater(p*p/1024-b_hat, 2*math.log(18))


def gf2_rank(columns):
    pivots = {}
    for col in columns:
        while col:
            pivot = col.bit_length()-1
            if pivot in pivots:
                col ^= pivots[pivot]
            else:
                pivots[pivot] = col
                break
    return len(pivots)


class ExactWeightedZ2Tests(unittest.TestCase):
    """Exact 2D Z2 torus weights, not a test of 4D SU(2) probabilities."""
    @classmethod
    def setUpClass(cls):
        cls.lat = Cube(dim=2)
        cls.pindex = {p: i for i, p in enumerate(cls.lat.plaquettes)}
        cls.blocks = tuple(product(range(2), repeat=2))
        cls.bits = [i for i in range(1 << 16) if i.bit_count() % 2 == 0]
        cls.weights = {}
        cls.normalizers = {}
        cls.cache = {}
        # Relative weight per bad plaquette. These are positive cell-local tilts
        # of a raw weight 1/16 per bad plaquette, including both signs of the tilt.
        for a, b in ((1, 4), (1, 64), (4, 1)):
            weights = [a**bits.bit_count()*b**(16-bits.bit_count()) for bits in cls.bits]
            cls.weights[(a, b)] = weights
            cls.normalizers[(a, b)] = sum(weights)

    @classmethod
    def mask(cls, direction, prototype, block):
        start = tuple(prototype if j == direction else 1 for j in range(2))
        result = 0
        for x, mu, nu in cls.lat.stars[(start, direction)]:
            y = tuple((2*block[j]+(x[j] if block[j] % 2 == 0 else 1-x[j])) % 4
                      for j in range(2))
            result |= 1 << cls.pindex[(y, mu, nu)]
        return result

    @classmethod
    def numerator(cls, weight_key, requirements):
        key = (weight_key, tuple(sorted(set(requirements))))
        if key not in cls.cache:
            cls.cache[key] = sum(w for bits, w in zip(cls.bits, cls.weights[weight_key])
                                 if all((bits & mask).bit_count() >= count
                                        for mask, count in key[1]))
        return cls.cache[key]

    def test_even_flux_enumeration_and_weight_normalization(self):
        columns = [sum(1 << self.pindex[p] for p in self.lat.stars[e]) for e in self.lat.links]
        self.assertTrue(all(col.bit_count() % 2 == 0 for col in columns))
        self.assertEqual(gf2_rank(columns), 15)
        self.assertEqual(len(self.bits), 2**15)
        for (a, b), z in self.normalizers.items():
            self.assertEqual(2*z, (a+b)**16+(b-a)**16)

    def test_weighted_event_chessboard_with_distinct_blocks_exactly(self):
        rng = random.Random(SEED+6)
        for size in (1, 2, 3, 4):
            for _ in range(5):
                events = [(block, rng.randrange(2), rng.randrange(2), rng.randrange(1, 3))
                          for block in rng.sample(list(self.blocks), size)]
                local = [(self.mask(mu, prototype, block), count)
                         for block, mu, prototype, count in events]
                for weight_key, z in self.normalizers.items():
                    left = self.numerator(weight_key, local)**4
                    right = z**(4-size)
                    for _, mu, prototype, count in events:
                        full = [(self.mask(mu, prototype, block), count) for block in self.blocks]
                        right *= self.numerator(weight_key, full)
                    self.assertLessEqual(left, right, (weight_key, events))

    def test_duplicate_block_still_fails_after_positive_reweighting(self):
        for weight_key in ((1, 4), (1, 64)):
            z = self.normalizers[weight_key]
            single = [(self.mask(0, 0, (0, 0)), 2)]
            full = [(self.mask(0, 0, block), 2) for block in self.blocks]
            a, d = self.numerator(weight_key, single), self.numerator(weight_key, full)
            self.assertGreater(a**4, d*d*z*z)


if __name__ == '__main__':
    print('Weighted-boundary diagnostics; standard library only; seed', SEED, flush=True)
    print('Exact rational probabilities, integer Q8 links, 4D cell geometry, and exact 2D Z2 sums.', flush=True)
    print('NOT an SU(2) partition-function computation, independent review, analytic proof, or RG certificate.', flush=True)
    unittest.main(verbosity=2)
