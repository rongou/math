"""Bounded, independent checks of the Phase 3 construction and its limits."""
from contextlib import redirect_stderr
from fractions import Fraction
from itertools import combinations, product
import io
import json
from pathlib import Path
import random
import unittest
from unittest.mock import patch

import tube_probe as tp


def literal_cube_points(n, choices):
    return {x for x in range(1 << n)
            if all(value == -1 or ((x >> i) & 1) == value for i, value in enumerate(choices))}


class ArithmeticCircuitTests(unittest.TestCase):
    def test_xor_is_four_ordinary_gates(self):
        b = tp.Builder(2)
        c = b.finish(tp.xor_gate(b, 0, 1))
        self.assertEqual(c.size, 4)
        self.assertEqual(tp.evaluate_packed(c), 0b0110)

    def test_population_counters_all_inputs(self):
        for n in range(9):
            b = tp.Builder(n)
            bits = tp.popcount(b, tuple(range(n)))
            width = max(1, n.bit_length())
            self.assertEqual(len(bits), width)
            self.assertEqual(len(b.gates), n * (5 * width - 1))
            circuits = [b.finish(wire) for wire in bits]
            packed = [tp.evaluate_packed(c, max_inputs=8) for c in circuits]
            for x in range(1 << n):
                scalar = sum(int(c.evaluate(x)) << i for i, c in enumerate(circuits))
                vector = sum(((v >> x) & 1) << i for i, v in enumerate(packed))
                self.assertEqual(scalar, x.bit_count())
                self.assertEqual(vector, scalar)

    def test_comparator_all_inputs_and_endpoints(self):
        for width in range(1, 7):
            for limit in range(-1, (1 << width) + 1):
                b = tp.Builder(width)
                c = b.finish(tp.leq_constant(b, tuple(range(width)), limit))
                self.assertEqual(c.size, 2 * width if 0 <= limit < (1 << width) else 0)
                actual = tp.evaluate_packed(c)
                expected = sum(int(x <= limit) << x for x in range(1 << width))
                self.assertEqual(actual, expected)
        with self.assertRaises(ValueError):
            tp.leq_constant(tp.Builder(1), (), 0)

    def test_interpreter_rejects_forward_wires_and_unknown_gates(self):
        from certificate_controls import Circuit, Gate
        for gate in (Gate('AND', (0, 3)), Gate('XOR', (0, 0)), Gate('NOT', (0, 0))):
            with self.assertRaises(ValueError):
                tp.evaluate_packed(Circuit(1, (gate,), 3))
        with self.assertRaises(ValueError):
            tp.evaluate_packed(Circuit(1, (), 3))
        with self.assertRaises(tp.BudgetExceeded):
            tp.evaluate_packed(Circuit(17, (), 0))


class SemanticFamilyTests(unittest.TestCase):
    def test_blocks_partition_addresses_and_keep_selected_coordinates(self):
        for m in range(1, 6):
            for k in range(m + 1):
                for support in tp.supports(m, k):
                    groups = tp.blocks(m, support)
                    self.assertEqual(len(groups), 1 << k)
                    self.assertEqual(sorted(a for group in groups for a in group), list(range(1 << m)))
                    for label, group in enumerate(groups):
                        self.assertEqual(len(group), 1 << (m - k))
                        for a in group:
                            self.assertEqual(sum(((a >> i) & 1) << j for j, i in enumerate(support)), label)
        for invalid in ((1, 0), (0, 0), (3,)):
            with self.assertRaises(ValueError):
                tp.blocks(3, invalid)

    def test_block_majority_distance_matches_explicit_centers(self):
        for m in range(1, 4):
            for k in range(m + 1):
                for shifted in (False, True):
                    centers = tp.center_tables(m, k, shifted)
                    for x in range(1 << (1 << m)):
                        self.assertEqual(tp.distance_to_family(m, k, x, shifted),
                                         min((x ^ c).bit_count() for c in centers))

    def test_inner_dnf_and_parity_shift_all_small_functions(self):
        for m in range(1, 5):
            for k in range(min(m, 2) + 1):
                for support in tp.supports(m, k):
                    for table in range(1 << (1 << k)):
                        for shifted in (False, True):
                            c = tp.inner_center(m, support, table, shifted)
                            self.assertLessEqual(c.size, tp.center_size_bound(m, k))
                            for x in range(1 << m):
                                address = sum(((x >> i) & 1) << j for j, i in enumerate(support))
                                expected = ((table >> address) & 1) ^ ((x.bit_count() & 1) if shifted else 0)
                                self.assertEqual(c.evaluate(x), bool(expected))

    def test_coarse_minimum_distance_bound_in_its_declared_regime(self):
        for m in range(1, 7):
            for k in range(min(m, 2) + 1):
                centers = tp.center_tables(m, k)
                bound = tp.coarse_separation(m, k)
                if 2 * k >= m:
                    self.assertIsNone(bound)
                else:
                    self.assertGreaterEqual(tp.minimum_distance(centers), bound)
        # k=0 includes constants AND full parity: separation is N/2, not N.
        self.assertEqual(tp.coarse_separation(3, 0), 4)
        self.assertEqual(tp.minimum_distance(tp.center_tables(3, 0)), 4)

    def test_shift_family_includes_projections_and_full_parity(self):
        for m in range(3, 7):
            k = 1
            self.assertEqual(tp.distance_to_family(m, k, tp.address_parity(m)), 0)
            for i in range(m):
                table = sum(((a >> i) & 1) << a for a in range(1 << m))
                self.assertEqual(tp.distance_to_family(m, k, table), 0)

    def test_explicit_missing_cheap_parities_prove_incompleteness(self):
        for m, k in ((4, 1), (6, 2), (8, 3), (6, 0)):
            subset = tuple(range(k + 1))
            table = sum((sum((a >> i) & 1 for i in subset) % 2) << a for a in range(1 << m))
            self.assertEqual(tp.distance_to_family(m, k, table), 1 << (m - 1))
            b = tp.Builder(m)
            wire = subset[0]
            for i in subset[1:]:
                wire = tp.xor_gate(b, wire, i)
            c = b.finish(wire)
            self.assertEqual(c.size, 4 * k)
            self.assertEqual(c.truth_table(), table)

    def test_actual_outer_circuits_beyond_full_atlas(self):
        rng = random.Random(203)
        for m, k in ((4, 1), (5, 2), (6, 2)):
            for radius in (0, 1, 3):
                circuit = tp.build_recognizer(m, k, radius).circuit
                for _ in range(16):
                    x = rng.getrandbits(1 << m)
                    self.assertEqual(circuit.evaluate(x), tp.distance_to_family(m, k, x) <= radius)


