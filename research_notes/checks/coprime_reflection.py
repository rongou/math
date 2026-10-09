#!/usr/bin/env python3
"""Exact coprime Gauss conversion and conditional reflection scale arithmetic.

No theta-reflection theorem for divisor weights is assumed or proved by this
program. The scale model is explicitly hypothetical, not a bound for P4.
"""
from __future__ import annotations

import json
from fractions import Fraction as F
from functools import lru_cache

from fourth_moment import (
    Eisenstein, ONE, P7, P7BAR, P13, P19, P5_INERT, ResidueRing, RootSum,
    finite_fourier,
)


def eisenstein_in_roots(x: Eisenstein, order: int) -> RootSum:
    if order % 3:
        raise ValueError('omega requires an order divisible by 3')
    return RootSum.from_terms(order, {0: x.a, order // 3: x.b})


@lru_cache(maxsize=None)
def gauss_by_crt(ring: ResidueRing, exponent: int) -> RootSum:
    """Unnormalized Gauss sum of chi_ring^exponent, with every CRT phase."""
    order = 6 * ring.norm
    result = RootSum.integer(order, 1)
    for p in ring.primes:
        cofactor = ring.generator.exact_div(p.generator)
        j = p.character_log(cofactor)
        if j is None:
            raise ArithmeticError('noncoprime CRT moduli')
        tau = finite_fourier(ResidueRing((p,)), (exponent,), ONE).embed(order)
        result = result * tau.shift(ring.norm * exponent * j)
    return result


def character_log(ring: ResidueRing, x: Eisenstein) -> int:
    result = ring.value_log((1,) * len(ring.primes), x)
    if result is None:
        raise ValueError('character zero cannot be used as a phase')
    return result


def check_single_conversion(ring: ResidueRing) -> bool:
    """Check two square-root-free forms of the manuscript's Gauss identities."""
    q, n = ring.norm, ring.generator
    order, mu = 6 * q, (-1) ** len(ring.primes)
    t1, tm1, t2, t3 = (gauss_by_crt(ring, j) for j in (1, -1, 2, 3))
    log4, logminus1 = character_log(ring, Eisenstein(4)), character_log(ring, Eisenstein(-1))
    # mu*q*tau_1 = conjugate(chi(4))*n*tau_3*conjugate(tau_2).
    first_left = t1.scale(mu * q)
    first_right = (eisenstein_in_roots(n, order) * t3 * t2.conjugate()).shift(-q * log4)
    # mu*tau_-1*tau_3 = chi(-1)*chi(4)*conjugate(n)*tau_2.
    second_left = (tm1 * t3).scale(mu)
    second_right = (eisenstein_in_roots(n.conjugate(), order) * t2).shift(q * (logminus1 + log4))
    return first_left == first_right and second_left == second_right


def check_coprime_conversion(v: ResidueRing, w: ResidueRing) -> bool:
    """Direct mixed Fourier sum versus the converted cubic coefficient product.

The normalized identity in coprime_reflection.md is cleared of square roots:
mu(v)mu(w) Nv tau_mixed tau_3(w)
 = R(v,w) chi_w(-1) conjugate(chi_v(4)) chi_w(4)
   * v conjugate(w) tau_3(v) conjugate(tau_2(v)) tau_2(w).
"""
    union = ResidueRing(v.primes + w.primes)
    order, norm = 6 * union.norm, union.norm
    mu_product = (-1) ** (len(v.primes) + len(w.primes))
    mixed = finite_fourier(union, (1,) * len(v.primes) + (-1,) * len(w.primes), ONE)
    t3w = gauss_by_crt(w, 3).embed(order)
    left = (mixed * t3w).scale(mu_product * v.norm)
    reciprocity_log = (character_log(v, w.generator) - character_log(w, v.generator)) % 6
    if reciprocity_log not in (0, 3):
        raise ArithmeticError('reciprocity factor is not a sign')
    phase_log = (reciprocity_log + character_log(w, Eisenstein(-1))
                 - character_log(v, Eisenstein(4)) + character_log(w, Eisenstein(4)))
    right = (eisenstein_in_roots(v.generator * w.generator.conjugate(), order)
             * gauss_by_crt(v, 3).embed(order)
             * gauss_by_crt(v, 2).embed(order).conjugate()
             * gauss_by_crt(w, 2).embed(order)).shift(norm * phase_log)
    return left == right


def check_bilinear_theta_product(v: ResidueRing, w: ResidueRing) -> bool:
    """Check a(v*w)=a(v)*a(w)*chi_w(v)^4 for coprime squarefree ideals.

The alpha and norm factors are multiplicative, so it suffices to check the
corresponding unnormalized cubic Gauss identity.
"""
    union = ResidueRing(v.primes + w.primes)
    order = 6 * union.norm
    left = finite_fourier(union, (2,) * len(union.primes), ONE)
    right = (gauss_by_crt(v, 2).embed(order) * gauss_by_crt(w, 2).embed(order))
    right = right.shift(union.norm * 4 * character_log(w, v.generator))
    return left == right


def poisson_scale(row: F, column: F) -> tuple[F, F]:
    """Log_D scales for fixed-column row duality: U -> X^2/U."""
    return 2 * column - row, column


def theta_scale(row: F, column: F) -> tuple[F, F]:
    """Nominal generic-conductor theta scale: X -> U^2/X.

This is NOT permission to apply theta reflection to a new coefficient class.
"""
    return row, 2 * row - column


def scale_budget(h: F, x: F = F(2)) -> dict:
    if not isinstance(h, (int, F)) or not isinstance(x, (int, F)):
        raise TypeError('use exact rational exponents')
    h, x = F(h), F(x)
    if x <= 0 or h < 0 or h > 2 * x:
        raise ValueError('this scale budget requires X>1 and H, X^2/H >= 1')
    u = 2 * x - h
    reflected_column = 2 * u - x
    conditional_fourth = max(h + u, h + 2 * u - x)
    return {
        'original_row': str(h), 'product_column': str(x),
        'poisson_row': str(u), 'poisson_row_over_column': str(u - x),
        'nominal_reflected_column': str(reflected_column),
        'formal_cube_cutoff': str(min(x / 3, F(2, 3) * (x - u))),
        'required_strict_gap_available': u < x,
        'target_fourth': str(h + x),
        'hypothetical_completed_bound': str(conditional_fourth),
        'hypothetical_bound_excess': str(conditional_fourth - (h + x)),
        'added_diagonal_mass': str(2 * x),
        'added_diagonal_excess_over_target': str(x - h),
        'same_column_two_poisson_steps': [str(s) for s in poisson_scale(*poisson_scale(h, x))],
        'WARNING': 'completed bound transfer and weighted reflection are NOT established',
    }


def model_orbit(steps: int, row: F = F(4, 3), column: F = F(2)) -> list[dict]:
    """Toy length orbit only; coefficient-family closure is not asserted."""
    if steps < 0:
        raise ValueError('steps must be nonnegative')
    values = [{'cycle': 0, 'row': str(row), 'column': str(column)}]
    for i in range(1, steps + 1):
        row, column = theta_scale(*poisson_scale(row, column))
        values.append({'cycle': i, 'row': str(row), 'column': str(column)})
    return values


def report() -> dict:
    singles = [ResidueRing((p,)) for p in (P7, P7BAR, P13, P19, P5_INERT)]
    singles += [ResidueRing(()), ResidueRing((P7, P7BAR)), ResidueRing((P7, P13))]
    cases = [
        (ResidueRing((P7,)), ResidueRing((P13,))),
        (ResidueRing((P13,)), ResidueRing((P7,))),
        (ResidueRing((P7,)), ResidueRing((P7BAR,))),
        (ResidueRing((P19,)), ResidueRing((P7,))),
        (ResidueRing((P5_INERT,)), ResidueRing((P7,))),
        (ResidueRing((P7, P7BAR)), ResidueRing((P13,))),
        (ResidueRing(()), ResidueRing((P7,))),
    ]
    single_results = [check_single_conversion(ring) for ring in singles]
    pair_results = [check_coprime_conversion(v, w) for v, w in cases]
    product_results = [check_bilinear_theta_product(v, w) for v, w in cases]
    if not all(single_results + pair_results + product_results):
        raise ArithmeticError('a coprime Gauss conversion failed')
    return {
        'status': 'exact finite identities and a conditional scale obstruction; P4 and RH NOT proved',
        'source_revision': 'fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb',
        'single_conversion_cases': len(single_results),
        'single_identities_per_case': 2,
        'coprime_conversion_cases': len(pair_results),
        'bilinear_theta_product_cases': len(product_results),
        'all_conversion_checks_passed': True,
        'pilot_scale_budget': scale_budget(F(4, 3)),
        'toy_poisson_then_theta_orbit': model_orbit(3),
        'divisor_weight_nonmultiplicativity': {
            'example': 'unit weight 0; positive weights 1 on two distinct prime columns',
            'weight_on_first_prime_product_column': 0,
            'weight_on_second_prime_product_column': 0,
            'weight_on_their_product_column': 2,
        },
    }


if __name__ == '__main__':
    print(json.dumps(report(), indent=2))
