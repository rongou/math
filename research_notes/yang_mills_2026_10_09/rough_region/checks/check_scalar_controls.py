#!/usr/bin/env python3
"""Standard-library exact controls and one-link quaternion regression checks.

These checks do not prove the analytic replacement or probability theorems.
The central-staple case and the abstract two-cell counterexamples use exact
rational arithmetic; generic quaternion cases are deterministic diagnostics.
"""
from fractions import Fraction
from math import fsum, sqrt
import random
import unittest


def norm2(x):
    return fsum(a*a for a in x)


def dot(x, y):
    return fsum(a*b for a, b in zip(x, y))


def unit(rng):
    v = [rng.gauss(0, 1) for _ in range(4)]
    n = sqrt(norm2(v))
    return [x/n for x in v]


def boundary_values(staples):
    b = [fsum(s[i] for s in staples) for i in range(4)]
    magnitude = sqrt(norm2(b))
    discrepancy = fsum(norm2([a-b for a, b in zip(staples[i], staples[j])])
                       for i in range(6) for j in range(i+1, 6))
    return b, magnitude, discrepancy


class ScalarControls(unittest.TestCase):
    def test_central_balanced_staples_exact(self):
        signs = [1, 1, 1, -1, -1, -1]
        amplitude = abs(sum(signs))
        discrepancy = sum((signs[i]-signs[j])**2
                          for i in range(6) for j in range(i+1, 6))
        self.assertEqual(amplitude, 0)
        self.assertEqual(discrepancy, 36)
        self.assertEqual(Fraction(discrepancy, 6+amplitude), 6-amplitude)

    def test_arbitrary_staple_minimum_diagnostic(self):
        rng = random.Random(20261009)
        for _ in range(120):
            staples = [unit(rng) for _ in range(6)]
            b, mag, discrepancy = boundary_values(staples)
            self.assertAlmostEqual(discrepancy, 36-mag*mag, places=11)
            emin = 6-mag
            self.assertAlmostEqual(emin, discrepancy/(6+mag), places=11)
            self.assertLessEqual(discrepancy/12, emin+1e-12)
            self.assertLessEqual(emin, discrepancy/6+1e-12)
            optimum = [v/mag for v in b]
            self.assertAlmostEqual(sum(1-dot(optimum,s) for s in staples), emin, places=11)
            for _ in range(5):
                candidate = unit(rng)
                self.assertGreaterEqual(sum(1-dot(candidate,s) for s in staples), emin-1e-12)

    def test_positive_weight_integral_can_exceed_one(self):
        # Two cells with Haar masses b,1-b. E=0 on B, E=h on A,
        # e^(-Hh)=1/10; Q=10000 on B,1 on A. Reset uniformly to B.
        b, weight, q = Fraction(1,100), Fraction(1,10), 10000
        zq = b*q + (1-b)*weight
        iq = (1-b)*weight*q/zq
        bound = weight/b
        self.assertGreater(iq, 1)
        self.assertLessEqual(iq, bound)
        self.assertEqual(bound, 10)

    def test_density_cost_is_necessary(self):
        b, weight = Fraction(1,4), Fraction(1,10)
        event_probability = (1-b)*weight/(b+(1-b)*weight)
        self.assertEqual(event_probability, Fraction(3,13))
        self.assertGreater(event_probability, weight)
        self.assertLessEqual(event_probability, weight/b)

    def test_adaptive_support_requires_counting(self):
        # 100 independent bits, e^(-H)=1/100: Gibbs P(bit=1)=1/101.
        # Selecting first one cannot use a single fixed-coordinate M=2 bound.
        event_probability = 1-Fraction(100,101)**100
        invalid_bound = Fraction(2,100)
        self.assertGreater(event_probability, invalid_bound)

    def test_compatible_volume_absorption_exact(self):
        for c in (Fraction(1), Fraction(100), Fraction(1000,7)):
            for n in (1, 3, 16, 101):
                for s in (Fraction(1), Fraction(3), Fraction(15,2)):
                    p2 = 4*s*c
                    k = (n*s.denominator + s.numerator-1)//s.numerator
                    exponent = -k*p2/2+n*c
                    self.assertLessEqual(exponent, -n*p2/(4*s))


if __name__ == '__main__':
    unittest.main(verbosity=2)
