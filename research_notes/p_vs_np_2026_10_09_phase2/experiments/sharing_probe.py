#!/usr/bin/env python3
"""Bounded exact tests of DAG sharing, syntactic unfolding, and gate shrinkage.

FINITE COMPUTATIONS, NOT GENERAL PROOFS.  No Phase 1 code is imported or changed.

Model: one output; topologically ordered AND/OR (fanin 2) and NOT (fanin 1)
gates; inputs and constants are sources, not gates.  Operand slots are WIRES:
AND(v,v) has two wires, although v is one node.  S counts reachable gates once.
R sums max(0, reachable outdegree - 1) over internal gates ONLY, excluding reused
primary inputs and constants.  Unused consumers do not increase that fan-out.

"leaf_count" includes input and constant leaves.  "literal_leaf_count" counts
input occurrences only; NOT is an explicit gate, even immediately above a leaf.
Unfolding is syntactic: no idempotence, constant propagation, or optimization.

Default: all descriptions with <=2 gates over two inputs and two constants,
200 seeded small DAGs, idempotent chains through length 64, and parity tests.
Every integer and probability is exact.  Large unfolded trees are counted by
DP, never materialized beyond an explicit node budget.  The N=64 restriction
expectation uses a binomial sum, not enumeration of 3**64 restrictions.
A SEPARATE N=256 control tests the naive gate analogue with p*sqrt(S) and an
additive constant, at A=B=1 only.  An integer square-root enclosure bounds its
RHS rationally; no 3**256 restrictions or exponentially large trees are built.
Neither gate control is claimed to refute the audited formula-leaf bound.

Usage:
  python3 -B sharing_probe.py --self-test
  python3 -B sharing_probe.py
  python3 -B sharing_probe.py --exhaustive-max-gates 1 --seeded-cases 10 \
      --max-chain 8 --output -
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import chain, product
import json
from math import comb, isqrt, prod
from pathlib import Path
import random
import sys
import unittest
from typing import Iterator

GATES = frozenset(("AND", "OR", "NOT"))
BINARY = frozenset(("AND", "OR"))
SOURCES = frozenset(("INPUT", "CONST"))
ARITY = {"INPUT": 0, "CONST": 0, "NOT": 1, "AND": 2, "OR": 2}
ZERO, ONE = Fraction(0), Fraction(1)


def jsonable(value):
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(v) for v in value]
    return value


@dataclass(frozen=True)
class Node:
    op: str
    args: tuple[int, ...] = ()
    name: str | None = None
    value: int | None = None


@dataclass(frozen=True)
class DAG:
    name: str
    nodes: tuple[Node, ...]
    output: int
    suite: str = "chosen"

    def description(self) -> dict:
        return {"name": self.name, "suite": self.suite, "output": self.output,
                "nodes": [{"id": i, "op": n.op, "args": n.args, "name": n.name,
                           "value": n.value} for i, n in enumerate(self.nodes)]}


class Builder:
    """Append gates WITHOUT simplification or structural hash-consing."""
    def __init__(self):
        self.nodes: list[Node] = []
        self.inputs: dict[str, int] = {}
        self.constants: dict[int, int] = {}

    def input(self, name: str) -> int:
        if name not in self.inputs:
            self.inputs[name] = len(self.nodes)
            self.nodes.append(Node("INPUT", name=name))
        return self.inputs[name]

    def constant(self, value: int) -> int:
        if type(value) is not int or value not in (0, 1):
            raise ValueError("a constant must be the integer 0 or 1")
        if value not in self.constants:
            self.constants[value] = len(self.nodes)
            self.nodes.append(Node("CONST", value=value))
        return self.constants[value]

    def gate(self, op: str, *args: int) -> int:
        if op not in GATES or len(args) != ARITY[op]:
            raise ValueError("AND/OR need two operand slots; NOT needs one")
        if any(type(a) is not int or not 0 <= a < len(self.nodes) for a in args):
            raise ValueError("operands must be existing node IDs")
        index = len(self.nodes)
        self.nodes.append(Node(op, tuple(args)))
        return index

    def finish(self, name: str, output: int, suite: str = "chosen") -> DAG:
        dag = DAG(name, tuple(self.nodes), output, suite)
        validate_dag(dag)
        return dag


def validate_dag(dag: DAG) -> None:
    if not dag.nodes or type(dag.output) is not int or not 0 <= dag.output < len(dag.nodes):
        raise ValueError("a DAG needs a valid single output node")
    names = set()
    for i, node in enumerate(dag.nodes):
        if node.op not in ARITY or len(node.args) != ARITY[node.op]:
            raise ValueError(f"invalid operation or arity at node {i}")
        if any(type(a) is not int or not 0 <= a < i for a in node.args):
            raise ValueError("node IDs must be topological: no future, self, or cyclic references")
        if node.op == "INPUT":
            if not isinstance(node.name, str) or not node.name or node.name in names or node.value is not None:
                raise ValueError("inputs need distinct nonempty names and no constant value")
            names.add(node.name)
        elif node.op == "CONST":
            if node.name is not None or type(node.value) is not int or node.value not in (0, 1):
                raise ValueError("constants need a bit value and no input name")
        elif node.name is not None or node.value is not None:
            raise ValueError("internal gates have no source labels")


def reachable_nodes(dag: DAG) -> tuple[int, ...]:
    reached, pending = set(), [dag.output]
    while pending:
        node = pending.pop()
        if node not in reached:
            reached.add(node)
            pending.extend(dag.nodes[node].args)
    return tuple(sorted(reached))


def measure_dag(dag: DAG) -> dict:
    """Two independent counting directions: downward paths and upward tree sizes."""
    validate_dag(dag)
    reachable = reachable_nodes(dag)
    reached = set(reachable)
    internal = tuple(i for i in reachable if dag.nodes[i].op in GATES)
    n = len(dag.nodes)
    declared_outdegree, outdegree = [0] * n, [0] * n
    for i, node in enumerate(dag.nodes):
        for operand in node.args:  # Deliberately NOT set(node.args).
            declared_outdegree[operand] += 1
            if i in reached:
                outdegree[operand] += 1
    paths = [0] * n
    paths[dag.output] = 1  # The zero-length output-to-itself path.
    for i in reversed(reachable):
        for operand in dag.nodes[i].args:
            paths[operand] += paths[i]
    gate_sizes, binary_sizes = [0] * n, [0] * n
    literals, constants = [0] * n, [0] * n
    for i in reachable:
        node = dag.nodes[i]
        # No memoized tree object: these are only exact integer occurrence counts.
        gate_sizes[i] = int(node.op in GATES) + sum(gate_sizes[a] for a in node.args)
        binary_sizes[i] = int(node.op in BINARY) + sum(binary_sizes[a] for a in node.args)
        literals[i] = int(node.op == "INPUT") + sum(literals[a] for a in node.args)
        constants[i] = int(node.op == "CONST") + sum(constants[a] for a in node.args)
    s = len(internal)
    r = sum(max(0, outdegree[i] - 1) for i in internal)
    fanout_product = prod(max(1, outdegree[i]) for i in internal)
    root = dag.output
    return {
        "S": s, "declared_S": sum(node.op in GATES for node in dag.nodes),
        "unused_gates": sum(node.op in GATES for node in dag.nodes) - s,
        "reachable_nodes": reachable, "internal_nodes": internal,
        "reachable_binary_gates": sum(dag.nodes[i].op in BINARY for i in internal),
        "reachable_NOT_gates": sum(dag.nodes[i].op == "NOT" for i in internal),
        "reachable_wire_slots": sum(len(dag.nodes[i].args) for i in reachable),
        "duplicate_wire_slots": sum(len(dag.nodes[i].args) - len(set(dag.nodes[i].args)) for i in reachable),
        "outdegree": tuple(outdegree), "declared_outdegree": tuple(declared_outdegree),
        "internal_fanout": {i: outdegree[i] for i in internal},
        "excluded_input_surplus": sum(max(0, outdegree[i] - 1) for i in reachable if dag.nodes[i].op == "INPUT"),
        "excluded_constant_surplus": sum(max(0, outdegree[i] - 1) for i in reachable if dag.nodes[i].op == "CONST"),
        "R": r, "outdegree_product": fanout_product,
        "output_to_node_paths": tuple(paths),
        "unfolded_gate_count": gate_sizes[root], "unfolded_binary_gate_count": binary_sizes[root],
        "literal_leaf_count": literals[root], "constant_leaf_count": constants[root],
        "leaf_count": literals[root] + constants[root],
        "unfolded_total_nodes": gate_sizes[root] + literals[root] + constants[root],
        "gate_bound_S_2R": s * 2**r, "gate_bound_S_product": s * fanout_product,
        "leaf_bound_1_S_2R": 1 + s * 2**r,
        "leaf_bound_1_S_product": 1 + s * fanout_product,
    }


@dataclass(frozen=True)
class Tree:
    source_id: int
    op: str
    children: tuple[Tree, ...]
    name: str | None = None
    value: int | None = None


class BudgetExceeded(RuntimeError):
    pass


def unfold_tree(dag: DAG, max_nodes: int = 10_000) -> Tree:
    """Explicitly copy EVERY operand slot, but refuse exponentially large trees."""
    if max_nodes < 1 or measure_dag(dag)["unfolded_total_nodes"] > max_nodes:
        raise BudgetExceeded("explicit unfolded tree exceeds its node budget")
    created = 0

    def copy(i: int) -> Tree:
        nonlocal created
        created += 1
        if created > max_nodes:
            raise BudgetExceeded("explicit unfolded tree exceeded its node budget while copying")
        node = dag.nodes[i]
        return Tree(i, node.op, tuple(copy(a) for a in node.args), node.name, node.value)

    return copy(dag.output)


def tree_measurements(tree: Tree) -> dict:
    paths: Counter = Counter()
    counts: Counter = Counter()
    pending = [tree]
    while pending:
        node = pending.pop()
        paths[node.source_id] += 1
        counts["gates"] += int(node.op in GATES)
        counts["binary"] += int(node.op in BINARY)
        counts["literals"] += int(node.op == "INPUT")
        counts["constants"] += int(node.op == "CONST")
        pending.extend(node.children)
    return {**counts, "paths": paths}


def evaluate_dag(dag: DAG, assignment: dict[str, int]) -> int:
    values = {}
    for i in reachable_nodes(dag):
        node = dag.nodes[i]
        if node.op == "INPUT":
            value = assignment[node.name]
            if type(value) is not int or value not in (0, 1):
                raise ValueError("assignments must use integer bits")
        elif node.op == "CONST":
            value = node.value
        elif node.op == "NOT":
            value = 1 - values[node.args[0]]
        elif node.op == "AND":
            value = values[node.args[0]] & values[node.args[1]]
        else:
            value = values[node.args[0]] | values[node.args[1]]
        values[i] = value
    return values[dag.output]


def evaluate_tree(tree: Tree, assignment: dict[str, int]) -> int:
    if tree.op == "INPUT":
        return assignment[tree.name]
    if tree.op == "CONST":
        return tree.value
    if tree.op == "NOT":
        return 1 - evaluate_tree(tree.children[0], assignment)
    left, right = (evaluate_tree(child, assignment) for child in tree.children)
    return left & right if tree.op == "AND" else left | right


def restrict_dag(dag: DAG, fixed: dict[str, int]) -> DAG:
    """Substitute source constants, preserving all gates and repeated wire slots."""
    known = {node.name for node in dag.nodes if node.op == "INPUT"}
    if any(name not in known or type(bit) is not int or bit not in (0, 1) for name, bit in fixed.items()):
        raise ValueError("restriction must assign known inputs to integer bits")
    nodes = tuple(Node("CONST", value=fixed[n.name]) if n.op == "INPUT" and n.name in fixed else n
                  for n in dag.nodes)
    result = DAG(dag.name + "-restricted", nodes, dag.output, dag.suite)
    validate_dag(result)
    return result


def input_names(dag: DAG) -> tuple[str, ...]:
    return tuple(dag.nodes[i].name for i in reachable_nodes(dag) if dag.nodes[i].op == "INPUT")


def truth_table(dag: DAG, max_inputs: int = 12) -> tuple[tuple[str, ...], tuple[int, ...]]:
    names = input_names(dag)
    if len(names) > max_inputs:
        raise BudgetExceeded("truth table exceeds its input budget; use semantic witnesses instead")
    values = tuple(evaluate_dag(dag, {name: (bits >> i) & 1 for i, name in enumerate(names)})
                   for bits in range(1 << len(names)))
    return names, values


def essential_inputs(names: tuple[str, ...], values: tuple[int, ...]) -> tuple[str, ...]:
    if len(values) != 1 << len(names):
        raise ValueError("truth table length does not match its variable list")
    return tuple(name for i, name in enumerate(names)
                 if any(values[bits] != values[bits ^ (1 << i)] for bits in range(len(values))))


class Audit:
    def __init__(self, limit: int = 20):
        self.counts: Counter = Counter()
        self.failures: Counter = Counter()
        self.examples: list[dict] = []
        self.limit = limit

    def check(self, condition: bool, kind: str, context: dict, observed=None, expected=None) -> None:
        self.counts[kind] += 1
        if not condition:
            self.failures[kind] += 1
            if len(self.examples) < self.limit:
                self.examples.append(jsonable({"check": kind, **context, "observed": observed, "expected": expected}))

    @property
    def ok(self) -> bool:
        return not self.failures


def check_dag(dag: DAG, audit: Audit, *, materialize_limit: int = 10_000,
              truth_input_limit: int = 6) -> dict:
    before = audit.counts.copy()
    stats = measure_dag(dag)
    context = {"dag": dag.description()}
    nodes, paths = dag.nodes, stats["output_to_node_paths"]
    audit.counts["DAG_descriptions"] += 1
    audit.counts["reachable_gate_occurrences_across_DAGs"] += stats["S"]
    audit.counts["reachable_wire_slots_across_DAGs"] += stats["reachable_wire_slots"]
    audit.counts["duplicate_wire_slots_across_DAGs"] += stats["duplicate_wire_slots"]
    audit.counts["unused_gates_across_DAGs"] += stats["unused_gates"]
    audit.check(sum(stats["outdegree"]) == stats["reachable_wire_slots"], "wire_slot_accounting", context)
    audit.check(paths[dag.output] == 1, "output_zero_length_path", context)
    for i in range(len(nodes)):
        audit.check((paths[i] > 0) == (i in stats["reachable_nodes"]), "path_reachability", {**context, "node": i})
    for i in stats["internal_nodes"]:
        audit.check(paths[i] <= stats["outdegree_product"], "internal_path_product_bound", {**context, "node": i},
                    paths[i], stats["outdegree_product"])
    audit.check(stats["outdegree_product"] <= 2**stats["R"], "product_vs_surplus_bound", context,
                stats["outdegree_product"], 2**stats["R"])
    for kind, op, key in (("gate_path_sum", GATES, "unfolded_gate_count"),
                          ("binary_path_sum", BINARY, "unfolded_binary_gate_count"),
                          ("literal_path_sum", {"INPUT"}, "literal_leaf_count"),
                          ("constant_path_sum", {"CONST"}, "constant_leaf_count")):
        summed = sum(paths[i] for i, node in enumerate(nodes) if node.op in op)
        audit.check(summed == stats[key], kind, context, summed, stats[key])
    for target, bound, kind in (
        ("unfolded_gate_count", "gate_bound_S_2R", "unfolded_gate_S_2R_bound"),
        ("unfolded_gate_count", "gate_bound_S_product", "unfolded_gate_product_bound"),
        ("leaf_count", "leaf_bound_1_S_2R", "total_leaf_S_2R_bound"),
        ("leaf_count", "leaf_bound_1_S_product", "total_leaf_product_bound"),
        ("literal_leaf_count", "leaf_bound_1_S_2R", "literal_leaf_S_2R_bound"),
    ):
        audit.check(stats[target] <= stats[bound], kind, context, stats[target], stats[bound])
    audit.check(stats["leaf_count"] == stats["unfolded_binary_gate_count"] + 1,
                "unfolded_binary_tree_leaf_identity", context, stats["leaf_count"], stats["unfolded_binary_gate_count"] + 1)
    tree = None
    if stats["unfolded_total_nodes"] <= materialize_limit:
        tree = unfold_tree(dag, materialize_limit)
        explicit = tree_measurements(tree)
        audit.counts["explicit_unfolded_trees"] += 1
        audit.counts["explicit_unfolded_tree_nodes"] += sum(explicit["paths"].values())
        for name, key in (("gates", "unfolded_gate_count"), ("binary", "unfolded_binary_gate_count"),
                          ("literals", "literal_leaf_count"), ("constants", "constant_leaf_count")):
            audit.check(explicit.get(name, 0) == stats[key], "explicit_tree_size", context, explicit.get(name, 0), stats[key])
        audit.check(tuple(explicit["paths"][i] for i in range(len(nodes))) == paths,
                    "explicit_tree_path_multiplicities", context)
    else:
        audit.counts["explicit_tree_skipped_node_budget"] += 1
    names = input_names(dag)
    semantic = {"input_names": names, "truth_table_checked": False, "essential_inputs": None}
    if len(names) <= truth_input_limit:
        names, values = truth_table(dag)
        essential = essential_inputs(names, values)
        semantic.update(truth_table_checked=True, essential_inputs=essential, values=values)
        audit.counts["truth_table_rows"] += len(values)
        audit.check(stats["reachable_binary_gates"] >= max(len(essential) - 1, 0),
                    "semantic_binary_support_lower_bound", context, stats["reachable_binary_gates"], max(len(essential) - 1, 0))
        for bits, value in enumerate(values):
            assignment = {name: (bits >> i) & 1 for i, name in enumerate(names)}
            if tree is not None:
                audit.check(evaluate_tree(tree, assignment) == value, "DAG_vs_unfolded_truth_table", {**context, "bits": bits},
                            evaluate_tree(tree, assignment), value)
    else:
        audit.counts["truth_table_skipped_input_budget"] += 1
    if dag.suite == "selector-diamond":
        audit.check(all(len(set(node.args)) == 2 for node in dag.nodes if node.op in BINARY),
                    "selector_distinct_binary_operands", context)
        if semantic["truth_table_checked"]:
            x_position = names.index("x")
            audit.check(values == tuple((bits >> x_position) & 1 for bits in range(len(values))),
                        "selector_diamond_computes_x", context)
        semantic["control_caveat"] = "Non-identical-input selector diamonds still compute x; syntactic unfolding is not an intrinsic formula lower bound."
    return {"dag": dag.description(), "measurements": stats, "semantic": semantic,
            "explicit_tree_materialized": tree is not None, "counts": dict(audit.counts - before)}


def idempotent_chain(length: int, mode: str = "alternating") -> DAG:
    if type(length) is not int or length < 0 or mode not in ("AND", "OR", "alternating"):
        raise ValueError("invalid idempotent chain length or mode")
    b = Builder()
    current = b.input("x")
    for i in range(length):
        op = ("AND" if i % 2 == 0 else "OR") if mode == "alternating" else mode
        current = b.gate(op, current, current)
    return b.finish(f"idempotent-{mode}-{length}", current, "idempotent")


def selector_diamond_chain(length: int) -> DAG:
    """Repeated (s AND v) OR ((NOT s) AND v), with distinct binary operands.

    Fresh selectors keep each diamond's two inputs non-identical. The result is
    still x, so a zero-gate formula exists regardless of syntactic unfolding.
    """
    if type(length) is not int or not 0 <= length <= 128:
        raise ValueError("selector diamond length must be an integer in 0..128")
    b = Builder()
    current = b.input("x")
    for i in range(length):
        selector = b.input(f"selector{i}")
        negated = b.gate("NOT", selector)
        left = b.gate("AND", selector, current)
        right = b.gate("AND", negated, current)
        current = b.gate("OR", left, right)
    return b.finish(f"selector-diamonds-{length}", current, "selector-diamond")


def parity_dag(n: int) -> DAG:
    """Even parity with four AND/OR/NOT gates per XOR, then one output NOT.

    XOR(a,b) = (a OR b) AND NOT(a AND b).  a/b references are really shared,
    not copied subcircuits.  For n>=1 the reachable gate count is exactly 4n-3.
    """
    if type(n) is not int or n < 0:
        raise ValueError("parity input count must be a nonnegative integer")
    b = Builder()
    inputs = [b.input(f"x{i}") for i in range(n)]
    if not n:
        return b.finish("even-parity-0", b.constant(1), "parity")
    current = inputs[0]
    for source in inputs[1:]:
        either = b.gate("OR", current, source)
        both = b.gate("AND", current, source)
        not_both = b.gate("NOT", both)
        current = b.gate("AND", either, not_both)
    current = b.gate("NOT", current)
    return b.finish(f"even-parity-{n}", current, "parity")


def named_dags() -> tuple[DAG, ...]:
    result = []
    b = Builder(); x = b.input("x")
    result.append(b.finish("input-is-output", x))
    for value in (0, 1):
        b = Builder(); c = b.constant(value)
        result.append(b.finish(f"constant-{value}-output", c))
    b = Builder(); x = b.input("x")
    result.append(b.finish("duplicate-primary-wire", b.gate("AND", x, x)))
    b = Builder(); x, y = b.input("x"), b.input("y")
    a, c = b.gate("AND", x, y), b.gate("OR", x, y)
    result.append(b.finish("only-primary-inputs-reused", b.gate("AND", a, c)))
    b = Builder(); x, y, z = (b.input(name) for name in ("x", "y", "z"))
    a = b.gate("NOT", x)
    left, right = b.gate("AND", a, y), b.gate("OR", a, z)
    result.append(b.finish("reconvergent-diamond", b.gate("AND", left, right)))
    b = Builder(); x = b.input("x"); a = b.gate("NOT", x)
    pair = b.gate("AND", a, a)
    result.append(b.finish("internal-fanout-three", b.gate("OR", pair, a)))
    b = Builder(); x = b.input("x"); a = b.gate("NOT", x)
    left, right = b.gate("AND", a, a), b.gate("OR", a, a)
    result.append(b.finish("internal-fanout-four", b.gate("AND", left, right)))
    b = Builder(); x, y = b.input("x"), b.input("y"); a = b.gate("NOT", x)
    root = b.gate("AND", a, y)
    unused = b.gate("OR", a, a)
    b.gate("AND", unused, a)
    result.append(b.finish("unused-consumers-do-not-increase-R", root))
    b = Builder(); one = b.constant(1); a = b.gate("NOT", one)
    result.append(b.finish("shared-gate-over-constant", b.gate("OR", a, a)))
    b = Builder(); zero = b.constant(0); x = b.input("unused-x"); a = b.gate("NOT", x)
    b.gate("AND", a, a)
    result.append(b.finish("constant-output-with-unused-sharing", zero))
    b = Builder(); x = b.input("x"); neg = b.gate("NOT", x)
    result.append(b.finish("semantically-false-but-syntactically-nonempty", b.gate("AND", x, neg)))
    b = Builder(); x, y = b.input("x"), b.input("y")
    a, c = b.gate("AND", x, y), b.gate("AND", x, y)
    result.append(b.finish("identical-gates-are-distinct-nodes", b.gate("OR", a, c)))
    result.extend(selector_diamond_chain(n) for n in (1, 5))
    result.extend(parity_dag(n) for n in range(1, 7))
    return tuple(result)


def gate_options(available: int) -> Iterator[Node]:
    for a in range(available):
        yield Node("NOT", (a,))
    for op in ("AND", "OR"):
        for args in product(range(available), repeat=2):
            yield Node(op, args)


def exhaustive_count(max_gates: int) -> int:
    count, descriptions = 0, 1
    for gates in range(max_gates + 1):
        if gates:
            available = 4 + gates - 1
            descriptions *= available + 2 * available**2
        count += descriptions * (4 + gates)
    return count


def exhaustive_dags(max_gates: int) -> Iterator[DAG]:
    sources = (Node("INPUT", name="x"), Node("INPUT", name="y"), Node("CONST", value=0), Node("CONST", value=1))

    def extensions(nodes, remaining):
        if not remaining:
            yield nodes
        else:
            for gate in gate_options(len(nodes)):
                yield from extensions(nodes + (gate,), remaining - 1)

    for gates in range(max_gates + 1):
        for ordinal, nodes in enumerate(extensions(sources, gates)):
            for output in range(len(nodes)):
                yield DAG(f"exhaustive-g{gates}-{ordinal}-out{output}", nodes, output, "exhaustive")


def seeded_dags(count: int, seed: int, max_gates: int = 10, max_inputs: int = 4) -> tuple[DAG, ...]:
    rng = random.Random(seed)
    result = []
    for case in range(count):
        b = Builder()
        for i in range(rng.randrange(max_inputs + 1)):
            b.input(f"x{i}")
        b.constant(0); b.constant(1)
        for _ in range(rng.randrange(max_gates + 1)):
            op = rng.choice(("AND", "OR", "AND", "OR", "NOT"))
            a = rng.randrange(len(b.nodes))
            if op == "NOT":
                b.gate(op, a)
            else:
                other = a if rng.random() < 0.35 else rng.randrange(len(b.nodes))
                b.gate(op, a, other)
        output = len(b.nodes) - 1 if rng.random() < 0.7 else rng.randrange(len(b.nodes))
        result.append(b.finish(f"seed-{seed}-case-{case}", output, "seeded"))
    return tuple(result)


def submasks(mask: int) -> Iterator[int]:
    current = mask
    while True:
        yield current
        if not current:
            break
        current = (current - 1) & mask


def binomial_binary_lower_bound(n: int, p: Fraction) -> dict:
    """Exact distributional calculation, NOT a search for minimum circuits."""
    if type(n) is not int or not 0 <= n <= 256 or not isinstance(p, Fraction) or not 0 < p < 1:
        raise ValueError("need 0 <= n <= 256 and rational 0 < p < 1")
    strata = []
    for m in range(n + 1):
        restriction_count = comb(n, m) * 2**(n - m)
        per_restriction = p**m * ((1 - p) / 2)**(n - m)
        mass = comb(n, m) * p**m * (1 - p)**(n - m)
        lower = max(m - 1, 0)
        strata.append({"m": m, "restriction_count": restriction_count,
                       "probability_per_restriction": per_restriction, "binomial_mass": mass,
                       "binary_gate_lower_bound": lower, "weighted_lower_bound": lower * mass})
    return {
        "N": n, "p": p, "strata": strata,
        "restriction_count": sum(s["restriction_count"] for s in strata),
        "probability_mass": sum((s["binomial_mass"] for s in strata), ZERO),
        "expected_live_inputs": sum((s["m"] * s["binomial_mass"] for s in strata), ZERO),
        "expected_binary_gate_lower_bound": sum((s["weighted_lower_bound"] for s in strata), ZERO),
        "closed_form": n * p - 1 + (1 - p)**n,
    }


def check_small_parity_restrictions(audit: Audit, max_n: int = 6) -> dict:
    before = audit.counts.copy()
    details = []
    for n in range(max_n + 1):
        dag = parity_dag(n)
        ps = (Fraction(1, 8), Fraction(1, 4))
        direct_expectations = {p: ZERO for p in ps}
        for live in range(1 << n):
            m = live.bit_count()
            for fixed in submasks(((1 << n) - 1) & ~live):
                assignment = {f"x{i}": (fixed >> i) & 1 for i in range(n) if not live & (1 << i)}
                reduced = restrict_dag(dag, assignment)
                names, values = truth_table(reduced)
                context = {"N": n, "live": live, "fixed": fixed}
                audit.counts["small_parity_restrictions"] += 1
                essential = essential_inputs(names, values)
                audit.check(len(essential) == m, "residual_parity_essential_inputs", context, len(essential), m)
                for bits, value in enumerate(values):
                    complete = fixed
                    for i, name in enumerate(names):
                        if bits & (1 << i):
                            complete |= 1 << int(name[1:])
                    target = int(complete.bit_count() % 2 == 0)
                    audit.check(value == target, "residual_parity_truth_table", {**context, "bits": bits}, value, target)
                for p in ps:
                    direct_expectations[p] += p**m * ((1 - p) / 2)**(n - m) * max(len(essential) - 1, 0)
        for p in ps:
            grouped = binomial_binary_lower_bound(n, p)
            audit.check(direct_expectations[p] == grouped["expected_binary_gate_lower_bound"],
                        "enumerated_vs_binomial_parity_expectation", {"N": n, "p": p},
                        direct_expectations[p], grouped["expected_binary_gate_lower_bound"])
            details.append({"N": n, "p": p, "enumerated_expectation": direct_expectations[p]})
    return {"max_N": max_n, "counts": dict(audit.counts - before), "expectations": details}


def check_parity_obstruction(n: int, p: Fraction, audit: Audit) -> dict:
    before = audit.counts.copy()
    dag = parity_dag(n)
    stats = measure_dag(dag)
    distribution = binomial_binary_lower_bound(n, p)
    context = {"branch": "universal_quadratic_gate_contraction", "N": n, "p": p}
    advertised_s = 4 * n - 3 if n else 0
    audit.check(stats["S"] == advertised_s, "parity_linear_AND_OR_NOT_gate_count", context, stats["S"], advertised_s)
    audit.check(stats["reachable_binary_gates"] == 3 * max(n - 1, 0), "parity_binary_gate_count", context)
    audit.check(distribution["restriction_count"] == 3**n, "binomial_stratum_restriction_count", context)
    audit.check(distribution["probability_mass"] == 1, "binomial_probability_mass", context)
    audit.check(distribution["expected_live_inputs"] == n * p, "binomial_expected_live_inputs", context)
    audit.check(distribution["expected_binary_gate_lower_bound"] == distribution["closed_form"],
                "binomial_lower_bound_closed_form", context, distribution["expected_binary_gate_lower_bound"], distribution["closed_form"])
    for stratum in distribution["strata"]:
        audit.check(stratum["restriction_count"] * stratum["probability_per_restriction"] == stratum["binomial_mass"],
                    "binomial_vs_individual_restriction_mass", {**context, "m": stratum["m"]})
    # At each m check a canonical residual and both attainable fixed parities.
    # Single-bit flips at one assignment witness every live variable's essentiality.
    # This is O(n^2) semantic witnesses, NOT enumeration of all 3**n restrictions.
    for m in range(n + 1):
        for offset in ((0, 1) if m < n else (0,)):
            base = {f"x{i}": 0 for i in range(n)}
            if offset:
                base[f"x{m}"] = 1
            value = evaluate_dag(dag, base)
            audit.check(value == 1 - offset, "large_parity_canonical_residual_value", {**context, "m": m, "offset": offset})
            for i in range(m):
                flipped = dict(base); flipped[f"x{i}"] = 1
                observed = evaluate_dag(dag, flipped)
                audit.check(observed == 1 - value, "large_parity_essential_input_witness", {**context, "m": m, "offset": offset, "input": i})
    rhs = p**2 * stats["S"]
    lower = distribution["expected_binary_gate_lower_bound"]
    return {
        "N": n, "p": p, "source_S": stats["S"], "source_binary_gates": stats["reachable_binary_gates"],
        "source_gate_upper_bound_4N_minus_3": advertised_s,
        "expected_binary_gate_lower_bound": lower, "p_squared_times_source_S": rhs,
        "gap": lower - rhs, "ratio": lower / rhs if rhs else None,
        "violates_coefficient_one_bound": lower > rhs,
        "distribution": distribution, "counts": dict(audit.counts - before),
        "source_unfolding_summary": {key: stats[key] for key in (
            "S", "R", "outdegree_product", "unfolded_gate_count", "literal_leaf_count", "leaf_count")},
        "interpretation": "The residual binary-gate lower bound also lower-bounds total gates. The source is an explicit size upper bound; a smaller optimal source only decreases p^2*S.",
        "not_claimed": "No promise-correct GapMCSP solver consequence, no intrinsic unfolding lower bound, and no refutation of every additive-term or unspecified-constant variant.",
    }


def check_parity_sqrt_additive_control(audit: Audit) -> dict:
    """Compact fixed-A,B counterexample using rational RHS and linear lower bound.

    This tests a NAIVE GATE analogue, not the formula bound in literal leaves L.
    E[max(M-1,0)] >= E[M]-1 = Np-1 is sufficient; the value Np-1 is a lower
    bound, not the exact expectation.  No binomial-stratum or restriction
    enumeration is needed here, and sqrt(S) is never evaluated in floating point.
    """
    before = audit.counts.copy()
    n, p, a, b = 256, Fraction(1, 8), ONE, ONE
    dag = parity_dag(n)
    stats = measure_dag(dag)
    source_s = stats["S"]
    context = {"branch": "naive_gate_sqrt_additive_control", "N": n, "p": p,
               "A": a, "B": b, "S": source_s}
    audit.check(source_s == 4 * n - 3, "sqrt_additive_parity_source_gate_count", context,
                source_s, 4 * n - 3)
    sqrt_floor = isqrt(source_s)
    sqrt_upper = sqrt_floor + int(sqrt_floor**2 < source_s)
    audit.check(sqrt_floor**2 <= source_s <= sqrt_upper**2,
                "sqrt_additive_integer_sqrt_enclosure", context,
                (sqrt_floor**2, source_s, sqrt_upper**2))
    quadratic_term = p**2 * source_s
    sqrt_term_upper = p * sqrt_upper
    rhs_upper = a * (quadratic_term + sqrt_term_upper) + b
    lower = n * p - 1
    audit.check(lower > rhs_upper, "sqrt_additive_fixed_AB_counterexample", context,
                lower, rhs_upper)
    # Bounded semantic sanity checks of the actual 1021-gate constructor.
    # Single-bit flips witness all 256 source inputs; they are not random
    # restrictions and are not claimed to enumerate all residual circuits.
    zero = {f"x{i}": 0 for i in range(n)}
    audit.check(evaluate_dag(dag, zero) == 1, "sqrt_additive_parity_zero_assignment", context)
    for i in range(n):
        flipped = dict(zero)
        flipped[f"x{i}"] = 1
        audit.check(evaluate_dag(dag, flipped) == 0,
                    "sqrt_additive_parity_single_flip_witness", {**context, "input": i})
    return {
        "candidate_bound": "E SIZE <= A*(p^2*S + p*sqrt(S)) + B",
        "N": n, "p": p, "A": a, "B": b, "source_S": source_s,
        "source_binary_gates": stats["reachable_binary_gates"],
        "source_gate_upper_bound_4N_minus_3": 4 * n - 3,
        "sqrt_S_integer_upper_bound": sqrt_upper,
        "sqrt_enclosure_squared": {"floor_squared": sqrt_floor**2, "S": source_s,
                                   "upper_squared": sqrt_upper**2},
        "p_squared_S": quadratic_term, "p_sqrt_S_rational_upper_bound": sqrt_term_upper,
        "RHS_rational_upper_bound": rhs_upper, "expected_size_lower_bound_used": lower,
        "lower_bound_is_exact_expectation": False,
        "certified_gap_lower_bound": lower - rhs_upper,
        "ratio_lower_to_RHS_upper": lower / rhs_upper,
        "violates_fixed_A_B_bound": lower > rhs_upper,
        "certificate": "A=B=1, N=256, p=1/8, S=1021: sqrt(S)<=32, so RHS<=1341/64<31<=E SIZE.",
        "expectation_method": "For M~Binomial(N,p), E SIZE >= E[max(M-1,0)] >= E[M]-1 = Np-1. No 3^256 enumeration.",
        "scope": "Finite obstruction to this naive GATE-size analogue at A=B=1 only. The pure p^2 control remains separate. This does not refute the formula-leaf bound using L or establish a promise-correct GapMCSP solver consequence.",
        "general_argument_deferred": "The fixed-small-p, large-N argument for arbitrary fixed A,B, using sqrt(S)=o(N), is left to the parent/peer; no generic refutation is claimed from this finite check.",
        "unfolding_caveat": "No intrinsic formula lower bound is inferred from syntactic DAG unfolding.",
        "counts": dict(audit.counts - before),
    }


def additive_investigation(chain_results: list[dict], audit: Audit) -> dict:
    rows = []
    for result in chain_results:
        stats = result["measurements"]
        length = stats["S"]
        context = {"dag": result["dag"]}
        audit.check(stats["R"] == max(length - 1, 0), "idempotent_chain_R", context, stats["R"], max(length - 1, 0))
        audit.check(stats["unfolded_gate_count"] == 2**length - 1, "idempotent_chain_gate_closed_form", context)
        audit.check(stats["literal_leaf_count"] == 2**length, "idempotent_chain_leaf_closed_form", context)
        audit.check(tuple(result["semantic"]["values"]) == (0, 1), "idempotent_chain_computes_one_bit", context)
        rows.append({"name": result["dag"]["name"], "S": length, "R": stats["R"],
                     "unfolded_gates": stats["unfolded_gate_count"], "literal_leaves": stats["literal_leaf_count"],
                     "S_plus_R": length + stats["R"], "S_times_R_plus_1": length * (stats["R"] + 1),
                     "semantic_formula_gates": 0, "semantic_formula_literal_leaves": 1})
    candidates = []
    for constant in (1, 2, 4, 8, 16, 64, 256, 1024):
        witness = next((r for r in rows if r["unfolded_gates"] > constant * r["S_plus_R"]), None)
        candidates.append({"candidate": "F_unfold <= C*(S+R)", "C": constant,
                           "counterexample": witness,
                           "comparison_bound": None if witness is None else constant * witness["S_plus_R"]})
    quadratic = next((r for r in rows if r["unfolded_gates"] > r["S_times_R_plus_1"]), None)
    return {"chains": rows, "constant_multiplier_candidates": candidates,
            "S_times_R_plus_1_counterexample": quadratic,
            "asymptotic_caveat": "O(S+R) has an unspecified constant, so one finite example cannot refute that notation by itself. These are explicit violations for the listed constants, plus checked exact counts for a parameterized exponential-unfolding family; the parent supplies the general argument.",
            "semantic_caveat": "Every chain computes x. A formula consisting of the input alone has zero gates and one literal. This is exponential SYNTACTIC unfolding, never an intrinsic formula-size lower bound."}


def run_experiment(*, exhaustive_max_gates: int = 2, seeded_cases: int = 200,
                   seed: int = 20261009, max_seeded_gates: int = 10, max_chain: int = 64,
                   max_cases: int = 25_000, materialize_limit: int = 10_000,
                   parity_n: int = 64, parity_p: Fraction = Fraction(1, 64),
                   include_parity: bool = True, failure_limit: int = 20) -> dict:
    if not -1 <= exhaustive_max_gates <= 3 or not 0 <= seeded_cases <= 10_000:
        raise ValueError("exhaustive gate limit must be -1..3 and seeded count 0..10000")
    if not 0 <= max_seeded_gates <= 32 or not 0 <= max_chain <= 128:
        raise ValueError("seeded gate cap must be 0..32 and chain cap 0..128")
    if max_cases < 1 or materialize_limit < 1 or failure_limit < 0:
        raise ValueError("case/tree budgets must be positive and failure limit nonnegative")
    if not 1 <= parity_n <= 128:
        raise ValueError("large parity N must be 1..128")
    binomial_binary_lower_bound(parity_n, parity_p)
    chosen = named_dags()
    chains = tuple(idempotent_chain(n) for n in range(max_chain + 1))
    chains += tuple(idempotent_chain(n, mode) for mode in ("AND", "OR") for n in sorted({min(5, max_chain), max_chain}))
    count = exhaustive_count(exhaustive_max_gates) + len(chosen) + len(chains) + seeded_cases
    if count > max_cases:
        raise BudgetExceeded(f"requested {count} DAG descriptions exceeds case budget {max_cases}")
    audit = Audit(failure_limit)
    digest = hashlib.sha256()
    detailed, chain_results = [], []
    coverage: dict[str, Counter] = {}
    maxima = {}
    for dag in chain(exhaustive_dags(exhaustive_max_gates), chosen, chains,
                     seeded_dags(seeded_cases, seed, max_seeded_gates)):
        digest.update((json.dumps(jsonable(dag.description()), sort_keys=True, separators=(",", ":")) + "\n").encode())
        result = check_dag(dag, audit, materialize_limit=materialize_limit)
        stats = result["measurements"]
        cov = coverage.setdefault(dag.suite, Counter())
        cov["DAG_descriptions"] += 1
        cov["truth_table_rows"] += result["counts"].get("truth_table_rows", 0)
        cov["reachable_gates_counted_once"] += stats["S"]
        if dag.suite not in ("exhaustive", "seeded", "idempotent"):
            detailed.append(result)
        if dag.suite == "idempotent":
            chain_results.append(result)
        for key, numerator, denominator in (
            ("gate_to_S_2R", stats["unfolded_gate_count"], stats["gate_bound_S_2R"]),
            ("gate_to_S_product", stats["unfolded_gate_count"], stats["gate_bound_S_product"]),
            ("leaf_to_1_S_2R", stats["leaf_count"], stats["leaf_bound_1_S_2R"]),
            ("gate_to_S_plus_R", stats["unfolded_gate_count"], stats["S"] + stats["R"]),
            ("gate_to_S_times_R_plus_1", stats["unfolded_gate_count"], stats["S"] * (stats["R"] + 1)),
        ):
            if denominator:
                ratio = Fraction(numerator, denominator)
                if key not in maxima or ratio > maxima[key]["ratio"]:
                    maxima[key] = {"ratio": ratio, "numerator": numerator, "denominator": denominator,
                                   "dag": dag.description(), "S": stats["S"], "R": stats["R"]}
    sharing_counts = dict(audit.counts)
    sharing_failures = dict(audit.failures)
    additive = additive_investigation(chain_results, audit)
    if max_chain >= 5:
        audit.check(additive["S_times_R_plus_1_counterexample"] is not None,
                    "expected_additive_replacement_counterexample_found", {})
    parity = None
    sqrt_additive_control = None
    if include_parity:
        small = check_small_parity_restrictions(audit)
        requested = check_parity_obstruction(parity_n, parity_p, audit)
        clean = check_parity_obstruction(16, Fraction(1, 8), audit)
        audit.check(clean["expected_binary_gate_lower_bound"] > 1 > clean["p_squared_times_source_S"],
                    "clean_parity_gate_contraction_counterexample", {}, clean["expected_binary_gate_lower_bound"], clean["p_squared_times_source_S"])
        if parity_n == 64 and parity_p == Fraction(1, 64):
            audit.check(requested["violates_coefficient_one_bound"], "requested_parity64_counterexample", {})
        parity = {"candidate_bound": "E SIZE <= p^2*S",
                  "formula_comparison_caveat": "This p^2-only control is not the audited formula bound, which also has p*sqrt(L); the naive gate analogue with a square-root additive term is tested separately.",
                  "small_exhaustive_semantics": small, "requested_instance": requested, "clean_instance": clean,
                  "clean_certificate": "N=16, p=1/8, S=61: E lower = 1+(7/8)^16 > 1 > 61/64 = p^2*S.",
                  "lower_bound_used": "A fanin-two circuit with m essential inputs needs at least max(m-1,0) binary gates; NOT gates do not merge dependencies. This elementary structural fact is the semantic lower bound, not an exhaustive search over all competing circuits.",
                  "scope": "Obstruction to the stated universal coefficient-one pure p^2 GATE-size contraction; not a promise-correct GapMCSP algorithm result, not a formal general proof, and not a rejection of all additive-term or arbitrary-constant variants."}
        sqrt_additive_control = check_parity_sqrt_additive_control(audit)
    return jsonable({
        "schema_version": 1, "experiment": "phase2-exact-finite-DAG-sharing-probe",
        "status": "passed" if audit.ok else "check_failures_found", "complete": True,
        "claim": "Bounded exact finite tests, NOT general proofs or intrinsic formula lower bounds.",
        "phase1_read_only": True,
        "config": {"exhaustive_max_gates": exhaustive_max_gates, "seeded_cases": seeded_cases, "seed": seed,
                   "max_seeded_gates": max_seeded_gates, "max_chain": max_chain, "max_cases": max_cases,
                   "materialize_node_limit": materialize_limit, "parity_N": parity_n, "parity_p": parity_p,
                   "include_parity": include_parity, "failure_limit": failure_limit},
        "model": {
            "basis": "Single-output topological DAG; AND/OR fanin 2, NOT fanin 1; input/constant sources fanin 0.",
            "size": "S counts reachable AND/OR/NOT gates once; declared_S also reports unused gates. Constants are leaves, not gates.",
            "wire_multiplicity": "Ordered operand slots are separate wires, including AND(v,v) or OR(v,v). Structurally identical gate nodes are not silently merged.",
            "fanout": "Source-to-consumer wire count in the reachable subgraph only. No virtual output wire. R uses internal gates only; reused inputs and constants are excluded.",
            "path_direction": "Output-to-operand paths. The root has one zero-length path. Unreachable nodes have zero paths. The product bound on path counts is for INTERNAL nodes only, not reused input leaves.",
            "product": "P=product_internal max(1,outdegree). Finite checks test internal path counts<=P, P<=2^R, unfolded gates<=S*P<=S*2^R.",
            "leaves": "leaf_count includes constants; literal_leaf_count counts variable occurrences. NOT stays an explicit gate. Both satisfy the tested 1+S*2^R bound.",
            "unfolding": "Copy every wire recursively with no Boolean simplification. DP sizes, path sums, and budgeted explicit trees independently agree.",
            "exhaustive_scope": "All topologically ordered descriptions through the configured gate limit over two inputs x,y and constant sources 0,1, with all output choices. Not all circuits.",
            "arithmetic": "Python integers and fractions.Fraction; rationals serialized as numerator/denominator strings.",
        },
        "DAG_descriptions": count, "exhaustive_descriptions": exhaustive_count(exhaustive_max_gates),
        "DAG_stream_sha256": digest.hexdigest(), "coverage": {k: dict(v) for k, v in sorted(coverage.items())},
        "sharing_bounds": {"passed": not sharing_failures, "counts": sharing_counts,
                           "failure_counts": sharing_failures, "max_ratios": maxima},
        "named_DAG_details": detailed, "additive_replacements": additive,
        "universal_quadratic_gate_contraction": parity,
        "naive_gate_sqrt_additive_contraction": sqrt_additive_control,
        "all_counts": dict(audit.counts), "failure_counts": dict(audit.failures),
        "counterexamples_to_asserted_bounds": audit.examples,
        "failure_examples_omitted": max(0, sum(audit.failures.values()) - len(audit.examples)),
        "caveat": "Expected counterexamples to the tempting additive and universal contraction claims are stored in their own sections, not mislabeled as failures of the tested sharing upper bounds. The parent handles general proofs.",
    })


def run_self_tests() -> bool:
    sys.dont_write_bytecode = True
    directory = str(Path(__file__).resolve().parent)
    if directory not in sys.path:
        sys.path.insert(0, directory)
    suite = unittest.defaultTestLoader.discover(directory, pattern="test_sharing_probe.py")
    return unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--self-test", action="store_true", help="run tests only; do not write results")
    parser.add_argument("--exhaustive-max-gates", type=int, default=2, help="-1 disables exhaustive descriptions")
    parser.add_argument("--seeded-cases", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20261009)
    parser.add_argument("--max-seeded-gates", type=int, default=10)
    parser.add_argument("--max-chain", type=int, default=64)
    parser.add_argument("--max-cases", type=int, default=25_000)
    parser.add_argument("--materialize-limit", type=int, default=10_000)
    parser.add_argument("--parity-n", type=int, default=64)
    parser.add_argument("--parity-p", type=Fraction, default=Fraction(1, 64))
    parser.add_argument("--skip-parity", action="store_true",
                        help="skip both the pure p^2 and square-root-additive parity controls")
    parser.add_argument("--failure-limit", type=int, default=20)
    parser.add_argument("--output", default=str(Path(__file__).with_name("sharing_results.json")), help="JSON path, or '-' for stdout")
    args = parser.parse_args(argv)
    if args.self_test:
        return 0 if run_self_tests() else 1
    try:
        result = run_experiment(exhaustive_max_gates=args.exhaustive_max_gates, seeded_cases=args.seeded_cases,
                                seed=args.seed, max_seeded_gates=args.max_seeded_gates, max_chain=args.max_chain,
                                max_cases=args.max_cases, materialize_limit=args.materialize_limit,
                                parity_n=args.parity_n, parity_p=args.parity_p, include_parity=not args.skip_parity,
                                failure_limit=args.failure_limit)
    except (ValueError, BudgetExceeded) as error:
        parser.error(str(error))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output == "-":
        sys.stdout.write(text)
    else:
        Path(args.output).write_text(text)
        counts = result["sharing_bounds"]["counts"]
        print(f"{result['status']}: {result['DAG_descriptions']} DAG descriptions; "
              f"{counts['unfolded_gate_S_2R_bound']} gate/leaf bound cases; "
              f"{counts.get('DAG_vs_unfolded_truth_table', 0)} explicit-tree semantic comparisons")
        witness = result["additive_replacements"]["S_times_R_plus_1_counterexample"]
        if witness:
            print(f"Additive counterexample: S={witness['S']}, R={witness['R']}, "
                  f"F_unfold={witness['unfolded_gates']} > S*(R+1)={witness['S_times_R_plus_1']}; computes x")
        parity = result["universal_quadratic_gate_contraction"]
        if parity:
            print(parity["clean_certificate"])
            print(f"Requested parity instance violates p^2*S: {parity['requested_instance']['violates_coefficient_one_bound']}")
            print(result["naive_gate_sqrt_additive_contraction"]["certificate"])
        print(f"Results: {args.output}\nFinite tests only; no intrinsic formula lower bound.")
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
