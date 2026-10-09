"""Regression tests for the finite checker, including hand-computed quantities."""
from contextlib import redirect_stderr, redirect_stdout
from fractions import Fraction as F
from itertools import permutations
import io
import json
from math import comb
import unittest

import restriction_check as rc


class LiteralAndRestrictionTests(unittest.TestCase):
    def test_unique_patterns_indices_and_constants(self):
        source = rc.Formula("normalization", 3,
                            (None, (1, -1), (1, 1, -2), (1, -2), (), (-3,)))
        prepared = rc.prepare_formula(source)
        self.assertEqual(prepared.discarded_true_or_tautological, 2)
        self.assertEqual([c.index for c in prepared.clauses], [1, 2, 3, 4])
        self.assertEqual([c.literals for c in prepared.clauses], [(1, -2), (1, -2), (), (-3,)])
        self.assertEqual(prepared.clauses[0].scope, 0b011)
        self.assertEqual(prepared.clauses[0].violating_pattern, 0b010)
        self.assertEqual(prepared.k, 2)
        for y in range(8):
            self.assertEqual(prepared.clauses[0].violated(y), int(not(y & 1) and bool(y & 2)))
            self.assertEqual(prepared.clauses[2].violated(y), 1)
            self.assertEqual(prepared.clauses[3].violated(y), int(bool(y & 4)))

    def test_restricted_CNF_is_literal_substitution(self):
        raw = ((1, -2, 3), (-1, 2), (2, -2), None, ())
        # Prescribe x1=x3=0, leave x2 live. The second clause becomes true.
        self.assertEqual(rc.restrict_cnf(raw, 0b101, 0), ((-2,), (2, -2), ()))
        for live in range(8):
            for fixed in rc.submasks(7 & ~live):
                reduced = rc.restrict_cnf(raw, 7 & ~live, fixed)
                for z in rc.submasks(live):
                    self.assertEqual(rc.cnf_value(reduced, z), rc.cnf_value(raw, fixed | z))

    def test_empty_true_false_and_empty_live_sets(self):
        for d in (0, 2):
            for raw, truth in (((), 1), ((None,), 1), (((),), 0), (((), (), None), 0)):
                prepared = rc.prepare_formula(rc.Formula("constant", d, raw))
                for fixed in range(1 << d):
                    weights, paths = rc.path_weights(prepared, 0, fixed, 1)
                    self.assertEqual(sum(weights), 1)
                    self.assertFalse(paths)
                    self.assertEqual(rc.cnf_value(raw, fixed), truth)

    def test_invalid_inputs_and_integer_b(self):
        for source in (rc.Formula("bad", 1, ((0,),)), rc.Formula("bad", 1, ((2,),)),
                       rc.Formula("bad", 0, ((1,),)), rc.Formula("bad", 7, ()),
                       rc.Formula("bad", 2, ((1, 2),), declared_k=1)):
            with self.assertRaises(ValueError):
                rc.prepare_formula(source)
        for b in (0, -1, F(1, 2), True):
            with self.assertRaises(ValueError):
                rc.theta(2, b, F(1, 4))
        for p in (F(0), F(1), F(-1, 2), 0.25):
            with self.assertRaises(ValueError):
                rc.theta(2, 1, p)
        prepared = rc.prepare_formula(rc.Formula("bits", 2, ((1, 2),)))
        for live, fixed in ((1, 1), (4, 0), (0, 4), (-1, 0)):
            with self.assertRaises(ValueError):
                rc.path_weights(prepared, live, fixed, 1)

    def test_theta_exact_values(self):
        self.assertEqual(rc.theta(2, 1, F(1, 8)), F(4, 49))
        self.assertEqual(rc.theta(2, 1, F(1, 4)), F(4, 9))
        self.assertEqual(rc.theta(3, 1, F(1, 4)), F(44, 27))
        self.assertEqual(rc.theta(6, 1, F(1, 4)), F(11980, 729))
        self.assertEqual(rc.theta(0, 1, F(1, 4)), 0)
        self.assertEqual(rc.theta(2, 2, F(1, 4)), 0)


