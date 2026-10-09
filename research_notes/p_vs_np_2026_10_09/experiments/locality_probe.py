#!/usr/bin/env python3
"""Exact finite tests for bottom-local predicate expansion and parity obstruction.

This is an independent, standard-library-only experiment. It does not prove
family 112 or any asymptotic complexity-class separation. Bit i of an assignment
integer is coordinate i; bit x of a predicate's truth-table integer is its value
at local assignment x. A clause (variable, forbidden_bit) is satisfied when at
least one of those variables differs from its forbidden bit.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
from math import comb
from pathlib import Path
import random
import unittest

Clause = tuple[tuple[int, int], ...]


def assignments(n: int):
    return range(1 << n)


def bit(x: int, i: int) -> int:
    return (x >> i) & 1


@dataclass(frozen=True)
class LocalGate:
    scope: tuple[int, ...]
    truth_table: int

    def evaluate(self, assignment: int) -> bool:
        local = sum(bit(assignment, variable) << i
                    for i, variable in enumerate(self.scope))
        return bool(bit(self.truth_table, local))

    @property
    def raw_scope(self) -> tuple[int, ...]:
        """Distinct raw variables, in their first-occurrence order."""
        return tuple(dict.fromkeys(self.scope))

    def normalize_scope(self) -> 'LocalGate':
        """Discard unreachable local patterns caused by repeated input wires."""
        distinct = self.raw_scope
        if distinct == self.scope:
            return self
        position = {variable: i for i, variable in enumerate(distinct)}
        table = 0
        for x in assignments(len(distinct)):
            original = sum(bit(x, position[variable]) << i
                           for i, variable in enumerate(self.scope))
            if bit(self.truth_table, original):
                table |= 1 << x
        return LocalGate(distinct, table)

    def as_clauses(self) -> tuple[Clause, ...]:
        # q measures DISTINCT raw variables, not duplicated input-wire positions.
        normalized = self.normalize_scope()
        return tuple(
            tuple((variable, bit(local, i))
                  for i, variable in enumerate(normalized.scope))
            for local in assignments(len(normalized.scope))
            if not bit(normalized.truth_table, local)
        )


def clause_value(clause: Clause, assignment: int) -> bool:
    return any(bit(assignment, variable) != forbidden
               for variable, forbidden in clause)


def cnf_value(clauses: tuple[Clause, ...], assignment: int) -> bool:
    return all(clause_value(clause, assignment) for clause in clauses)


@dataclass(frozen=True)
class BottomLocalCircuit:
    """An OR of AND gates reading a shared pool of raw-input local predicates."""
    gates: tuple[LocalGate, ...]
    middle: tuple[tuple[int, ...], ...]
    top: tuple[int, ...]

    @property
    def gate_count(self) -> int:
        return len(self.gates) + len(self.middle) + 1

    @property
    def max_arity(self) -> int:
        return max((len(g.raw_scope) for g in self.gates), default=0)

    def evaluate(self, assignment: int) -> bool:
        values = [gate.evaluate(assignment) for gate in self.gates]
        return any(all(values[i] for i in self.middle[j]) for j in self.top)

    def compile(self) -> 'ClauseCircuit':
        clauses: list[Clause] = []
        ranges: list[tuple[int, ...]] = []
        for gate in self.gates:
            expanded = gate.as_clauses()
            ranges.append(tuple(range(len(clauses), len(clauses) + len(expanded))))
            clauses.extend(expanded)
        middle = tuple(tuple(i for gate in group for i in ranges[gate])
                       for group in self.middle)
        return ClauseCircuit(tuple(clauses), middle, self.top)


@dataclass(frozen=True)
class ClauseCircuit:
    clauses: tuple[Clause, ...]
    middle: tuple[tuple[int, ...], ...]
    top: tuple[int, ...]

    @property
    def gate_count(self) -> int:
        return len(self.clauses) + len(self.middle) + 1

    def evaluate(self, assignment: int) -> bool:
        values = [clause_value(c, assignment) for c in self.clauses]
        return any(all(values[i] for i in self.middle[j]) for j in self.top)


def exact_predicate_checks(max_arity: int = 3) -> dict:
    cases = 0
    input_checks = 0
    empty_true = empty_false = 0
    for k in range(max_arity + 1):
        for table in range(1 << (1 << k)):
            gate = LocalGate(tuple(range(k)), table)
            clauses = gate.as_clauses()
            assert len(clauses) <= 1 << k
            assert all(len(c) == k for c in clauses)
            for x in assignments(k):
                assert gate.evaluate(x) == cnf_value(clauses, x)
                input_checks += 1
            cases += 1
            if k == 0:
                empty_true += int(gate.evaluate(0))
                empty_false += int(not gate.evaluate(0))
    return dict(max_arity=max_arity, predicates_exhaustively_checked=cases,
                assignment_equivalences=input_checks,
                empty_scope_true_cases=empty_true, empty_scope_false_cases=empty_false)


def exact_circuit_checks(seed: int = 112, random_cases: int = 300) -> dict:
    rng = random.Random(seed)
    n = 4
    cases = [
        BottomLocalCircuit((), (), ()),
        BottomLocalCircuit((), ((),), (0,)),
        BottomLocalCircuit((LocalGate((), 0),), ((0,),), (0,)),
        BottomLocalCircuit((LocalGate((), 1),), ((0,),), (0,)),
        # Shared parity predicate, duplicated wires, and an overlapping predicate.
        BottomLocalCircuit((LocalGate((0, 1), 0b0110),
                            LocalGate((1, 2), 0b1000)),
                           ((0, 1), (0,), (1, 0, 0)), (0, 1, 2)),
        # Repeated wires are normalized first; q still counts distinct raw variables.
        BottomLocalCircuit((LocalGate((0, 0), 0b0110),), ((0,),), (0,)),
    ]
    for _ in range(random_cases):
        count = rng.randrange(0, 7)
        gates = []
        for _ in range(count):
            arity = rng.randrange(0, 4)
            scope = tuple(rng.sample(range(n), arity))
            gates.append(LocalGate(scope, rng.randrange(1 << (1 << arity))))
        groups = tuple(tuple(rng.randrange(count) for _ in range(rng.randrange(5)))
                       if count else () for _ in range(rng.randrange(0, 6)))
        top = tuple(j for j in range(len(groups)) if rng.randrange(2))
        cases.append(BottomLocalCircuit(tuple(gates), groups, top))
    worst_ratio = Fraction(0)
    for circuit in cases:
        compiled = circuit.compile()
        bound = circuit.gate_count * (1 << circuit.max_arity)
        assert compiled.gate_count <= bound
        worst_ratio = max(worst_ratio, Fraction(compiled.gate_count, bound))
        for x in assignments(n):
            assert compiled.evaluate(x) == circuit.evaluate(x)
    return dict(seed=seed, circuits_checked=len(cases), variables=n,
                assignment_equivalences=len(cases) * (1 << n),
                worst_compiled_size_over_bound=str(worst_ratio),
                bound='compiled_gate_count <= original_gate_count * 2**max_distinct_raw_arity',
                arity_convention='distinct raw variables; repeated input wires normalized first',
                model='OR-AND-shared-bottom-predicates; bottom predicates read raw inputs')


@lru_cache(maxsize=None)
def parity_subcube_correlations(m: int) -> tuple[Fraction, int]:
    """Enumerate all consistent width-one CNFs, i.e. subcubes.

    The false CNF contributes correlation zero and need not be enumerated.
    Return the maximum absolute correlation of parity sign with a subcube.
    """
    maximum = Fraction(0)
    count = 0
    for pattern in product((-1, 0, 1), repeat=m):
        signed_sum = sum(
            (-1 if x.bit_count() % 2 else 1)
            for x in assignments(m)
            if all(value == -1 or bit(x, i) == value for i, value in enumerate(pattern))
        )
        maximum = max(maximum, abs(Fraction(signed_sum, 1 << m)))
        count += 1
    return maximum, count


def parity_restriction_table(d: int, restriction: tuple[int, ...]) -> tuple[bool, ...]:
    live = [i for i, value in enumerate(restriction) if value == -1]
    fixed_ones = sum(value == 1 for value in restriction)
    return tuple((fixed_ones + z.bit_count()) % 2 == 0
                 for z in assignments(len(live)))


def parity_atomic_norm_from_primal_dual(table: tuple[bool, ...]) -> Fraction:
    """Certify the norm by matching explicit primal and dual bounds.

    Primal: sum of accepted singleton indicators, each a width-one CNF.
    Dual: parity sign divided by its largest subcube correlation. Only used
    on parity restrictions, not as a general-purpose atomic norm solver.
    """
    m = (len(table) - 1).bit_length()
    assert len(table) == 1 << m
    upper = Fraction(sum(table))
    correlation, _ = parity_subcube_correlations(m)
    inner = Fraction(sum((-1 if x.bit_count() % 2 else 1) * table[x]
                         for x in assignments(m)), 1 << m)
    lower = abs(inner) / correlation
    assert lower == upper, (m, table, lower, upper)
    return upper


def exact_parity_checks(max_dimension: int = 8) -> dict:
    rows = []
    restriction_cases = 0
    for d in range(1, max_dimension + 1):
        # Group by live-coordinate count while calculating all restricted tables.
        totals = [Fraction(0) for _ in range(d + 1)]
        counts = [0 for _ in range(d + 1)]
        for restriction in product((-1, 0, 1), repeat=d):
            m = restriction.count(-1)
            table = parity_restriction_table(d, restriction)
            norm = parity_atomic_norm_from_primal_dual(table)
            totals[m] += norm
            counts[m] += 1
            restriction_cases += 1
        for m in range(d + 1):
            assert counts[m] == comb(d, m) * (1 << (d - m))
        for p in (Fraction(1, 8), Fraction(1, 4), Fraction(1, 2)):
            expectation = sum(totals[m] * p**m * ((1-p)/2)**(d-m)
                              for m in range(d + 1))
            formula = (1+p)**d / 2
            assert expectation == formula
            rows.append(dict(d=d, p=str(p), expected_minimum_mass=str(expectation),
                             predicted_mass=str(formula)))
    return dict(max_dimension=max_dimension, restriction_cases=restriction_cases,
                subcubes_checked=sum(parity_subcube_correlations(m)[1]
                                     for m in range(max_dimension + 1)),
                expectation_identity='E[minimal signed width-1 CNF mass] = (1+p)**d / 2, d>=1',
                rows=rows,
                scope='Obstructs the naive maximum-internal-gate-fan-in substitution, NOT the original lemma')


def fanin_two_counterexample() -> dict:
    """Disprove replacing CNF width by maximum internal gate fan-in.

    The gate list is a DAG over the ordinary AND/OR/NOT basis; XOR is expanded
    into four gates, so no oracle or nonstandard primitive is required.
    """
    d = 6
    gates: list[tuple[str, tuple[int, ...]]] = []

    def append_gate(op: str, inputs: tuple[int, ...]) -> int:
        index = d + len(gates)
        assert all(i < index for i in inputs)
        gates.append((op, inputs))
        return index

    wires = list(range(d))
    while len(wires) > 1:
        next_wires = []
        for i in range(0, len(wires) - 1, 2):
            a, b = wires[i:i+2]
            either = append_gate('OR', (a, b))
            both = append_gate('AND', (a, b))
            not_both = append_gate('NOT', (both,))
            next_wires.append(append_gate('AND', (either, not_both)))
        if len(wires) % 2:
            next_wires.append(wires[-1])
        wires = next_wires
    output = append_gate('NOT', (wires[0],))
    depths = [0] * d
    for op, inputs in gates:
        depths.append(1 + max(depths[i] for i in inputs))
    for x in assignments(d):
        values = [bool(bit(x, i)) for i in range(d)]
        for op, inputs in gates:
            args = [values[i] for i in inputs]
            value = (all(args) if op == 'AND' else
                     any(args) if op == 'OR' else not args[0])
            values.append(value)
        assert values[output] == (x.bit_count() % 2 == 0)
    p = Fraction(1, 4)
    k, b = 2, 1
    theta = sum(Fraction(comb(k, ell)) * (2*p/(1-p))**ell
                for ell in range(b+1, k+1))
    predicted_bound = 1 / (1-theta)
    certified_mass = Fraction(0)
    for restriction in product((-1, 0, 1), repeat=d):
        m = restriction.count(-1)
        norm = parity_atomic_norm_from_primal_dual(parity_restriction_table(d, restriction))
        certified_mass += p**m * ((1-p)/2)**(d-m) * norm
    assert theta == Fraction(4, 9)
    assert predicted_bound == Fraction(9, 5)
    assert certified_mass == Fraction(15625, 8192)
    assert certified_mass > predicted_bound
    return dict(
        status='REFUTED: naive maximum-gate-fan-in generalization',
        not_refuted='Original width-k CNF restriction lemma',
        function='even parity of six raw input bits', variables=d,
        gate_basis=['AND', 'OR', 'NOT'], gate_count=len(gates),
        maximum_gate_fanin=max(len(inputs) for _, inputs in gates),
        circuit_depth=depths[output], circuit_assignments_checked=1 << d,
        restrictions_checked=3**d, b=b, p=str(p), incorrectly_substituted_k=k,
        theta=str(theta), proposed_expected_mass_bound=str(predicted_bound),
        certified_expected_minimum_mass=str(certified_mass),
        strict_violation=str(certified_mass-predicted_bound),
        reason='Small gate fan-in does not bound a composed gate output raw-input scope.',
    )


class ProbeTests(unittest.TestCase):
    def test_constant_gates(self):
        self.assertEqual(LocalGate((), 1).as_clauses(), ())
        self.assertEqual(LocalGate((), 0).as_clauses(), ((),))

    def test_all_small_predicates(self):
        self.assertEqual(exact_predicate_checks()['predicates_exhaustively_checked'], 278)

    def test_shared_circuit_compilation(self):
        self.assertEqual(exact_circuit_checks(random_cases=30)['circuits_checked'], 36)

    def test_repeated_scope_uses_distinct_raw_arity(self):
        # Peer-review regression: this gate is x_0, not a three-variable function.
        gate = LocalGate((0, 0, 0), 1 << 7)
        circuit = BottomLocalCircuit((gate,), ((0,),), (0,))
        self.assertEqual(gate.normalize_scope(), LocalGate((0,), 0b10))
        self.assertEqual(circuit.max_arity, 1)
        self.assertEqual(circuit.compile().gate_count, 3)
        self.assertLessEqual(circuit.compile().gate_count, circuit.gate_count * 2)
        for x in assignments(1):
            self.assertEqual(circuit.compile().evaluate(x), circuit.evaluate(x))

    def test_scope_normalization_preserves_predicates(self):
        for scope in ((0, 0), (1, 0, 1), (2, 2, 0)):
            for table in range(1 << (1 << len(scope))):
                gate = LocalGate(scope, table)
                normalized = gate.normalize_scope()
                clauses = gate.as_clauses()
                self.assertLessEqual(len(clauses), 1 << len(gate.raw_scope))
                for x in assignments(3):
                    self.assertEqual(gate.evaluate(x), normalized.evaluate(x))
                    self.assertEqual(gate.evaluate(x), cnf_value(clauses, x))

    def test_parity_dual(self):
        for m in range(1, 6):
            self.assertEqual(parity_subcube_correlations(m)[0], Fraction(1, 1 << m))

    def test_internal_fanin_counterexample(self):
        row = fanin_two_counterexample()
        self.assertEqual(row['gate_count'], 21)
        self.assertEqual(row['maximum_gate_fanin'], 2)
        self.assertEqual(row['proposed_expected_mass_bound'], '9/5')
        self.assertEqual(row['certified_expected_minimum_mass'], '15625/8192')

    def test_parity_expected_mass(self):
        rows = exact_parity_checks(4)['rows']
        row = next(row for row in rows if row['d'] == 4 and row['p'] == '1/2')
        self.assertEqual(row['expected_minimum_mass'], '81/32')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--max-parity-dimension', type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.max_parity_dimension <= 10:
        parser.error('dimension must be in 1..10 to keep exhaustive runs bounded')
    report = dict(
        arithmetic='exact fractions.Fraction; no floating point optimization',
        predicate_compilation=exact_predicate_checks(),
        circuit_compilation=exact_circuit_checks(),
        parity_obstruction=exact_parity_checks(args.max_parity_dimension),
        internal_fanin_counterexample=fanin_two_counterexample(),
        interpretation='Finite validation of stated constructions and identities, not a P-vs-NP proof',
    )
    rendered = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
