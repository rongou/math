import unittest
from fractions import Fraction as F

from fourth_moment import (
    Eisenstein, ONE, P7, P7BAR, P13, P5_INERT, ResidueRing,
    RootSum, finite_fourier, core_square_coefficient,
)
from coprime_reflection import (
    eisenstein_in_roots, gauss_by_crt, check_single_conversion,
    check_coprime_conversion, check_bilinear_theta_product, poisson_scale, theta_scale,
    scale_budget, model_orbit, report,
)


class CoprimeConversionTests(unittest.TestCase):
    def test_eisenstein_embedding(self):
        omega = eisenstein_in_roots(Eisenstein(0, 1), 42)
        self.assertEqual(omega * omega * omega, RootSum.integer(42, 1))
        self.assertEqual(eisenstein_in_roots(Eisenstein(2, 3), 42),
                         RootSum.from_terms(42, {0: 2, 14: 3}))

    def test_gauss_crt_against_direct_composite_sum(self):
        ring = ResidueRing((P7, P7BAR))
        for e in (1, -1, 2, 3):
            self.assertEqual(gauss_by_crt(ring, e), finite_fourier(ring, (e, e), ONE))

    def test_single_conversions(self):
        for ring in (ResidueRing((P7,)), ResidueRing((P5_INERT,)), ResidueRing((P7, P13))):
            self.assertTrue(check_single_conversion(ring))

    def test_coprime_kernel_conversions(self):
        result = report()
        self.assertTrue(result['all_conversion_checks_passed'])
        self.assertEqual(result['coprime_conversion_cases'], 7)
        self.assertEqual(result['single_conversion_cases'], 8)

    def test_bilinear_theta_product(self):
        for v, w in ((ResidueRing((P7,)), ResidueRing((P13,))),
                     (ResidueRing((P7, P7BAR)), ResidueRing((P13,)))):
            self.assertTrue(check_bilinear_theta_product(v, w))

    def test_coprime_restriction_cannot_be_dropped_by_positivity(self):
        columns = (frozenset(('p', 'r')), frozenset(('q', 's')), frozenset(('p', 'q')))
        coefficients = (1, 1, -2)
        restricted = sum(coefficients[i] * coefficients[j]
                         for i in range(3) for j in range(3)
                         if columns[i].isdisjoint(columns[j]))
        unrestricted = sum(coefficients) ** 2
        self.assertEqual(restricted, 2)
        self.assertEqual(unrestricted, 0)
        self.assertGreater(restricted, unrestricted)

    def test_diagonal_mass_is_not_a_lower_bound_for_energy(self):
        coefficients = (1, -1)
        self.assertEqual(sum(c * c for c in coefficients), 2)
        self.assertEqual(sum(coefficients) ** 2, 0)

    def test_overlapping_moduli_are_not_allowed(self):
        with self.assertRaises(ValueError):
            check_coprime_conversion(ResidueRing((P7,)), ResidueRing((P7,)))

    def test_divisor_weight_is_not_multiplicative(self):
        weights = {(0, 0): 0, (1, 0): 1, (0, 1): 1, (1, 1): 0}
        nu = (ONE, ONE)
        self.assertEqual(core_square_coefficient((1, 0), weights, nu), Eisenstein(0))
        self.assertEqual(core_square_coefficient((0, 1), weights, nu), Eisenstein(0))
        # With two core primes, the Mobius sign is +1, so this is V_D(pq).
        self.assertEqual(core_square_coefficient((1, 1), weights, nu), Eisenstein(2))


class ReflectionScaleTests(unittest.TestCase):
    def test_poisson_and_theta_are_length_involutions(self):
        for u in (F(1, 2), F(4, 3), F(8, 3), F(4)):
            for x in (F(1), F(2), F(10, 3)):
                self.assertEqual(poisson_scale(*poisson_scale(u, x)), (u, x))
                self.assertEqual(theta_scale(*theta_scale(u, x)), (u, x))

    def test_pilot_has_no_strict_gap(self):
        budget = scale_budget(F(4, 3))
        self.assertEqual(budget['poisson_row'], '8/3')
        self.assertEqual(budget['nominal_reflected_column'], '10/3')
        self.assertEqual(budget['formal_cube_cutoff'], '-4/9')
        self.assertFalse(budget['required_strict_gap_available'])

    def test_even_hypothetical_completed_bound_is_too_large(self):
        budget = scale_budget(F(4, 3))
        self.assertEqual(budget['hypothetical_completed_bound'], '14/3')
        self.assertEqual(budget['target_fourth'], '10/3')
        self.assertEqual(budget['hypothetical_bound_excess'], '4/3')
        self.assertEqual(budget['added_diagonal_excess_over_target'], '2/3')

    def test_frontier_h_equals_x(self):
        self.assertFalse(scale_budget(F(2))['required_strict_gap_available'])
        self.assertEqual(scale_budget(F(2))['hypothetical_bound_excess'], '0')
        self.assertTrue(scale_budget(F(5, 2))['required_strict_gap_available'])

    def test_model_cycle_expands_in_the_short_row_regime(self):
        orbit = model_orbit(3)
        self.assertEqual([(r['row'], r['column']) for r in orbit],
                         [('4/3', '2'), ('8/3', '10/3'), ('4', '14/3'), ('16/3', '6')])
        for u, x in ((F(4, 3), F(2)), (F(1), F(3)), (F(2), F(5, 2))):
            pu, px = theta_scale(*poisson_scale(u, x))
            self.assertEqual((pu - u, px - x), (2 * (x - u), 2 * (x - u)))


if __name__ == '__main__':
    unittest.main()