class GeometryTests(unittest.TestCase):
    def test_all_cube_masks_match_independent_ternary_generator(self):
        for n in range(5):
            seen = set()
            for choices in product((-1, 0, 1), repeat=n):
                mask = sum((value != -1) << i for i, value in enumerate(choices))
                value = sum((v == 1) << i for i, v in enumerate(choices))
                literal = literal_cube_points(n, choices)
                actual = set(tp.completions(n, mask, value))
                self.assertEqual(actual, literal)
                seen.add(tuple(sorted(actual)))
            self.assertEqual(len(seen), 3 ** n)

    def test_general_separated_tube_lemma_exhaustively_through_three_coordinates(self):
        checked = 0
        for n in range(4):
            for center_mask in range(1 << (1 << n)):
                centers = [c for c in range(1 << n) if (center_mask >> c) & 1]
                for radius in range(n + 1):
                    if any((c ^ d).bit_count() <= 2 * radius + 1 for c, d in combinations(centers, 2)):
                        continue
                    accepted = {x for x in range(1 << n) if any((x ^ c).bit_count() <= radius for c in centers)}
                    actual = tp.cube_profile(n, accepted)
                    for choices in product((-1, 0, 1), repeat=n):
                        cube = literal_cube_points(n, choices)
                        if cube <= accepted:
                            self.assertLessEqual(choices.count(-1), radius)
                            self.assertTrue(any(all((x ^ c).bit_count() <= radius for x in cube) for c in centers))
                    if centers:
                        self.assertEqual(actual['maximum_accepting_dimension'], radius)
                        self.assertEqual(actual['minimum_certificate_histogram'], {n - radius: len(accepted)})
                    else:
                        self.assertIsNone(actual['maximum_accepting_dimension'])
                    checked += 1
        self.assertEqual(checked, 87)

    def test_unique_decoding_separation_is_not_enough(self):
        centers, radius = (0, 7), 1
        self.assertGreater(tp.minimum_distance(centers), 2 * radius)
        accepted = {x for x in range(8) if any((x ^ c).bit_count() <= radius for c in centers)}
        self.assertEqual(accepted, set(range(8)))
        self.assertEqual(tp.cube_profile(3, accepted)['maximum_accepting_dimension'], 3)

    def test_exact_eight_bit_control_and_omitted_one_gate_function(self):
        centers = tp.center_tables(3, 1)
        self.assertEqual(len(centers), 16)
        self.assertEqual(tp.minimum_distance(centers), 4)
        accepted = {x for x in range(256) if any((x ^ c).bit_count() <= 1 for c in centers)}
        self.assertEqual(len(accepted), 144)
        profile = tp.cube_profile(8, accepted)
        self.assertEqual(profile['subcubes_examined'], 6561)
        self.assertEqual(profile['minimum_certificate_histogram'], {7: 144})
        self.assertEqual(profile['maximum_accepting_dimension'], 1)
        self.assertNotIn(136, accepted)  # AND(x0,x1) on three address variables
        self.assertEqual(tp.distance_to_family(3, 1, 136), 2)

    def test_relative_certificates_charge_only_new_fixed_coordinates(self):
        centers = tp.center_tables(3, 1)
        radius, n = 1, 8
        accepted = {x for x in range(256) if any((x ^ c).bit_count() <= radius for c in centers)}
        rng = random.Random(41)
        for _ in range(32):
            x = rng.choice(sorted(accepted))
            center, = [c for c in centers if (x ^ c).bit_count() <= radius]
            initial = rng.randrange(256)
            live = 255 ^ initial
            remaining = n - initial.bit_count()
            fixed_errors = ((x ^ center) & initial).bit_count()
            best = remaining
            for additional in tp.completions(n, initial, 0):
                final = initial | additional
                forced = set(tp.completions(n, final, x & final)) <= accepted
                if forced:
                    best = min(best, additional.bit_count())
                    self.assertLessEqual(remaining - additional.bit_count(), radius)
                    # Adding already-fixed coordinates changes neither cost nor semantics.
                    duplicate_mask = additional | initial
                    self.assertEqual((duplicate_mask & ~initial).bit_count(), additional.bit_count())
            self.assertEqual(best, max(0, remaining - (radius - fixed_errors)))


