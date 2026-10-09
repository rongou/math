"""Independent hand examples and finite regression tests for sharing_probe."""
from contextlib import redirect_stderr, redirect_stdout
from fractions import Fraction as F
import io
import json
import unittest
from unittest.mock import patch

import sharing_probe as sp


class ModelTests(unittest.TestCase):
    def named(self, name):
        return next(dag for dag in sp.named_dags() if dag.name == name)

    def test_input_and_constant_outputs(self):
        for name, literal, constant in (("input-is-output", 1, 0),
                                         ("constant-0-output", 0, 1),
                                         ("constant-1-output", 0, 1)):
            dag = self.named(name)
            stats = sp.measure_dag(dag)
            self.assertEqual((stats["S"], stats["R"], stats["unfolded_gate_count"]), (0, 0, 0))
            self.assertEqual(stats["outdegree_product"], 1)
            self.assertEqual(stats["leaf_count"], 1)
            self.assertEqual(stats["literal_leaf_count"], literal)
            self.assertEqual(stats["constant_leaf_count"], constant)
            self.assertEqual(stats["output_to_node_paths"], (1,))

    def test_repeated_wires_count_but_primary_input_surplus_does_not(self):
        dag = self.named("duplicate-primary-wire")
        stats = sp.measure_dag(dag)
        self.assertEqual(dag.nodes[dag.output].args, (0, 0))
        self.assertEqual(stats["outdegree"], (2, 0))
        self.assertEqual(stats["output_to_node_paths"], (2, 1))
        self.assertEqual(stats["duplicate_wire_slots"], 1)
        self.assertEqual(stats["S"], 1)
        self.assertEqual(stats["R"], 0)
        self.assertEqual(stats["excluded_input_surplus"], 1)
        self.assertEqual(stats["unfolded_gate_count"], 1)
        self.assertEqual(stats["literal_leaf_count"], 2)
        # P only bounds INTERNAL path multiplicities. The reused input exceeds P.
        self.assertGreater(stats["output_to_node_paths"][0], stats["outdegree_product"])

    def test_reused_primary_inputs_alone_create_no_internal_surplus(self):
        stats = sp.measure_dag(self.named("only-primary-inputs-reused"))
        self.assertEqual((stats["S"], stats["R"], stats["outdegree_product"]), (3, 0, 1))
        self.assertEqual(stats["unfolded_gate_count"], 3)
        self.assertEqual(stats["literal_leaf_count"], 4)
        self.assertEqual(stats["excluded_input_surplus"], 2)

    def test_reconvergent_diamond(self):
        stats = sp.measure_dag(self.named("reconvergent-diamond"))
        self.assertEqual(stats["S"], 4)
        self.assertEqual(stats["R"], 1)
        self.assertEqual(stats["outdegree_product"], 2)
        self.assertEqual(stats["unfolded_gate_count"], 5)
        self.assertEqual(stats["literal_leaf_count"], 4)
        self.assertEqual(stats["output_to_node_paths"], (2, 1, 1, 2, 1, 1, 1))

    def test_product_bound_is_stronger_for_fanout_three_and_four(self):
        for name, s, r, p, f in (("internal-fanout-three", 3, 2, 3, 5),
                                  ("internal-fanout-four", 4, 3, 4, 7)):
            stats = sp.measure_dag(self.named(name))
            self.assertEqual((stats["S"], stats["R"], stats["outdegree_product"], stats["unfolded_gate_count"]), (s, r, p, f))
            self.assertLess(stats["gate_bound_S_product"], stats["gate_bound_S_2R"])
            self.assertEqual(stats["output_to_node_paths"][1], p)

    def test_unused_consumers_do_not_inflate_fanout(self):
        dag = self.named("unused-consumers-do-not-increase-R")
        stats = sp.measure_dag(dag)
        self.assertEqual((stats["declared_S"], stats["S"], stats["unused_gates"]), (4, 2, 2))
        self.assertEqual(stats["outdegree"][2], 1)
        self.assertEqual(stats["declared_outdegree"][2], 4)
        self.assertEqual(stats["R"], 0)
        self.assertEqual(stats["output_to_node_paths"][4:], (0, 0))
        trimmed = sp.DAG("trimmed", dag.nodes[:dag.output + 1], dag.output)
        trimmed_stats = sp.measure_dag(trimmed)
        for key in ("S", "R", "outdegree_product", "unfolded_gate_count", "literal_leaf_count"):
            self.assertEqual(stats[key], trimmed_stats[key])

    def test_unused_entire_circuit_and_constant_leaves(self):
        dag = self.named("constant-output-with-unused-sharing")
        stats = sp.measure_dag(dag)
        self.assertEqual((stats["S"], stats["R"], stats["declared_S"]), (0, 0, 2))
        self.assertEqual(sp.evaluate_dag(dag, {}), 0)
        shared = self.named("shared-gate-over-constant")
        stats = sp.measure_dag(shared)
        self.assertEqual((stats["S"], stats["R"], stats["unfolded_gate_count"]), (2, 1, 3))
        self.assertEqual((stats["literal_leaf_count"], stats["constant_leaf_count"]), (0, 2))
        self.assertEqual(sp.evaluate_dag(shared, {}), 0)
        b = sp.Builder(); c = b.constant(1); root = b.gate("AND", c, c)
        stats = sp.measure_dag(b.finish("constant-wire", root))
        self.assertEqual((stats["R"], stats["excluded_constant_surplus"]), (0, 1))

    def test_identical_nodes_are_not_silently_merged(self):
        separate = self.named("identical-gates-are-distinct-nodes")
        b = sp.Builder(); x, y = b.input("x"), b.input("y")
        a = b.gate("AND", x, y); root = b.gate("OR", a, a)
        shared = b.finish("shared", root)
        first, second = sp.measure_dag(separate), sp.measure_dag(shared)
        self.assertEqual((first["S"], first["R"]), (3, 0))
        self.assertEqual((second["S"], second["R"]), (2, 1))
        self.assertEqual(first["unfolded_gate_count"], second["unfolded_gate_count"])
        self.assertEqual(sp.truth_table(separate), sp.truth_table(shared))

    def test_restriction_preserves_gates_and_wire_slots_without_optimization(self):
        b = sp.Builder(); x, y = b.input("x"), b.input("y")
        pair = b.gate("AND", x, x); root = b.gate("OR", pair, y)
        dag = b.finish("restricted", root)
        restricted = sp.restrict_dag(dag, {"x": 0})
        self.assertEqual(restricted.nodes[0], sp.Node("CONST", value=0))
        self.assertEqual(restricted.nodes[pair].args, (0, 0))
        self.assertEqual(sp.measure_dag(restricted)["S"], 2)
        self.assertEqual(sp.truth_table(restricted), (("y",), (0, 1)))
        for ybit in (0, 1):
            self.assertEqual(sp.evaluate_dag(restricted, {"y": ybit}), sp.evaluate_dag(dag, {"x": 0, "y": ybit}))
        with self.assertRaises(ValueError):
            sp.restrict_dag(dag, {"unknown": 1})

    def test_semantics_distinguish_essential_inputs_from_syntactic_leaves(self):
        dag = self.named("semantically-false-but-syntactically-nonempty")
        names, table = sp.truth_table(dag)
        self.assertEqual(names, ("x",))
        self.assertEqual(table, (0, 0))
        self.assertEqual(sp.essential_inputs(names, table), ())
        self.assertEqual(sp.measure_dag(dag)["literal_leaf_count"], 2)

    def test_invalid_cycles_arities_sources_and_outputs(self):
        bad = [
            sp.DAG("empty", (), 0),
            sp.DAG("output", (sp.Node("CONST", value=0),), 1),
            sp.DAG("self", (sp.Node("NOT", (0,)),), 0),
            sp.DAG("future", (sp.Node("NOT", (1,)), sp.Node("CONST", value=0)), 0),
            sp.DAG("arity", (sp.Node("INPUT", name="x"), sp.Node("AND", (0,))), 1),
            sp.DAG("constant", (sp.Node("CONST", value=2),), 0),
            sp.DAG("duplicate-input", (sp.Node("INPUT", name="x"), sp.Node("INPUT", name="x")), 0),
            sp.DAG("labelled-gate", (sp.Node("INPUT", name="x"), sp.Node("NOT", (0,), name="bad")), 1),
        ]
        for dag in bad:
            with self.subTest(dag=dag.name), self.assertRaises(ValueError):
                sp.validate_dag(dag)
        b = sp.Builder(); x = b.input("x")
        self.assertEqual(x, b.input("x"))
        with self.assertRaises(ValueError):
            b.gate("AND", x)
        with self.assertRaises(ValueError):
            b.gate("NOT", 20)
        with self.assertRaises(ValueError):
            sp.evaluate_dag(b.finish("input", x), {"x": 2})


