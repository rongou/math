#!/usr/bin/env python3
"""Exact finite arithmetic for the fourth-moment derivation.

Eisenstein integers, selected split/inert residue fields, CRT, and cyclotomic
arithmetic.  No floating point is used in the algebraic checks.  This does not
establish the infinite-scale fourth-moment bound P4 or the Riemann Hypothesis.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from dataclasses import dataclass
from functools import cached_property, lru_cache
from fractions import Fraction as F


@dataclass(frozen=True)
class Eisenstein:
    """a + b*omega, where omega^2 + omega + 1 = 0."""
    a: int = 0
    b: int = 0

    def __add__(self, other: Eisenstein) -> Eisenstein:
        return Eisenstein(self.a + other.a, self.b + other.b)

    def __neg__(self) -> Eisenstein:
        return Eisenstein(-self.a, -self.b)

    def __sub__(self, other: Eisenstein) -> Eisenstein:
        return self + (-other)

    def __mul__(self, other: Eisenstein) -> Eisenstein:
        return Eisenstein(self.a * other.a - self.b * other.b,
                          self.a * other.b + self.b * other.a - self.b * other.b)

    def __pow__(self, exponent: int) -> Eisenstein:
        if exponent < 0:
            raise ValueError('negative integral exponent')
        result, base = ONE, self
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent //= 2
        return result

    def conjugate(self) -> Eisenstein:
        return Eisenstein(self.a - self.b, -self.b)

    def norm(self) -> int:
        return self.a * self.a - self.a * self.b + self.b * self.b

    def exact_div(self, denominator: Eisenstein) -> Eisenstein:
        norm = denominator.norm()
        if not norm:
            raise ZeroDivisionError
        numerator = self * denominator.conjugate()
        if numerator.a % norm or numerator.b % norm:
            raise ValueError('not an exact Eisenstein division')
        return Eisenstein(numerator.a // norm, numerator.b // norm)

    def to_complex(self) -> complex:
        """For optional floating-point diagnostics only."""
        return complex(self.a - self.b / 2, self.b * math.sqrt(3) / 2)


ZERO, ONE = Eisenstein(), Eisenstein(1)
ZETA6 = Eisenstein(1, 1)
SIXTH_ROOTS = tuple(ZETA6 ** j for j in range(6))


def product(values):
    result = ONE
    for value in values:
        result = result * value
    return result


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


@dataclass(frozen=True)
class PrimeField:
    """O/(pi) for a prime-norm pi, or a primary inert integer -p.

