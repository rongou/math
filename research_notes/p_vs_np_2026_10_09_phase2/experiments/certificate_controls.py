#!/usr/bin/env python3
"""Exact controls for promise certificates and truth-table patching.

Models are explicit: AND/OR gates have two inputs; NOT has one; every gate is
counted; primary inputs and constant 0/1 wires are free. Inner inputs encode an
m-variable function; outer inputs are its N=2**m truth-table bits. No SAT solver,
formula-only dynamic program, or unproved minimum-size assumption is used here.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import random
import unittest


@dataclass(frozen=True)
class Gate:
    op: str
    inputs: tuple[int, ...]


@dataclass(frozen=True)
class Circuit:
    inputs: int
    gates: tuple[Gate, ...]
    output: int

    @property
    def size(self) -> int:
        return len(self.gates)

    def evaluate(self, x: int) -> bool:
        values = [bool((x >> i) & 1) for i in range(self.inputs)] + [False, True]
        for gate in self.gates:
            if gate.op == 'NOT':
                assert len(gate.inputs) == 1
                values.append(not values[gate.inputs[0]])
            elif gate.op == 'AND':
                assert len(gate.inputs) == 2
                values.append(values[gate.inputs[0]] and values[gate.inputs[1]])
            elif gate.op == 'OR':
                assert len(gate.inputs) == 2
                values.append(values[gate.inputs[0]] or values[gate.inputs[1]])
            else:
                raise ValueError(gate.op)
        return values[self.output]

    def truth_table(self) -> int:
        return sum(int(self.evaluate(x)) << x for x in range(1 << self.inputs))

    def validate(self) -> None:
        for j, gate in enumerate(self.gates):
            assert all(0 <= i < self.inputs + 2 + j for i in gate.inputs)
            assert gate.op in ('AND', 'OR', 'NOT')
            assert len(gate.inputs) == (1 if gate.op == 'NOT' else 2)
        assert 0 <= self.output < self.inputs + 2 + self.size


class Builder:
    def __init__(self, inputs: int, gates=()):
        self.inputs = inputs
        self.gates = list(gates)

    def gate(self, op: str, *inputs: int) -> int:
        index = self.inputs + 2 + len(self.gates)
        if op not in ('AND', 'OR', 'NOT') or len(inputs) != (1 if op == 'NOT' else 2):
            raise ValueError((op, inputs))
        if any(i < 0 or i >= index for i in inputs):
            raise ValueError('not a topologically ordered circuit')
        self.gates.append(Gate(op, tuple(inputs)))
        return index

    def fold(self, op: str, wires: list[int]) -> int:
        if not wires:
            return self.inputs + (1 if op == 'AND' else 0)
        result = wires[0]
        for wire in wires[1:]:
            result = self.gate(op, result, wire)
        return result

    def finish(self, output: int) -> Circuit:
        circuit = Circuit(self.inputs, tuple(self.gates), output)
        circuit.validate()
        return circuit


def zero_gate_tables(m: int) -> tuple[int, ...]:
    """The COMPLETE size-zero inner circuit class in the declared model."""
    if m < 0:
        raise ValueError('m must be nonnegative')
    n = 1 << m
    projections = tuple(sum(((address >> i) & 1) << address for address in range(n))
                        for i in range(m))
    return (0, (1 << n) - 1) + projections


def membership_classifier(m: int) -> Circuit:
    """Outer DNF recognizing exactly zero-gate inner truth tables."""
    n = 1 << m
    builder = Builder(n)
    negations = [builder.gate('NOT', i) for i in range(n)]
    equalities = []
    for table in zero_gate_tables(m):
        literals = [i if (table >> i) & 1 else negations[i] for i in range(n)]
        equalities.append(builder.fold('AND', literals))
    return builder.finish(builder.fold('OR', equalities))


def zero_gate_control(max_m: int = 6, exhaustive_outer_m: int = 3) -> dict:
    rows = []
    for m in range(2, max_m + 1):
        n = 1 << m
        accepted = zero_gate_tables(m)
        assert len(set(accepted)) == m + 2
        distance = min((a ^ b).bit_count() for j, a in enumerate(accepted)
                       for b in accepted[j+1:])
        assert distance == n // 2 and distance >= 2
        circuit = membership_classifier(m)
        assert circuit.size == (m + 3) * n - 1
        point_checks = 0
        for table in accepted:
            assert circuit.evaluate(table)
            point_checks += 1
            for i in range(n):
                neighbor = table ^ (1 << i)
                assert neighbor not in accepted
                assert not circuit.evaluate(neighbor)
                point_checks += 1
        exhaustive_checks = 0
        if m <= exhaustive_outer_m:
            for table in range(1 << n):
                assert circuit.evaluate(table) == (table in accepted)
                exhaustive_checks += 1
        certificate_masks_checked = 0
        if m <= 3:
            # EVERY proper coordinate-fixing certificate at EVERY YES point:
            # a missing coordinate gives a rejected one-bit neighbor agreeing
            # with all fixed bits. This checks a witness, not a guessed minimum.
            all_coordinates = (1 << n) - 1
            for table in accepted:
                for fixed in range(all_coordinates):
                    missing = all_coordinates ^ fixed
                    i_bit = missing & -missing
                    neighbor = table ^ i_bit
                    assert ((neighbor ^ table) & fixed) == 0
                    assert neighbor not in accepted
                    certificate_masks_checked += 1
        rows.append(dict(m=m, truth_table_length=n, YES_count=len(accepted),
                         gate_count=circuit.size, formula_literal_leaves=(m+2)*n,
                         minimum_pairwise_hamming_distance=distance,
                         exact_accepting_certificate_size=n,
                         local_neighbor_and_acceptance_checks=point_checks,
                         exhaustive_outer_truth_table_checks=exhaustive_checks,
                         all_proper_certificate_masks_checked=certificate_masks_checked))
    return dict(
        claim='Exact MCSP[0,0] has O(N log N) classifiers but full N-bit YES certificates.',
        model='AND2/OR2/NOT; gates counted, constants/input wires free, NOT not free',
        NO_endpoint='inner circuit size > 0',
        scope='Negative control ONLY; constant thresholds are not the fixed-beta OPS regime.',
        general_reason='Distinct accepted tables have Hamming distance >=N/2>=2, so every unfixed coordinate has a rejected one-bit neighbor.',
        rows=rows)


def patch_truth_table(base: Circuit, changed_addresses: tuple[int, ...]) -> Circuit:
    """Flip specified entries using shared input negations, minterms, and XOR.

    For t>=1 distinct addresses, added gates = m + t*m + 3. This is a
    CONSTRUCTIVE UPPER BOUND, never a minimum-size claim.
    """
    m = base.inputs
    if m < 1:
        raise ValueError('patch bound is stated for m>=1')
    changes = tuple(sorted(set(changed_addresses)))
    if any(a < 0 or a >= 1 << m for a in changes):
        raise ValueError('address outside the inner input cube')
    if not changes:
        return base
    builder = Builder(m, base.gates)
    negations = [builder.gate('NOT', i) for i in range(m)]
    terms = []
    for address in changes:
        literals = [i if (address >> i) & 1 else negations[i] for i in range(m)]
        terms.append(builder.fold('AND', literals))
    patch = builder.fold('OR', terms)
    either = builder.gate('OR', base.output, patch)
    both = builder.gate('AND', base.output, patch)
    not_both = builder.gate('NOT', both)
    return builder.finish(builder.gate('AND', either, not_both))


def patching_checks(seed: int = 11202, random_cases: int = 120) -> dict:
    rng = random.Random(seed)
    checks = 0
    cases = 0
    max_added = 0
    for _ in range(random_cases):
        m = rng.randrange(1, 6)
        builder = Builder(m)
        for _ in range(rng.randrange(0, 9)):
            op = rng.choice(('AND', 'OR', 'NOT'))
            available = m + 2 + len(builder.gates)
            ins = [rng.randrange(available) for _ in range(1 if op == 'NOT' else 2)]
            builder.gate(op, *ins)
        base = builder.finish(rng.randrange(m+2+len(builder.gates)))
        changes = tuple(rng.sample(range(1 << m), rng.randrange(min(5, 1 << m)+1)))
        patched = patch_truth_table(base, changes)
        bound = 0 if not changes else m + len(changes)*m + 3
        assert patched.size-base.size == bound
        mask = sum(1 << address for address in changes)
        assert patched.truth_table() == base.truth_table() ^ mask
        checks += 1 << m
        cases += 1
        max_added = max(max_added, bound)
    # A whole freely varying truth-table subcube, not just individual patches.
    subcube_cases = 0
    m = 3
    base = Circuit(m, (), 0)  # a projection, cost zero
    free_addresses = (0, 2, 5, 7)
    for subset in range(1 << len(free_addresses)):
        changes = tuple(a for j, a in enumerate(free_addresses) if subset >> j & 1)
        patched = patch_truth_table(base, changes)
        assert patched.size <= base.size + m + len(free_addresses)*m + 3
        for address in range(1 << m):
            assert patched.evaluate(address) == (base.evaluate(address) ^ (address in changes))
        subcube_cases += 1
    return dict(
        seed=seed, random_inner_circuits=cases, assignment_checks=checks,
        maximum_added_gates=max_added, full_patch_subcube_completions=subcube_cases,
        upper_bound_for_t_positive='Size(patched) <= Size(base) + m + t*m + 3',
        zero_patch_cost='0 additional gates',
        scope='Explicit AND/OR/NOT construction; no assertion of minimum size.',
        mathematical_consequence='If base size s0 and s0+m+r*m+3 <= s1, every completion of any r selected table coordinates is YES, so every correct separator accepts that subcube.')


class ControlTests(unittest.TestCase):
    def test_complete_zero_gate_table_class(self):
        self.assertEqual(set(zero_gate_tables(2)), {0, 15, 10, 12})
        self.assertEqual(set(zero_gate_tables(3)), {0, 255, 170, 204, 240})

    def test_negative_control(self):
        rows = zero_gate_control(3)['rows']
        self.assertEqual(rows[0]['gate_count'], 19)
        self.assertEqual(rows[1]['gate_count'], 47)
        self.assertEqual(rows[1]['exact_accepting_certificate_size'], 8)
        self.assertEqual(rows[1]['all_proper_certificate_masks_checked'], 5*255)

    def test_patch_semantics_and_gate_count(self):
        out = patching_checks(random_cases=25)
        self.assertEqual(out['random_inner_circuits'], 25)
        self.assertEqual(out['full_patch_subcube_completions'], 16)

    def test_patch_empty_duplicate_and_invalid_addresses(self):
        base = Circuit(2, (), 0)
        self.assertIs(patch_truth_table(base, ()), base)
        one = patch_truth_table(base, (2,))
        repeated = patch_truth_table(base, (2, 2))
        self.assertEqual(one, repeated)
        self.assertEqual(one.size, 7)
        with self.assertRaises(ValueError):
            patch_truth_table(base, (4,))
        with self.assertRaises(ValueError):
            patch_truth_table(Circuit(0, (), 0), (0,))

    def test_zero_gate_endpoint(self):
        # Negated projections need one NOT gate, so they are NO at upper=0.
        m = 3
        mask = (1 << (1 << m)) - 1
        low = set(zero_gate_tables(m))
        for projection in zero_gate_tables(m)[2:]:
            self.assertNotIn(mask ^ projection, low)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    out = dict(zero_gate_promise=zero_gate_control(), truth_table_patching=patching_checks(),
               claim='Finite constructive checks and negative controls, not a P-versus-NP separation.')
    text = json.dumps(out, indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
