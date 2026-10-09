#!/usr/bin/env python3
"""Independent checks for the four-dimensional finite-size argument.

Standard library only. Exact integer coefficient identities and Fraction
certificates check the scalar bookkeeping. Decimal examples are regression
checks, not a proof of the operator theorem or of Yang--Mills mass generation.
"""
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import permutations
import random
import unittest


DIM = 4
EPSILON = Fraction(1, 2048)
RECURSION_CONSTANT = 1024
A_CAPS = (1, 3, 5, 9)
U_CAPS = tuple(4 * a * a for a in A_CAPS)


def shifted(v, i):
    w = list(v)
    w[i] += 1
    return tuple(w)


def linear_combination(*terms):
    result = defaultdict(int)
    for coefficient, expression in terms:
        for variable, value in expression.items():
            result[variable] += coefficient * value
    return {key: value for key, value in result.items() if value}


def p(i, v):
    """Formal expression 2 F(v) - F(v + e_i), with logarithmic side lengths."""
    return {v: 2, shifted(v, i): -1}


def defect(v):
    return {v: 2 ** len(v), tuple(x + 1 for x in v): -1}


def log_trace_defect(spectrum, n):
    zn = sum(x ** n for x in spectrum)
    z2n = sum(x ** (2 * n) for x in spectrum)
    return 2 * zn.ln() - z2n.ln()


