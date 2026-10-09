#!/usr/bin/env python3
"""One-round Boolean composition of the Phase 3 noisy YES family.

This is a strict-subpromise recognizer, NOT a full GapMCSP solver. The network
uses only ordinary AND2/OR2/NOT gates: majority decoding, a Boolean 2-CSP
implication graph, and an explicitly expanded transitive-closure circuit.
No SAT oracle or unit-cost population count is hidden in the circuit.

Prior gate interpreters and patching constructors are imported read-only.
Large parameter calculations are symbolic; materialization is budgeted.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import random
import sys

PHASE3 = Path(__file__).resolve().parents[2] / 'p_vs_np_2026_10_09_phase3' / 'experiments'
if str(PHASE3) not in sys.path:
    sys.path.insert(0, str(PHASE3))
import tube_probe as tp  # noqa: E402

TOPS = ('AND', 'NAND', 'XOR')
TEMPLATES = tuple(product(TOPS, (0, 1), (0, 1)))


def bool_op(op: str, a: int, b: int) -> int:
    if op == 'AND':
        return a & b
    if op == 'NAND':
        return 1 ^ (a & b)
    if op == 'XOR':
        return a ^ b
    raise ValueError(op)


def apply_binary(code: int, a: int, b: int, coordinates: int) -> int:
    """A four-bit operation code, indexed by 2*left+right."""
    if type(code) is not int or not 0 <= code < 16 or not 0 <= coordinates <= 1024:
        raise ValueError('invalid operation or materialized dimension')
    mask = (1 << coordinates) - 1
    if min(a, b) < 0 or (a | b) & ~mask:
        raise ValueError('table outside cube')
    result = 0
    for u, v in product((0, 1), repeat=2):
        if (code >> (2 * u + v)) & 1:
            result |= (a if u else mask ^ a) & (b if v else mask ^ b)
    return result


def binary_gate(builder: tp.Builder, code: int, a: int, b: int) -> int:
    """Each two-input Boolean function needs at most four ordinary fresh gates."""
    if type(code) is not int or not 0 <= code < 16:
        raise ValueError('invalid binary operation')
    if code in (0, 15):
        return builder.inputs + (code == 15)
    if code in (12, 10):
        return a if code == 12 else b
    if code in (3, 5):
        return builder.gate('NOT', a if code == 3 else b)
    if code in (8, 14):
        return builder.gate('AND' if code == 8 else 'OR', a, b)
    if code in (7, 1):
        return builder.gate('NOT', builder.gate('AND' if code == 7 else 'OR', a, b))
    if code == 6:
        return tp.xor_gate(builder, a, b)
    if code == 9:
        both = builder.gate('AND', a, b)
        neither = builder.gate('NOT', builder.gate('OR', a, b))
        return builder.gate('OR', both, neither)
    if code in (2, 11):
        return builder.gate('AND' if code == 2 else 'OR', builder.gate('NOT', a), b)
    return builder.gate('AND' if code == 4 else 'OR', a, builder.gate('NOT', b))


def top_table(op: str, a: int, b: int, coordinates: int) -> int:
    return apply_binary({'AND': 8, 'NAND': 7, 'XOR': 6}[op], a, b, coordinates)


def binary_centers(m: int, k: int, max_pairs: int = 100_000) -> tuple[int, ...]:
    atoms = tp.center_tables(m, k)
    if len(atoms) ** 2 > max_pairs:
        raise tp.BudgetExceeded('explicit binary center enumeration exceeds budget')
    mask = (1 << (1 << m)) - 1
    return tuple(sorted({value for a in atoms for b in atoms
                         for value in (a & b, mask ^ (a & b), a ^ b)}))


def _support(m: int, values: tuple[int, ...]) -> None:
    if tuple(sorted(set(values))) != values or any(type(i) is not int or not 0 <= i < m for i in values):
        raise ValueError('support must be sorted, distinct inner coordinates')


def check_regime(m: int, k: int, radius: int) -> None:
    tp.parameters(m, k, radius)
    if 2 * k >= m:
        raise ValueError('parity-fiber decoder requires 2*k < m')
    if 2 * radius >= (1 << (m - 2 * k - 1)):
        raise ValueError('radius exceeds the guaranteed block-majority decoding regime')


@lru_cache(maxsize=128)
def feature_blocks(m: int, union: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    _support(m, union)
    if not 1 <= m <= 12 or len(union) >= m:
        raise tp.BudgetExceeded('require m <= 12 and an unused parity coordinate')
    groups = [[] for _ in range(1 << (len(union) + 1))]
    for address in range(1 << m):
        index = sum(((address >> i) & 1) << j for j, i in enumerate(union))
        groups[2 * index + (address.bit_count() & 1)].append(address)
    expected = 1 << (m - len(union) - 1)
    if any(len(group) != expected for group in groups):
        raise AssertionError('feature fibers are not uniform')
    return tuple(tuple(group) for group in groups)


@lru_cache(maxsize=128)
def slice_layout(left: tuple[int, ...], right: tuple[int, ...]):
    """Common assignments, then left-only rows and right-only columns."""
    common = tuple(sorted(set(left) & set(right)))
    a = tuple(i for i in left if i not in common)
    b = tuple(i for i in right if i not in common)
    union = tuple(sorted(set(left) | set(right)))
    if len(union) > 12:
        raise tp.BudgetExceeded('slice layout materialization exceeds budget')
    def packed(indices, value):
        return {i: (value >> j) & 1 for j, i in enumerate(indices)}
    result = []
    for fixed in range(1 << len(common)):
        rows = []
        for av in range(1 << len(a)):
            row = []
            for bv in range(1 << len(b)):
                values = packed(common, fixed) | packed(a, av) | packed(b, bv)
                row.append(sum(values[i] << j for j, i in enumerate(union)))
            rows.append(tuple(row))
        result.append(tuple(rows))
    return tuple(result)


def template_label(template: tuple[str, int, int], u: int, v: int) -> tuple[int, int]:
    op, alpha, beta = template
    return bool_op(op, u, v), bool_op(op, u ^ alpha, v ^ beta)


def validate_labels(labels) -> tuple[int, int]:
    rows = len(labels)
    cols = len(labels[0]) if rows else 0
    if not rows or not cols or any(len(row) != cols for row in labels):
        raise ValueError('nonempty rectangular label matrix required')
    if any(tuple(label) not in ((0, 0), (0, 1), (1, 0), (1, 1)) for row in labels for label in row):
        raise ValueError('each cell has two Boolean labels')
    return rows, cols


def brute_slice_witness(labels, template) -> tuple[int, int] | None:
    """Independent literal enumeration; never used by the compiled recognizer."""
    rows, cols = validate_labels(labels)
    if rows + cols > 16:
        raise tp.BudgetExceeded('brute constraint witness budget exceeded')
    for left in range(1 << rows):
        for right in range(1 << cols):
            if all(template_label(template, (left >> r) & 1, (right >> c) & 1) == labels[r][c]
                   for r in range(rows) for c in range(cols)):
                return left, right
    return None


def slice_sat(labels, template) -> bool:
    """Reference 2-SAT decision via separate graph traversals, not Warshall."""
    rows, cols = validate_labels(labels)
    vertices = 2 * (rows + cols)
    if vertices > 256:
        raise tp.BudgetExceeded('reference implication graph budget exceeded')
    edges = [set() for _ in range(vertices)]
    for r in range(rows):
        for c in range(cols):
            for u, v in product((0, 1), repeat=2):
                if template_label(template, u, v) != labels[r][c]:
                    edges[2*r+u].add(2*(rows+c)+(1-v))
                    edges[2*(rows+c)+v].add(2*r+(1-u))
    reach = []
    for start in range(vertices):
        seen, todo = set(), [start]
        while todo:
            x = todo.pop()
            if x not in seen:
                seen.add(x)
                todo.extend(edges[x] - seen)
        reach.append(seen)
    return not any(2*i+1 in reach[2*i] and 2*i in reach[2*i+1] for i in range(rows+cols))


def semantic_pair(m: int, table: int, left: tuple[int, ...], right: tuple[int, ...], radius: int) -> bool:
    union = tuple(sorted(set(left) | set(right)))
    decoded, errors = [], 0
    for group in feature_blocks(m, union):
        ones = sum((table >> i) & 1 for i in group)
        decoded.append(int(2 * ones > len(group)))
        errors += min(ones, len(group)-ones)
    if errors > radius:
        return False
    layout = slice_layout(left, right)
    labels = [tuple(tuple((decoded[2*i], decoded[2*i+1]) for i in row) for row in block)
              for block in layout]
    return any(all(slice_sat(block, template) for block in labels) for template in TEMPLATES)


def semantic_recognize(m: int, k: int, radius: int, table: int) -> bool:
    check_regime(m, k, radius)
    tp.validate_table(m, table)
    if m > 10 or comb(m, k) ** 2 > 1000:
        raise tp.BudgetExceeded('semantic support-pair budget exceeded')
    choices = tuple(combinations(range(m), k))
    return any(semantic_pair(m, table, left, right, radius) for left in choices for right in choices)


def label_bad_wires(builder: tp.Builder, label: tuple[int, int]) -> tuple[int, ...]:
    a, b = label
    na, nb = builder.gate('NOT', a), builder.gate('NOT', b)
    return tuple(builder.gate('OR', a if not u else na, b if not v else nb)
                 for u, v in product((0, 1), repeat=2))


def compile_slice_sat(builder: tp.Builder, bads, template) -> int:
    rows, cols = len(bads), len(bads[0])
    if any(len(row) != cols for row in bads) or not rows or not cols:
        raise ValueError('invalid compiled label layout')
    variables, zero, one = rows + cols, builder.inputs, builder.inputs + 1
    vertices = 2 * variables
    if vertices > 64:
        raise tp.BudgetExceeded('dense closure circuit vertex budget exceeded')
    reach = [[one if i == j else zero for j in range(vertices)] for i in range(vertices)]
    for r in range(rows):
        for c in range(cols):
            for u, v in product((0, 1), repeat=2):
                e0, e1 = template_label(template, u, v)
                wire = bads[r][c][2*e0+e1]
                # Each endpoint pair is unique. Row/column unknowns are distinct,
                # even when their original address supports overlap completely.
                reach[2*r+u][2*(rows+c)+(1-v)] = wire
                reach[2*(rows+c)+v][2*r+(1-u)] = wire
    for pivot in range(vertices):
        old = reach
        reach = [[builder.gate('OR', old[i][j], builder.gate('AND', old[i][pivot], old[pivot][j]))
                  for j in range(vertices)] for i in range(vertices)]
    checks = [builder.gate('NOT', builder.gate('AND', reach[2*i][2*i+1], reach[2*i+1][2*i]))
              for i in range(variables)]
    return builder.fold('AND', checks)


def size_estimate(m: int, k: int, radius: int) -> dict:
    check_regime(m, k, radius)
    n, supports = 1 << m, comb(m, k)
    rows = []
    for overlap in range(k + 1):
        multiplicity = supports * comb(k, overlap) * comb(m-k, k-overlap)
        union = 2*k-overlap
        blocks, block_size = 1 << (union+1), 1 << (m-union-1)
        b, w = m-union, m+1
        decoder = n*(5*b-1)+blocks*(2*b+1)+4*n+n*(5*w-1)+2*w
        common = 1 << overlap
        variables = 1 << (k-overlap+1)
        graph = 16*variables**3+3*variables-1
        structure = 6*(1 << union)+len(TEMPLATES)*(common*graph+common-1)+len(TEMPLATES)-1
        pair_size = decoder+structure+1
        rows.append({'overlap':overlap,'ordered_support_pairs':multiplicity,
                     'union_size':union,'feature_blocks':blocks,'fiber_size':block_size,
                     'variables_per_slice':variables,'graph_gates_per_slice':graph,
                     'decoder_gates':decoder,'structure_gates':structure,'pair_gates':pair_size,
                     'majority_surplus_lower_bound_per_pair':2*n-blocks})
    pairs = supports**2
    return {'N':n,'supports':supports,'ordered_pairs':pairs,'by_overlap':rows,
            'gates':sum(row['ordered_support_pairs']*row['pair_gates'] for row in rows)+pairs-1,
            'simple_gate_upper_bound':4000*pairs*(n*(m+1)+(1 << (3*k))),
            'majority_surplus_lower_bound':sum(row['ordered_support_pairs']*row['majority_surplus_lower_bound_per_pair'] for row in rows)}


@dataclass(frozen=True)
class Recognizer:
    circuit: tp.Circuit
    majority_wires: tuple[int, ...]
    estimate: dict


def build_recognizer(m: int, k: int, radius: int, max_gates: int = 2_000_000) -> Recognizer:
    estimate = size_estimate(m, k, radius)
    if m > 10 or estimate['gates'] > max_gates:
        raise tp.BudgetExceeded('outer ordinary-gate materialization budget exceeded')
    n = 1 << m
    builder = tp.Builder(n)
    outputs, majorities = [], []
    supports = tuple(combinations(range(m), k))
    for left in supports:
        for right in supports:
            union = tuple(sorted(set(left) | set(right)))
            decoded, errors = [], []
            for group in feature_blocks(m, union):
                count = tp.popcount(builder, group)
                value = builder.gate('NOT', tp.leq_constant(builder, count, len(group)//2))
                decoded.append(value)
                majorities.append(value)
                errors.extend(tp.xor_gate(builder, i, value) for i in group)
            close = tp.leq_constant(builder, tp.popcount(builder, tuple(errors)), radius)
            bad = [label_bad_wires(builder, (decoded[2*i],decoded[2*i+1])) for i in range(1 << len(union))]
            layout = slice_layout(left, right)
            templates = []
            for template in TEMPLATES:
                checks = [compile_slice_sat(builder, tuple(tuple(bad[i] for i in row) for row in block), template)
                          for block in layout]
                templates.append(builder.fold('AND', checks))
            valid = builder.fold('OR', templates)
            outputs.append(builder.gate('AND', close, valid))
    circuit = builder.finish(builder.fold('OR', outputs))
    if circuit.size != estimate['gates']:
        raise AssertionError(('gate count mismatch', circuit.size, estimate['gates']))
    return Recognizer(circuit, tuple(majorities), estimate)


def evaluate_samples(circuit: tp.Circuit, samples: tuple[int, ...], max_samples: int = 1024) -> tuple[bool, ...]:
    """Independent bit-vector interpreter on a fixed list, not all 2**N inputs."""
    if len(samples) > max_samples or circuit.inputs > 1024:
        raise tp.BudgetExceeded('sample vector budget exceeded')
    if any(type(x) is not int or x < 0 or x.bit_length() > circuit.inputs for x in samples):
        raise ValueError('invalid sample table')
    full = (1 << len(samples))-1
    values = [sum(((x >> i) & 1) << j for j,x in enumerate(samples)) for i in range(circuit.inputs)]+[0,full]
    for pos,gate in enumerate(circuit.gates):
        if any(not 0 <= i < circuit.inputs+2+pos for i in gate.inputs):
            raise ValueError('forward/invalid wire')
        if gate.op == 'NOT' and len(gate.inputs)==1:
            values.append(full ^ values[gate.inputs[0]])
        elif gate.op in ('AND','OR') and len(gate.inputs)==2:
            a,b=(values[i] for i in gate.inputs)
            values.append(a & b if gate.op=='AND' else a | b)
        else:
            raise ValueError('invalid gate')
    result=values[circuit.output]
    return tuple(bool((result >> j)&1) for j in range(len(samples)))


def circuit_hash(circuit: tp.Circuit) -> str:
    h=hashlib.sha256(f'{circuit.inputs}:{circuit.output}\n'.encode())
    for gate in circuit.gates:
        h.update((gate.op+':'+','.join(map(str,gate.inputs))+'\n').encode())
    return h.hexdigest()


def reachable_gates(builder: tp.Builder, output: int) -> set[int]:
    first=builder.inputs+2
    if not 0 <= output < first+len(builder.gates):
        raise ValueError('invalid output')
    seen,todo=set(),[output]
    while todo:
        x=todo.pop()
        if x>=first and x not in seen:
            seen.add(x)
            todo.extend(builder.gates[x-first].inputs)
    return seen


class SharedInner:
    """Multi-output DAG with explicitly shared negations, parity and repeated atoms."""
    def __init__(self,m: int):
        tp.parameters(m,0,0)
        if m>64:
            raise tp.BudgetExceeded('inner circuit construction budget exceeded')
        self.m=m
        self.builder=tp.Builder(m)
        self.negations={}
        self.parity=None
        self.atoms={}

    def atom(self,support: tuple[int,...],table: int,shifted: bool=False) -> int:
        _support(self.m,support)
        k=len(support)
        if k>8 or table<0 or table.bit_length()>(1 << k):
            raise ValueError('invalid or oversized primitive')
        key=(support,table,shifted)
        if key in self.atoms:
            return self.atoms[key]
        b=self.builder
        for i in support:
            if i not in self.negations:
                self.negations[i]=b.gate('NOT',i)
        terms=[]
        for value in range(1 << k):
            if (table >> value)&1:
                terms.append(b.fold('AND',[i if (value >> j)&1 else self.negations[i] for j,i in enumerate(support)]))
        wire=b.fold('OR',terms)
        if shifted:
            if self.parity is None:
                self.parity=0
                for i in range(1,self.m):
                    self.parity=tp.xor_gate(b,self.parity,i)
            wire=tp.xor_gate(b,wire,self.parity)
        self.atoms[key]=wire
        return wire

    def compose(self,left: int,right: int,op: str) -> tuple[tp.Circuit,dict]:
        b=self.builder
        a,c=reachable_gates(b,left),reachable_gates(b,right)
        if op=='XOR':
            output=tp.xor_gate(b,left,right)
            new=4
        elif op in ('AND','NAND'):
            output=b.gate('AND',left,right)
            new=1
            if op=='NAND':
                output=b.gate('NOT',output)
                new=2
        else:
            raise ValueError(op)
        result=b.finish(output)
        actual=reachable_gates(b,output)
        data={'left_gates':len(a),'right_gates':len(c),'shared_gates':len(a&c),
              'union_gates':len(a|c),'top_gates':new,'reachable_composition_gates':len(actual),
              'allocated_gates':result.size}
        if len(actual)!=len(a)+len(c)-len(a&c)+new:
            raise AssertionError('shared gate accounting failed')
        return result,data


def fixed_beta_sample(m: int,beta: Fraction,epsilon: Fraction,c: int=1) -> dict:
    if not isinstance(epsilon,Fraction) or epsilon<=0:
        raise ValueError('epsilon must be a positive Fraction')
    if not isinstance(beta,Fraction) or not 0<beta<Fraction(1,5):
        raise ValueError('this regime needs fixed beta in (0,1/5)')
    base=tp.schedule(m,beta,c)
    k,r=base['k'],base['radius']
    radius=2*r
    estimate=size_estimate(m,k,radius)
    inner=2*tp.center_size_bound(m,k)+4+m+radius*m+3
    exponent=m-4*k-1
    separation=(1 << exponent) if exponent>=0 else None
    power=(1+epsilon)*m
    if power.denominator!=1 or epsilon<=0:
        raise ValueError('exact epsilon comparison requires integral exponent')
    return {'m':m,'beta':str(beta),'epsilon':str(epsilon),'c':c,'s1':base['s1'],'s2':base['s2'],
            'k':k,'seed_radius':r,'output_radius':radius,'inner_upper_bound':inner,
            'all_accepted_are_YES_by_bound':inner<=base['s1'],
            'coarse_separation':separation,'separated_tubes':separation is not None and separation>2*radius+1,
            'outer_gates_symbolic':estimate['gates'],'outer_gates_bit_length':estimate['gates'].bit_length(),
            'outer_size_below_target':estimate['gates']<(1 << power.numerator),
            'ordered_support_pairs':estimate['ordered_pairs'],'materialized':False}


def run_experiment(seed: int=11204) -> dict:
    rng=random.Random(seed)
    full=[]
    for m,k,radius in ((3,0,0),(3,1,0),(4,0,2)):
        centers=binary_centers(m,k)
        net=build_recognizer(m,k,radius)
        # At most 16 OUTER inputs here. Larger cases below use explicit samples.
        actual=tp.evaluate_packed(net.circuit,max_inputs=16)
        accepted={x for x in range(1 << (1 << m)) if min((x^c).bit_count() for c in centers)<=radius}
        expected=sum(1 << x for x in accepted)
        if actual!=expected:
            raise AssertionError(('complete circuit replay failed',m,k,radius))
        sharing=tp.sharing_measurements(net)
        if sharing['majority_surplus']<net.estimate['majority_surplus_lower_bound']:
            raise AssertionError('decoder sharing undercount')
        row={'m':m,'k':k,'radius':radius,'input_comparisons':1 << (1 << m),
             'centers':len(centers),'accepted_tables':len(accepted),'center_minimum_distance':tp.minimum_distance(centers),
             'ordinary_gates':net.circuit.size,'circuit_sha256':circuit_hash(net.circuit),'sharing':sharing}
        if m==3 and k==1:
            row['certificate_atlas']=tp.cube_profile(8,accepted)
            row['phase3_missed_AND_now_accepted']=136 in accepted
            row['omitted_five_gate_table']=120
            if 120 in accepted or row['certificate_atlas']['maximum_accepting_dimension']!=0:
                raise AssertionError('selected exact control failed')
        full.append(row)
    # One genuinely noisy round on ALL primitive supports, with nontrivial XOR/AND/NAND.
    m,k,r=6,1,1
    radius=2*r
    centers=binary_centers(m,k)
    atoms=tp.center_tables(m,k)
    net=build_recognizer(m,k,radius)
    samples=[]
    for _ in range(96):
        a,b=rng.choice(atoms),rng.choice(atoms)
        x=a^(1 << rng.randrange(64))
        y=b^(1 << rng.randrange(64))
        code=rng.randrange(16)
        value=apply_binary(code,x,y,64)
        center=apply_binary(code,a,b,64)
        if center not in centers or (value^center).bit_count()>2:
            raise AssertionError('one-round noisy closure failed')
        samples.append(value)
    for _ in range(32):
        center=rng.choice(centers)
        changes=rng.sample(range(64),2)
        samples.append(center ^ sum(1 << i for i in changes))
    samples.extend(rng.getrandbits(64) for _ in range(64))
    missing=sum((sum((a >> i)&1 for i in range(3))%2) << a for a in range(64))
    samples.append(missing)
    actual=evaluate_samples(net.circuit,tuple(samples))
    expected=tuple(min((x^c).bit_count() for c in centers)<=radius for x in samples)
    if actual!=expected or not all(actual[:128]) or actual[-1]:
        raise AssertionError('sampled noisy circuit failed')
    sharing=tp.sharing_measurements(net)
    large={'m':m,'k':k,'seed_radius':r,'output_radius':radius,'primitive_centers':len(atoms),
           'binary_centers':len(centers),'center_minimum_distance':tp.minimum_distance(centers),
           'sample_count':len(samples),'forced_positive_samples':128,'ordinary_gates':net.circuit.size,
           'circuit_sha256':circuit_hash(net.circuit),'sharing':sharing,
           'omitted_three_bit_parity':missing,'omitted_distance':min((missing^c).bit_count() for c in centers),
           'accepted_count_from_disjoint_ball_count':len(centers)*sum(comb(64,i) for i in range(3)),
           'certificate_dimension_bound_from_separation':2}
    if large['center_minimum_distance']<=2*radius+1:
        raise AssertionError('large finite separated-tube claim failed')
    inner=[]
    for _ in range(48):
        m,k=6,1
        joint=SharedInner(m)
        left_support=(rng.randrange(m),)
        right_support=(rng.randrange(m),)
        left=joint.atom(left_support,rng.randrange(4),bool(rng.randrange(2)))
        right=joint.atom(right_support,rng.randrange(4),bool(rng.randrange(2)))
        op=rng.choice(TOPS)
        circuit,cost=joint.compose(left,right,op)
        if circuit.truth_table() not in centers or circuit.size>2*tp.center_size_bound(m,k)+4:
            raise AssertionError('inner witness/cost failed')
        changes=tuple(sorted(rng.sample(range(64),rng.randrange(3))))
        patched=tp.patch_truth_table(circuit,changes)
        expected_table=circuit.truth_table() ^ sum(1 << i for i in changes)
        if patched.truth_table()!=expected_table:
            raise AssertionError('inner patch semantics failed')
        cost_bound=circuit.size if not changes else circuit.size+m+len(changes)*m+3
        if patched.size>cost_bound:
            raise AssertionError('inner patch cost failed')
        inner.append(cost | {'operation':op,'patches':len(changes),'patched_gates':patched.size})
    # Same-k shared parity and repeated-atom controls, independent of the random cases.
    joint=SharedInner(6)
    a=joint.atom((0,),2,True)
    b=joint.atom((1,),2,True)
    _,shared_parity=joint.compose(a,b,'XOR')
    joint=SharedInner(6)
    a=joint.atom((0,),2,True)
    b=joint.atom((0,),2,True)
    _,repeated=joint.compose(a,b,'AND')
    joint=SharedInner(6)
    a,b,c=(joint.atom((i,),2) for i in range(3))
    first,first_cost=joint.compose(a,b,'XOR')
    second,second_cost=joint.compose(first.output,c,'XOR')
    first_table,second_table=first.truth_table(),second.truth_table()
    if first_table not in centers or second_table in centers or second_table!=missing or second_cost['reachable_composition_gates']!=8:
        raise AssertionError('one-more-round budgeted closure control failed')
    further={'first_table':first_table,'second_table':second_table,'first_cost':first_cost,
             'second_cost':second_cost,'first_is_binary_center':True,
             'second_distance_from_binary_centers':32,'second_is_accepted':False}
    examples=[fixed_beta_sample(m,beta,eps) for m,beta,eps in
              ((512,Fraction(1,16),Fraction(3,4)),
               (1536,Fraction(1,32),Fraction(1,2)),
               (3072,Fraction(1,64),Fraction(1,3)))]
    if not all(x['all_accepted_are_YES_by_bound'] and x['separated_tubes'] and x['outer_size_below_target'] for x in examples):
        raise AssertionError('fixed beta arithmetic control failed')
    return {'schema_version':1,'seed':seed,
            'scope':'A strict YES subfamily, complete for ONE binary-composition round of Phase 3 noisy inputs. NOT full budgeted closure or full GapMCSP.',
            'full_circuit_replays':full,'all_input_comparisons':sum(x['input_comparisons'] for x in full),
            'noisy_round_sampled_circuit':large,'inner_shared_compositions':inner,
            'explicit_sharing_controls':{'shared_parity':shared_parity,'identical_atom':repeated},
            'one_more_round_witness':further,
            'symbolic_fixed_beta_examples':examples,'failures':[]}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--output',type=Path)
    group.add_argument('--check',type=Path)
    args=parser.parse_args(argv)
    result=run_experiment()
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
        print(f'Wrote {args.output}: {result["all_input_comparisons"]} complete input comparisons.')
    elif args.check:
        if json.loads(args.check.read_text())!=json.loads(text):
            raise SystemExit('replay differs from saved composition artifact')
        print('Exact composition replay matches.')
    else:
        print(text,end='')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
