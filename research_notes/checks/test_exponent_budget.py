"""Algebraic regression checks; no test establishes the missing moment bounds."""

import unittest
from fractions import Fraction as F

from exponent_budget import (
    coefficient_uniform_obstruction, effective_boundary, endpoint_polynomials,
    endpoint_value, extraction_exponent, extraction_terms, optimal_scale, report,
)


class ExponentBudgetTests(unittest.TestCase):
    def test_companion_extraction(self):
        theta = F(1, 10)
        first, second = extraction_terms(6, 1, 1 + theta)
        self.assertEqual(first, F(11, 12) + F(5, 12) * theta)
        self.assertEqual(second, F(5, 6) - theta / 6)
        self.assertEqual(extraction_exponent(6, 1, F(1)), F(11, 12))

    def test_crossing_formula(self):
        for k in (2, 3, 6, 10):
            for m in (1, 2, 3, 10, 100):
                h, expected = optimal_scale(k, m)
                first, second = extraction_terms(k, m, h)
                self.assertEqual(first, second)
                self.assertEqual(first, expected)
                for shift in (F(-1, 10), F(-1, 100), F(1, 100), F(1, 10)):
                    self.assertGreaterEqual(extraction_exponent(k, m, h + shift), expected)

    def test_optimized_sextic_values(self):
        self.assertEqual(optimal_scale(6, 1), (F(6, 7), F(6, 7)))
        self.assertEqual(optimal_scale(6, 2), (F(4, 3), F(7, 9)))
        self.assertEqual(optimal_scale(6, 100), (F(120, 41), F(21, 41)))

    def test_fixed_scale_all_moments_consequence(self):
        for m in (1, 2, 3, 4, 10, 100, 1000):
            self.assertEqual(extraction_terms(6, m, F(3)), (F(1, 2) + F(5, 4 * m), F(1, 2)))

    def test_normalization_does_not_change_boundary(self):
        low, offset = F(3, 16), F(-11, 16)
        for shift in (F(-5), F(-1, 2), F(0), F(4, 7), F(10)):
            self.assertEqual(effective_boundary(low + shift, offset + shift), F(7, 8))
        self.assertEqual(effective_boundary(F(17, 96), offset), F(83, 96))

    def test_endpoint_polynomial_identity(self):
        left, right = endpoint_polynomials()
        self.assertEqual(left, right)  # coefficient identity, not sampled equality
        self.assertTrue(left)

    def test_endpoint_rational_spot_checks(self):
        # Diagnostic evaluations supplement, but do not replace, the identity.
        for d_num in range(31):
            for x_num in range(21):
                self.assertGreaterEqual(
                    endpoint_value(F(5, 6) * F(d_num, 30), F(x_num, 40)),
                    F(49, 440640),
                )

    def test_certificate_bound_arithmetic(self):
        self.assertEqual(F(49, 176256) / F(5, 2), F(49, 440640))
        self.assertGreater(F(49, 440640), F(1, 10000))
        self.assertEqual(1 - F(13, 16) / 4, F(51, 64))

    def test_coefficient_uniform_obstruction(self):
        self.assertEqual(coefficient_uniform_obstruction(6, 3, F(3)), F(1, 2))
        self.assertGreater(coefficient_uniform_obstruction(6, 4, F(3)), 0)
        self.assertLess(coefficient_uniform_obstruction(6, 2, F(3)), 0)

    def test_invalid_parameters(self):
        for k, m, h in ((1, 1, F(1)), (6, 0, F(1)), (6, 1, F(-1))):
            with self.assertRaises(ValueError):
                extraction_terms(k, m, h)
        with self.assertRaises(TypeError):
            extraction_terms(6, 1, 1.0)
        with self.assertRaises(ValueError):
            endpoint_value(F(1), F(0))

    def test_report_keeps_hypotheses_explicit(self):
        output = report()
        self.assertIn("not verified", output["status"])
        self.assertTrue(output["endpoint_certificate"]["polynomial_identity"])


if __name__ == "__main__":
    unittest.main()