def product_chain_log_z(lengths, q):
    """Actual RP model: four independent spin species, one chain per axis.

    Each single-chain transfer kernel is 1 + q*s*t on probability-uniform
    spins s,t in {-1,1}, with eigenvalues 1,q. In direction i there are
    product(lengths[j], j != i) independent periodic chains.
    """
    volume = 1
    for length in lengths:
        volume *= length
    return sum(Decimal(volume // n) * (1 + q ** n).ln() for n in lengths)


class FormalIdentityTests(unittest.TestCase):
    def test_every_telescoping_order(self):
        for order in permutations(range(DIM)):
            v = (0,) * DIM
            terms = []
            for step, i in enumerate(order):
                terms.append((2 ** (DIM - step - 1), p(i, v)))
                v = shifted(v, i)
            self.assertEqual(linear_combination(*terms), defect((0,) * DIM))

    def test_rectangle_identities(self):
        origin = (0,) * DIM
        for i in range(DIM):
            for j in range(DIM):
                if i == j:
                    continue
                rhs = linear_combination(
                    (2, p(i, origin)),
                    (-2, p(j, origin)),
                    (1, p(j, shifted(origin, i))),
                )
                self.assertEqual(p(i, shifted(origin, j)), rhs)

    def test_unsquared_direction_bookkeeping(self):
        for i in range(DIM):
            base = tuple(0 if h == i else 1 for h in range(DIM))
            target = tuple(2 if h < i else 0 if h == i else 1
                           for h in range(DIM))
            terms = [(2 ** i, p(i, base))]
            for j in range(i):
                x = tuple(2 if h < j else 0 if h == i else 1
                          for h in range(DIM))
                u_base = tuple(2 if h < j else 1 for h in range(DIM))
                weight = 2 ** (i - j - 1)
                # Exact equality; the -2*p_j(x) terms can be discarded
                # only after positivity of the directional traces is proved.
                terms.extend([(weight, p(j, u_base)),
                              (-2 * weight, p(j, x))])
            self.assertEqual(p(i, target), linear_combination(*terms))

    def test_final_weighted_defect(self):
        terms = []
        for i in range(DIM):
            x = tuple(2 if h < i else 1 for h in range(DIM))
            terms.append((2 ** (DIM - i - 1), p(i, x)))
        self.assertEqual(linear_combination(*terms), defect((1,) * DIM))


class ExactConstantTests(unittest.TestCase):
    def test_inductive_linear_caps(self):
        for i, cap in enumerate(A_CAPS):
            quadratic = sum(2 ** (i - j - 1) * U_CAPS[j]
                            for j in range(i))
            # For 0 <= delta <= epsilon, delta^2 <= epsilon*delta.
            self.assertLessEqual(2 ** i + quadratic * EPSILON, cap)
            self.assertLessEqual(cap * EPSILON, Fraction(1, 4))
            self.assertEqual(U_CAPS[i], 4 * cap * cap)

    def test_recursion_and_threshold(self):
        total = sum(2 ** (DIM - i - 1) * U_CAPS[i] for i in range(DIM))
        self.assertEqual(total, 700)
        self.assertLessEqual(total, RECURSION_CONSTANT)
        self.assertEqual(RECURSION_CONSTANT * EPSILON, Fraction(1, 2))
        self.assertLessEqual(RECURSION_CONSTANT * EPSILON ** 2, EPSILON)

    def test_iterated_majorant(self):
        delta = EPSILON
        for k in range(9):
            majorant = Fraction(1, RECURSION_CONSTANT * 2 ** (2 ** k))
            self.assertEqual(delta, majorant)
            delta = RECURSION_CONSTANT * delta * delta

    def test_cutoff_comparison_volume_factor(self):
        # Simultaneous 4D doubling cancels the same bulk constant and
        # costs 16 errors on M plus one error on 2M.
        self.assertEqual(16 * 1 ** 4 - 2 ** 4, 0)
        self.assertEqual(16 * 1 ** 4 + 2 ** 4, 32)

    def test_elementary_strong_coupling_bound(self):
        plaquettes = 6 * 4 ** 4
        bound = 16 * plaquettes * Fraction(1, 2 ** 26)
        self.assertEqual(bound, Fraction(3, 8192))
        self.assertLess(bound, EPSILON)


class NumericalRegressionTests(unittest.TestCase):
    def test_positive_spectra_purity_and_squaring(self):
        rng = random.Random(20261009)
        with localcontext() as ctx:
            ctx.prec = 100
            samples = [
                [Decimal(1)],
                [Decimal(1), Decimal(1)],  # Degenerate ground state.
                [Decimal(1), Decimal('0.9999')],
                [Decimal(1), Decimal('0.001')],
            ]
            for _ in range(150):
                samples.append([Decimal(1)] +
                               [Decimal(rng.randrange(1, 9999)) / 10000
                                for _ in range(rng.randrange(1, 20))])
            tolerance = Decimal('1e-85')
            for spectrum in samples:
                for n in (4, 8, 16):
                    value = log_trace_defect(spectrum, n)
                    tail = sum(x ** n for x in spectrum[1:])
                    self.assertGreaterEqual(value, -tolerance)
                    self.assertLessEqual(tail, value.exp() - 1 + tolerance)
                    if value <= Decimal('0.25'):
                        doubled = log_trace_defect(spectrum, 2 * n)
                        self.assertLessEqual(doubled, 4 * value * value + tolerance)

    def test_actual_four_dimensional_product_models(self):
        with localcontext() as ctx:
            ctx.prec = 110
            eps = Decimal(EPSILON.numerator) / EPSILON.denominator
            tolerance = Decimal('1e-90')
            successes = 0
            for q in map(Decimal, ('0', '0.01', '0.1', '0.3', '0.7', '0.95')):
                for n in (4, 8, 16, 32):
                    delta = 16 * product_chain_log_z((n,) * 4, q) - \
                            product_chain_log_z((2 * n,) * 4, q)
                    self.assertGreaterEqual(delta, -tolerance)
                    if delta <= eps:
                        successes += 1
                        delta2 = 16 * product_chain_log_z((2 * n,) * 4, q) - \
                                 product_chain_log_z((4 * n,) * 4, q)
                        self.assertLessEqual(delta2, 700 * delta * delta + tolerance)
                        # The true nonzero transfer eigenvalue ratio is q.
                        self.assertLessEqual(q ** n, Decimal('0.5'))
            self.assertGreater(successes, 5)

    def test_positive_entries_do_not_imply_positive_operator(self):
        # A strictly entrywise-positive symmetric 2x2 transfer kernel can
        # have normalized eigenvalues 1,-q; the odd-period trace test fails.
        with localcontext() as ctx:
            ctx.prec = 60
            value = log_trace_defect([Decimal(1), Decimal('-0.99')], 5)
            self.assertLess(value, 0)

    def test_one_transfer_direction_is_insufficient(self):
        # Fake time-transfer family: P + exp(-c/w)*(I-P), rank two.
        # It has a tiny 4D cubic defect, but is not a model with consistent
        # positive transfer traces in the transverse directions.
        with localcontext() as ctx:
            ctx.prec = 80
            c = Decimal(16)
            f_cube = (1 + (-c).exp()).ln()
            delta = 15 * f_cube
            self.assertLess(delta, Decimal(1) / 2048)
            n, w = 4, 128
            excited_ratio = (-c / w).exp()
            claimed_ratio = (-Decimal(2).ln() / n).exp()
            self.assertGreater(excited_ratio, claimed_ratio)
            transverse_defect = 2 * f_cube - (1 + (-c / 2).exp()).ln()
            self.assertLess(transverse_defect, 0)

    def test_uniform_gap_does_not_control_trace_multiplicities(self):
        # T_w = a I + (1-a) P on 2^w row states has a constant gap,
        # yet excited trace multiplicity swamps the w-step torus trace.
        with localcontext() as ctx:
            ctx.prec = 80
            a, w = Decimal('0.75'), 64
            tail = (Decimal(2) ** w - 1) * a ** w
            self.assertGreater(tail, 1000)
            cylinder = (1 + a) / 2
            torus = 1 - ((1-a) * (1-a**(w-1))) / (2 * (1+tail))
            self.assertGreater(torus - cylinder, Decimal('0.12'))

    def test_vacuum_multiplicity_blocks_small_defect(self):
        with localcontext() as ctx:
            ctx.prec = 60
            for multiplicity in (2, 3, 10):
                # Constant Z=m is the trace of an m-dimensional identity.
                delta = 15 * Decimal(multiplicity).ln()
                self.assertGreater(delta, Decimal(1) / 2048)


if __name__ == '__main__':
    unittest.main(verbosity=2)