class UnfoldingAndFiniteSuiteTests(unittest.TestCase):
    def test_small_explicit_trees_match_sizes_paths_and_truth_tables(self):
        audit = sp.Audit()
        for dag in sp.named_dags():
            result = sp.check_dag(dag, audit)
            self.assertTrue(result["explicit_tree_materialized"])
            self.assertTrue(result["semantic"]["truth_table_checked"])
        self.assertTrue(audit.ok, audit.examples)
        self.assertGreater(audit.counts["DAG_vs_unfolded_truth_table"], 100)

    def test_idempotent_chain_exact_counts_and_counterexample(self):
        for mode in ("AND", "OR", "alternating"):
            dag = sp.idempotent_chain(5, mode)
            stats = sp.measure_dag(dag)
            self.assertEqual((stats["S"], stats["R"]), (5, 4))
            self.assertEqual(stats["unfolded_gate_count"], 31)
            self.assertEqual(stats["literal_leaf_count"], 32)
            self.assertEqual(stats["output_to_node_paths"], (32, 16, 8, 4, 2, 1))
            self.assertGreater(stats["unfolded_gate_count"], stats["S"] * (stats["R"] + 1))
            self.assertEqual(sp.truth_table(dag), (("x",), (0, 1)))
            # Compare with the zero-gate formula x; this is not an intrinsic lower bound.
            self.assertEqual(sp.truth_table(sp.idempotent_chain(0)), sp.truth_table(dag))

    def test_selector_diamonds_have_nonidentical_operands_but_still_compute_x(self):
        for length in range(6):
            dag = sp.selector_diamond_chain(length)
            stats = sp.measure_dag(dag)
            self.assertEqual(stats["S"], 4 * length)
            self.assertEqual(stats["R"], max(length - 1, 0))
            self.assertEqual(stats["unfolded_gate_count"], 4 * (2**length - 1))
            self.assertEqual(stats["literal_leaf_count"], 3 * 2**length - 2)
            self.assertEqual(stats["duplicate_wire_slots"], 0)
            self.assertTrue(all(node.args[0] != node.args[1] for node in dag.nodes if node.op in sp.BINARY))
            names, values = sp.truth_table(dag)
            self.assertEqual(values, tuple(bits & 1 for bits in range(1 << (length + 1))))
            self.assertEqual(sp.essential_inputs(names, values), ("x",))
            audit = sp.Audit()
            result = sp.check_dag(dag, audit)
            self.assertTrue(audit.ok, audit.examples)
            self.assertIn("not an intrinsic formula lower bound", result["semantic"]["control_caveat"])

    def test_large_chain_counted_without_materializing_exponential_tree(self):
        dag = sp.idempotent_chain(64)
        stats = sp.measure_dag(dag)
        self.assertEqual((stats["S"], stats["R"]), (64, 63))
        self.assertEqual(stats["unfolded_gate_count"], 2**64 - 1)
        self.assertEqual(stats["literal_leaf_count"], 2**64)
        with self.assertRaises(sp.BudgetExceeded):
            sp.unfold_tree(dag, 10_000)
        audit = sp.Audit()
        result = sp.check_dag(dag, audit)
        self.assertTrue(audit.ok, audit.examples)
        self.assertFalse(result["explicit_tree_materialized"])
        self.assertEqual(result["counts"]["explicit_tree_skipped_node_budget"], 1)

    def test_exhaustive_description_counts_including_all_output_choices(self):
        self.assertEqual(sp.exhaustive_count(-1), 0)
        self.assertEqual(sp.exhaustive_count(0), 4)
        self.assertEqual(sp.exhaustive_count(1), 184)
        self.assertEqual(sp.exhaustive_count(2), 12064)
        self.assertEqual(sum(1 for _ in sp.exhaustive_dags(2)), 12064)
        with self.assertRaises(sp.BudgetExceeded):
            sp.run_experiment(exhaustive_max_gates=3, include_parity=False)

    def test_seeded_dags_reproducible_and_all_small_bounds(self):
        first, second = sp.seeded_dags(50, 112), sp.seeded_dags(50, 112)
        self.assertEqual(first, second)
        self.assertNotEqual([(g.nodes, g.output) for g in first],
                            [(g.nodes, g.output) for g in sp.seeded_dags(50, 113)])
        audit = sp.Audit()
        for dag in first:
            sp.check_dag(dag, audit)
        self.assertTrue(audit.ok, audit.examples)
        self.assertGreater(audit.counts["duplicate_wire_slots_across_DAGs"], 0)
        self.assertGreater(audit.counts["unused_gates_across_DAGs"], 0)

    def test_report_reproducibility_and_additive_witnesses(self):
        kwargs = dict(exhaustive_max_gates=1, seeded_cases=10, max_chain=16, include_parity=False)
        a, b = sp.run_experiment(**kwargs), sp.run_experiment(**kwargs)
        self.assertEqual(a, b)
        self.assertEqual(a["status"], "passed", a["counterexamples_to_asserted_bounds"])
        witness = a["additive_replacements"]["S_times_R_plus_1_counterexample"]
        self.assertEqual((witness["S"], witness["R"], witness["unfolded_gates"]), (5, 4, 31))
        linear = a["additive_replacements"]["constant_multiplier_candidates"]
        self.assertEqual(linear[0]["counterexample"]["S"], 3)
        self.assertTrue(all(row["counterexample"] is not None for row in linear))
        self.assertIn("NOT general proofs", a["claim"])
        self.assertIn("never an intrinsic formula-size lower bound", a["additive_replacements"]["semantic_caveat"])

    def test_CLI_stdout_and_invalid_arguments_do_not_write_files(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = sp.main(["--exhaustive-max-gates", "-1", "--seeded-cases", "0",
                            "--max-chain", "5", "--skip-parity", "--output", "-"])
        self.assertEqual(code, 0)
        output = json.loads(stdout.getvalue())
        self.assertEqual(output["status"], "passed")
        self.assertIsNone(output["universal_quadratic_gate_contraction"])
        self.assertIsNone(output["naive_gate_sqrt_additive_contraction"])
        for args in (["--parity-p", "0"], ["--max-cases", "1"]):
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                sp.main(args + ["--output", "-"])
            self.assertEqual(error.exception.code, 2)

    def test_failure_records_keep_exact_rationals_and_respect_cap(self):
        audit = sp.Audit(limit=1)
        audit.check(False, "deliberate-test", {}, F(1, 3), F(1, 4))
        audit.check(False, "deliberate-test", {}, 2, 1)
        self.assertFalse(audit.ok)
        self.assertEqual(audit.failures["deliberate-test"], 2)
        self.assertEqual(len(audit.examples), 1)
        self.assertEqual(audit.examples[0]["observed"], "1/3")


class SemanticParityTests(unittest.TestCase):
    def test_parity_constructor_and_gate_counts(self):
        for n in range(7):
            dag = sp.parity_dag(n)
            stats = sp.measure_dag(dag)
            self.assertEqual(stats["S"], 4 * n - 3 if n else 0)
            self.assertEqual(stats["reachable_binary_gates"], 3 * max(n - 1, 0))
            _, values = sp.truth_table(dag)
            self.assertEqual(values, tuple(int(bits.bit_count() % 2 == 0) for bits in range(1 << n)))
        with self.assertRaises(sp.BudgetExceeded):
            sp.truth_table(sp.parity_dag(64))

    def test_binomial_hand_values_and_empty_restrictions(self):
        p = F(1, 4)
        self.assertEqual(sp.binomial_binary_lower_bound(0, p)["expected_binary_gate_lower_bound"], 0)
        self.assertEqual(sp.binomial_binary_lower_bound(1, p)["expected_binary_gate_lower_bound"], 0)
        self.assertEqual(sp.binomial_binary_lower_bound(2, p)["expected_binary_gate_lower_bound"], p**2)
        self.assertEqual(sp.binomial_binary_lower_bound(3, p)["expected_binary_gate_lower_bound"], F(11, 64))
        self.assertEqual(sp.binomial_binary_lower_bound(4, p)["expected_binary_gate_lower_bound"], F(81, 256))
        for p in (F(0), F(1), 0.25):
            with self.assertRaises(ValueError):
                sp.binomial_binary_lower_bound(64, p)
        with self.assertRaises(ValueError):
            sp.binomial_binary_lower_bound(-1, F(1, 4))

    def test_small_restricted_parity_semantics_against_complete_enumeration(self):
        audit = sp.Audit()
        result = sp.check_small_parity_restrictions(audit, max_n=4)
        self.assertTrue(audit.ok, audit.examples)
        self.assertEqual(result["counts"]["small_parity_restrictions"], 121)
        self.assertEqual(result["counts"]["residual_parity_truth_table"], 341)
        self.assertEqual(result["counts"]["enumerated_vs_binomial_parity_expectation"], 10)

    def test_requested_N64_exact_semantic_obstruction(self):
        audit = sp.Audit()
        result = sp.check_parity_obstruction(64, F(1, 64), audit)
        self.assertTrue(audit.ok, audit.examples)
        self.assertEqual(result["source_S"], 253)
        self.assertEqual(result["source_binary_gates"], 189)
        self.assertEqual(result["expected_binary_gate_lower_bound"], F(63, 64)**64)
        self.assertEqual(result["p_squared_times_source_S"], F(253, 4096))
        self.assertTrue(result["violates_coefficient_one_bound"])
        self.assertGreater(result["gap"], 0)
        self.assertEqual(result["distribution"]["probability_mass"], 1)
        self.assertEqual(result["distribution"]["restriction_count"], 3**64)
        self.assertEqual(len(result["distribution"]["strata"]), 65)
        self.assertEqual(result["counts"]["large_parity_essential_input_witness"], 4096)
        self.assertEqual(result["counts"]["large_parity_canonical_residual_value"], 129)
        self.assertIn("No promise-correct GapMCSP", result["not_claimed"])

    def test_clean_violation_and_a_nonviolating_instance(self):
        audit = sp.Audit()
        clean = sp.check_parity_obstruction(16, F(1, 8), audit)
        self.assertEqual(clean["source_S"], 61)
        self.assertEqual(clean["expected_binary_gate_lower_bound"], 1 + F(7, 8)**16)
        self.assertEqual(clean["p_squared_times_source_S"], F(61, 64))
        self.assertGreater(clean["expected_binary_gate_lower_bound"], 1)
        self.assertLess(clean["p_squared_times_source_S"], 1)
        self.assertTrue(clean["violates_coefficient_one_bound"])
        other = sp.check_parity_obstruction(4, F(1, 4), audit)
        self.assertFalse(other["violates_coefficient_one_bound"])
        self.assertEqual(other["p_squared_times_source_S"], F(13, 16))
        self.assertTrue(audit.ok, audit.examples)

    def test_sqrt_additive_N256_exact_rational_certificate(self):
        audit = sp.Audit()
        result = sp.check_parity_sqrt_additive_control(audit)
        self.assertTrue(audit.ok, audit.examples)
        self.assertEqual((result["N"], result["p"], result["A"], result["B"]),
                         (256, F(1, 8), F(1), F(1)))
        self.assertEqual(result["source_S"], 1021)
        self.assertEqual(result["source_binary_gates"], 765)
        self.assertEqual(result["sqrt_S_integer_upper_bound"], 32)
        self.assertEqual(result["sqrt_enclosure_squared"],
                         {"floor_squared": 961, "S": 1021, "upper_squared": 1024})
        self.assertEqual(result["p_squared_S"], F(1021, 64))
        self.assertEqual(result["p_sqrt_S_rational_upper_bound"], 4)
        self.assertEqual(result["RHS_rational_upper_bound"], F(1341, 64))
        self.assertEqual(result["expected_size_lower_bound_used"], 31)
        self.assertFalse(result["lower_bound_is_exact_expectation"])
        self.assertEqual(result["certified_gap_lower_bound"], F(643, 64))
        self.assertEqual(result["ratio_lower_to_RHS_upper"], F(1984, 1341))
        self.assertTrue(result["violates_fixed_A_B_bound"])
        self.assertEqual(result["counts"]["sqrt_additive_parity_single_flip_witness"], 256)
        # Independent exact binomial aggregation validates the deliberately weaker
        # lower bound, without serializing 257 strata into the compact control.
        exact = sp.binomial_binary_lower_bound(256, F(1, 8))["expected_binary_gate_lower_bound"]
        self.assertEqual(exact, 31 + F(7, 8)**256)
        self.assertGreater(exact, result["expected_size_lower_bound_used"])
        self.assertIn("A=B=1 only", result["scope"])
        self.assertIn("parent/peer", result["general_argument_deferred"])

    def test_sqrt_additive_control_does_not_enumerate_restrictions_or_trees(self):
        audit = sp.Audit()
        with patch.object(sp, "submasks", side_effect=AssertionError("no restriction enumeration")), \
             patch.object(sp, "truth_table", side_effect=AssertionError("no full truth table")), \
             patch.object(sp, "unfold_tree", side_effect=AssertionError("no explicit unfolded tree")):
            result = sp.check_parity_sqrt_additive_control(audit)
        self.assertTrue(audit.ok, audit.examples)
        self.assertNotIn("distribution", result)
        self.assertNotIn("strata", result)
        self.assertEqual(result["expected_size_lower_bound_used"], 31)

    def test_full_report_parity_sections_and_no_floating_point(self):
        report = sp.run_experiment(exhaustive_max_gates=-1, seeded_cases=0, max_chain=5)
        self.assertEqual(report["status"], "passed", report["counterexamples_to_asserted_bounds"])
        parity = report["universal_quadratic_gate_contraction"]
        self.assertEqual(parity["candidate_bound"], "E SIZE <= p^2*S")
        self.assertIn("p*sqrt(L)", parity["formula_comparison_caveat"])
        additive = report["naive_gate_sqrt_additive_contraction"]
        self.assertEqual(additive["candidate_bound"], "E SIZE <= A*(p^2*S + p*sqrt(S)) + B")
        self.assertEqual(additive["RHS_rational_upper_bound"], "1341/64")
        self.assertTrue(additive["violates_fixed_A_B_bound"])
        self.assertTrue(parity["requested_instance"]["violates_coefficient_one_bound"])
        self.assertTrue(parity["clean_instance"]["violates_coefficient_one_bound"])
        self.assertEqual(parity["small_exhaustive_semantics"]["counts"]["small_parity_restrictions"], 1093)
        self.assertEqual(parity["small_exhaustive_semantics"]["counts"]["residual_parity_truth_table"], 5461)
        def inspect(value):
            self.assertNotIsInstance(value, float)
            if isinstance(value, dict):
                for child in value.values():
                    inspect(child)
            elif isinstance(value, list):
                for child in value:
                    inspect(child)
        inspect(report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