This small test implementation deliberately supports only these checked forms.
The actual primary generator is kept for the additive character e(x/pi).
"""
    generator: Eisenstein

    def __post_init__(self):
        g, q = self.generator, self.generator.norm()
        if g.a % 3 != 1 or g.b % 3 != 0 or math.gcd(q, 6) != 1:
            raise ValueError('need a primary generator away from 2 and 3')
        r = math.isqrt(q)
        split = is_prime(q) and g.b % q != 0
        inert = r * r == q and is_prime(r) and r % 3 == 2 and g.b == 0
        if not (split or inert):
            raise ValueError('unsupported or nonprime test modulus')

    @property
    def q(self) -> int:
        return self.generator.norm()

    @property
    def split(self) -> bool:
        return is_prime(self.q)

    @cached_property
    def residues(self) -> tuple[Eisenstein, ...]:
        if self.split:
            return tuple(Eisenstein(a) for a in range(self.q))
        p = math.isqrt(self.q)
        return tuple(Eisenstein(a, b) for a in range(p) for b in range(p))

    def reduce(self, x: Eisenstein) -> Eisenstein:
        if self.split:
            omega = -self.generator.a * pow(self.generator.b, -1, self.q) % self.q
            return Eisenstein((x.a + omega * x.b) % self.q)
        p = math.isqrt(self.q)
        return Eisenstein(x.a % p, x.b % p)

    def power(self, x: Eisenstein, exponent: int) -> Eisenstein:
        if exponent < 0:
            raise ValueError('nonnegative field exponent required')
        result, base = ONE, self.reduce(x)
        while exponent:
            if exponent & 1:
                result = self.reduce(result * base)
            base = self.reduce(base * base)
            exponent //= 2
        return result

    def inverse(self, x: Eisenstein) -> Eisenstein:
        if self.reduce(x) == ZERO:
            raise ZeroDivisionError('nonunit in residue field')
        return self.power(x, self.q - 2)

    @cached_property
    def character_table(self) -> dict[Eisenstein, int | None]:
        roots = {self.reduce(root): j for j, root in enumerate(SIXTH_ROOTS)}
        if len(roots) != 6:
            raise ArithmeticError('sixth roots collapsed')
        return {x: (None if x == ZERO else roots[self.power(x, (self.q - 1) // 6)])
                for x in self.residues}

    def character_log(self, x: Eisenstein) -> int | None:
        """j for (x/pi)_6=zeta6^j; None means the zero extension."""
        return self.character_table[self.reduce(x)]


P7 = PrimeField(Eisenstein(-2, -3))
P7BAR = PrimeField(Eisenstein(1, 3))
P13 = PrimeField(Eisenstein(4, 3))
P19 = PrimeField(Eisenstein(-2, 3))
P5_INERT = PrimeField(Eisenstein(-5))


@dataclass(frozen=True)
class ResidueRing:
    primes: tuple[PrimeField, ...]

    def __post_init__(self):
        for p, q in itertools.combinations(self.primes, 2):
            if p.reduce(q.generator) == ZERO:
                raise ValueError('CRT primes must be distinct ideals')

    @cached_property
    def generator(self) -> Eisenstein:
        return product(p.generator for p in self.primes)

    @property
    def norm(self) -> int:
        return self.generator.norm()

    @cached_property
    def idempotents(self) -> tuple[Eisenstein, ...]:
        result = []
        for p in self.primes:
            cofactor = self.generator.exact_div(p.generator)
            result.append(cofactor * p.inverse(cofactor))
        return tuple(result)

    @cached_property
    def residues(self) -> tuple[Eisenstein, ...]:
        return tuple(sum((e * x for e, x in zip(self.idempotents, local)), ZERO)
                     for local in itertools.product(*(p.residues for p in self.primes)))

    def value_log(self, exponents: tuple[int, ...], x: Eisenstein,
                  keep_balanced_masks: bool = True) -> int | None:
        if len(exponents) != len(self.primes):
            raise ValueError('one exponent per prime is required')
        result = 0
        for p, exponent in zip(self.primes, exponents):
            if not keep_balanced_masks and exponent % 6 == 0:
                continue
            j = p.character_log(x)
            if j is None:
                return None
            result += exponent * j
        return result % 6


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def divide_monic_exact(numerator: list[int], denominator: tuple[int, ...]) -> list[int]:
    if denominator[-1] != 1:
        raise ValueError('denominator must be monic')
    remainder = numerator.copy()
    d = len(denominator) - 1
    quotient = [0] * (len(remainder) - d)
    for i in range(len(remainder) - 1, d - 1, -1):
        coefficient = remainder[i]
        quotient[i - d] = coefficient
        if coefficient:
            for j, term in enumerate(denominator):
                remainder[i - d + j] -= coefficient * term
    if any(remainder):
        raise ArithmeticError('polynomial division was not exact')
    return trim(quotient)


@lru_cache(maxsize=None)
def cyclotomic(n: int) -> tuple[int, ...]:
    if n < 1:
        raise ValueError('positive cyclotomic order required')
    poly = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            poly = divide_monic_exact(poly, cyclotomic(d))
    return tuple(poly)


@dataclass(frozen=True)
class RootSum:
    """Canonical element of Z[zeta_order], using the cyclotomic polynomial."""
    order: int
    coefficients: tuple[int, ...]

    @classmethod
    def from_terms(cls, order: int, terms: dict[int, int]) -> RootSum:
        phi = cyclotomic(order)
        degree = len(phi) - 1
        coefficients = [0] * order
        for exponent, coefficient in terms.items():
            coefficients[exponent % order] += coefficient
        nonzero_phi = [(j, a) for j, a in enumerate(phi) if a]
        for i in range(order - 1, degree - 1, -1):
            coefficient = coefficients[i]
            if coefficient:
                for j, a in nonzero_phi:
                    coefficients[i - degree + j] -= coefficient * a
        return cls(order, tuple(coefficients[:degree]))

    @classmethod
    def integer(cls, order: int, value: int) -> RootSum:
        return cls.from_terms(order, {0: value})

    def scale(self, scalar: int) -> RootSum:
        return RootSum(self.order, tuple(scalar * c for c in self.coefficients))

    def shift(self, exponent: int) -> RootSum:
        return RootSum.from_terms(self.order,
                                  {i + exponent: c for i, c in enumerate(self.coefficients) if c})

    def embed(self, order: int) -> RootSum:
        if order % self.order:
            raise ValueError('target order must be a multiple')
        return RootSum.from_terms(order, {i * (order // self.order): c
                                         for i, c in enumerate(self.coefficients) if c})

    def conjugate(self) -> RootSum:
        return RootSum.from_terms(self.order, {-i: c for i, c in enumerate(self.coefficients) if c})

    def __mul__(self, other: RootSum) -> RootSum:
        if self.order != other.order:
            raise ValueError('embed in a common cyclotomic ring first')
        terms = Counter()
        for i, a in enumerate(self.coefficients):
            if a:
                for j, b in enumerate(other.coefficients):
                    if b:
                        terms[i + j] += a * b
        return RootSum.from_terms(self.order, terms)

    def to_complex(self) -> complex:
        """Approximate evaluation used only by optional numerical diagnostics."""
        import cmath
        return sum(c * cmath.exp(2j * math.pi * i / self.order)
                   for i, c in enumerate(self.coefficients))


@lru_cache(maxsize=None)
def finite_fourier(ring: ResidueRing, exponents: tuple[int, ...], k: Eisenstein) -> RootSum:
    """sum_{x mod Q} F(x) e(k*x/Q), retaining every zero mask."""
    order, terms = 6 * ring.norm, Counter()
    conjugate_q = ring.generator.conjugate()
    for x in ring.residues:
        j = ring.value_log(exponents, x)
        if j is not None:
            # e(z)=exp(2*pi*i * coefficient_of_omega(z)).
            additive_numerator = (k * x * conjugate_q).b
            terms[(6 * additive_numerator + ring.norm * j) % order] += 1
    return RootSum.from_terms(order, terms)


def ramanujan(primes: tuple[PrimeField, ...], k: Eisenstein) -> int:
    result = 1
    for p in primes:
        result *= p.q - 1 if p.reduce(k) == ZERO else -1
    return result


def primitive_mask_fourier(ring: ResidueRing, exponents: tuple[int, ...],
                           k: Eisenstein) -> RootSum:
    """Predicted CRT formula: chi(b)*tau_c(chi)*conj(chi(k))*r_b(k)."""
    if len(exponents) != len(ring.primes):
        raise ValueError('one exponent per prime is required')
    active = [(p, e) for p, e in zip(ring.primes, exponents) if e % 6]
    balanced = tuple(p for p, e in zip(ring.primes, exponents) if e % 6 == 0)
    c_ring = ResidueRing(tuple(p for p, _ in active))
    c_exponents = tuple(e for _, e in active)
    k_log = c_ring.value_log(c_exponents, k)
    if k_log is None:
        return RootSum.integer(6 * ring.norm, 0)
    b = product(p.generator for p in balanced)
    b_log = c_ring.value_log(c_exponents, b)
    if b_log is None:
        raise ArithmeticError('conductor and mask are not coprime')
    tau = finite_fourier(c_ring, c_exponents, ONE).embed(6 * ring.norm)
    return tau.shift(ring.norm * (b_log - k_log)).scale(ramanujan(balanced, k))


def unit_charge(ring: ResidueRing, exponents: tuple[int, ...]) -> int:
    """chi(zeta6)=zeta6^charge; radial row sums vanish unless charge is zero."""
    if len(exponents) != len(ring.primes):
        raise ValueError('one exponent per prime is required')
    return sum(e * ((p.q - 1) // 6) for p, e in zip(ring.primes, exponents)) % 6


def incidence(mask: int) -> dict:
    if not 1 <= mask <= 15:
        raise ValueError('a nonempty subset of four columns is required')
    plus = sum((mask >> i) & 1 for i in (0, 1))
    minus = sum((mask >> i) & 1 for i in (2, 3))
    exponent = plus - minus
    return {
        'columns': [i + 1 for i in range(4) if (mask >> i) & 1],
        'multiplicity': plus + minus,
        'exponent': exponent,
        'mobius_sign': (-1) ** (plus + minus),
        'channel': 'mask' if not exponent else ('cubic' if abs(exponent) == 2 else 'sextic'),
    }


def convolution(coefficients: dict[tuple[int, ...], Eisenstein]) -> dict[tuple[int, ...], Eisenstein]:
    answer = {}
    for left, a in coefficients.items():
        for right, b in coefficients.items():
            key = tuple(x + y for x, y in zip(left, right))
            answer[key] = answer.get(key, ZERO) + a * b
    return answer


def complete_fourth_moment(ring: ResidueRing,
                           coefficients: dict[tuple[int, ...], Eisenstein]) -> tuple[int, int]:
    """Direct moment and grouped diagonal over a complete finite residue ring.