class PathAndMixtureTests(unittest.TestCase):
    def weights(self, raw, d, b=1, live=None, fixed=0):
        source = rc.Formula("hand-computed", d, raw)
        return rc.path_weights(rc.prepare_formula(source), (1 << d) - 1 if live is None else live, fixed, b)

    def test_repeated_clauses_do_not_lose_indexed_multiplicities(self):
        weights, paths = self.weights(((1, 2),) * 7, 2)
        self.assertEqual(weights, (F(1), F(1)))
        self.assertEqual(len(paths), 7)
        self.assertEqual(len({p.path.indices for p in paths}), 7)
        self.assertTrue(all(p.c_counts == (7,) and p.weight == F(1, 7) for p in paths))

    def test_false_clause_contributes_to_c_even_when_K_is_false(self):
        weights, paths = self.weights(((1, 2), (1, 2), (), None, (1, -1)), 2)
        self.assertEqual(weights, (F(1), F(2, 3)))
        self.assertTrue(all(p.c_counts == (3,) and p.weight == F(1, 3) for p in paths))
        self.assertEqual(len(paths), 2)

    def test_unselected_closed_clauses_are_counted_literally(self):
        weights, paths = self.weights(((1, 2), (1,), (-1,), ()), 2)
        self.assertEqual(weights, (F(1), F(1, 3)))
        self.assertEqual(paths[0].c_counts, (3,))  # selected + (1,) + false, not (-1,)

    def test_three_steps_and_unequal_repetitions(self):
        for raw in (((1, 2), (3, 4), (5, 6)),
                    ((1, 2), (3, 4), (3, 4), (5, 6), (5, 6), (5, 6))):
            weights, paths = self.weights(raw, 6)
            self.assertEqual(weights, (F(1), F(3), F(3), F(1)))
            self.assertEqual(max(len(p.path.indices) for p in paths), 3)
        weights, _ = self.weights(((1, 2, 3), (4, 5, 6)), 6, b=2)
        self.assertEqual(weights, (F(1), F(2), F(1)))

    def test_overlapping_compatible_and_incompatible_paths(self):
        good, good_paths = self.weights(((1, 2), (1, 3, 4)), 4)
        bad, bad_paths = self.weights(((1, 2), (-1, 3, 4)), 4)
        self.assertEqual(good, (F(1), F(2), F(1, 2)))
        self.assertEqual(bad, (F(1), F(2), F(0)))
        self.assertEqual([p.path.indices for p in good_paths], [(0,), (0, 1), (1,)])
        incompatible = next(p for p in bad_paths if len(p.path.indices) == 2)
        self.assertFalse(incompatible.compatible)
        self.assertEqual(incompatible.weight, 0)

    def test_compatibility_with_fixed_assignment(self):
        # Clause x1 OR not x2 OR x3: violating pattern is x1=0,x2=1,x3=0.
        incompatible, paths = self.weights(((1, -2, 3),), 3, live=0b101, fixed=0)
        compatible, good_paths = self.weights(((1, -2, 3),), 3, live=0b101, fixed=0b010)
        self.assertEqual(incompatible[1], 0)
        self.assertFalse(paths[0].compatible)
        self.assertEqual(compatible[1], 1)
        self.assertTrue(good_paths[0].compatible)
        self.assertEqual(good_paths[0].sigma, 0)

    def test_I_h_keeps_final_true_false_and_repeated_clauses(self):
        _, paths = self.weights(((1, 2), (3, 4), (1, 3), (1, 3), (1, -3)), 4)
        path = next(p for p in paths if p.path.indices == (0, 1))
        self.assertEqual(path.c_counts, (1, 4))
        self.assertEqual(path.weight, F(1, 4))
        self.assertEqual(path.mixture_families, (((), (), None), ()))
        mixture = rc.marker_mixture_value(3, 1, 2) * rc.marker_mixture_value(0, 4, 0)
        self.assertEqual(path.weight * mixture, F(1, 12))

    def test_marker_mixture_against_literal_permutations(self):
        # Enumerate actual labelled objects, independent of factorial subset counts.
        for a in range(5):
            for c in range(1, 4):
                totals = [0] * (a + 1)
                permutations_count = 0
                for ordering in permutations(range(a + c)):
                    prefix = []
                    for obj in ordering:
                        if obj >= a:
                            break
                        prefix.append(obj)
                    permutations_count += 1
                    for w in range(a + 1):
                        totals[w] += int(not any(obj < w for obj in prefix))
                for w in range(a + 1):
                    with self.subTest(a=a, c=c, w=w):
                        direct = F(totals[w], permutations_count)
                        self.assertEqual(rc.marker_mixture_value(a, c, w), direct)
                        self.assertEqual(direct, F(c, c + w))
        # Actual clauses including repeated, false and true objects.
        family = (None, (), (1,), (1,), (-1,))
        for y in (0, 1):
            a, c, successes, total = len(family), 2, 0, 0
            for ordering in permutations(range(a + c)):
                conjunction = 1
                for obj in ordering:
                    if obj >= a:
                        break
                    conjunction &= rc.clause_value(family[obj], y)
                successes += conjunction
                total += 1
            w = sum(1 - rc.clause_value(clause, y) for clause in family)
            self.assertEqual(rc.marker_mixture_value(a, c, w), F(successes, total))

    def test_reverse_recurrence_keeps_false_clause_in_denominator(self):
        prepared = rc.prepare_formula(rc.Formula("reverse", 2, ((1, 2), (1, 2), ())))
        table = rc.reverse_tables(prepared, (1, 1, 1), 1, F(1, 4))
        self.assertEqual(table[0], (F(1),) * 4)
        self.assertEqual(table[1], (F(8, 27), F(0), F(0), F(0)))

    def test_clause_permutation_and_discarded_true_padding_invariance(self):
        raw = ((1, 2), (-1, 3), (1, 2), (2, 3))
        p = rc.prepare_formula(rc.Formula("original", 3, raw))
        q = rc.prepare_formula(rc.Formula("permuted", 3, (None, (2, -2)) + tuple(reversed(raw))))
        for live in range(8):
            for fixed in rc.submasks(7 & ~live):
                self.assertEqual(rc.path_weights(p, live, fixed, 1)[0], rc.path_weights(q, live, fixed, 1)[0])

    def test_path_budget_prevents_explosion(self):
        prepared = rc.prepare_formula(rc.Formula("budget", 2, ((1, 2),) * 5))
        with self.assertRaises(rc.BudgetExceeded):
            rc.scope_paths(prepared, 3, 1, max_paths=3)


