"""Exact tests for finite arithmetic, not tests of P4 at increasing scales."""

import itertools
import unittest
from collections import Counter
from fractions import Fraction as F

from fourth_moment import (
    Eisenstein, ONE, ZERO, SIXTH_ROOTS, ZETA6, P7, P7BAR, P13, P19, P5_INERT,
    PrimeField, ResidueRing, RootSum, complete_fourth_moment, convolution,
    core_square_coefficient, cyclotomic, finite_fourier, incidence, product,
    completion_fourth_exponent, exponent_report,
    unit_charge, verify_finite_identities,
)


class EisensteinTests(unittest.TestCase):
    def test_norm_and_conjugation(self):
        for a, b, c, d in itertools.product(range(-2, 3), repeat=4):
            x, y = Eisenstein(a, b), Eisenstein(c, d)
            self.assertEqual((x * y).norm(), x.norm() * y.norm())
            self.assertEqual(x * x.conjugate(), Eisenstein(x.norm()))

    def test_exact_division(self):
        self.assertEqual((P7.generator * P13.generator).exact_div(P7.generator), P13.generator)
        with self.assertRaises(ValueError):
            ONE.exact_div(P7.generator)
        with self.assertRaises(ZeroDivisionError):
            ONE.exact_div(ZERO)

    def test_sixth_roots(self):
        self.assertEqual(ZETA6 ** 6, ONE)
        self.assertEqual(len(set(SIXTH_ROOTS)), 6)
        self.assertTrue(all(root.norm() == 1 for root in SIXTH_ROOTS))

    def test_fields_and_character_multiplicativity(self):
        for p in (P7, P7BAR, P13, P19, P5_INERT):
            counts = Counter(p.character_table.values())
            self.assertEqual(counts[None], 1)
            self.assertTrue(all(counts[j] == (p.q - 1) // 6 for j in range(6)))
            for x in p.residues:
                if x != ZERO:
                    self.assertEqual(p.reduce(x * p.inverse(x)), ONE)
                    for y in p.residues:
                        if y != ZERO:
                            self.assertEqual(p.character_log(x * y),
                                             (p.character_log(x) + p.character_log(y)) % 6)

    def test_crt_including_conjugate_split_primes(self):
        for ring in (ResidueRing((P7, P7BAR)), ResidueRing((P7, P13, P5_INERT))):
            self.assertEqual(len(ring.residues), ring.norm)
            self.assertEqual(len({tuple(p.reduce(x) for p in ring.primes) for x in ring.residues}), ring.norm)
            for i, e in enumerate(ring.idempotents):
                self.assertEqual([p.reduce(e) for p in ring.primes],
                                 [ONE if i == j else ZERO for j in range(len(ring.primes))])

    def test_invalid_moduli_and_field_exponent(self):
        with self.assertRaises(ValueError):
            PrimeField(Eisenstein(2))
        with self.assertRaises(ValueError):
            ResidueRing((P7, P7))
        with self.assertRaises(ValueError):
            P7.power(ONE, -1)


class CyclotomicTests(unittest.TestCase):
    def test_known_polynomials(self):
        self.assertEqual(cyclotomic(1), (-1, 1))
        self.assertEqual(cyclotomic(6), (1, -1, 1))
        self.assertEqual(cyclotomic(7), (1,) * 7)
        self.assertEqual(cyclotomic(25), (1, 0, 0, 0, 0) * 4 + (1,))

    def test_roots_unity_sum(self):
        for order in (6, 42, 78, 150, 294, 546):
            self.assertEqual(RootSum.from_terms(order, {i: 1 for i in range(order)}),
                             RootSum.integer(order, 0))

    def test_embedding_conjugation_and_product(self):
        z = RootSum.from_terms(6, {1: 1})
        self.assertEqual(z * z.conjugate(), RootSum.integer(6, 1))
        self.assertEqual(z.embed(42), RootSum.from_terms(42, {7: 1}))
        self.assertEqual((z * z).embed(42), z.embed(42) * z.embed(42))
        self.assertNotEqual(z, z.conjugate())


class FourthMomentTests(unittest.TestCase):
    def test_all_incidence_patterns_and_masks(self):
        patterns = [incidence(mask) for mask in range(1, 16)]
        self.assertEqual(Counter(p['channel'] for p in patterns),
                         {'mask': 5, 'sextic': 8, 'cubic': 2})
        for pattern in patterns:
            self.assertEqual(pattern['mobius_sign'], (-1) ** pattern['exponent'])
        # Cancellation of exponents does not remove the zero extension.
        ring = ResidueRing((P7,))
        self.assertIsNone(ring.value_log((0,), ZERO))
        self.assertEqual(ring.value_log((0,), ZERO, keep_balanced_masks=False), 0)

    def test_all_local_and_crt_fourier_identities(self):
        report = verify_finite_identities()
        self.assertEqual(report['local_fourier_equalities'], 355)
        self.assertEqual(report['crt_fourier_equalities'], 721)
        self.assertEqual(report['complete_fourth_moment']['direct'],
                         report['complete_fourth_moment']['grouped_diagonal'])

    def test_global_gauss_sum_keeps_crt_phases(self):
        for ring in (ResidueRing((P7, P13)), ResidueRing((P7, P7BAR)),
                     ResidueRing((P7, P5_INERT))):
            order = 6 * ring.norm
            for exponents in itertools.product((-2, -1, 1, 2), repeat=2):
                predicted = RootSum.integer(order, 1)
                for p, e in zip(ring.primes, exponents):
                    local = finite_fourier(ResidueRing((p,)), (e,), ONE).embed(order)
                    cofactor = ring.generator.exact_div(p.generator)
                    j = p.character_log(cofactor)
                    self.assertIsNotNone(j)
                    predicted = predicted * local.shift(ring.norm * e * j)
                self.assertEqual(predicted, finite_fourier(ring, exponents, ONE))

    def test_elementary_exponent_budget(self):
        self.assertEqual(completion_fourth_exponent(F(4, 3)), F(5))
        self.assertEqual(completion_fourth_exponent(F(3)), F(6))
        result = exponent_report()
        self.assertEqual(result['gap_to_P4'], '5/3')
        self.assertEqual(result['replica_extraction_from_elementary_bound'], '43/36')
        self.assertEqual(result['positive_coefficient_excess_over_P4'], '8/9')

    def test_gauss_norms(self):
        for p in (P7, P7BAR, P13, P19, P5_INERT):
            ring = ResidueRing((p,))
            for e in (-2, -1, 1, 2):
                tau = finite_fourier(ring, (e,), ONE)
                self.assertEqual(tau * tau.conjugate(), RootSum.integer(6 * p.q, p.q))

    def test_cubic_gauss_normalization_in_companion(self):
        # gamma_2(pi)^3 = -pi/sqrt(Npi), equivalently tau_2^3=-pi*Npi.
        for p in (P7, P7BAR, P13, P19, P5_INERT):
            order, pi = 6 * p.q, p.generator
            tau = finite_fourier(ResidueRing((p,)), (2,), ONE)
            expected = RootSum.from_terms(order, {0: -pi.a * p.q, order // 3: -pi.b * p.q})
            self.assertEqual(tau * tau * tau, expected)

    def test_unit_character_and_norm_congruence(self):
        ring = ResidueRing((P7, P13, P5_INERT))
        for v in itertools.product(range(3), repeat=3):
            for w in itertools.product(range(3), repeat=3):
                exponents = tuple(a - b for a, b in zip(v, w))
                charge = unit_charge(ring, exponents)
                self.assertEqual(charge, ring.value_log(exponents, ZETA6))
                nv = product(p.generator ** a for p, a in zip(ring.primes, v)).norm()
                nw = product(p.generator ** b for p, b in zip(ring.primes, w)).norm()
                self.assertEqual(charge == 0, (nv - nw) % 36 == 0)

    def test_core_square_convolution(self):
        nu = (SIXTH_ROOTS[1], SIXTH_ROOTS[2], SIXTH_ROOTS[4])
        weights = {bits: i + 1 for i, bits in enumerate(itertools.product((0, 1), repeat=3))}
        coefficients = {bits: Eisenstein((-1) ** sum(bits) * weight)
                        * product(z ** v for z, v in zip(nu, bits)) for bits, weight in weights.items()}
        expanded = convolution(coefficients)
        for v in itertools.product(range(3), repeat=3):
            self.assertEqual(expanded[v], core_square_coefficient(v, weights, nu))

    def test_unit_ideal_and_zero_row(self):
        ring = ResidueRing((P7,))
        direct, diagonal = complete_fourth_moment(ring, {(0,): Eisenstein(2)})
        self.assertEqual(direct, P7.q * 16)
        self.assertEqual(direct, diagonal)
        self.assertEqual(ResidueRing(()).value_log((), ZERO), 0)
        self.assertEqual(finite_fourier(ResidueRing(()), (), ZERO), RootSum.integer(6, 1))


if __name__ == '__main__':
    unittest.main()