class ResourceAndReportTests(unittest.TestCase):
    def test_literal_sharing_not_hidden_truth_table_enumeration(self):
        for m, k, radius in ((3, 1, 1), (4, 1, 1), (5, 2, 1)):
            c = tp.build_recognizer(m, k, radius)
            measure = tp.sharing_measurements(c)
            estimate = c.estimate
            self.assertEqual(c.circuit.size, estimate['gates'])
            self.assertLessEqual(c.circuit.size, estimate['simple_size_upper_bound'])
            self.assertTrue(measure['all_majorities_reachable'])
            self.assertEqual(measure['majority_nodes'], estimate['detectors'] * (1 << k))
            self.assertEqual(measure['majority_fanouts'], {2 * (1 << (m - k)): measure['majority_nodes']})
            self.assertEqual(measure['majority_surplus'], estimate['majority_surplus_lower_bound'])
            self.assertGreaterEqual(measure['reuse_surplus'], measure['majority_surplus'])
        # The recognizer must not invoke explicit center enumeration.
        with patch.object(tp, 'center_tables', side_effect=AssertionError('centers were enumerated')):
            self.assertGreater(tp.build_recognizer(4, 1, 1).circuit.size, 0)

    def test_resource_and_parameter_guards(self):
        for args in ((0, 0, 0), (3, 4, 1), (3, 1, -1), (True, 0, 0), (3, 1, 9)):
            with self.assertRaises(ValueError):
                tp.parameters(*args)
        for operation in (lambda: tp.build_recognizer(3, 1, 1, max_gates=2),
                          lambda: tp.build_recognizer(32, 1, 1),
                          lambda: tp.center_tables(10, 5),
                          lambda: tp.center_tables(6, 3, budget=1),
                          lambda: tp.blocks(17, (0,)),
                          lambda: tp.cube_profile(9, set())):
            with self.assertRaises(tp.BudgetExceeded):
                operation()
        with self.assertRaises(ValueError):
            tp.distance_to_family(3, 1, 256)
        with self.assertRaises(ValueError):
            tp.inner_center(3, (0, 0), 0)
        with self.assertRaises(ValueError):
            tuple(tp.completions(3, 1, 2))

    def test_fixed_beta_schedule_integer_checks_and_no_materialization(self):
        for m, beta, eps in ((256, Fraction(1, 8), Fraction(3, 4)),
                             (512, Fraction(1, 16), Fraction(1, 2)),
                             (1536, Fraction(1, 32), Fraction(1, 3))):
            with patch.object(tp, 'build_recognizer', side_effect=AssertionError('must stay symbolic')):
                result = tp.schedule(m, beta, epsilon=eps)
            self.assertFalse(result['materialized'])
            self.assertTrue(result['all_accepted_are_YES_by_bound'])
            self.assertTrue(result['separated_balls'])
            self.assertTrue(result['outer_size_below_target'])
            self.assertGreaterEqual(result['s1'], 64 * m)
            self.assertLess(result['radius'], result['s2'])
        for args in ((255, Fraction(1, 8)), (10, Fraction(1, 2)), (8, Fraction(1, 8))):
            with self.assertRaises(ValueError):
                tp.schedule(*args)

    def test_cli_rejects_conflicting_write_and_check_without_running(self):
        with patch.object(tp, 'run_experiment') as runner, redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                tp.main(['--output', '/tmp/unused-phase3.json', '--check', '/tmp/unused-phase3.json'])
            runner.assert_not_called()

    def test_saved_report_replays_exactly(self):
        result = tp.run_experiment()
        saved = json.loads(Path(__file__).with_name('tube_results.json').read_text())
        self.assertEqual(json.loads(json.dumps(result)), saved)
        self.assertEqual(len(result['exhaustive_circuit_replays']), 54)
        self.assertEqual(result['all_input_comparisons'], 6480)
        self.assertEqual(len(result['inner_patching_cases']), 48)
        self.assertEqual(result['failures'], [])
        self.assertIn('NOT full GapMCSP', result['scope'])


if __name__ == '__main__':
    unittest.main()
