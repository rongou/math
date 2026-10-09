#!/usr/bin/env python3
"""Exact algebra behind the RH research notes; no analytic theorem is proved.

Only standard-library Fraction arithmetic is used.  The moment inequalities
whose consequences we calculate are hypotheses, not outputs of this program.
The endpoint polynomial is from the September 30, 2026 manuscript, label
`eq:balanced-endpoint-certificate`.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from typing import TypeAlias

Polynomial: TypeAlias = dict[tuple[int, int], F]  # powers of (y, delta)


def extraction_terms(k: int, m: int, h: F) -> tuple[F, F]:
    """Exponents from a 2m-th moment and kth-power prime amplification.

Assume sum_{Nu<=D^h} |A_u(D)|^(2m) << D^(m+epsilon) D^h,
~D^(h/k) prime-power replica rows, and error O(D^(1-h/k)).
Returns (moment term, replica error), with epsilon/logarithms suppressed.
"""
    if not isinstance(k, int) or not isinstance(m, int) or k < 2 or m < 1:
        raise ValueError("k must be an integer >= 2 and m an integer >= 1")
    if not isinstance(h, (int, F)):
        raise TypeError("h must be exact (int or Fraction), not floating point")
    h = F(h)
    if h < 0:
        raise ValueError("h must be nonnegative")
    return F(1, 2) + F(k - 1, 2 * m * k) * h, 1 - h / k


def extraction_exponent(k: int, m: int, h: F) -> F:
    return max(extraction_terms(k, m, h))


def optimal_scale(k: int, m: int) -> tuple[F, F]:
    """Crossing of increasing/decreasing affine terms, assuming availability.

This does NOT assert a moment estimate at the returned scale.  h=0 is only
an algebraic boundary; the prime-count argument needs fixed h>0 as D grows.
"""
    extraction_terms(k, m, F(0))  # validate parameters
    h = F(m * k, 2 * m + k - 1)
    return h, F(m + k - 1, 2 * m + k - 1)


def effective_boundary(low_exponent: F, mellin_offset: F) -> F:
    """For C(s)=s+c, low exponent L can exclude only beta > L-c."""
    return F(low_exponent) - F(mellin_offset)


def coefficient_uniform_obstruction(k: int, m: int, h: F) -> F:
    """Exponent excess for positive coefficients on prime columns.

Power-replica rows contribute D^(2m+h/k), ignoring logarithms; the
hypothetical coefficient-uniform moment bound is D^(m+h).
A positive answer contradicts that bound.  In the notes h=3<k=6, so
prime columns of size D and replica primes of size D^(h/k) are disjoint.
"""
    extraction_terms(k, m, h)
    return F(m) - F(k - 1, k) * h


def constant(value: int | F) -> Polynomial:
    value = F(value)
    return {(0, 0): value} if value else {}


def add(*polys: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            answer[monomial] = answer.get(monomial, F(0)) + coefficient
    return {monomial: c for monomial, c in answer.items() if c}


def scale(poly: Polynomial, value: int | F) -> Polynomial:
    return {monomial: c * value for monomial, c in poly.items() if c * value}


def mul(*polys: Polynomial) -> Polynomial:
    answer = constant(1)
    for poly in polys:
        product: Polynomial = {}
        for (ay, ad), ac in answer.items():
            for (by, bd), bc in poly.items():
                index = (ay + by, ad + bd)
                product[index] = product.get(index, F(0)) + ac * bc
        answer = {monomial: c for monomial, c in product.items() if c}
    return answer


def endpoint_polynomials() -> tuple[Polynomial, Polynomial]:
    """Independently expand both sides of the manuscript's identity."""
    y: Polynomial = {(1, 0): F(1)}
    delta: Polynomial = {(0, 1): F(1)}
    v = add(constant(51), scale(y, 41))
    p = add(constant(7), scale(y, 18), scale(mul(y, y), 8))
    j = add(
        constant(185), scale(y, 170),
        mul(add(constant(-138), scale(y, 12), scale(mul(y, y), 96)), delta),
    )
    # 10368 * J * (-E), with J=j/108, from the rational expression for E.
    numerator = add(
        scale(mul(j, add(constant(1), mul(add(constant(3), scale(y, 8)), delta))), 2),
        scale(mul(add(constant(F(5, 6)), scale(delta, -1)), delta, p), -468),
    )
    left = mul(v, numerator)
    square_base = add(scale(mul(v, delta), 4), constant(-79))
    right = add(
        mul(add(constant(3), scale(y, 5)),
            add(mul(square_base, square_base), constant(49))),
        scale(mul(y, add(
            scale(mul(v, delta, add(
                mul(add(constant(1), scale(y, 3)),
                    add(constant(15), scale(y, 32)), delta),
                constant(9), scale(y, -13))), 4),
            constant(265), scale(y, 3485))), 4),
    )
    return left, right


