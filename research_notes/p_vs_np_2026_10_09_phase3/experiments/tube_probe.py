#!/usr/bin/env python3
"""Exact shared-circuit controls for a STRICT SUBSET of the GapMCSP YES set.

No function here solves full GapMCSP. A center is a k-junta, optionally XORed
with full address parity. The recognizer accepts exactly truth tables within
an integer Hamming radius of these centers. It enumerates coordinate supports,
NOT center truth tables, and builds ordinary AND2/OR2/NOT gates.

The Phase 2 gate interpreter and truth-table patcher are imported read-only.
All claimed asymptotics are proved separately in README; bounded replay cannot
prove them. Enumeration and materialization have explicit resource limits.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
import json
from math import comb
from pathlib import Path
import random
import sys

PHASE2 = Path(__file__).resolve().parents[2] / 'p_vs_np_2026_10_09_phase2' / 'experiments'
if str(PHASE2) not in sys.path:
    sys.path.insert(0, str(PHASE2))
from certificate_controls import Builder, Circuit, patch_truth_table  # noqa: E402


class BudgetExceeded(ValueError):
    pass


def parameters(m: int, k: int, radius: int) -> None:
    if any(type(x) is not int for x in (m, k, radius)):
        raise ValueError('parameters must be integers, not booleans')
    if not 1 <= m <= 4096 or not 0 <= k <= m or not 0 <= radius <= (1 << m):
        raise ValueError('require 1 <= m <= 4096, 0 <= k <= m, 0 <= radius <= 2**m')


def supports(m: int, k: int):
    return combinations(range(m), k)


def blocks(m: int, support: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    parameters(m, len(support), 0)
    if m > 16:
        raise BudgetExceeded('block materialization supports m <= 16')
    if tuple(sorted(set(support))) != support or any(not 0 <= i < m for i in support):
        raise ValueError('support must have sorted distinct inner coordinates')
    groups = [[] for _ in range(1 << len(support))]
    for address in range(1 << m):
        label = sum(((address >> i) & 1) << j for j, i in enumerate(support))
        groups[label].append(address)
    return tuple(tuple(group) for group in groups)


def address_parity(m: int) -> int:
    if not 1 <= m <= 16:
        raise BudgetExceeded('parity table materialization supports 1 <= m <= 16')
    return sum((address.bit_count() & 1) << address for address in range(1 << m))


def validate_table(m: int, table: int) -> None:
    if type(table) is not int or table < 0 or table.bit_length() > (1 << m):
        raise ValueError('truth table outside the declared cube')


def distance_to_support(m: int, table: int, support: tuple[int, ...]) -> int:
    validate_table(m, table)
    return sum(min(ones := sum((table >> a) & 1 for a in group), len(group) - ones)
               for group in blocks(m, support))


def distance_to_family(m: int, k: int, table: int, shifted: bool = True) -> int:
    parameters(m, k, 0)
    if m > 12 or comb(m, k) > 10000:
        raise BudgetExceeded('semantic support enumeration too large')
    validate_table(m, table)
    shifts = (0, address_parity(m)) if shifted else (0,)
    return min(distance_to_support(m, table ^ shift, support)
               for shift in shifts for support in supports(m, k))


def center_tables(m: int, k: int, shifted: bool = True,
                  budget: int = 100_000) -> tuple[int, ...]:
    parameters(m, k, 0)
    if m > 12 or k > 4:
        raise BudgetExceeded('explicit centers support m <= 12 and k <= 4')
    estimated = (2 if shifted else 1) * comb(m, k) * (1 << (1 << k))
    if estimated > budget:
        raise BudgetExceeded(f'{estimated} center descriptions exceed budget {budget}')
    result = set()
    shifts = (0, address_parity(m)) if shifted else (0,)
    for support in supports(m, k):
        block_masks = tuple(sum(1 << a for a in group) for group in blocks(m, support))
        for small_table in range(1 << (1 << k)):
            value = 0
            for i, mask in enumerate(block_masks):
                if (small_table >> i) & 1:
                    value |= mask
            result.update(value ^ shift for shift in shifts)
    return tuple(sorted(result))


def xor_gate(builder: Builder, a: int, b: int) -> int:
    either = builder.gate('OR', a, b)
    both = builder.gate('AND', a, b)
    not_both = builder.gate('NOT', both)
    return builder.gate('AND', either, not_both)


def popcount(builder: Builder, wires: tuple[int, ...]) -> tuple[int, ...]:
    """Little-endian ripple increments; exactly len(wires)*(5*w-1) gates."""
    width = max(1, len(wires).bit_length())
    count = [builder.inputs] * width  # free constant zero
    for wire in wires:
        carry = wire
        updated = []
        for bit, old in enumerate(count):
            updated.append(xor_gate(builder, old, carry))
            if bit + 1 < width:
                carry = builder.gate('AND', old, carry)
        count = updated
    return tuple(count)


def leq_constant(builder: Builder, bits: tuple[int, ...], limit: int) -> int:
    """Unsigned comparison; exactly 2*width gates for an in-range limit."""
    if type(limit) is not int or not bits:
        raise ValueError('nonempty bit vector and integer threshold required')
    if limit < 0:
        return builder.inputs
    if limit >= (1 << len(bits)):
        return builder.inputs + 1
    result = builder.inputs + 1
    for i, wire in enumerate(bits):
        not_wire = builder.gate('NOT', wire)
        result = builder.gate('OR' if ((limit >> i) & 1) else 'AND', not_wire, result)
    return result


def size_estimate(m: int, k: int, radius: int, shifted: bool = True) -> dict:
    parameters(m, k, radius)
    n, block_count, block_size = 1 << m, 1 << k, 1 << (m - k)
    local_width, total_width = block_size.bit_length(), n.bit_length()
    detectors = (2 if shifted else 1) * comb(m, k)
    per_detector = (n * (5 * local_width - 1) + block_count * (2 * local_width + 1)
                    + 4 * n + n * (5 * total_width - 1) + 2 * total_width)
    size = (n // 2 if shifted else 0) + detectors * per_detector + detectors - 1
    return {'N': n, 'blocks_per_detector': block_count, 'block_size': block_size,
            'local_width': local_width, 'total_width': total_width,
            'detectors': detectors, 'per_detector': per_detector, 'gates': size,
            'majority_surplus_lower_bound': detectors * (2 * n - block_count),
            'simple_size_upper_bound': 50 * comb(m, k) * n * (m + 1)}


@dataclass(frozen=True)
class Recognizer:
    circuit: Circuit
    majority_wires: tuple[int, ...]
    estimate: dict


def build_recognizer(m: int, k: int, radius: int, shifted: bool = True,
                     max_gates: int = 2_000_000) -> Recognizer:
    estimate = size_estimate(m, k, radius, shifted)
    if m > 12 or estimate['gates'] > max_gates:
        raise BudgetExceeded('recognizer exceeds gate/materialization budget')
    n = 1 << m
    builder = Builder(n)
    original = tuple(range(n))
    transformed = [original]
    if shifted:
        transformed.append(tuple(builder.gate('NOT', i) if i.bit_count() & 1 else i
                                 for i in range(n)))
    outputs, majority_wires = [], []
    for wires in transformed:
        for support in supports(m, k):
            errors = []
            for group in blocks(m, support):
                count = popcount(builder, tuple(wires[a] for a in group))
                majority = builder.gate('NOT', leq_constant(builder, count, len(group) // 2))
                majority_wires.append(majority)
                errors.extend(xor_gate(builder, wires[a], majority) for a in group)
            outputs.append(leq_constant(builder, popcount(builder, tuple(errors)), radius))
    circuit = builder.finish(builder.fold('OR', outputs))
    if circuit.size != estimate['gates']:
        raise AssertionError(('gate count mismatch', circuit.size, estimate))
    return Recognizer(circuit, tuple(majority_wires), estimate)


def evaluate_packed(circuit: Circuit, max_inputs: int = 16) -> int:
    """Independent all-input interpreter using bit-vector Boolean operations."""
    if not 0 <= circuit.inputs <= min(max_inputs, 16):
        raise BudgetExceeded('all-input interpreter budget exceeded')
    assignments = 1 << circuit.inputs
    mask = (1 << assignments) - 1
    values = [sum(((x >> i) & 1) << x for x in range(assignments))
              for i in range(circuit.inputs)] + [0, mask]
    for position, gate in enumerate(circuit.gates):
        available = circuit.inputs + 2 + position
        if any(type(i) is not int or not 0 <= i < available for i in gate.inputs):
            raise ValueError('invalid forward wire')
        if gate.op == 'NOT' and len(gate.inputs) == 1:
            values.append(values[gate.inputs[0]] ^ mask)
        elif gate.op in ('AND', 'OR') and len(gate.inputs) == 2:
            a, b = (values[i] for i in gate.inputs)
            values.append(a & b if gate.op == 'AND' else a | b)
        else:
            raise ValueError('invalid gate')
    if not 0 <= circuit.output < len(values):
        raise ValueError('invalid output')
    return values[circuit.output]


def sharing_measurements(recognizer: Recognizer) -> dict:
    circuit = recognizer.circuit
    first_gate = circuit.inputs + 2
    reachable = set()
    todo = [circuit.output]
    while todo:
        wire = todo.pop()
        if wire in reachable:
            continue
        reachable.add(wire)
        if wire >= first_gate:
            todo.extend(circuit.gates[wire - first_gate].inputs)
    fanout = Counter(wire for node in reachable if node >= first_gate
                     for wire in circuit.gates[node - first_gate].inputs)
    majorities = recognizer.majority_wires
    return {'reachable_gates': sum(i >= first_gate for i in reachable),
            'reuse_surplus': sum(max(0, fanout[i] - 1) for i in reachable if i >= first_gate),
            'majority_nodes': len(majorities),
            'all_majorities_reachable': all(i in reachable for i in majorities),
            'majority_fanouts': dict(sorted(Counter(fanout[i] for i in majorities).items())),
            'majority_surplus': sum(max(0, fanout[i] - 1) for i in majorities)}


def inner_center(m: int, support: tuple[int, ...], small_table: int,
                 shifted: bool = False) -> Circuit:
    k = len(support)
    parameters(m, k, 0)
    if k > 12 or m > 64:
        raise BudgetExceeded('inner DNF construction budget exceeded')
    if tuple(sorted(set(support))) != support or any(not 0 <= i < m for i in support):
        raise ValueError('invalid support')
    if type(small_table) is not int or small_table < 0 or small_table.bit_length() > (1 << k):
        raise ValueError('invalid inner table')
    builder = Builder(m)
    negated = {i: builder.gate('NOT', i) for i in support}
    terms = []
    for value in range(1 << k):
        if (small_table >> value) & 1:
            terms.append(builder.fold('AND', [i if (value >> j) & 1 else negated[i]
                                               for j, i in enumerate(support)]))
    result = builder.fold('OR', terms)
    if shifted:
        parity = 0
        for i in range(1, m):
            parity = xor_gate(builder, parity, i)
        result = xor_gate(builder, result, parity)
    return builder.finish(result)


def center_size_bound(m: int, k: int) -> int:
    parameters(m, k, 0)
    return k + k * (1 << k) + 4 * m


def coarse_separation(m: int, k: int, shifted: bool = True) -> int | None:
    parameters(m, k, 0)
    if shifted and 2 * k >= m:
        return None
    exponent = max(1, 2 * k) if shifted else min(m, 2 * k)
    return 1 << (m - exponent)


def minimum_distance(centers: tuple[int, ...]) -> int | None:
    if len(centers) < 2:
        return None
    if len(centers) > 2000:
        raise BudgetExceeded('quadratic center comparison budget exceeded')
    return min((a ^ b).bit_count() for a, b in combinations(centers, 2))


def completions(coordinates: int, fixed_mask: int, value: int):
    if not 0 <= fixed_mask < (1 << coordinates) or value & ~fixed_mask:
        raise ValueError('noncanonical partial assignment')
    free = ((1 << coordinates) - 1) ^ fixed_mask
    sub = free
    while True:
        yield value | sub
        if not sub:
            break
        sub = (sub - 1) & free


def cube_profile(coordinates: int, accepted: set[int]) -> dict:
    """All 3**coordinates subcubes, with at most 4**coordinates point visits."""
    if not 0 <= coordinates <= 8:
        raise BudgetExceeded('cube atlas supports at most eight outer bits')
    if any(type(x) is not int or not 0 <= x < (1 << coordinates) for x in accepted):
        raise ValueError('accepted point outside cube')
    best = {x: -1 for x in accepted}
    sizes, cube_count = Counter(), 0
    for mask in range(1 << coordinates):
        for value in completions(coordinates, ((1 << coordinates) - 1) ^ mask, 0):
            points = tuple(completions(coordinates, mask, value))
            cube_count += 1
            if all(x in accepted for x in points):
                dimension = coordinates - mask.bit_count()
                sizes[dimension] += 1
                for x in points:
                    best[x] = max(best[x], dimension)
    return {'subcubes_examined': cube_count,
            'accepting_subcubes_by_dimension': dict(sorted(sizes.items())),
            'maximum_accepting_dimension': max(sizes, default=None),
            'minimum_certificate_histogram': dict(sorted(Counter(coordinates - d for d in best.values()).items()))}


def schedule(m: int, beta: Fraction, c: int = 1, epsilon: Fraction | None = None) -> dict:
    """Exact subsequence beta*m integral; symbolic integers, NOT built circuits."""
    if type(m) is not int or not 1 <= m <= 4096 or not isinstance(beta, Fraction):
        raise ValueError('require bounded integer m and Fraction beta')
    if not 0 < beta < Fraction(1, 3) or type(c) is not int or c < 1:
        raise ValueError('require 0 < beta < 1/3 and positive integer c')
    power = beta * m
    if power.denominator != 1:
        raise ValueError('this exact numerical schedule requires beta*m integral')
    s2 = 1 << power.numerator
    s1 = s2 // (c * m)
    quotient = s1 // (8 * m)
    if quotient < 1:
        raise ValueError('length too small for the asymptotic schedule')
    k = quotient.bit_length() - 1
    radius = s1 // (4 * m)
    estimate = size_estimate(m, k, radius)
    separation = coarse_separation(m, k)
    bound = center_size_bound(m, k) + m + radius * m + 3
    result = {'m': m, 'beta': str(beta), 'c': c, 's1': s1, 's2': s2,
              'k': k, 'radius': radius, 'N': 1 << m, 'inner_bound': bound,
              'all_accepted_are_YES_by_bound': bound <= s1,
              'coarse_center_separation': separation,
              'separated_balls': separation is not None and separation > 2 * radius + 1,
              'outer_gate_count_symbolic': estimate['gates'],
              'outer_gates_bit_length': estimate['gates'].bit_length(),
              'detectors': estimate['detectors'], 'materialized': False}
    if epsilon is not None:
        if not isinstance(epsilon, Fraction) or epsilon <= 0:
            raise ValueError('epsilon must be a positive Fraction')
        power = (1 + epsilon) * m
        if power.denominator != 1:
            raise ValueError('exact size comparison requires (1+epsilon)*m integral')
        result['epsilon'] = str(epsilon)
        result['outer_size_below_target'] = estimate['gates'] < (1 << power.numerator)
    return result


def run_experiment(seed: int = 11203) -> dict:
    rng = random.Random(seed)
    replay = []
    total_inputs = 0
    for m in range(1, 4):
        for k in range(m + 1):
            for shifted in (False, True):
                centers = center_tables(m, k, shifted)
                distances = [min((x ^ y).bit_count() for y in centers) for x in range(1 << (1 << m))]
                for radius in (0, 1, 2):
                    if radius > (1 << m):
                        continue
                    built = build_recognizer(m, k, radius, shifted)
                    actual = evaluate_packed(built.circuit, max_inputs=8)
                    expected = sum(int(d <= radius) << x for x, d in enumerate(distances))
                    if actual != expected:
                        raise AssertionError(('semantic mismatch', m, k, radius, shifted))
                    for x in range(min(16, 1 << (1 << m))):
                        if built.circuit.evaluate(x) != bool((actual >> x) & 1):
                            raise AssertionError('scalar/packed mismatch')
                    sharing = sharing_measurements(built)
                    if not sharing['all_majorities_reachable'] or sharing['majority_surplus'] != built.estimate['majority_surplus_lower_bound']:
                        raise AssertionError(('sharing mismatch', m, k, radius, shifted))
                    if built.circuit.size > built.estimate['simple_size_upper_bound']:
                        raise AssertionError('simple gate-count upper bound failed')
                    replay.append({'m': m, 'k': k, 'radius': radius, 'shifted': shifted,
                                   'center_count': len(centers), 'accepted_count': sum(d <= radius for d in distances),
                                   'outer_gates': built.circuit.size, 'sharing': sharing})
                    total_inputs += len(distances)
    selected_centers = center_tables(3, 1, True)
    selected_accepted = {x for x in range(256) if min((x ^ c).bit_count() for c in selected_centers) <= 1}
    profile = cube_profile(8, selected_accepted)
    if minimum_distance(selected_centers) != 4 or profile['maximum_accepting_dimension'] != 1:
        raise AssertionError('selected tube geometry failed')
    # This tiny case has affine centers; the one-gate AND of two address bits is omitted.
    and_table = sum(int(bool(x & 1) and bool(x & 2)) << x for x in range(8))
    if and_table in selected_accepted:
        raise AssertionError('the claimed omitted easy table was accepted')
    chosen = {'m': 3, 'k': 1, 'radius': 1, 'shifted': True,
              'centers': list(selected_centers), 'center_minimum_distance': 4,
              'accepted_count': len(selected_accepted), 'outer_gate_count': build_recognizer(3, 1, 1).circuit.size,
              'certificate_profile': profile, 'omitted_one_gate_AND_table': and_table,
              'omitted_table_distance': distance_to_family(3, 1, and_table)}
    # The strict separation endpoint is necessary: distance 2t+1 allows adjacent balls.
    borderline_accepted = {x for x in range(8) if min(x.bit_count(), (x ^ 7).bit_count()) <= 1}
    borderline = {'coordinates': 3, 'centers': [0, 7], 'radius': 1,
                  'distance': 3, 'profile': cube_profile(3, borderline_accepted)}
    if borderline['profile']['maximum_accepting_dimension'] != 3:
        raise AssertionError('strict endpoint control failed')
    patch_cases = []
    for m, k in ((3, 1), (4, 1), (5, 2), (6, 2)):
        for _ in range(12):
            support = tuple(sorted(rng.sample(range(m), k)))
            small = rng.randrange(1 << (1 << k))
            shifted = bool(rng.randrange(2))
            base = inner_center(m, support, small, shifted)
            if base.size > center_size_bound(m, k):
                raise AssertionError('inner DNF/shift bound failed')
            base_table = base.truth_table()
            radius = rng.randrange(3)
            changed = tuple(sorted(rng.sample(range(1 << m), radius)))
            patched = patch_truth_table(base, changed)
            expected = base_table ^ sum(1 << x for x in changed)
            if patched.truth_table() != expected or distance_to_family(m, k, expected) > radius:
                raise AssertionError('patched table mismatch')
            cost_bound = base.size if not changed else base.size + m + radius * m + 3
            if patched.size > cost_bound:
                raise AssertionError('patching cost bound failed')
            recognizer = build_recognizer(m, k, radius)
            if not recognizer.circuit.evaluate(expected):
                raise AssertionError('actual circuit rejected a patched center')
            patch_cases.append({'m': m, 'k': k, 'changes': radius, 'base_gates': base.size,
                                'patched_gates': patched.size, 'inner_cost_bound': cost_bound})
    # Integer-valued sample lengths only; these finite examples do not establish asymptotics.
    schedules = [schedule(m, beta, epsilon=eps) for m, beta, eps in
                 ((256, Fraction(1, 8), Fraction(3, 4)),
                  (512, Fraction(1, 16), Fraction(1, 2)),
                  (1536, Fraction(1, 32), Fraction(1, 3)))]
    if not all(r['all_accepted_are_YES_by_bound'] and r['separated_balls'] and r['outer_size_below_target'] for r in schedules):
        raise AssertionError('parameter sample failed')
    return {'schema_version': 1, 'seed': seed,
            'scope': 'Strict YES-subfamily recognizers, NOT full GapMCSP solvers.',
            'exhaustive_circuit_replays': replay, 'all_input_comparisons': total_inputs,
            'selected_finite_control': chosen, 'strict_separation_endpoint_control': borderline,
            'inner_patching_cases': patch_cases, 'symbolic_parameter_examples': schedules,
            'failures': []}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', type=Path, help='replay and compare an existing JSON artifact')
    args = parser.parse_args(argv)
    if args.output and args.check:
        parser.error('--output and --check are mutually exclusive')
    result = run_experiment()
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        if json.loads(args.check.read_text()) != json.loads(text):
            raise SystemExit('replayed result differs from saved artifact')
        print('Exact tube replay matches the saved artifact.')
    elif args.output:
        args.output.write_text(text)
        print(f'Wrote {args.output}: {len(result["exhaustive_circuit_replays"])} complete circuit replays, '
              f'{result["all_input_comparisons"]} input comparisons.')
    else:
        print(text, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
