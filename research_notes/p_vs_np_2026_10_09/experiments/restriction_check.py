#!/usr/bin/env python3
"""Independent, exact, SMALL FINITE checks of family112's restriction lemma.

This is a computational experiment, not a proof.  In particular, "exhaustive"
means all multisets of at most --exhaustive-max-clauses canonical clauses, NOT
all CNFs (whose indexed clause count is unbounded).  Every restriction and
live assignment of each chosen formula is checked, without sampling them.

Literal i means x_i, literal -i means not x_i, with coordinates numbered 1..d.
A raw clause is a tuple of literals; () is false and None is an explicit true
clause.  Only true/tautological clauses are discarded.  Repeated literals in a
clause are normalized, but repeated CLAUSES retain distinct indices.

Default parameters are p in {1/8, 1/4} and integer b in {1, 2}.  All coefficient
bounds E W_j <= theta**j are checked, even if theta >= 1.  The infinite geometric
bound is compared ONLY when theta < 1.  No floating point or LP is used.

Examples (run from any directory):
  python3 -B restriction_check.py --self-test
  python3 -B restriction_check.py                  # full default experiment
  python3 -B restriction_check.py --exhaustive-max-d 2 --chosen-max-d 3 \
      --random-cases 1 --skip-parity --output -     # small stdout-only run

The separate parity check concerns an INVALID gate-fanin substitution for CNF
width, not the original lemma.  It does not import the parent's locality probe.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations_with_replacement, product
import json
from math import comb, factorial, prod
from pathlib import Path
import random
import sys
import unittest
from typing import Iterator

RawClause = tuple[int, ...] | None
CNF = tuple[RawClause, ...]
ZERO, ONE = Fraction(0), Fraction(1)
DEFAULT_PS = (Fraction(1, 8), Fraction(1, 4))
MANUSCRIPT = (
    "preprints/Beyond-the-Square-Root-Exponent-for-Depth-Three-Boolean-Circuits-"
    "September-23-2026/build/latex/sections/02_restriction.tex"
)


def rational(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def jsonable(value):
    if isinstance(value, Fraction):
        return rational(value)
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(v) for v in value]
    return value


def submasks(mask: int) -> Iterator[int]:
    """All bit patterns supported on mask, including zero, in fixed order."""
    current = mask
    while True:
        yield current
        if current == 0:
            break
        current = (current - 1) & mask


def clause_value(clause: RawClause, assignment: int) -> int:
    """Literal-level evaluation, independent of scope/violating-pattern code."""
    return int(clause is None or any(
        bool(assignment & (1 << (abs(lit) - 1))) == (lit > 0)
        for lit in clause
    ))


def cnf_value(cnf: CNF, assignment: int) -> int:
    return int(all(clause_value(clause, assignment) for clause in cnf))


def restrict_clause(clause: RawClause, fixed_mask: int, fixed_bits: int) -> RawClause:
    """Literal substitution; keep false, repeated, and not-yet-true clauses."""
    if clause is None:
        return None
    remaining = []
    for lit in clause:
        bit = 1 << (abs(lit) - 1)
        if bit & fixed_mask:
            if bool(bit & fixed_bits) == (lit > 0):
                return None
        else:
            remaining.append(lit)
    return tuple(remaining)


def restrict_cnf(cnf: CNF, fixed_mask: int, fixed_bits: int) -> CNF:
    """Drop clauses made true; do not deduplicate the surviving clauses."""
    reduced = (restrict_clause(c, fixed_mask, fixed_bits) for c in cnf)
    return tuple(c for c in reduced if c is not None)


@dataclass(frozen=True)
class Clause:
    index: int  # 1-based index AFTER dropping true/tautological clauses
    literals: tuple[int, ...]
    scope: int
    violating_pattern: int

    def violated(self, assignment: int) -> int:
        return int((assignment & self.scope) == self.violating_pattern)


@dataclass(frozen=True)
class Formula:
    name: str
    d: int
    raw: CNF
    suite: str = "chosen"
    declared_k: int | None = None

    def description(self) -> dict:
        return {"name": self.name, "d": self.d, "cnf": self.raw,
                "suite": self.suite, "declared_k": self.declared_k}


@dataclass(frozen=True)
class PreparedFormula:
    source: Formula
    clauses: tuple[Clause, ...]
    k: int
    discarded_true_or_tautological: int


def prepare_formula(formula: Formula) -> PreparedFormula:
    if type(formula.d) is not int or not 0 <= formula.d <= 6:
        raise ValueError("this small finite checker requires 0 <= d <= 6")
    clauses = []
    discarded = 0
    for raw in formula.raw:
        if raw is None:
            discarded += 1
            continue
        if any(type(lit) is not int or not 1 <= abs(lit) <= formula.d for lit in raw):
            raise ValueError("literals must be nonzero integers in +/-[1,d]")
        literals = set(raw)
        if any(-lit in literals for lit in literals):
            discarded += 1
            continue
        canonical = tuple(sorted(literals, key=abs))
        scope = sum(1 << (abs(lit) - 1) for lit in canonical)
        # A positive literal is violated at 0, a negative literal at 1.
        pattern = sum(1 << (abs(lit) - 1) for lit in canonical if lit < 0)
        clauses.append(Clause(len(clauses) + 1, canonical, scope, pattern))
    width = max((c.scope.bit_count() for c in clauses), default=0)
    k = width if formula.declared_k is None else formula.declared_k
    if type(k) is not int or k < width:
        raise ValueError("declared k must be an integer at least the normalized CNF width")
    return PreparedFormula(formula, tuple(clauses), k, discarded)


def validate_b(b: int) -> None:
    if type(b) is not int or b < 1:
        raise ValueError("b must be a positive integer; use b=1 and b=2, not b=1/2")


def theta(k: int, b: int, p: Fraction) -> Fraction:
    validate_b(b)
    if type(k) is not int or k < 0 or not isinstance(p, Fraction) or not 0 < p < 1:
        raise ValueError("need integer k >= 0 and rational 0 < p < 1")
    alpha = 2 * p / (1 - p)
    return sum((comb(k, ell) * alpha**ell for ell in range(b + 1, k + 1)), ZERO)


class BudgetExceeded(RuntimeError):
    pass


@dataclass(frozen=True)
class ScopePath:
    indices: tuple[int, ...]  # zero-based tuple positions; serialized as 1-based
    unions: tuple[int, ...]   # U_1,...,U_j
    required_scope: int
    required_pattern: int
    internally_compatible: bool


@dataclass(frozen=True)
class WeightedPath:
    path: ScopePath
    compatible: bool
    sigma: int
    c_counts: tuple[int, ...]
    weight: Fraction
    # Keep indexed true, false, and repeated clauses in every I_h family.
    mixture_families: tuple[CNF, ...]


def scope_paths(formula: PreparedFormula, live: int, b: int,
                max_paths: int = 20_000) -> tuple[ScopePath, ...]:
    """Enumerate the paper's scope-defined paths, INCLUDING incompatible ones.

    No truth values and no claimed inequality prune this enumeration.
    """
    validate_b(b)
    found = []

    def extend(indices, unions, required_scope, required_pattern, compatible):
        used = unions[-1] if unions else 0
        for i, clause in enumerate(formula.clauses):
            if (clause.scope & live & ~used).bit_count() <= b:
                continue
            new_used = used | (clause.scope & live)
            good = compatible and not (
                (required_pattern ^ clause.violating_pattern) & required_scope & clause.scope
            )
            path = ScopePath(indices + (i,), unions + (new_used,),
                             required_scope | clause.scope,
                             required_pattern | clause.violating_pattern, bool(good))
            found.append(path)
            if len(found) > max_paths:
                raise BudgetExceeded(f"more than {max_paths} scope paths for one live set")
            extend(path.indices, path.unions, path.required_scope,
                   path.required_pattern, path.internally_compatible)

    extend((), (), 0, 0, True)
    return tuple(found)


def classifications(formula: PreparedFormula, live: int, paths: tuple[ScopePath, ...],
                    b: int) -> dict[int, tuple[tuple[int, ...], tuple[int, ...]]]:
    unions = {0}
    unions.update(u for path in paths for u in path.unions)
    answer = {}
    for u in sorted(unions):
        remaining_sizes = [(c.scope & live & ~u).bit_count() for c in formula.clauses]
        answer[u] = (tuple(i for i, n in enumerate(remaining_sizes) if n <= b),
                     tuple(i for i, n in enumerate(remaining_sizes) if n == 0))
    return answer


def weight_paths(formula: PreparedFormula, live: int, fixed: int, b: int,
                 paths: tuple[ScopePath, ...], classes=None) -> tuple[WeightedPath, ...]:
    """Literal c_U counts over ALL retained clause indices, never just the path."""
    all_mask = (1 << formula.source.d) - 1
    classes = classifications(formula, live, paths, b) if classes is None else classes
    answer = []
    for path in paths:
        compatible = path.internally_compatible and not (
            (path.required_pattern ^ fixed) & path.required_scope & ~live
        )
        sigma = path.required_pattern & live
        if not compatible:
            answer.append(WeightedPath(path, False, sigma, (), ZERO, ()))
            continue
        final_fixed = fixed | sigma
        counts, families = [], []
        for u in path.unions:
            easy, closed = classes[u]
            c = sum(formula.clauses[i].violated(final_fixed) for i in closed)
            if c <= 0:
                raise ArithmeticError("a compatible path has a nonpositive literal c_U count")
            counts.append(c)
            # I_h is defined BEFORE substituting the FINAL pattern.  In particular
            # do not drop I_h entries subsequently made constant or duplicates.
            closed_set = set(closed)
            families.append(tuple(
                restrict_clause(formula.clauses[i].literals,
                                (all_mask & ~live) | path.unions[-1], final_fixed)
                for i in easy if i not in closed_set
            ))
        answer.append(WeightedPath(path, True, sigma, tuple(counts),
                                   Fraction(1, prod(counts)), tuple(families)))
    return tuple(answer)


def path_weights(formula: PreparedFormula, live: int, fixed: int, b: int,
                 max_paths: int = 20_000) -> tuple[tuple[Fraction, ...], tuple[WeightedPath, ...]]:
    """Return W_0,...,W_floor(d/(b+1)) and the explicit indexed weighted paths."""
    validate_b(b)
    all_mask = (1 << formula.source.d) - 1
    if live < 0 or fixed < 0 or (live | fixed) & ~all_mask or live & fixed:
        raise ValueError("live and fixed must be disjoint bit masks within [d]")
    paths = scope_paths(formula, live, b, max_paths)
    weighted = weight_paths(formula, live, fixed, b, paths)
    weights = [ONE] + [ZERO] * (formula.source.d // (b + 1))
    for item in weighted:
        weights[len(item.path.indices)] += item.weight
    return tuple(weights), weighted


@lru_cache(maxsize=4096)
def marker_mixture_value(a: int, c: int, w: int) -> Fraction:
    """Enumerate prefix SUBSETS by exact counts of indexed-object permutations.

    For one specified subset S of s clauses before the first marker there are
    s! * c * (a+c-s-1)! permutations.  There are C(a-w,s) passing subsets.
    This computes the experiment, NOT the target expression c/(c+w), and avoids
    factorial-time permutation enumeration.  True/false/repeated clauses still
    count as separate objects in a and w.
    """
    if a < 0 or c < 1 or not 0 <= w <= a:
        raise ValueError("need a >= w >= 0 and c >= 1")
    passing_permutations = sum(
        comb(a - w, s) * factorial(s) * c * factorial(a + c - s - 1)
        for s in range(a - w + 1)
    )
    return Fraction(passing_permutations, factorial(a + c))


class Audit:
    def __init__(self, max_counterexamples: int = 25):
        self.counts: Counter = Counter()
        self.failures: Counter = Counter()
        self.counterexamples: list[dict] = []
        self.max_counterexamples = max_counterexamples

    def check(self, condition: bool, kind: str, context: dict,
              observed=None, expected=None) -> None:
        self.counts[kind] += 1
        if not condition:
            self.failures[kind] += 1
            if len(self.counterexamples) < self.max_counterexamples:
                self.counterexamples.append(jsonable({
                    "check": kind, **context, "observed": observed, "expected": expected,
                }))

    @property
    def ok(self) -> bool:
        return not self.failures


@lru_cache(maxsize=256)
def large_subsets(scope: int, b: int) -> tuple[int, ...]:
    return tuple(d for d in submasks(scope) if d.bit_count() > b)


def reverse_tables(formula: PreparedFormula, violations: tuple[int, ...], b: int,
                   p: Fraction) -> tuple[tuple[Fraction, ...], ...]:
    """Independent finite recurrence F_s(R), with literal indexed multiplicities.

    This function does not use forward path weights or theta.  Only the caller
    compares its fully computed entries with bounds.
    """
    nstates = 1 << formula.source.d
    choices = []
    for r in range(nstates):
        eligible = [c for c, violated in zip(formula.clauses, violations)
                    if violated and not c.scope & r]
        steps = tuple((r | delta, delta.bit_count())
                      for c in eligible for delta in large_subsets(c.scope, b))
        choices.append((len(eligible), steps))
    alpha = 2 * p / (1 - p)
    powers = [alpha**n for n in range(formula.source.d + 1)]
    rows = [(ONE,) * nstates]
    for _ in range(formula.source.d // (b + 1)):
        previous = rows[-1]
        row = []
        for count, steps in choices:
            value = sum((powers[size] * previous[next_r] for next_r, size in steps
                         if previous[next_r]), ZERO)
            row.append(value / count if count else ZERO)
        rows.append(tuple(row))
    return tuple(rows)


def check_formula(source: Formula, b: int, ps: tuple[Fraction, ...] = DEFAULT_PS,
                  *, audit: Audit | None = None, reverse: bool = True,
                  max_paths: int = 20_000) -> dict:
    """Check EVERY restriction, point, path, and requested expectation of a CNF."""
    validate_b(b)
    audit = Audit() if audit is None else audit
    before = audit.counts.copy()
    formula = prepare_formula(source)
    d, clauses = source.d, formula.clauses
    all_mask, max_j = (1 << d) - 1, d // (b + 1)
    context = {"formula": source.description(), "b": b, "k": formula.k}
    thetas = {p: theta(formula.k, b, p) for p in ps}
    probability = {p: [p**m * ((1 - p) / 2)**(d - m) for m in range(d + 1)] for p in ps}
    live_probability = {p: [p**m * (1 - p)**(d - m) for m in range(d + 1)] for p in ps}
    masses = {p: ZERO for p in ps}
    expected = {p: [ONE] + [ZERO] * max_j for p in ps}
    # Separate pointwise reweighting, grouped by the FULL assignment y.
    full_assignment_sums = {p: [[ONE] + [ZERO] * max_j for _ in range(1 << d)] for p in ps}
    direct_values, violation_rows = [], []
    for y in range(1 << d):
        row = tuple(c.violated(y) for c in clauses)
        direct = cnf_value(source.raw, y)
        direct_values.append(direct)
        violation_rows.append(row)
        audit.check(direct == int(not any(row)), "normalized_formula", context, int(not any(row)), direct)
        for c, v in zip(clauses, row):
            literal_violation = 1 - clause_value(c.literals, y)
            audit.check(v == literal_violation, "unique_violating_pattern", context, v, literal_violation)
    maximum_w = {"value": ONE, "live": 0, "fixed": 0, "W_j": (ONE,) + (ZERO,) * max_j}
    maximum_c, maximum_length = 0, 0
    for live in range(1 << d):
        m = live.bit_count()
        outside = all_mask & ~live
        paths = scope_paths(formula, live, b, max_paths)
        classes = classifications(formula, live, paths, b)
        children = {path.indices: [] for path in paths}
        for n, path in enumerate(paths):
            if len(path.indices) > 1:
                children[path.indices[:-1]].append(n)
            prev = 0
            valid = len(path.indices) <= m // (b + 1) and len(set(path.indices)) == len(path.indices)
            for i, u in zip(path.indices, path.unions):
                valid &= (u == (prev | (clauses[i].scope & live)) and (u & ~prev).bit_count() > b)
                prev = u
            audit.check(bool(valid), "scope_path_rules", context)
            # Reconstruct T and the ordered indices from the reverse encoding.
            r = live & ~path.unions[-1]
            deltas = tuple(u & ~(path.unions[h - 1] if h else 0)
                           for h, u in enumerate(path.unions))
            reconstructed_indices = []
            for i, delta in reversed(tuple(zip(path.indices, deltas))):
                valid_step = not (r & delta) and not (delta & ~clauses[i].scope)
                audit.check(valid_step, "reverse_encoding_step", context)
                r |= delta
                reconstructed_indices.append(i)
            audit.check(r == live and tuple(reversed(reconstructed_indices)) == path.indices,
                        "reverse_encoding_reconstruction", context)
        maximum_length = max(maximum_length, max((len(p.indices) for p in paths), default=0))
        for p in ps:
            masses[p] += (1 << (d - m)) * probability[p][m]
        for fixed in submasks(outside):
            context.update(live=live, fixed=fixed)
            context.pop("assignment", None)
            audit.counts["restrictions"] += 1
            audit.counts["scope_path_occurrences"] += len(paths)
            if not live:
                audit.counts["empty_live_restrictions"] += 1
            weighted = weight_paths(formula, live, fixed, b, paths, classes)
            weights = [ONE] + [ZERO] * max_j
            for item in weighted:
                weights[len(item.path.indices)] += item.weight
                if item.compatible:
                    audit.counts["compatible_path_occurrences"] += 1
                    maximum_c = max(maximum_c, *item.c_counts)
                    audit.check(all(c >= h for h, c in enumerate(item.c_counts, 1)),
                                "positive_path_counts", context)
                    for family in item.mixture_families:
                        audit.counts["mixture_indexed_clause_occurrences"] += len(family)
                        audit.counts["mixture_constant_true_occurrences"] += sum(c is None for c in family)
                        audit.counts["mixture_constant_false_occurrences"] += sum(c == () for c in family)
                        audit.counts["mixture_repeated_clause_occurrences"] += len(family) - len(set(family))
                        audit.check(all(c is None or len({abs(lit) for lit in c}) <= b for c in family),
                                    "mixture_clause_width", context)
            total_w = sum(weights, ZERO)
            if total_w > maximum_w["value"]:
                maximum_w = {"value": total_w, "live": live, "fixed": fixed, "W_j": tuple(weights)}
            for p in ps:
                for j in range(1, max_j + 1):
                    if weights[j]:
                        expected[p][j] += probability[p][m] * weights[j]
            easy_cnf = restrict_cnf(tuple(clauses[i].literals for i in classes[0][0]), outside, fixed)
            raw_restricted = restrict_cnf(source.raw, outside, fixed)
            audit.check(all(len({abs(lit) for lit in c}) <= b for c in easy_cnf),
                        "initial_CNF_width", context)
            reweighted_sums = [ZERO] * (max_j + 1)
            support_sizes = [0] * len(paths)
            for z in submasks(live):
                y = fixed | z
                context["assignment"] = y
                audit.counts["live_assignments"] += 1
                row = violation_rows[y]
                q = sum(row)
                a = {u: sum(row[i] for i in easy) for u, (easy, _) in classes.items()}
                c_direct = {u: sum(row[i] for i in closed) for u, (_, closed) in classes.items()}
                k_value = cnf_value(easy_cnf, z)
                audit.check(cnf_value(raw_restricted, z) == direct_values[y],
                            "restricted_CNF", context, cnf_value(raw_restricted, z), direct_values[y])
                audit.check(k_value == int(a[0] == 0), "initial_CNF_value", context)
                terms, residuals = [], []
                t_by_length, r_by_length = [ZERO] * (max_j + 2), [ZERO] * (max_j + 2)
                reweighted = [ONE] + [ZERO] * max_j
                for n, item in enumerate(weighted):
                    path = item.path
                    j = len(path.indices)
                    numerator = int(all(row[i] for i in path.indices))
                    on_cylinder = item.compatible and (z & path.unions[-1]) == item.sigma
                    audit.check(bool(numerator) == on_cylinder, "path_cylinder", context)
                    if numerator:
                        support_sizes[n] += 1
                        ac = tuple(a[u] for u in path.unions)
                        cc = tuple(c_direct[u] for u in path.unions)
                        audit.check(all(aa >= c >= h for h, (aa, c) in enumerate(zip(ac, cc), 1)),
                                    "pointwise_positive_counts", context, (ac, cc))
                        if not all(ac) or not all(cc) or not q:
                            raise ArithmeticError("a supported path fraction has a zero denominator")
                        term = Fraction(1, prod(ac))
                        residual = Fraction(1, q * prod(ac[:-1]))
                        reweighted[j] += Fraction(1 << path.unions[-1].bit_count(), prod(cc))
                        audit.check(cc == item.c_counts, "c_U_constant_on_cylinder", context, cc, item.c_counts)
                        mixture = ONE
                        for h, (family, count) in enumerate(zip(item.mixture_families, item.c_counts)):
                            w = sum(1 - clause_value(clause, z) for clause in family)
                            u = path.unions[h]
                            audit.check(w == a[u] - c_direct[u], "indexed_I_h_count", context, w, a[u] - c_direct[u])
                            marginal = marker_mixture_value(len(family), count, w)
                            audit.check(marginal == Fraction(count, count + w),
                                        "finite_marker_mixture", context, marginal, Fraction(count, count + w))
                            mixture *= marginal
                        mixture_rhs = k_value * item.weight * mixture
                        if reverse:
                            left_base = Fraction(1 << path.unions[-1].bit_count(), prod(cc))
                            for p in ps:
                                alpha = 2 * p / (1 - p)
                                rhs = live_probability[p][(live & ~path.unions[-1]).bit_count()]
                                prev = 0
                                for h, (i, u) in enumerate(zip(path.indices, path.unions)):
                                    r = live & ~u
                                    delta = u & ~prev
                                    # Count V_R from literal evaluations, not from cached c_h.
                                    vr = [cl for cl in clauses if not cl.scope & r
                                          and not clause_value(cl.literals, y)]
                                    audit.check(len(vr) == cc[h] and clauses[i] in vr,
                                                "reverse_V_R_count", context, len(vr), cc[h])
                                    rhs *= alpha**delta.bit_count() / len(vr)
                                    prev = u
                                lhs = live_probability[p][m] * left_base
                                audit.check(lhs == rhs, "reverse_weight_factorization", context, lhs, rhs)
                    else:
                        # The paper's zero-numerator convention, even for 0/0.
                        term = residual = mixture_rhs = ZERO
                    audit.check(k_value * term == mixture_rhs, "path_mixture_identity", context,
                                k_value * term, mixture_rhs)
                    terms.append(term)
                    residuals.append(residual)
                    t_by_length[j] += term
                    r_by_length[j] += residual
                expanded = k_value * (ONE + sum(((-1)**j * t_by_length[j]
                                                for j in range(1, max_j + 1)), ZERO))
                audit.check(expanded == direct_values[y], "pointwise_expansion", context,
                            expanded, direct_values[y])
                for n, path in enumerate(paths):
                    replaced = terms[n] - sum((residuals[i] for i in children[path.indices]), ZERO)
                    audit.check(residuals[n] == replaced, "pointwise_residual_identity", context,
                                residuals[n], replaced)
                if k_value and q:
                    partial = ONE
                    for s in range(m // (b + 1) + 1):
                        if s:
                            partial += (-1)**s * t_by_length[s]
                        value = partial + (-1)**(s + 1) * r_by_length[s + 1]
                        audit.check(value == 0, "truncated_expansion", context, value, ZERO)
                for j in range(max_j + 1):
                    reweighted_sums[j] += reweighted[j]
                    if j and reweighted[j]:
                        for p in ps:
                            full_assignment_sums[p][y][j] += live_probability[p][m] * reweighted[j]
            context.pop("assignment", None)
            for n, item in enumerate(weighted):
                target_size = (1 << (m - item.path.unions[-1].bit_count())) if item.compatible else 0
                audit.check(support_sizes[n] == target_size, "path_support_cardinality", context,
                            support_sizes[n], target_size)
            for j, w in enumerate(weights):
                averaged = reweighted_sums[j] / (1 << m)
                audit.check(averaged == w, "conditional_full_assignment_reweighting", context, averaged, w)
    context.pop("live", None)
    context.pop("fixed", None)
    expectation_reports = []
    for p in ps:
        th = thetas[p]
        context["p"] = rational(p)
        audit.check(masses[p] == 1, "restriction_probability_mass", context, masses[p], ONE)
        for j, value in enumerate(expected[p]):
            context["j"] = j
            full_average = sum((row[j] for row in full_assignment_sums[p]), ZERO) / (1 << d)
            audit.check(value == full_average, "unconditional_full_assignment_reweighting", context, value, full_average)
            audit.check(value <= th**j, "expected_W_j_bound", context, value, th**j)
        context.pop("j", None)
        finite_bound = sum((th**j for j in range(max_j + 1)), ZERO)
        e_total = sum(expected[p], ZERO)
        audit.check(e_total <= finite_bound, "finite_sum_bound", context, e_total, finite_bound)
        geometric = ONE / (1 - th) if th < 1 else None
        if geometric is not None:
            audit.check(e_total <= geometric, "geometric_bound", context, e_total, geometric)
        else:
            audit.counts["geometric_bound_skipped_theta_ge_1"] += 1
        if reverse:
            pi = [live_probability[p][r.bit_count()] for r in range(1 << d)]
            for y, row in enumerate(violation_rows):
                context["assignment"] = y
                table = reverse_tables(formula, row, b, p)
                for j, f_values in enumerate(table):
                    context["j"] = j
                    for r, f in enumerate(f_values):
                        audit.check(f <= th**j, "reverse_state_bound", {**context, "R": r}, f, th**j)
                    reverse_sum = sum((pi[r] * f for r, f in enumerate(f_values)), ZERO)
                    forward_sum = full_assignment_sums[p][y][j]
                    audit.check(forward_sum <= reverse_sum, "fixed_y_reverse_domination", context, forward_sum, reverse_sum)
                    audit.check(reverse_sum <= th**j, "fixed_y_expected_bound", context, reverse_sum, th**j)
            context.pop("assignment", None)
            context.pop("j", None)
        expectation_reports.append({
            "p": p, "theta": th, "E_W_j": tuple(expected[p]), "E_W": e_total,
            "coefficient_bounds": tuple(th**j for j in range(max_j + 1)),
            "finite_sum_bound": finite_bound, "geometric_bound": geometric,
            "geometric_comparison_performed": geometric is not None,
            "geometric_skip_reason": None if geometric is not None else "theta >= 1",
        })
    return {
        "formula": source.description(), "b": b, "k": formula.k,
        "retained_indexed_clauses": len(clauses),
        "discarded_true_or_tautological": formula.discarded_true_or_tautological,
        "reverse_recurrence_checked": reverse,
        "counts": dict(audit.counts - before), "expectations": expectation_reports,
        "max_restriction_W": maximum_w, "max_c_h": maximum_c,
        "max_scope_path_length": maximum_length,
    }


def canonical_clauses(d: int) -> tuple[tuple[int, ...], ...]:
    """Exactly 3**d clauses: absent/positive/negative per variable, incl. false."""
    return tuple(tuple((i + 1) * sign for i, sign in enumerate(signs) if sign)
                 for signs in product((0, 1, -1), repeat=d))


def exhaustive_formula_count(max_d: int, max_clauses: int) -> int:
    return sum(comb(3**d + n - 1, n)
               for d in range(max_d + 1) for n in range(max_clauses + 1))


def exhaustive_formulas(max_d: int, max_clauses: int) -> Iterator[Formula]:
    for d in range(max_d + 1):
        universe = canonical_clauses(d)
        for n in range(max_clauses + 1):
            for ordinal, indices in enumerate(combinations_with_replacement(range(len(universe)), n)):
                yield Formula(f"exhaustive-d{d}-n{n}-{ordinal}", d,
                              tuple(universe[i] for i in indices), "exhaustive")


def chosen_formulas(max_d: int, seed: int, random_cases: int) -> tuple[Formula, ...]:
    cases = [Formula("zero-dimensional-empty", 0, ()),
             Formula("zero-dimensional-false-repeated", 0, ((), (), None)),
             Formula("zero-dimensional-true-declared-k2", 0, (None,), declared_k=2)]
    for d in range(1, max_d + 1):
        whole = tuple(range(1, d + 1))
        cases.extend([
            Formula(f"true-tautologies-d{d}", d, (None, (1, -1), (1, -1, 1))),
            Formula(f"single-wide-d{d}", d, (whole,)),
            Formula(f"repeated-wide-d{d}", d, (whole,) * 4 + (None, (1, -1))),
            Formula(f"false-with-wide-d{d}", d, (whole, whole, (), None)),
            Formula(f"repeated-literals-d{d}", d, (whole + (1, 1),)),
            Formula(f"conflicting-units-and-wide-d{d}", d, ((1,), (-1,), whole)),
        ])
    cases.extend([
        Formula("disjoint-pairs", 4, ((1, 2), (3, 4))),
        Formula("overlapping-compatible", 4, ((1, 2), (1, 3, 4))),
        Formula("overlapping-incompatible", 4, ((1, 2), (-1, 3, 4))),
        Formula("final-substitution-true-false-repeats", 4,
                ((1, 2), (3, 4), (1, 3), (1, 3), (1, -3))),
        Formula("unselected-closed-counts", 4, ((1, 2), (1,), (-1,), (), (3, 4))),
        Formula("three-disjoint-pairs", 6, ((1, 2), (3, 4), (5, 6))),
        Formula("three-disjoint-pairs-unequal-multiplicity", 6,
                ((1, 2), (3, 4), (3, 4), (5, 6), (5, 6), (5, 6))),
        Formula("two-disjoint-triples", 6, ((1, -2, 3), (-4, 5, -6))),
        Formula("nested-and-crossing", 6,
                ((1, 2), (1, 2, 3, 4), (1, 2, 3, 4, 5, 6), (-1, 3, 5),
                 (2, -4, 6), (2, -4, 6))),
    ])
    for d in range(2, max_d + 1):
        # All full-scope patterns, each twice: a false formula with many indexed
        # clauses, but only one-step paths, so this is deliberately inexpensive.
        complete = tuple(tuple(-(i + 1) if y & (1 << i) else i + 1 for i in range(d))
                         for y in range(1 << d))
        cases.append(Formula(f"all-patterns-repeated-d{d}", d, complete + complete))
    rng = random.Random(seed)
    for d in range(max_d + 1):
        for n in range(random_cases):
            raw = []
            for _ in range(rng.randrange(9)):
                r = rng.random()
                if raw and r < 0.25:
                    clause = rng.choice(raw)
                elif r < 0.35:
                    clause = None
                elif d and r < 0.45:
                    i = rng.randrange(1, d + 1)
                    clause = (i, -i)
                else:
                    scope = sorted(rng.sample(range(1, d + 1), rng.randrange(d + 1)))
                    clause = tuple(i if rng.randrange(2) else -i for i in scope)
                    if clause and rng.random() < 0.2:
                        clause += (clause[0],)
                raw.append(clause)
            cases.append(Formula(f"seed-{seed}-d{d}-case-{n}", d, tuple(raw), "seeded"))
    return tuple(c for c in cases if c.d <= max_d)


def check_naive_parity_extension(audit: Audit | None = None) -> dict:
    """Independently verify the d=6 claim with finite primal AND dual witnesses.

    Enumerate literal 1-CNF subcubes, not an LP or the parent's implementation.
    The zero CNF function adds only a zero correlation to this complete list.
    """
    audit = Audit() if audit is None else audit
    before = audit.counts.copy()
    d, b, k, p = 6, 1, 2, Fraction(1, 4)
    all_mask = (1 << d) - 1
    th = theta(k, b, p)
    promised = ONE / (1 - th)
    expected_minimum, probability_mass = ZERO, ZERO
    by_live = {m: {"restrictions": 0, "minimal_W_sum": ZERO, "probability_mass": ZERO}
               for m in range(d + 1)}
    for live in range(1 << d):
        m = live.bit_count()
        outside = all_mask & ~live
        zs = tuple(submasks(live))
        # All nonzero 1-CNF functions: choose each variable free, fixed 0, fixed 1.
        subcubes = tuple(tuple((i + 1) if bits & (1 << i) else -(i + 1)
                               for i in range(d) if constrained & (1 << i))
                         for constrained in submasks(live) for bits in submasks(constrained))
        cube_truths = tuple(tuple(cnf_value(tuple((lit,) for lit in cube), z) for z in zs)
                           for cube in subcubes)
        for fixed in submasks(outside):
            ctx = {"branch": "naive_gate_fanin_extension_only", "live": live, "fixed": fixed}
            audit.counts["parity_restrictions"] += 1
            h = tuple(int((fixed | z).bit_count() % 2 == 0) for z in zs)
            g = tuple(2 * value - 1 for value in h)
            corr = max(Fraction(abs(sum(gi * ji for gi, ji in zip(g, cube))), 1 << m)
                       for cube in cube_truths)
            audit.counts["parity_subcube_correlations"] += len(cube_truths)
            correlation = Fraction(abs(sum(gi * hi for gi, hi in zip(g, h))), 1 << m)
            audit.check(corr == Fraction(1, 1 << m), "parity_dual_corr_1", ctx, corr, Fraction(1, 1 << m))
            target_correlation = Fraction(1, 2) if m else Fraction(h[0])
            audit.check(correlation == target_correlation, "parity_GH_correlation", ctx,
                        correlation, target_correlation)
            lower = correlation / corr
            # Primal: coefficient +1 on each satisfying singleton, using m units.
            singletons = tuple(tuple(((i + 1) if z & (1 << i) else -(i + 1),)
                                      for i in range(d) if live & (1 << i))
                               for z, value in zip(zs, h) if value)
            for z, value in zip(zs, h):
                reconstructed = sum(cnf_value(cube, z) for cube in singletons)
                audit.check(reconstructed == value, "parity_primal_pointwise", {**ctx, "z": z},
                            reconstructed, value)
            upper = Fraction(len(singletons))
            audit.check(upper == lower, "parity_primal_dual_match", ctx, upper, lower)
            prob = p**m * ((1 - p) / 2)**(d - m)
            probability_mass += prob
            expected_minimum += prob * lower
            by_live[m]["restrictions"] += 1
            by_live[m]["minimal_W_sum"] += lower
            by_live[m]["probability_mass"] += prob
    # A separate fanin-two truth table, computed by binary XOR gates and NOT.
    xor_table = (0, 1, 1, 0)
    parity_cnf = tuple(tuple(-(i + 1) if y & (1 << i) else i + 1 for i in range(d))
                       for y in range(1 << d) if y.bit_count() % 2)
    for y in range(1 << d):
        accumulator = y & 1
        for i in range(1, d):
            accumulator = xor_table[2 * accumulator + ((y >> i) & 1)]
        expected_truth = int(y.bit_count() % 2 == 0)
        audit.check(1 - accumulator == expected_truth, "parity_fanin2_truth_table", {"y": y})
        audit.check(cnf_value(parity_cnf, y) == expected_truth, "parity_width6_CNF_truth_table", {"y": y})
    closed_form = (1 + p)**d / 2
    audit.check(probability_mass == 1, "parity_probability_mass", {}, probability_mass, ONE)
    audit.check(expected_minimum == closed_form, "parity_expected_minimum", {}, expected_minimum, closed_form)
    audit.check(expected_minimum > promised, "parity_naive_extension_strict_counterexample", {},
                expected_minimum, promised)
    for m, entry in by_live.items():
        entry["m"] = m
        entry["average_minimal_W"] = entry["minimal_W_sum"] / entry["restrictions"]
    return {
        "scope": "counterexample to substituting maximum gate fanin for CNF width; NOT to the original lemma",
        "independent_of_parent_script": True, "d": d, "b": b, "p": p, "naive_k": k,
        "naive_theta": th, "naive_geometric_bound": promised,
        "exact_expected_minimal_W": expected_minimum, "closed_form": closed_form,
        "strict_gap": expected_minimum - promised, "ratio_to_naive_bound": expected_minimum / promised,
        "claim_verified": expected_minimum == Fraction(15625, 8192) and expected_minimum > promised,
        "witness": "G=2H-1; dual: all 1-CNF subcubes; primal: satisfying singleton subcubes",
        "fanin2_representation": {"binary_XOR_gates": 5, "unary_NOT_gates": 1,
                                    "truth_table_rows_checked": 64},
        "original_CNF": {"clause_count": len(parity_cnf), "k": d,
                           "theta_at_same_b_p": theta(d, b, p),
                           "geometric_hypothesis_satisfied": theta(d, b, p) < 1},
        "by_live_dimension": list(by_live.values()), "counts": dict(audit.counts - before),
    }


def update_maximum(table: dict, key: tuple, value: Fraction, witness: dict) -> None:
    if key not in table or value > table[key]["ratio"]:
        table[key] = {"ratio": value, **witness}


def run_experiment(*, exhaustive_max_d: int = 4, exhaustive_max_clauses: int = 2,
                   chosen_max_d: int = 6, random_cases: int = 3, seed: int = 112,
                   bs: tuple[int, ...] = (1, 2), ps: tuple[Fraction, ...] = DEFAULT_PS,
                   reverse_checks: str = "chosen", max_formulas: int = 10_000,
                   max_paths: int = 20_000, max_counterexamples: int = 25,
                   include_parity: bool = True, progress_every: int = 0) -> dict:
    if not -1 <= exhaustive_max_d <= 6 or not 0 <= chosen_max_d <= 6:
        raise ValueError("exhaustive max d must be -1..6; chosen max d must be 0..6")
    if exhaustive_max_clauses < 0 or random_cases < 0:
        raise ValueError("clause and random-case budgets must be nonnegative")
    if reverse_checks not in ("all", "chosen", "none"):
        raise ValueError("reverse_checks must be all, chosen, or none")
    if not bs or not ps or len(set(bs)) != len(bs) or len(set(ps)) != len(ps):
        raise ValueError("b and p lists must be nonempty and have no duplicates")
    for b in bs:
        for p in ps:
            theta(0, b, p)
    chosen = chosen_formulas(chosen_max_d, seed, random_cases)
    n_exhaustive = exhaustive_formula_count(exhaustive_max_d, exhaustive_max_clauses)
    if n_exhaustive + len(chosen) > max_formulas:
        raise BudgetExceeded(f"requested {n_exhaustive + len(chosen)} formulas exceeds --max-formulas {max_formulas}")
    audit = Audit(max_counterexamples)
    formula_digest = hashlib.sha256()
    coverage, max_coefficients, max_geometric, max_finite = {}, {}, {}, {}
    detailed, max_witness = [], None
    zero_bound_checks = 0
    formula_count = formula_b_count = 0
    # Do not materialize a potentially large exhaustive formula list.
    from itertools import chain
    for source in chain(exhaustive_formulas(exhaustive_max_d, exhaustive_max_clauses), chosen):
        formula_count += 1
        formula_digest.update((json.dumps(jsonable(source.description()), sort_keys=True,
                                         separators=(",", ":")) + "\n").encode())
        cov_key = (source.suite, source.d, len(source.raw))
        if cov_key not in coverage:
            coverage[cov_key] = {"suite": source.suite, "d": source.d, "raw_clause_count": len(source.raw),
                                 "formulas": 0, "formula_b_pairs": 0, "restrictions": 0, "live_assignments": 0}
        coverage[cov_key]["formulas"] += 1
        for b in bs:
            formula_b_count += 1
            reverse = reverse_checks == "all" or (reverse_checks == "chosen" and source.suite != "exhaustive")
            result = check_formula(source, b, ps, audit=audit, reverse=reverse, max_paths=max_paths)
            coverage[cov_key]["formula_b_pairs"] += 1
            for name in ("restrictions", "live_assignments"):
                coverage[cov_key][name] += result["counts"][name]
            if source.suite != "exhaustive":
                detailed.append(result)
            witness = {"formula": source.description(), "b": b, "k": result["k"]}
            w = result["max_restriction_W"]
            if max_witness is None or w["value"] > max_witness["value"]:
                max_witness = {**w, **witness}
            for entry in result["expectations"]:
                th, p = entry["theta"], entry["p"]
                for j, (value, bound) in enumerate(zip(entry["E_W_j"], entry["coefficient_bounds"])):
                    if not bound:
                        zero_bound_checks += 1
                        continue
                    key = (b, p, result["k"], j)
                    update_maximum(max_coefficients, key, value / bound,
                                   {**witness, "p": p, "j": j, "theta": th, "E_W_j": value, "bound": bound})
                extra = {**witness, "p": p, "theta": th, "E_W": entry["E_W"]}
                update_maximum(max_finite, (b, p, result["k"]), entry["E_W"] / entry["finite_sum_bound"],
                               {**extra, "bound": entry["finite_sum_bound"]})
                if entry["geometric_bound"] is not None:
                    update_maximum(max_geometric, (b, p, result["k"]), entry["E_W"] / entry["geometric_bound"],
                                   {**extra, "bound": entry["geometric_bound"]})
        if progress_every and formula_count % progress_every == 0:
            print(f"checked {formula_count}/{n_exhaustive + len(chosen)} formulas", file=sys.stderr, flush=True)
    original_failures = dict(audit.failures)
    original_counterexamples = list(audit.counterexamples)
    original_counts = dict(audit.counts)
    parity = check_naive_parity_extension(audit) if include_parity else None
    root = Path(__file__).resolve().parents[3]
    manuscript_path = root / MANUSCRIPT
    manuscript_sha256 = hashlib.sha256(manuscript_path.read_bytes()).hexdigest() if manuscript_path.is_file() else None
    nontrivial_ratios = [r for r in max_coefficients.values() if r["j"] > 0]
    return jsonable({
        "schema_version": 1, "experiment": "family112-independent-restriction-finite-checks",
        "status": "passed" if audit.ok else "counterexamples_or_check_failures_found", "complete": True,
        "claim": "Small finite computational checks, NOT a proof of the restriction lemma.",
        "manuscript": {"path": MANUSCRIPT, "sha256": manuscript_sha256},
        "config": {"exhaustive_max_d": exhaustive_max_d, "exhaustive_max_clauses": exhaustive_max_clauses,
                   "chosen_max_d": chosen_max_d, "random_cases_per_dimension": random_cases, "seed": seed,
                   "b": bs, "p": ps, "reverse_checks": reverse_checks, "max_formulas": max_formulas,
                   "max_paths_per_live_set": max_paths, "include_parity": include_parity,
                   "max_counterexamples_stored": max_counterexamples},
        "method": {
            "arithmetic": "fractions.Fraction exclusively; all stored rationals are numerator/denominator strings",
            "literal_convention": "signed 1-based literals; null clause=true; [] clause=false; [] CNF=true",
            "exhaustive_scope": "All canonical clause multisets up to the stated clause-count bound, including false and repeated clauses. Clause order is canonical, but every occurrence retains a separate index. NOT all CNFs.",
            "restriction_scope": "Every one of 3^d restrictions and every live assignment (4^d restriction/point pairs per formula and b). No Monte Carlo expectations.",
            "paths": "All scope-defined indexed paths, including incompatible paths; c_U counts every retained fully prescribed violated clause index, not just selected indices.",
            "pointwise": "Raw literal substitution and evaluation vs signed path expansion; zero numerator means zero fraction; residual identities also checked.",
            "mixtures": "Exact permutation counts grouped by passing prefix subsets; I_h objects retain true/false clauses and repetitions after final substitution. Product of marginals avoids enumerating cross-products.",
            "reweighting": "Independent pointwise c_U counts give conditional and full-assignment expectation identities.",
            "reverse": "Direct finite F_s(R) recurrence, literal V_R counts and factorization; only for the configured formulas. Never used to set W_j or expectations.",
            "geometric_filter": "Compare E W <= 1/(1-theta) only if theta < 1; E W_j <= theta^j and finite-sum bounds checked for all theta.",
            "maximum_ratios": "Separate maxima by (b,p,k,j); zero coefficient bounds counted separately without dividing by zero. Ties keep the first deterministic witness.",
            "limitations": "Bounded dimensions and bounded exhaustive clause multiplicities; seeded formulas only supplement that class. No formal proof and no claim of exhaustive coverage of unbounded CNFs.",
        },
        "formula_count": formula_count, "formula_b_pairs": formula_b_count,
        "exhaustive_formula_count": n_exhaustive, "chosen_and_seeded_formula_count": len(chosen),
        "formula_stream_sha256": formula_digest.hexdigest(),
        "coverage": [coverage[key] for key in sorted(coverage)],
        "original_lemma": {"passed": not original_failures, "counts": original_counts,
                           "failure_counts": original_failures, "counterexamples": original_counterexamples,
                           "zero_coefficient_bound_checks": zero_bound_checks,
                           "max_nontrivial_coefficient_ratio": max(nontrivial_ratios, key=lambda r: r["ratio"], default=None),
                           "max_coefficient_ratios": [max_coefficients[key] for key in sorted(max_coefficients)],
                           "max_finite_sum_ratios": [max_finite[key] for key in sorted(max_finite)],
                           "max_geometric_ratios": [max_geometric[key] for key in sorted(max_geometric)],
                           "max_restriction_W": max_witness},
        "chosen_case_details": detailed, "naive_gate_fanin_extension": parity,
        "all_failure_counts": dict(audit.failures), "all_counterexamples": audit.counterexamples,
        "counterexamples_omitted": max(0, sum(audit.failures.values()) - len(audit.counterexamples)),
    })


def run_self_tests() -> bool:
    # Prevent test discovery/imports from creating extra files in the repository.
    sys.dont_write_bytecode = True
    directory = str(Path(__file__).resolve().parent)
    if directory not in sys.path:
        sys.path.insert(0, directory)
    suite = unittest.defaultTestLoader.discover(directory, pattern="test_restriction_check.py")
    return unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--self-test", action="store_true", help="run self-tests only, without writing results")
    parser.add_argument("--exhaustive-max-d", type=int, default=4, help="-1 disables exhaustive formulas (default: 4)")
    parser.add_argument("--exhaustive-max-clauses", type=int, default=2, help="finite multiset size bound (default: 2)")
    parser.add_argument("--chosen-max-d", type=int, default=6)
    parser.add_argument("--random-cases", type=int, default=3, help="seeded formulas per dimension, not sampled restrictions")
    parser.add_argument("--seed", type=int, default=112)
    parser.add_argument("--b", type=int, nargs="+", default=[1, 2])
    parser.add_argument("--p", type=Fraction, nargs="+", default=list(DEFAULT_PS))
    parser.add_argument("--reverse-checks", choices=("chosen", "all", "none"), default="chosen")
    parser.add_argument("--max-formulas", type=int, default=10_000)
    parser.add_argument("--max-paths", type=int, default=20_000)
    parser.add_argument("--max-counterexamples", type=int, default=25)
    parser.add_argument("--skip-parity", action="store_true")
    parser.add_argument("--progress-every", type=int, default=500)
    parser.add_argument("--output", default=str(Path(__file__).with_name("restriction_results.json")),
                        help="results JSON path, or '-' for stdout")
    args = parser.parse_args(argv)
    if args.self_test:
        return 0 if run_self_tests() else 1
    try:
        result = run_experiment(
            exhaustive_max_d=args.exhaustive_max_d, exhaustive_max_clauses=args.exhaustive_max_clauses,
            chosen_max_d=args.chosen_max_d, random_cases=args.random_cases, seed=args.seed,
            bs=tuple(args.b), ps=tuple(args.p), reverse_checks=args.reverse_checks,
            max_formulas=args.max_formulas, max_paths=args.max_paths,
            max_counterexamples=args.max_counterexamples, include_parity=not args.skip_parity,
            progress_every=args.progress_every,
        )
    except (ValueError, BudgetExceeded) as error:
        parser.error(str(error))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output == "-":
        sys.stdout.write(text)
    else:
        Path(args.output).write_text(text)
        original = result["original_lemma"]
        print(f"{result['status']}: {result['formula_count']} formulas, "
              f"{result['formula_b_pairs']} (formula,b) pairs, "
              f"{original['counts']['restrictions']} restrictions, "
              f"{original['counts']['live_assignments']} pointwise expansions")
        if result["naive_gate_fanin_extension"] is not None:
            parity = result["naive_gate_fanin_extension"]
            print(f"Separate naive-extension parity check: {parity['exact_expected_minimal_W']} > "
                  f"{parity['naive_geometric_bound']}; verified={parity['claim_verified']}")
        print(f"Results: {args.output}\nFinite checks only; not a proof.")
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