def endpoint_value(delta: F, x: F) -> F:
    """-E_* in the idealized endpoint calculation (not the full high bound)."""
    delta, x = F(delta), F(x)
    if not (0 <= delta <= F(5, 6) and 0 <= x <= F(1, 2)):
        raise ValueError("endpoint parameters outside the manuscript's rectangle")
    y = F(1, 2) - x
    d_x = (37 + 34 * y) / 18
    p_x = (7 + 18 * y + 8 * y * y) / 9
    capital_j = (F(5, 6) - delta) * d_x + delta * p_x
    return ((1 + (3 + 8 * y) * delta) / 48
            - F(13, 32) * (F(5, 6) - delta) * delta * p_x / capital_j)


def report() -> dict:
    left, right = endpoint_polynomials()
    if left != right:
        raise ArithmeticError("endpoint polynomial identity failed")
    return {
        "status": "exact algebra only; moment hypotheses and Lean proofs not verified",
        "source_revision": "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb",
        "second_moment_sextic_extraction": {
            "paper_scale_h_limit": "1 (approached from above)",
            "paper_exponent_limit": str(extraction_exponent(6, 1, F(1))),
            "hypothetical_all_scale_optimum_h": str(optimal_scale(6, 1)[0]),
            "hypothetical_all_scale_optimum_exponent": str(optimal_scale(6, 1)[1]),
        },
        "hypothetical_optimized_moments": [
            {"m": m, "h": str(optimal_scale(6, m)[0]),
             "exponent": str(optimal_scale(6, m)[1])}
            for m in (1, 2, 3, 4, 10, 100)
        ],
        "hypothetical_moments_at_h_3": [
            {"m": m, "exponent": str(extraction_exponent(6, m, F(3)))}
            for m in (1, 2, 3, 4, 10, 100)
        ],
        "fixed_probe_low_side": {
            "low_exponent": "3/16", "mellin_offset": "-11/16",
            "effective_boundary": str(effective_boundary(F(3, 16), F(-11, 16))),
            "low_exponent_needed_at_half": str(F(1, 2) - F(11, 16)),
            "required_low_exponent_improvement": str(F(3, 16) - F(-3, 16)),
            "boundary_if_only_gram_penalty_removed": str(
                effective_boundary(F(17, 96), F(-11, 16))),
        },
        "endpoint_certificate": {
            "polynomial_identity": left == right,
            "nonzero_monomial_count": len(left),
            "lower_bound": str(F(49, 440640)),
            "larger_than_one_ten_thousandth": F(49, 440640) > F(1, 10000),
            "positivity_requires": "0<=delta<=5/6, 0<=y<=1/2, 0<J<=5/2",
        },
        "positive_coefficient_counterexample": {
            "k": 6, "h": "3", "m": 3,
            "lower_bound_exponent": str(2 * 3 + F(3, 6)),
            "claimed_uniform_upper_exponent": "6",
            "excess": str(coefficient_uniform_obstruction(6, 3, F(3))),
            "scope": "refutes coefficient-uniform bound, NOT the Mobius-specific hypothesis",
        },
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2))