Not an asymptotic estimate or a short-row numerical test of P4.
"""
    direct = 0
    for u in ring.residues:
        total = ZERO
        for column, coefficient in coefficients.items():
            # A missing column prime must not introduce a zero mask.
            j = ring.value_log(column, u, keep_balanced_masks=False)
            if j is not None:
                total = total + coefficient * SIXTH_ROOTS[j]
        direct += total.norm() ** 2
    diagonal = 0
    for column, coefficient in convolution(coefficients).items():
        if any(v not in (0, 1, 2) for v in column):
            raise ValueError('test requires squarefree original columns')
        surviving_rows = math.prod(p.q - 1 if v else p.q for p, v in zip(ring.primes, column))
        diagonal += coefficient.norm() * surviving_rows
    return direct, diagonal


def core_square_coefficient(column: tuple[int, ...], weights: dict[tuple[int, ...], int],
                            nu: tuple[Eisenstein, ...]) -> Eisenstein:
    """Convolution coefficient using v=c*d^2 with squarefree coprime c,d."""
    if len(nu) != len(column) or any(v not in (0, 1, 2) for v in column):
        raise ValueError('invalid cubefree column')
    core = [i for i, v in enumerate(column) if v == 1]
    weight_sum = 0
    for selected in itertools.product((0, 1), repeat=len(core)):
        left = [int(v == 2) for v in column]
        right = left.copy()
        for i, bit in zip(core, selected):
            left[i], right[i] = bit, 1 - bit
        weight_sum += weights.get(tuple(left), 0) * weights.get(tuple(right), 0)
    return (Eisenstein((-1) ** len(core) * weight_sum)
            * product(z ** v for z, v in zip(nu, column)))


def completion_fourth_exponent(h: F) -> F:
    """Elementary bound min(H*D^4, H*D^3+D^5), ignoring epsilon losses.

