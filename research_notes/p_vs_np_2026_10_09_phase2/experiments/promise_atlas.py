#!/usr/bin/env python3
"""Small, exact, solver-free GapMCSP corpus (Python standard library only).

This enumerates circuit DAGs, not formulas: each gate may use ANY earlier wire,
including a gate used elsewhere. AND/OR fanins are ordered, repetition is allowed,
dead gates are retained, and every available wire is considered as the output.
Constants and positive input wires are free; each NOT, including input NOT, costs
one gate. No semantic deduplication prunes the syntactic enumeration.

Truth-table bit a is the output on x_i = (a >> i) & 1. For inner arity 3,
there are N=8 coordinates and 256 tables. The promise is YES: size<=1,
NO: size>2, GAP: size=2. Here "accepting" means accepted by the MAXIMAL
separator 1_Low: a promise-compatible subcube may contain GAP tables. It is NOT
necessarily accepted by a fixed solver, which may reject those GAP tables.
Every fixed valid solver's accepting subcube is contained in Low, so the maximal
separator's certificate minimum is a LOWER bound for that solver, not necessarily
its actual certificate minimum. Analytic gate bounds are reported separately
from bounded enumeration; no attainability or exact outer minimum is claimed.

Completeness is executable bounded enumeration plus tests, NOT a Lean proof,
not asymptotic evidence, and not an unbounded MCSP algorithm. Hashes are replay
fingerprints, not independent proofs. All budgets are checked before enumeration.
Run with python3 -B to avoid creating bytecode artifacts.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import struct
from typing import Iterator

NOT, AND, OR = 0, 1, 2
OP_NAMES = {NOT: "NOT", AND: "AND2", OR: "OR2"}
Gate = tuple[int, int, int]  # NOT's third field is -1, not a wire.
Program = tuple[Gate, ...]
MAX_GATE_BUDGET = 3
MAX_OUTPUT_VISITS_PER_ENUMERATION = 1_200_000
OUTER_GATE_BUDGET = 2  # Deliberately never escalated to 3.


class BudgetExceeded(ValueError):
    """Requested complete enumeration exceeds the deliberately small budget."""


def input_truth_tables(arity: int) -> tuple[int, ...]:
    if not 0 <= arity <= 8:
        raise ValueError("supported arity is 0..8")
    rows = 1 << arity
    full = (1 << rows) - 1
    return (0, full) + tuple(
        sum(((a >> i) & 1) << a for a in range(rows)) for i in range(arity)
    )


def gate_choices(wires: int) -> tuple[Gate, ...]:
    return tuple((NOT, a, -1) for a in range(wires)) + tuple(
        (op, a, b)
        for op in (AND, OR)
        for a in range(wires)
        for b in range(wires)
    )


def expected_counts(arity: int, bound: int) -> list[dict[str, int]]:
    if arity < 0 or bound < 0:
        raise ValueError("negative arity or gate bound")
    prefixes = 1
    result = []
    for gates in range(bound + 1):
        wires = arity + 2 + gates
        result.append({"gates": gates, "programs": prefixes,
                       "output_circuits": prefixes * wires})
        prefixes *= wires + 2 * wires * wires
    return result


def check_budget(arity: int, bound: int) -> list[dict[str, int]]:
    if not 0 <= arity <= 8:
        raise BudgetExceeded("supported enumeration arity is 0..8")
    if not 0 <= bound <= MAX_GATE_BUDGET:
        raise BudgetExceeded("enumeration gate budget must be 0..3")
    counts = expected_counts(arity, bound)
    if sum(row["output_circuits"] for row in counts) > MAX_OUTPUT_VISITS_PER_ENUMERATION:
        raise BudgetExceeded("complete enumeration exceeds 1,200,000 output visits")
    return counts


def iter_topological_programs(arity: int, bound: int) -> Iterator[tuple[Program, tuple[int, ...]]]:
    """Preorder DFS; yields every prefix once, including the empty program.

    A yielded record represents ALL outputs 0..len(values)-1. Gate order is
    NOT(a), then AND(a,b), then OR(a,b), with increasing wire indices.
    """
    check_budget(arity, bound)
    base = input_truth_tables(arity)
    full = base[1]
    choices = [gate_choices(len(base) + g) for g in range(bound)]

    def visit(program: Program, values: tuple[int, ...]):
        yield program, values
        if len(program) == bound:
            return
        for gate in choices[len(program)]:
            op, a, b = gate
            value = (full ^ values[a]) if op == NOT else (
                (values[a] & values[b]) if op == AND else (values[a] | values[b])
            )
            yield from visit(program + (gate,), values + (value,))

    yield from visit((), base)


@dataclass(frozen=True, slots=True)
class Circuit:
    arity: int
    gates: Program
    output: int

    def evaluate(self) -> int:
        values = list(input_truth_tables(self.arity))
        full = values[1]
        for op, a, b in self.gates:
            if op not in OP_NAMES or not 0 <= a < len(values):
                raise ValueError("invalid operation or forward/absent input wire")
            if op == NOT:
                if b != -1:
                    raise ValueError("NOT is unary")
                value = full ^ values[a]
            else:
                if not 0 <= b < len(values):
                    raise ValueError("forward/absent second input wire")
                value = values[a] & values[b] if op == AND else values[a] | values[b]
            values.append(value)
        if not 0 <= self.output < len(values):
            raise ValueError("invalid output wire")
        return values[self.output]

    def as_json(self) -> dict:
        return {"arity": self.arity, "gate_count": len(self.gates),
                "initial_wires": ["0", "1"] + [f"x{i}" for i in range(self.arity)],
                "gates": [{"wire": self.arity + 2 + i, "op": OP_NAMES[op],
                           "inputs": [a] if op == NOT else [a, b]}
                          for i, (op, a, b) in enumerate(self.gates)],
                "output_wire": self.output}


@dataclass(slots=True)
class Enumeration:
    arity: int
    bound: int
    minimum: dict[int, int]
    witnesses: dict[int, Circuit]
    audit: dict


def enumerate_dags(arity: int, bound: int) -> Enumeration:
    expected = check_budget(arity, bound)
    programs = [0] * (bound + 1)
    outputs = [0] * (bound + 1)
    minimum: dict[int, int] = {}
    witnesses: dict[int, Circuit] = {}
    word_bytes = max(1, ((1 << arity) + 7) // 8)
    digest = hashlib.sha256(b"promise-atlas-dag-v1\n" + bytes([arity, bound]))
    for gates, values in iter_topological_programs(arity, bound):
        size = len(gates)
        programs[size] += 1
        # One length-framed block represents this gate list and every output.
        block = bytearray([size, len(values)])
        for op, a, b in gates:
            block.extend((op, a, 255 if op == NOT else b))
        for output, value in enumerate(values):
            outputs[size] += 1
            block.extend(value.to_bytes(word_bytes, "little"))
            old = minimum.get(value)
            if old is None or size < old:
                minimum[value] = size
                witnesses[value] = Circuit(arity, gates, output)
        digest.update(block)
    actual = [{"gates": g, "programs": programs[g], "output_circuits": outputs[g]}
              for g in range(bound + 1)]
    assert actual == expected
    for table, witness in witnesses.items():
        assert witness.evaluate() == table and len(witness.gates) == minimum[table]
    semantic_hash = hashlib.sha256()
    for table, size in sorted(minimum.items()):
        semantic_hash.update(table.to_bytes(word_bytes, "little") + bytes([size]))
    audit = {
        "arity": arity, "gate_bound": bound, "complete": True,
        "counts_by_gate_count": actual,
        "program_count": sum(programs), "output_circuit_count": sum(outputs),
        "distinct_output_truth_tables": len(minimum),
        "new_semantics_at_minimum_gate_count": [sum(s == g for s in minimum.values())
                                                 for g in range(bound + 1)],
        "enumeration_sha256": digest.hexdigest(),
        "classified_semantics_sha256": semantic_hash.hexdigest(),
        "ordered_binary_fanins": True, "repeated_fanins_allowed": True,
        "dead_gates_retained": True, "all_available_output_wires_enumerated": True,
        "dag_sharing_retained": True, "semantic_pruning": False,
        "enumeration_hash_format": (
            "SHA256 of ASCII 'promise-atlas-dag-v1\\n', arity byte, bound byte; "
            "then preorder-DFS blocks: gate-count byte, wire-count byte, "
            "(opcode,left,right) bytes per gate (NOT=0/right=255, AND2=1, OR2=2), "
            "then each wire's truth table as a fixed-width little-endian word. "
            "All wire indices in a block are separate output-circuit choices."
        ),
        "truth_word_bytes": word_bytes,
    }
    return Enumeration(arity, bound, minimum, witnesses, audit)


def submasks(mask: int) -> Iterator[int]:
    if mask < 0:
        raise ValueError("negative mask")
    value = mask
    while True:
        yield value
        if value == 0:
            return
        value = (value - 1) & mask


def completions(coordinates: int, mask: int, value: int) -> Iterator[int]:
    if not 0 <= coordinates <= 8:
        raise ValueError("coordinate count must be 0..8")
    full = (1 << coordinates) - 1
    if not 0 <= mask <= full or not 0 <= value <= full or value & ~mask:
        raise ValueError("partial assignment requires mask in range and value subset of mask")
    for live_value in submasks(full ^ mask):
        yield value | live_value


def intersect_partial(coordinates: int, left_mask: int, left_value: int,
                      right_mask: int, right_value: int) -> tuple[int, int] | None:
    """None is the false/empty cube, not an unconstrained coordinate."""
    if not 0 <= coordinates <= 8:
        raise ValueError("coordinate count must be 0..8")
    full = (1 << coordinates) - 1
    for mask, value in ((left_mask, left_value), (right_mask, right_value)):
        if not 0 <= mask <= full or not 0 <= value <= full or value & ~mask:
            raise ValueError("invalid partial assignment")
    if (left_value ^ right_value) & left_mask & right_mask:
        return None
    return left_mask | right_mask, left_value | right_value


def minimum_fixed_from_count(live: int, low_count: int) -> int | None:
    """Necessary cardinality bound; None means no nonempty cube can fit."""
    if live < 0 or not 0 <= low_count <= 1 << live:
        raise ValueError("invalid relative cube cardinality")
    return None if low_count == 0 else live - (low_count.bit_length() - 1)


@dataclass(frozen=True, slots=True)
class Cube:
    coordinates: int
    mask: int
    value: int
    points: tuple[int, ...]
    yes_count: int
    gap_count: int
    no_count: int

    @property
    def live(self) -> int:
        return self.coordinates - self.mask.bit_count()

    @property
    def low_count(self) -> int:
        return self.yes_count + self.gap_count

    def as_json(self, include_points: bool = True) -> dict:
        result = {"mask": self.mask, "value": self.value,
                  "fixed_coordinates": [[i, (self.value >> i) & 1]
                                        for i in range(self.coordinates) if (self.mask >> i) & 1],
                  "live_count": self.live, "completion_count": len(self.points),
                  "yes_count": self.yes_count, "gap_count": self.gap_count,
                  "no_count": self.no_count, "low_count": self.low_count}
        if include_points:
            result["completions"] = sorted(self.points)
        return result


def build_cube_atlas(coordinates: int, yes: set[int], gap: set[int], no: set[int]):
    universe = set(range(1 << coordinates))
    assert not (yes & gap or yes & no or gap & no)
    assert yes | gap | no == universe
    low = yes | gap
    cubes: dict[tuple[int, int], Cube] = {}
    digest = hashlib.sha256(b"promise-atlas-cubes-v1\n" + bytes([coordinates]))
    completion_visits = 0
    for mask in range(1 << coordinates):
        for value in submasks(mask):
            points = tuple(completions(coordinates, mask, value))
            y = sum(t in yes for t in points)
            g = sum(t in gap for t in points)
            n = sum(t in no for t in points)
            cube = Cube(coordinates, mask, value, points, y, g, n)
            assert len(points) == 1 << cube.live
            assert y + g + n == len(points)
            if n == 0:
                assert all(t in low for t in points)
                assert len(points) <= len(low)
            cubes[mask, value] = cube
            completion_visits += len(points)
            digest.update(struct.pack("<BBHHH", mask, value, y, g, n) + bytes(points))
    assert len(cubes) == 3 ** coordinates
    assert completion_visits == 4 ** coordinates
    accepting = [c for c in cubes.values() if c.no_count == 0]
    count_allowed_but_not_accepting = [c for c in cubes.values()
                                      if len(c.points) <= len(low) and c.no_count > 0]
    summary = {
        "coordinate_count": coordinates,
        "subcube_count": len(cubes), "completion_visits": completion_visits,
        "subcube_count_including_false": len(cubes) + 1,
        "false_subcube": {"completion_count": 0, "contained_in_low": True,
                          "contains_a_yes_table": False,
                          "included_in_nonempty_subcube_enumeration": False},
        "sha256": digest.hexdigest(),
        "hash_format": "mask ascending, value descending submask order; header promise-atlas-cubes-v1\\n + coordinate byte; per cube little-endian <BBHHH> mask,value,YES,GAP,NO counts then descending-submask completions as bytes",
        "acceptance_definition": "promise-compatible: no NO completion; accepted by the maximal separator 1_Low",
        "fixed_solver_scope": "Not necessarily accepted by every fixed valid solver: GAP completions may be rejected.",
        "accepting_subcube_count": len(accepting),
        "accepting_subcubes_containing_yes": sum(c.yes_count > 0 for c in accepting),
        "gap_only_accepting_subcubes": sum(c.yes_count == 0 for c in accepting),
        "all_accepting_completions_directly_checked": True,
        "largest_accepting_completion_count": max((len(c.points) for c in accepting), default=0),
        "accepting_subcubes": [c.as_json() for c in accepting],
        "counts_by_live_dimension": [
            {"live": d, "all": sum(c.live == d for c in cubes.values()),
             "accepting": sum(c.live == d for c in accepting)}
            for d in range(coordinates + 1)],
        "cardinality_obstructed_subcubes": sum(len(c.points) > len(low) for c in cubes.values()),
        "cardinality_allowed_but_not_accepting": len(count_allowed_but_not_accepting),
    }
    return cubes, summary


def certificate_atlas(coordinates: int, yes: set[int], low: set[int], cubes: dict):
    rows = []
    count_bound = minimum_fixed_from_count(coordinates, len(low))
    for table in sorted(yes):
        candidates = [cubes[mask, table & mask] for mask in range(1 << coordinates)]
        accepting = [c for c in candidates if c.no_count == 0]
        minimum = min(c.mask.bit_count() for c in accepting)
        minima = [c for c in accepting if c.mask.bit_count() == minimum]
        strict_minimum = min(c.mask.bit_count() for c in candidates
                             if c.yes_count == len(c.points))
        assert count_bound is not None and minimum >= count_bound
        valid_masks = [c.mask for c in accepting]
        rows.append({"yes_table": table, "subsets_checked": len(candidates),
                     "accepting_masks": valid_masks,
                     "acceptance_bitset_hex": f"{sum(1 << mask for mask in valid_masks):064x}",
                     "minimum_fixed_coordinates": minimum,
                     "minimum_masks": [c.mask for c in minima],
                     "minimum_witness": minima[0].as_json(),
                     "strict_yes_only_minimum_fixed_coordinates": strict_minimum})
    return {"certificate_function": "maximal separator 1_Low",
            "fixed_solver_interpretation": "The minimum here is a lower bound for every fixed valid solver's accepting certificate at the same YES table; equality need not hold because the solver may reject GAP.",
            "yes_tables_checked": len(yes),
            "subset_tests": len(yes) * (1 << coordinates),
            "global_cardinality_lower_bound_fixed": count_bound,
            "minimum_certificate_size_histogram": {
                str(k): v for k, v in sorted(Counter(r["minimum_fixed_coordinates"] for r in rows).items())},
            "per_yes_table": rows}


def counting_endpoints() -> dict:
    checks = 0
    for live in range(9):
        for low_count in range((1 << live) + 1):
            bound = minimum_fixed_from_count(live, low_count)
            for fixed in range(live + 1):
                fits = (1 << (live - fixed)) <= low_count
                assert fits == (bound is not None and fixed >= bound)
                checks += 1
    endpoint_counts = [0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 63, 64, 127, 128, 255, 256]
    return {"checked_equivalences": checks, "live_dimensions": list(range(9)),
            "scope": "every 0<=Low_count<=2^live and 0<=new_fixed<=live",
            "formula": "2^(live-new_fixed)<=Low_count iff Low_count>0 and new_fixed>=live-floor(log2 Low_count)",
            "zero_dimensional": [{"low_count": c, "minimum_fixed": minimum_fixed_from_count(0, c)}
                                 for c in (0, 1)],
            "eight_dimensional_endpoints": [
                {"low_count": c, "minimum_fixed": minimum_fixed_from_count(8, c)} for c in endpoint_counts],
            "empty_low": "No consistent nonempty subcube fits, including a singleton.",
            "full_low": "The empty certificate is allowed; equality endpoints are inclusive."}


def audit_prior_overlap(coordinates: int, yes: set[int], cubes: dict) -> dict:
    """Every YES table x and every pair of masks A,C; values come from x.

    These are YES-centered incidences, NOT deduplicated restriction/certificate
    pairs. In the restricted problem, C is accepting iff A union C excludes NO.
    "Accepting" here refers to 1_Low restricted by the prior, not every fixed solver.
    C need not be globally accepting. Reusing a fixed coordinate costs zero NEW
    fixed coordinates, and the intersected cube has dimension N-|A union C|.
    """
    mask_count = 1 << coordinates
    pop = [m.bit_count() for m in range(mask_count)]
    tests = accepted = unchanged = 0
    hist: Counter = Counter()
    minima_hist: Counter = Counter()
    examples = {}
    digest = hashlib.sha256(b"promise-atlas-overlap-v1\n" + bytes([coordinates]))
    for table in sorted(yes):
        for prior_mask in range(mask_count):
            prior = cubes[prior_mask, table & prior_mask]
            bound = minimum_fixed_from_count(prior.live, prior.low_count)
            assert bound is not None  # This prior restriction contains a YES table.
            minimum_new = coordinates + 1
            for cert_mask in range(mask_count):
                union = prior_mask | cert_mask
                intersection = cubes[union, table & union]
                overlap = pop[prior_mask & cert_mask]
                newly_fixed = pop[cert_mask & ~prior_mask]
                tests += 1
                assert intersection.live == prior.live - newly_fixed
                assert intersection.live == coordinates - pop[prior_mask] - pop[cert_mask] + overlap
                if newly_fixed == 0:
                    unchanged += 1
                    assert intersection is prior
                is_accepting = intersection.no_count == 0
                digest.update(struct.pack("<BBBBBHH", table, prior_mask, cert_mask,
                                          newly_fixed, overlap, prior.low_count,
                                          intersection.no_count))
                if not is_accepting:
                    continue
                accepted += 1
                minimum_new = min(minimum_new, newly_fixed)
                assert len(intersection.points) == 1 << (prior.live - newly_fixed)
                assert len(intersection.points) <= prior.low_count
                assert newly_fixed >= bound
                assert (1 << prior.live) <= prior.low_count * (1 << newly_fixed)
                hist[newly_fixed, overlap, intersection.live] += 1
                kinds = []
                if prior_mask == 0:
                    kinds.append("empty_prior")
                if prior.live == 0 and cert_mask == 0:
                    kinds.append("fully_fixed_prior_empty_certificate")
                if cert_mask == 0 and prior.live > 0:
                    kinds.append("empty_certificate_on_already_accepting_prior")
                if overlap > 0 and newly_fixed == 0 and prior.live > 0:
                    kinds.append("wholly_overlapping_certificate_adds_no_constraints")
                if (overlap > 0 and newly_fixed > 0 and intersection.live > 0
                        and pop[prior_mask] + pop[cert_mask] <= coordinates):
                    kinds.append("nontrivial_overlap_changes_naive_dimension")
                for kind in kinds:
                    if kind not in examples:
                        examples[kind] = {
                            "yes_table": table, "prior": prior.as_json(False),
                            "certificate_mask": cert_mask, "certificate_value": table & cert_mask,
                            "certificate_fixed_count": pop[cert_mask], "overlap_fixed_count": overlap,
                            "newly_fixed_count": newly_fixed,
                            "relative_counting_lower_bound_new_fixed": bound,
                            "intersection": intersection.as_json(),
                            "incorrect_dimension_if_overlap_ignored": coordinates - pop[prior_mask] - pop[cert_mask]}
            assert bound <= minimum_new <= prior.live
            minima_hist[minimum_new] += 1
    assert intersect_partial(coordinates, 1, 0, 1, 1) is None
    assert tests == len(yes) * (1 << (2 * coordinates))
    assert unchanged == len(yes) * 3 ** coordinates
    return {"scope": "every YES table and all prior-mask/certificate-mask pairs consistent with it",
            "incidences_not_distinct_pairs": True,
            "pairs_without_any_yes_completion_not_audited_here": True,
            "inconsistent_pairs": "Cannot contain the distinguished YES table; power-of-two dimension formulas below are for compatible assignments only.",
            "contradictory_overlap_endpoint": {
                "prior_mask": 1, "prior_value": 0, "certificate_mask": 1,
                "certificate_value": 1, "intersection": None, "completion_count": 0},
            "relative_certificate_semantics": "only the intersection with the prior restriction must exclude NO; certificate for restricted 1_Low, not necessarily for a fixed solver",
            "pair_incidence_tests": tests, "accepting_pair_incidences": accepted,
            "zero_new_constraint_incidences": unchanged,
            "sha256": digest.hexdigest(),
            "hash_format": "header promise-atlas-overlap-v1\\n + coordinate byte; increasing YES table, prior mask, certificate mask; little-endian <BBBBBHH> table,prior,certificate,new_fixed,overlap,prior_Low_count,intersection_NO_count",
            "all_power_of_two_checks_passed": True,
            "formula": "2^(N-|A union C|) = 2^(prior_live-|C minus A|) <= |Low intersect prior|",
            "relative_minimum_new_fixed_histogram": {str(k): v for k, v in sorted(minima_hist.items())},
            "accepting_incidence_histogram": [
                {"new_fixed": a, "overlap": b, "live_after": c, "count": count}
                for (a, b, c), count in sorted(hist.items())],
            "examples": examples}


def search_outer_classifier(yes: set[int], no: set[int], enumeration: Enumeration) -> dict:
    assert enumeration.arity == 8 and enumeration.bound == OUTER_GATE_BUDGET
    yes_mask = sum(1 << t for t in yes)
    no_mask = sum(1 << t for t in no)
    candidates = []
    best = None
    for function, size in sorted(enumeration.minimum.items()):
        false_negative = yes_mask & ~function
        false_positive = no_mask & function
        errors = false_negative.bit_count() + false_positive.bit_count()
        score = errors, size, function
        if best is None or score < best:
            best = score
        if errors == 0:
            candidates.append(function)
    assert best is not None
    errors, size, function = best
    return {
        "basis": ["AND2", "OR2", "NOT"], "input_count": 8,
        "strict_gate_budget": OUTER_GATE_BUDGET, "enumeration": enumeration.audit,
        "promise_check": "output=1 on every YES and output=0 on every NO; GAP unrestricted",
        "semantic_deduplication_only_after_complete_syntactic_enumeration": True,
        "distinct_classifying_functions_within_budget": len(candidates),
        "status": "classifier_found_within_budget" if candidates else "exhausted_no_classifier_within_budget",
        "beyond_budget": "Not enumerated above 2. Exact minimum and attainability UNKNOWN. See separately reported analytic lower bound from eight promise edges.",
        "minimum_gate_count": min((enumeration.minimum[t] for t in candidates), default=None),
        "certified_minimum_lower_bound": None if candidates else OUTER_GATE_BUDGET + 1,
        "certified_minimum_lower_bound_scope": "bounded enumeration ONLY; not the strongest separate analytic bound",
        "best_bounded_promise_error_count": errors,
        "best_bounded_witness": enumeration.witnesses[function].as_json(),
        "best_bounded_false_negatives": [t for t in sorted(yes) if not (function >> t) & 1],
        "best_bounded_false_positives": [t for t in sorted(no) if (function >> t) & 1],
        "classifying_witnesses": [enumeration.witnesses[t].as_json() for t in candidates],
    }


def promise_essential_edges(inner: Enumeration, yes: set[int], no: set[int]) -> list[dict]:
    """Eight finite witnesses; the arbitrary-DAG support lemma is external."""
    edges = []
    for coordinate in range(8):
        yes_table = 0 if coordinate < 7 else 255
        no_table = yes_table ^ (1 << coordinate)
        assert yes_table in yes and no_table in no
        assert yes_table ^ no_table == 1 << coordinate
        assert inner.minimum[yes_table] == 0
        edges.append({"coordinate": coordinate, "yes_table": yes_table,
                      "no_table": no_table, "xor_difference": 1 << coordinate,
                      "yes_minimum_inner_size": 0,
                      "yes_witness": inner.witnesses[yes_table].as_json(),
                      "no_justification": "absent from the complete inner <=2 enumeration"})
    return edges


def small_arity_checks(one: Enumeration, two: Enumeration) -> dict:
    assert one.minimum == {0: 0, 3: 0, 2: 0, 1: 1}
    assert len(two.minimum) == 14
    xor = Circuit(2, ((AND, 2, 3), (OR, 2, 3), (NOT, 4, -1), (AND, 5, 6)), 7)
    xnor = Circuit(2, ((AND, 2, 3), (OR, 2, 3), (NOT, 5, -1), (OR, 4, 6)), 7)
    assert xor.evaluate() == 6 and xnor.evaluate() == 9
    assert 6 not in two.minimum and 9 not in two.minimum and two.bound == 3
    return {"m1": one.audit, "m2": two.audit,
            "m1_not_input_minimum_gate_count": 1,
            "m2_xor": {"table": 6, "exact_minimum_gate_count": 4, "witness": xor.as_json()},
            "m2_xnor": {"table": 9, "exact_minimum_gate_count": 4, "witness": xnor.as_json()},
            "xor_minimum_justification": "Complete enumeration through 3 finds neither function; explicit 4-gate DAG witnesses supply the matching upper bound. Four-gate circuits were NOT exhaustively enumerated."}


def build_results() -> dict:
    inner = enumerate_dags(3, 2)
    one = enumerate_dags(1, 2)
    two = enumerate_dags(2, 3)
    yes = {t for t, size in inner.minimum.items() if size <= 1}
    gap = {t for t, size in inner.minimum.items() if size == 2}
    low = yes | gap
    no = set(range(256)) - low
    assert [sum(s == g for s in inner.minimum.values()) for g in range(3)] == [5, 9, 26]
    assert (len(yes), len(gap), len(no), len(low)) == (14, 26, 216, 40)
    cubes, cube_summary = build_cube_atlas(8, yes, gap, no)
    certificates = certificate_atlas(8, yes, low, cubes)
    endpoints = counting_endpoints()
    overlap = audit_prior_overlap(8, yes, cubes)
    outer_enum = enumerate_dags(8, OUTER_GATE_BUDGET)
    outer = search_outer_classifier(yes, no, outer_enum)
    checks = small_arity_checks(one, two)
    essential_edges = promise_essential_edges(inner, yes, no)
    tables = []
    for table in range(256):
        size = inner.minimum.get(table)
        tables.append({"table": table,
                       "bits_coordinate_0_first": "".join(str((table >> i) & 1) for i in range(8)),
                       "promise_class": "YES" if table in yes else "GAP" if table in gap else "NO",
                       "minimum_size_class": str(size) if size is not None else ">2",
                       "exact_minimum_size": size,
                       "certified_size_lower_bound": size if size is not None else 3,
                       "witness": inner.witnesses[table].as_json() if size is not None else None})
    zero_certificate = next(r for r in certificates["per_yes_table"] if r["yes_table"] == 0)
    gap_accepting = cubes[127, 0]
    cardinality_not_sufficient = cubes[7, 0]
    assert gap_accepting.no_count == 0 and gap_accepting.gap_count > 0
    assert len(cardinality_not_sufficient.points) <= len(low) and cardinality_not_sufficient.no_count > 0
    assert zero_certificate["minimum_fixed_coordinates"] > certificates["global_cardinality_lower_bound_fixed"]
    work = {
        "circuit_output_visits": sum(e.audit["output_circuit_count"] for e in (inner, one, two, outer_enum)),
        "circuit_program_hash_records": sum(e.audit["program_count"] for e in (inner, one, two, outer_enum)),
        "cube_completion_visits": cube_summary["completion_visits"],
        "cube_hash_records": cube_summary["subcube_count"],
        "yes_subset_tests": certificates["subset_tests"],
        "prior_certificate_pair_incidences": overlap["pair_incidence_tests"],
        "counting_endpoint_equivalences": endpoints["checked_equivalences"],
        "outer_distinct_semantics_tested": len(outer_enum.minimum),
        "promise_edge_checks": len(essential_edges),
    }
    total_work = sum(work.values())
    assert total_work < 3_000_000
    source = Path(__file__).resolve()
    test_source = source.with_name("test_promise_atlas.py")
    return {
        "schema_version": 1, "status": "complete_exact_bounded_enumeration",
        "scope": {"finite_data_only": True, "external_solvers": False,
                  "dependencies": "Python standard library only", "kernel_checked": False,
                  "asymptotic_claims": False, "formula_dp_used_for_circuit_minima": False,
                  "phase1_modified": False,
                  "analytic_consequences_reported_separately": True,
                  "boundary": "Computational minimum/lower-bound claims use only the explicitly enumerated DAG basis and budgets, plus explicit 4-gate XOR/XNOR witnesses. Analytic outer lower bounds use finite witnesses and an external arbitrary-DAG support lemma supplied by the parent; no upper bound or exact outer minimum is asserted. The full atlas is not a Lean proof."},
        "convention": {"basis": ["AND2", "OR2", "NOT"], "not_costs_one_gate": True,
                       "input_complement_is_free": False, "constants_0_1_free": True,
                       "inputs_free": True, "fanout_unrestricted": True,
                       "binary_fanins_ordered_with_repetition": True,
                       "outputs_may_be_any_initial_or_gate_wire": True,
                       "truth_table_bit_a": "f(x) with x_i=(a>>i)&1",
                       "partial_assignment": "mask marks fixed truth-table coordinates; value & ~mask = 0"},
        "promise": {"m": 3, "N": 8, "lower": 1, "upper": 2,
                    "YES": "size<=1", "NO": "size>2", "GAP": "size=2", "Low": "size<=2",
                    "counts": {"YES": len(yes), "NO": len(no), "GAP": len(gap), "Low": len(low)},
                    "sets": {"YES": sorted(yes), "NO": sorted(no), "GAP": sorted(gap), "Low": sorted(low)}},
        "inner_enumeration": inner.audit, "truth_tables": tables,
        "small_arity_generator_checks": checks,
        "subcube_atlas": cube_summary, "promise_yes_certificates": certificates,
        "counting_obstruction": {"low_count": len(low),
                                 "necessary_fixed_coordinate_bound": minimum_fixed_from_count(8, len(low)),
                                 "not_a_sufficiency_claim": True, "endpoints": endpoints},
        "prior_restriction_overlap": overlap,
        "finite_falsification_witnesses": {
            "counting_bound_need_not_be_attained": {
                "false_claim": "A YES table always has a certificate attaining the cardinality lower bound.",
                "yes_table": 0, "cardinality_lower_bound": 3,
                "actual_minimum_fixed_coordinates": zero_certificate["minimum_fixed_coordinates"],
                "minimum_witness": zero_certificate["minimum_witness"],
                "a_counting_allowed_but_invalid_three_coordinate_candidate": cardinality_not_sufficient.as_json()},
            "promise_acceptance_need_not_mean_yes_only": {
                "false_claim": "Every completion of a promise-compatible subcube accepted by 1_Low must be YES (rather than Low).",
                "fixed_solver_caveat": "A particular valid solver may reject the GAP completion 128, so this need not be its accepting subcube.",
                "witness": gap_accepting.as_json(),
                "gap_completions": sorted(t for t in gap_accepting.points if t in gap)},
            "overlap_must_not_be_counted_twice": overlap["examples"]["nontrivial_overlap_changes_naive_dimension"]},
        "optional_finite_lean_witness": {
            "source": "research_notes/p_vs_np_2026_10_09_phase2/validation/AtlasWitness.lean",
            "manifest": "research_notes/p_vs_np_2026_10_09_phase2/validation/atlas_witness.json",
            "log": "research_notes/p_vs_np_2026_10_09_phase2/validation/atlas_witness.log",
            "covers": "Exact two-slot 55*78*7 grammar, explicit Low witnesses, zero-mask obstruction/attainment data, and eight promise edges.",
            "does_not_cover": "Arbitrary-DAG encoding/normalization, the general support lemma, the whole Python atlas, or gate-bound attainability.",
            "validation_status_location": "See the separate manifest and source hash; the whole-atlas kernel_checked flag remains false."},
        "promise_essential_edges": essential_edges,
        "analytic_outer_gate_lower_bounds": {
            "proof_status": "Conditional analytic consequences; the parent supplies and logs the arbitrary-DAG support proof separately. Not an additional synthesis search or a Lean theorem in the Python atlas.",
            "zero_certificate_argument": {
                "maximal_separator_zero_certificate_minimum": 7,
                "external_support_bound": "A fanin-2 DAG with S total gates depends on at most S+1 raw inputs.",
                "consequence_total_gates_at_least": 6,
                "reason": "Fixing all essential inputs to a YES input yields a certificate for a fixed solver, hence a promise-compatible certificate for 1_Low."},
            "eight_promise_edges_argument": {
                "essential_raw_coordinates": list(range(8)),
                "external_support_bound": "A DAG with B binary gates (and any number of unary NOT gates) depends on at most B+1 raw inputs.",
                "consequence_binary_gates_at_least": 7,
                "consequence_total_gates_at_least": 7,
                "reason": "Every valid separator must output differently on each YES/NO edge, so all eight raw inputs are essential."},
            "attainability": "UNKNOWN: no size-6 or size-7 construction or exact outer minimum is claimed.",
            "bounded_search_is_separate": "The exhaustive search remains at most 2 total gates."},
        "outer_classifier_search": outer,
        "bounded_work": {"items": work, "total_named_work_items": total_work,
                         "limit": 3_000_000,
                         "note": "Named enumeration/check work items, not CPU instructions or Python bytecodes; separate unittest replays are not included."},
        "reproducibility": {"source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                            "test_source_sha256": hashlib.sha256(test_source.read_bytes()).hexdigest() if test_source.exists() else None,
                            "generate": "python3 -B research_notes/p_vs_np_2026_10_09_phase2/experiments/promise_atlas.py",
                            "replay": "python3 -B research_notes/p_vs_np_2026_10_09_phase2/experiments/promise_atlas.py --check",
                            "test": "python3 -B research_notes/p_vs_np_2026_10_09_phase2/experiments/test_promise_atlas.py"}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit("Do not disable assertions: run without -O/-OO.")
    destination = Path(__file__).resolve().with_name("promise_results.json")
    result = build_results()
    if args.check:
        if json.loads(destination.read_text()) != result:
            raise SystemExit("FAIL: stored results differ from complete recomputation")
        print("PASS: stored JSON exactly matches complete recomputation")
    else:
        destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"Wrote {destination}")
    print(json.dumps({"promise_counts": result["promise"]["counts"],
                      "minimum_certificate_histogram": result["promise_yes_certificates"]["minimum_certificate_size_histogram"],
                      "certificate_function": "maximal separator 1_Low, not necessarily a fixed solver",
                      "analytic_binary_gate_lower_bound": 7,
                      "analytic_bound_basis": "eight finite promise edges plus the parent's external DAG support lemma; no attainability claim",
                      "outer_status": result["outer_classifier_search"]["status"],
                      "named_work_items": result["bounded_work"]["total_named_work_items"]}, sort_keys=True))


if __name__ == "__main__":
    main()