class ExhaustiveAndExpectationTests(unittest.TestCase):
    def test_single_clause_exact_expectations(self):
        for copies in (1, 5):
            audit = rc.Audit()
            result = rc.check_formula(rc.Formula("single/repeated", 2, ((1, 2),) * copies), 1, audit=audit)
            self.assertTrue(audit.ok, audit.counterexamples)
            for entry in result["expectations"]:
                self.assertEqual(entry["E_W_j"], (F(1), entry["p"]**2))
                self.assertEqual(entry["E_W"], 1 + entry["p"]**2)

    def test_disjoint_pairs_exact_nontrivial_expectations(self):
        audit = rc.Audit()
        result = rc.check_formula(rc.Formula("two-pairs", 4, ((1, 2), (3, 4))), 1, audit=audit)
        self.assertTrue(audit.ok, audit.counterexamples)
        expected = {F(1, 8): (F(1), F(463, 16384), F(1, 4096)),
                    F(1, 4): (F(1), F(119, 1024), F(1, 256))}
        for entry in result["expectations"]:
            self.assertEqual(entry["E_W_j"], expected[entry["p"]])
        self.assertEqual(result["counts"]["restrictions"], 81)
        self.assertEqual(result["counts"]["pointwise_expansion"], 256)

    def test_geometric_comparison_only_when_theta_less_than_one(self):
        audit = rc.Audit()
        result = rc.check_formula(rc.Formula("wide", 3, ((1, 2, 3),)), 1, audit=audit)
        self.assertTrue(audit.ok, audit.counterexamples)
        first, second = result["expectations"]
        self.assertTrue(first["geometric_comparison_performed"])
        self.assertFalse(second["geometric_comparison_performed"])
        self.assertIsNone(second["geometric_bound"])
        self.assertEqual(second["E_W_j"][1], F(11, 128))
        self.assertEqual(result["counts"]["expected_W_j_bound"], 4)
        self.assertEqual(result["counts"]["geometric_bound_skipped_theta_ge_1"], 1)

    def test_all_small_pair_multisets_and_both_cutoffs(self):
        report = rc.run_experiment(exhaustive_max_d=2, chosen_max_d=0,
                                   random_cases=0, reverse_checks="all", include_parity=False)
        self.assertEqual(report["status"], "passed", report["all_counterexamples"])
        self.assertEqual(report["exhaustive_formula_count"], 68)
        self.assertEqual(report["formula_count"], 71)
        self.assertEqual(report["formula_b_pairs"], 142)
        self.assertEqual(report["original_lemma"]["counts"]["restrictions"], 1062)
        self.assertEqual(report["original_lemma"]["counts"]["pointwise_expansion"], 1852)
        self.assertEqual(report["all_counterexamples"], [])

    def test_exhaustive_scope_and_formula_budgets(self):
        self.assertEqual(rc.exhaustive_formula_count(4, 2), 3877)
        self.assertEqual(len(rc.canonical_clauses(4)), 81)
        self.assertEqual(len(set(rc.canonical_clauses(4))), 81)
        self.assertEqual(len(list(rc.exhaustive_formulas(2, 2))), 68)
        self.assertEqual(rc.exhaustive_formula_count(-1, 2), 0)
        with self.assertRaises(rc.BudgetExceeded):
            rc.run_experiment(exhaustive_max_d=6, max_formulas=10_000, include_parity=False)

    def test_seeded_stream_and_results_are_reproducible(self):
        self.assertEqual(rc.chosen_formulas(3, 112, 2), rc.chosen_formulas(3, 112, 2))
        self.assertNotEqual([c.raw for c in rc.chosen_formulas(3, 112, 2) if c.suite == "seeded"],
                            [c.raw for c in rc.chosen_formulas(3, 113, 2) if c.suite == "seeded"])
        config = dict(exhaustive_max_d=1, chosen_max_d=1, random_cases=1, include_parity=False)
        first, second = rc.run_experiment(**config), rc.run_experiment(**config)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "passed")
        self.assertIn("NOT a proof", first["claim"])
        self.assertEqual(first["config"]["p"], ["1/8", "1/4"])

    def test_counterexample_records_are_bounded_and_exact(self):
        audit = rc.Audit(max_counterexamples=1)
        audit.check(False, "test", {"formula": "deliberate test failure"}, F(1, 3), F(1, 4))
        audit.check(False, "test", {}, F(2, 3), F(1, 4))
        self.assertFalse(audit.ok)
        self.assertEqual(audit.failures["test"], 2)
        self.assertEqual(len(audit.counterexamples), 1)
        self.assertEqual(audit.counterexamples[0]["observed"], "1/3")

    def test_CLI_stdout_no_files_and_invalid_options(self):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = rc.main(["--exhaustive-max-d", "-1", "--chosen-max-d", "0",
                                 "--random-cases", "0", "--skip-parity", "--output", "-"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(output.getvalue())["status"], "passed")
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            rc.main(["--b", "0", "--skip-parity", "--output", "-"])
        self.assertEqual(error.exception.code, 2)


class SeparateNaiveExtensionTests(unittest.TestCase):
    def test_d6_parity_primal_dual_and_exact_counterexample(self):
        audit = rc.Audit()
        result = rc.check_naive_parity_extension(audit)
        self.assertTrue(audit.ok, audit.counterexamples)
        self.assertTrue(result["claim_verified"])
        self.assertEqual(result["naive_theta"], F(4, 9))
        self.assertEqual(result["naive_geometric_bound"], F(9, 5))
        self.assertEqual(result["exact_expected_minimal_W"], F(15625, 8192))
        self.assertEqual(result["strict_gap"], F(4397, 40960))
        self.assertEqual(result["counts"]["parity_restrictions"], 729)
        self.assertEqual(result["counts"]["parity_subcube_correlations"], 15625)
        self.assertEqual(result["counts"]["parity_primal_pointwise"], 4096)
        for entry in result["by_live_dimension"]:
            m = entry["m"]
            self.assertEqual(entry["restrictions"], comb(6, m) * 2**(6-m))
            self.assertEqual(entry["average_minimal_W"], F(2**m, 2))
        self.assertEqual(result["original_CNF"]["clause_count"], 32)
        self.assertEqual(result["original_CNF"]["theta_at_same_b_p"], F(11980, 729))
        self.assertFalse(result["original_CNF"]["geometric_hypothesis_satisfied"])
        self.assertIn("NOT to the original lemma", result["scope"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
