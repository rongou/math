#!/usr/bin/env python3
"""Independent finite coverage/semantics tests; no solvers or file writes."""
from __future__ import annotations

import hashlib
import itertools
from pathlib import Path
import unittest

import promise_atlas as atlas


def reference_gate_lists(arity: int, bound: int):
    """Independent breadth-first syntactic product, not the production DFS."""
    layer = [()]
    result = {()}
    for position in range(bound):
        wires = arity + 2 + position
        options = [(atlas.NOT, i, -1) for i in range(wires)]
        options += [(op, a, b) for op in (atlas.AND, atlas.OR)
                    for a, b in itertools.product(range(wires), repeat=2)]
        layer = [prefix + (gate,) for prefix, gate in itertools.product(layer, options)]
        result.update(layer)
    return result


def reference_values(arity: int, gates: atlas.Program) -> tuple[int, ...]:
    """Row-at-a-time Boolean evaluation, independent of word-parallel evaluation."""
    truth_tables = [0] * (arity + 2 + len(gates))
    for assignment in range(1 << arity):
        values = [False, True] + [bool((assignment >> i) & 1) for i in range(arity)]
        for op, a, b in gates:
            if op == atlas.NOT:
                value = not values[a]
            elif op == atlas.AND:
                value = values[a] and values[b]
            elif op == atlas.OR:
                value = values[a] or values[b]
            else:
                raise AssertionError("bad op")
            values.append(value)
        for wire, value in enumerate(values):
            truth_tables[wire] |= int(value) << assignment
    return tuple(truth_tables)


def from_json(record: dict) -> atlas.Circuit:
    opcode = {"NOT": atlas.NOT, "AND2": atlas.AND, "OR2": atlas.OR}
    gates = tuple((opcode[g["op"]], g["inputs"][0],
                   -1 if g["op"] == "NOT" else g["inputs"][1]) for g in record["gates"])
    return atlas.Circuit(record["arity"], gates, record["output_wire"])


class PromiseAtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # One complete primary replay shared by the tests, rather than per-test reruns.
        cls.data = atlas.build_results()
        cls.yes = set(cls.data["promise"]["sets"]["YES"])
        cls.gap = set(cls.data["promise"]["sets"]["GAP"])
        cls.no = set(cls.data["promise"]["sets"]["NO"])
        cls.low = cls.yes | cls.gap

    def test_01_generator_covers_independent_syntactic_products_m1_m2(self):
        for arity in (1, 2):
            with self.subTest(arity=arity):
                generated = list(atlas.iter_topological_programs(arity, 2))
                syntaxes = [gates for gates, _ in generated]
                self.assertEqual(len(syntaxes), len(set(syntaxes)))
                self.assertEqual(set(syntaxes), reference_gate_lists(arity, 2))
                for gates, values in generated:
                    self.assertEqual(values, reference_values(arity, gates))
                for row in atlas.expected_counts(arity, 2):
                    self.assertEqual(sum(len(gates) == row["gates"] for gates in syntaxes),
                                     row["programs"])

    def test_02_literal_complete_enumeration_counts(self):
        expected = {
            (1, 2): ([1, 21, 756], [3, 84, 3780]),
            (2, 3): ([1, 36, 1980, 154440], [4, 180, 11880, 1081080]),
            (3, 2): ([1, 55, 4290], [5, 330, 30030]),
            (8, 2): ([1, 210, 53130], [10, 2310, 637560]),
        }
        audits = [self.data["inner_enumeration"],
                  self.data["small_arity_generator_checks"]["m1"],
                  self.data["small_arity_generator_checks"]["m2"],
                  self.data["outer_classifier_search"]["enumeration"]]
        for audit in audits:
            programs, outputs = expected[audit["arity"], audit["gate_bound"]]
            rows = audit["counts_by_gate_count"]
            self.assertEqual([r["programs"] for r in rows], programs)
            self.assertEqual([r["output_circuits"] for r in rows], outputs)
            self.assertEqual(audit["program_count"], sum(programs))
            self.assertEqual(audit["output_circuit_count"], sum(outputs))
            self.assertRegex(audit["enumeration_sha256"], r"^[0-9a-f]{64}$")

    def test_03_inner_partition_and_all_witnesses(self):
        rows = self.data["truth_tables"]
        self.assertEqual([row["table"] for row in rows], list(range(256)))
        self.assertEqual([sum(row["minimum_size_class"] == k for row in rows)
                          for k in ("0", "1", "2", ">2")], [5, 9, 26, 216])
        self.assertEqual((len(self.yes), len(self.gap), len(self.no)), (14, 26, 216))
        self.assertFalse(self.yes & self.gap or self.yes & self.no or self.gap & self.no)
        self.assertEqual(self.yes | self.gap | self.no, set(range(256)))
        for row in rows:
            if row["witness"] is None:
                self.assertEqual(row["promise_class"], "NO")
                self.assertIsNone(row["exact_minimum_size"])
                self.assertEqual(row["certified_size_lower_bound"], 3)
            else:
                witness = from_json(row["witness"])
                self.assertEqual(witness.evaluate(), row["table"])
                self.assertEqual(reference_values(3, witness.gates)[witness.output], row["table"])
                self.assertEqual(len(witness.gates), row["exact_minimum_size"])

    def test_04_not_is_not_free_and_xor_known_costs(self):
        self.assertEqual(atlas.input_truth_tables(3), (0, 255, 170, 204, 240))
        tables = self.data["truth_tables"]
        for complement in (85, 51, 15):
            self.assertEqual(tables[complement]["exact_minimum_size"], 1)
        checks = self.data["small_arity_generator_checks"]
        self.assertEqual(checks["m1"]["new_semantics_at_minimum_gate_count"], [3, 1, 0])
        self.assertEqual(checks["m2"]["new_semantics_at_minimum_gate_count"], [4, 4, 6, 0])
        for name, table in (("m2_xor", 6), ("m2_xnor", 9)):
            item = checks[name]
            witness = from_json(item["witness"])
            self.assertEqual(item["exact_minimum_gate_count"], 4)
            self.assertEqual(len(witness.gates), 4)
            self.assertEqual(reference_values(2, witness.gates)[witness.output], table)
        self.assertEqual(tables[170 ^ 204]["minimum_size_class"], ">2")

    def test_05_internal_dag_sharing_repetition_and_old_outputs(self):
        # First computed gate feeds TWO distinct later gates: an actual shared DAG.
        shared = ((atlas.NOT, 2, -1), (atlas.AND, 3, 2), (atlas.OR, 3, 4))
        found = False
        for gates, values in atlas.iter_topological_programs(1, 3):
            if gates == shared:
                found = True
                self.assertEqual(values, reference_values(1, gates))
                break
        self.assertTrue(found)
        two_gate_programs = {g for g, _ in atlas.iter_topological_programs(1, 2)}
        self.assertIn(((atlas.NOT, 2, -1), (atlas.AND, 3, 3)), two_gate_programs)
        # An earlier wire remains a legal output even after dead gates are added.
        self.assertEqual(atlas.Circuit(1, shared, 2).evaluate(), 2)
        with self.assertRaises(ValueError):
            atlas.Circuit(1, ((atlas.NOT, 3, -1),), 3).evaluate()

    def test_06_completion_generator_endpoints_and_independent_coverage(self):
        for n in range(5):
            cubes = set()
            total = 0
            for pattern in itertools.product((None, 0, 1), repeat=n):
                mask = sum(1 << i for i, bit in enumerate(pattern) if bit is not None)
                value = sum(bit << i for i, bit in enumerate(pattern) if bit is not None)
                expected = [x for x in range(1 << n)
                            if all(bit is None or (x >> i) & 1 == bit for i, bit in enumerate(pattern))]
                actual = list(atlas.completions(n, mask, value))
                self.assertEqual(sorted(actual), expected)
                self.assertEqual(len(actual), len(set(actual)))
                cubes.add((mask, value))
                total += len(actual)
            self.assertEqual(len(cubes), 3 ** n)
            self.assertEqual(total, 4 ** n)
        self.assertEqual(list(atlas.completions(0, 0, 0)), [0])
        self.assertEqual(list(atlas.completions(8, 255, 42)), [42])
        with self.assertRaises(ValueError):
            list(atlas.completions(8, 0, 1))

    def test_07_all_subcubes_directly_and_independently_classified(self):
        expected_accepting = {}
        cube_count = completion_count = 0
        for pattern in itertools.product((None, 0, 1), repeat=8):
            fixed = [(i, bit) for i, bit in enumerate(pattern) if bit is not None]
            live = [i for i, bit in enumerate(pattern) if bit is None]
            mask = sum(1 << i for i, _ in fixed)
            value = sum(bit << i for i, bit in fixed)
            points = [value | sum(bit << i for i, bit in zip(live, bits))
                      for bits in itertools.product((0, 1), repeat=len(live))]
            cube_count += 1
            completion_count += len(points)
            if set(points) <= self.low:
                expected_accepting[mask, value] = sorted(points)
        summary = self.data["subcube_atlas"]
        self.assertEqual((cube_count, completion_count), (6561, 65536))
        actual = {(c["mask"], c["value"]): c["completions"] for c in summary["accepting_subcubes"]}
        self.assertEqual(actual, expected_accepting)
        self.assertEqual(summary["accepting_subcube_count"], len(actual))
        self.assertEqual(summary["subcube_count_including_false"], 6562)
        self.assertFalse(summary["false_subcube"]["contains_a_yes_table"])

    def test_08_every_yes_and_every_coordinate_subset(self):
        certs = self.data["promise_yes_certificates"]
        self.assertEqual(certs["subset_tests"], 14 * 256)
        self.assertEqual({r["yes_table"] for r in certs["per_yes_table"]}, self.yes)
        expected_histogram = {"6": 6, "7": 5, "8": 3}
        self.assertEqual(certs["minimum_certificate_size_histogram"], expected_histogram)
        for row in certs["per_yes_table"]:
            table = row["yes_table"]
            valid = []
            for mask in range(256):
                # Independent direct scan of all 256 completions, not submask generation.
                points = [x for x in range(256) if x & mask == table & mask]
                if not (set(points) & self.no):
                    valid.append(mask)
            self.assertEqual(valid, row["accepting_masks"])
            minimum = min(mask.bit_count() for mask in valid)
            self.assertEqual(minimum, row["minimum_fixed_coordinates"])
            self.assertEqual([mask for mask in valid if mask.bit_count() == minimum], row["minimum_masks"])
            self.assertEqual(int(row["acceptance_bitset_hex"], 16), sum(1 << mask for mask in valid))
            w = row["minimum_witness"]
            self.assertEqual(w["completions"], [x for x in range(256) if x & w["mask"] == w["value"]])

    def test_09_counting_endpoints_without_floating_point(self):
        for live in range(9):
            for low_count in range((1 << live) + 1):
                valid = [fixed for fixed in range(live + 1) if 2 ** (live - fixed) <= low_count]
                self.assertEqual(atlas.minimum_fixed_from_count(live, low_count), min(valid, default=None))
        self.assertIsNone(atlas.minimum_fixed_from_count(8, 0))
        self.assertEqual(atlas.minimum_fixed_from_count(8, 1), 8)
        self.assertEqual(atlas.minimum_fixed_from_count(8, 32), 3)
        self.assertEqual(atlas.minimum_fixed_from_count(8, 40), 3)
        self.assertEqual(atlas.minimum_fixed_from_count(8, 255), 1)
        self.assertEqual(atlas.minimum_fixed_from_count(8, 256), 0)
        with self.assertRaises(ValueError):
            atlas.minimum_fixed_from_count(3, 9)

    def test_10_overlap_and_contradiction_by_direct_intersections(self):
        for n in range(4):
            partials = [(mask, value) for mask in range(1 << n)
                        for value in range(1 << n) if value & ~mask == 0]
            for (a, av), (c, cv) in itertools.product(partials, repeat=2):
                expected = [x for x in range(1 << n) if x & a == av and x & c == cv]
                intersection = atlas.intersect_partial(n, a, av, c, cv)
                actual = [] if intersection is None else sorted(atlas.completions(n, *intersection))
                self.assertEqual(actual, expected)
        audit = self.data["prior_restriction_overlap"]
        self.assertEqual(audit["pair_incidence_tests"], 917504)
        self.assertEqual(audit["zero_new_constraint_incidences"], 91854)
        self.assertEqual(sum(audit["relative_minimum_new_fixed_histogram"].values()), 3584)
        self.assertEqual(sum(r["count"] for r in audit["accepting_incidence_histogram"]),
                         audit["accepting_pair_incidences"])
        for example in audit["examples"].values():
            prior = example["prior"]
            a, av = prior["mask"], prior["value"]
            c, cv = example["certificate_mask"], example["certificate_value"]
            points = [x for x in range(256) if x & a == av and x & c == cv]
            self.assertEqual(points, example["intersection"]["completions"])
            self.assertEqual(len(points), 2 ** (8 - (a | c).bit_count()))
            self.assertEqual(example["newly_fixed_count"], (c & ~a).bit_count())
            self.assertEqual(example["overlap_fixed_count"], (a & c).bit_count())
            self.assertLessEqual(set(points), self.low)
            relative_low_count = sum(x & a == av for x in self.low)
            self.assertEqual(relative_low_count, prior["low_count"])
            self.assertLessEqual(len(points), relative_low_count)
        example = audit["examples"]["nontrivial_overlap_changes_naive_dimension"]
        self.assertNotEqual(example["intersection"]["live_count"], example["incorrect_dimension_if_overlap_ignored"])
        self.assertEqual(atlas.intersect_partial(8, 1, 0, 1, 1), None)

    def test_11_falsification_witnesses_are_finite_and_valid(self):
        witnesses = self.data["finite_falsification_witnesses"]
        count = witnesses["counting_bound_need_not_be_attained"]
        self.assertEqual((count["yes_table"], count["cardinality_lower_bound"],
                          count["actual_minimum_fixed_coordinates"]), (0, 3, 7))
        invalid = count["a_counting_allowed_but_invalid_three_coordinate_candidate"]
        self.assertLessEqual(invalid["completion_count"], len(self.low))
        self.assertGreater(invalid["no_count"], 0)
        promise = witnesses["promise_acceptance_need_not_mean_yes_only"]
        self.assertEqual(promise["witness"]["completions"], [0, 128])
        self.assertEqual(promise["gap_completions"], [128])
        self.assertIn(0, self.yes)
        self.assertIn(128, self.gap)

    def test_12_outer_search_is_bounded_circuit_search_and_never_claims_more(self):
        outer = self.data["outer_classifier_search"]
        self.assertEqual(outer["strict_gate_budget"], 2)
        self.assertEqual(outer["status"], "exhausted_no_classifier_within_budget")
        self.assertIsNone(outer["minimum_gate_count"])
        self.assertEqual(outer["certified_minimum_lower_bound"], 3)
        self.assertEqual(outer["distinct_classifying_functions_within_budget"], 0)
        self.assertIn("UNKNOWN", outer["beyond_budget"])
        witness = from_json(outer["best_bounded_witness"])
        table = reference_values(8, witness.gates)[witness.output]
        fn = [x for x in sorted(self.yes) if not (table >> x) & 1]
        fp = [x for x in sorted(self.no) if (table >> x) & 1]
        self.assertEqual(fn, outer["best_bounded_false_negatives"])
        self.assertEqual(fp, outer["best_bounded_false_positives"])
        self.assertEqual(len(fn) + len(fp), outer["best_bounded_promise_error_count"])
        with self.assertRaises(atlas.BudgetExceeded):
            atlas.enumerate_dags(8, 3)
        with self.assertRaises(atlas.BudgetExceeded):
            atlas.enumerate_dags(2, 4)

    def test_14_independent_full_m3_classification_by_boolean_rows(self):
        # A second complete m=3 implementation: BFS syntaxes and Boolean rows.
        # It neither calls the production circuit evaluator nor uses its minima.
        minimum = {}
        programs = reference_gate_lists(3, 2)
        self.assertEqual(len(programs), 4346)
        for gates in programs:
            for value in reference_values(3, gates):
                minimum[value] = min(len(gates), minimum.get(value, len(gates)))
        reported = {row["table"]: row["exact_minimum_size"]
                    for row in self.data["truth_tables"] if row["exact_minimum_size"] is not None}
        self.assertEqual(minimum, reported)
        self.assertEqual(set(range(256)) - set(minimum), self.no)

    def test_15_maximal_separator_scope_and_eight_essential_edges(self):
        certs = self.data["promise_yes_certificates"]
        self.assertEqual(certs["certificate_function"], "maximal separator 1_Low")
        zero = next(row for row in certs["per_yes_table"] if row["yes_table"] == 0)
        self.assertEqual(zero["minimum_fixed_coordinates"], 7)
        self.assertEqual(zero["strict_yes_only_minimum_fixed_coordinates"], 8)
        edges = self.data["promise_essential_edges"]
        self.assertEqual([edge["coordinate"] for edge in edges], list(range(8)))
        for edge in edges:
            self.assertIn(edge["yes_table"], self.yes)
            self.assertIn(edge["no_table"], self.no)
            self.assertEqual(edge["yes_table"] ^ edge["no_table"], 1 << edge["coordinate"])
            witness = from_json(edge["yes_witness"])
            self.assertEqual(len(witness.gates), 0)
            self.assertEqual(witness.evaluate(), edge["yes_table"])
        self.assertEqual([(e["yes_table"], e["no_table"]) for e in edges],
                         [(0, 1), (0, 2), (0, 4), (0, 8), (0, 16), (0, 32), (0, 64), (255, 127)])
        bounds = self.data["analytic_outer_gate_lower_bounds"]
        self.assertEqual(bounds["zero_certificate_argument"]["consequence_total_gates_at_least"], 6)
        self.assertEqual(bounds["eight_promise_edges_argument"]["consequence_binary_gates_at_least"], 7)
        self.assertIn("UNKNOWN", bounds["attainability"])

    def test_13_hash_replay_and_artifact_boundaries(self):
        a = atlas.enumerate_dags(1, 2).audit
        b = atlas.enumerate_dags(1, 2).audit
        self.assertEqual(a, b)
        self.assertEqual(a, self.data["small_arity_generator_checks"]["m1"])
        self.assertEqual(self.data["reproducibility"]["source_sha256"],
                         hashlib.sha256(Path(atlas.__file__).read_bytes()).hexdigest())
        self.assertEqual(self.data["reproducibility"]["test_source_sha256"],
                         hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        self.assertLess(self.data["bounded_work"]["total_named_work_items"], 3_000_000)
        self.assertFalse(self.data["scope"]["kernel_checked"])
        self.assertFalse(self.data["scope"]["asymptotic_claims"])
        self.assertFalse(self.data["scope"]["formula_dp_used_for_circuit_minima"])
        self.assertEqual(self.data["convention"]["input_complement_is_free"], False)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Tests require assertions enabled; do not use -O/-OO.")
    unittest.main(verbosity=2)