The analytic derivation is in fourth_moment.md; this is just its arithmetic.
"""
    if not isinstance(h, (int, F)) or h < 0:
        raise ValueError('a nonnegative exact exponent is required')
    h = F(h)
    return min(h + 4, max(h + 3, F(5)))


def exponent_report() -> dict:
    h = F(4, 3)
    elementary = completion_fourth_exponent(h)
    target = h + 2
    return {
        'row_exponent': str(h),
        'P4_target': str(target),
        'trivial_fourth_bound': str(h + 4),
        'elementary_completion_fourth_bound': str(elementary),
        'gap_to_P4': str(elementary - target),
        'replica_extraction_from_elementary_bound': str((elementary - h / 6) / 4),
        'positive_coefficient_lower_bound': str(4 + h / 6),
        'positive_coefficient_excess_over_P4': str(4 + h / 6 - target),
    }


def verify_finite_identities() -> dict:
    local_checks = 0
    for p in (P7, P7BAR, P13, P19, P5_INERT):
        ring = ResidueRing((p,))
        for exponent in (-2, -1, 0, 1, 2):
            for k in ring.residues:
                if finite_fourier(ring, (exponent,), k) != primitive_mask_fourier(ring, (exponent,), k):
                    raise ArithmeticError('local Fourier identity failed')
                local_checks += 1
    cases = [
        (ResidueRing((P7, P13)), (1, 0)),
        (ResidueRing((P7, P13)), (0, -1)),
        (ResidueRing((P7, P13)), (1, -2)),
        (ResidueRing((P7, P13)), (0, 0)),
        (ResidueRing((P7, P5_INERT)), (2, 0)),
        (ResidueRing((P7, P7BAR)), (1, 0)),
        (ResidueRing((P19, P7)), (2, 0)),
    ]
    crt_checks = 0
    for ring, exponents in cases:
        for k in ring.residues:
            if finite_fourier(ring, exponents, k) != primitive_mask_fourier(ring, exponents, k):
                raise ArithmeticError('CRT primitive/mask identity failed')
            crt_checks += 1
    ring = ResidueRing((P7, P13, P5_INERT))
    coefficients = {bits: Eisenstein((-1) ** sum(bits) * (1 + i)) * SIXTH_ROOTS[i % 6]
                    for i, bits in enumerate(itertools.product((0, 1), repeat=3)) if any(bits)}
    direct, diagonal = complete_fourth_moment(ring, coefficients)
    if direct != diagonal:
        raise ArithmeticError('complete finite fourth moment failed')
    return {
        'local_fourier_equalities': local_checks,
        'crt_fourier_equalities': crt_checks,
        'split_prime_norms': [7, 7, 13, 19],
        'inert_prime_norm': 25,
        'complete_fourth_moment': {
            'residue_count': ring.norm, 'column_count': len(coefficients),
            'direct': direct, 'grouped_diagonal': diagonal,
        },
    }


if __name__ == '__main__':
    print(json.dumps({
        'status': 'exact finite algebra only; P4 and RH are NOT proved',
        'source_revision': 'fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb',
        'incidence_patterns': [incidence(mask) for mask in range(1, 16)],
        'verification': verify_finite_identities(),
        'exponent_budget': exponent_report(),
    }, indent=2))
