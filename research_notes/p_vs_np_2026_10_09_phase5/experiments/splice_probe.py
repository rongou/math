#!/usr/bin/env python3
"""Exact prefix splices of Phase 4 centers, with optional old noisy inputs.

NOT full GapMCSP. Prefix/suffix extendability is decided by the earliest
inconsistent prefix of a 2-CNF model. Edge activation times are propagated
with min/max bottleneck closure, implemented with ordinary Boolean gates.
No SAT oracle, unit-cost integer comparison, or enumeration of all cuts or
center functions is hidden in the compiled circuit.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import random
import sys

PHASE4 = Path(__file__).resolve().parents[2] / 'p_vs_np_2026_10_09_phase4' / 'experiments'
if str(PHASE4) not in sys.path:
    sys.path.insert(0, str(PHASE4))
import composition_probe as cp  # noqa: E402

tp = cp.tp


def splice(n: int, cut: int, left: int, right: int) -> int:
    if type(n) is not int or not 0 <= n <= 4096 or type(cut) is not int or not 0 <= cut <= n:
        raise ValueError('invalid splice length or cut')
    if any(type(x) is not int or x < 0 or x.bit_length() > n for x in (left,right)):
        raise ValueError('table outside cube')
    prefix = (1 << cut) - 1
    return (left & prefix) | (right & (((1 << n) - 1) ^ prefix))


def brute_match_lengths(n: int, table: int, centers: tuple[int,...]) -> tuple[int,int]:
    if not centers:
        raise ValueError('nonempty center family required')
    p = q = 0
    for center in centers:
        diff = table ^ center
        if diff == 0:
            return n,n
        p = max(p, (diff & -diff).bit_length() - 1)
        q = max(q, n - diff.bit_length())
    return p,q


def brute_splice_distance(n: int,table: int,centers: tuple[int,...]) -> int:
    if not centers or (n+1)*len(centers)>500_000:
        raise tp.BudgetExceeded('exact finite splice-distance budget exceeded')
    full=(1 << n)-1
    return min(min(((table^c)&((1 << cut)-1)).bit_count() for c in centers)+
               min(((table^c)&(full^((1 << cut)-1))).bit_count() for c in centers)
               for cut in range(n+1))


def explicit_splices(n: int, centers: tuple[int,...], budget: int = 2_000_000) -> set[int]:
    if len(centers)**2 * (n+1) > budget:
        raise tp.BudgetExceeded('explicit splice enumeration exceeds budget')
    return {splice(n,j,f,g) for f in centers for g in centers for j in range(n+1)}


@lru_cache(maxsize=256)
def address_features(m: int, left: tuple[int,...], right: tuple[int,...]):
    cp._support(m,left)
    cp._support(m,right)
    if not 1 <= m <= 12:
        raise tp.BudgetExceeded('address feature materialization supports m <= 12')
    return tuple((sum(((a>>i)&1) << j for j,i in enumerate(left)),
                  sum(((a>>i)&1) << j for j,i in enumerate(right)),
                  a.bit_count()&1) for a in range(1 << m))


def bottleneck_closure(weights: tuple[tuple[int,...],...]) -> tuple[tuple[int,...],...]:
    n=len(weights)
    if not n or any(len(row)!=n for row in weights) or any(type(x) is not int or x<0 for row in weights for x in row):
        raise ValueError('nonempty square nonnegative integer matrix required')
    if n>64:
        raise tp.BudgetExceeded('numeric bottleneck vertex budget exceeded')
    current=[list(row) for row in weights]
    for pivot in range(n):
        old=current
        current=[[min(old[i][j],max(old[i][pivot],old[pivot][j])) for j in range(n)] for i in range(n)]
    return tuple(tuple(row) for row in current)


def model_weights(m: int, table: int, left: tuple[int,...], right: tuple[int,...], template, reverse=False):
    tp.validate_table(m,table)
    if len(left)!=len(right) or len(left)>4:
        raise ValueError('equal, bounded support sizes required')
    n=1 << m
    size=1 << len(left)
    vertices=4*size
    inf=n+1
    weights=[[0 if i==j else inf for j in range(vertices)] for i in range(vertices)]
    op,alpha,beta=template
    for address,(a,b,parity) in enumerate(address_features(m,left,right)):
        time=(n-address) if reverse else (address+1)
        value=(table >> address)&1
        for u,v in product((0,1),repeat=2):
            if cp.bool_op(op,u^(alpha&parity),v^(beta&parity)) != value:
                x,y=2*a+u,2*(size+b)+(1-v)
                weights[x][y]=min(weights[x][y],time)
                x,y=2*(size+b)+v,2*a+(1-u)
                weights[x][y]=min(weights[x][y],time)
    return tuple(tuple(row) for row in weights)


def first_inconsistent(weights) -> int:
    if len(weights)%2:
        raise ValueError('paired literal vertices required')
    reach=bottleneck_closure(weights)
    return min(max(reach[2*i][2*i+1],reach[2*i+1][2*i]) for i in range(len(reach)//2))


def numeric_match_lengths(m: int,k: int,table: int) -> tuple[int,int]:
    tp.parameters(m,k,0)
    tp.validate_table(m,table)
    if m>8 or len(cp.TEMPLATES)*comb(m,k)**2>1000:
        raise tp.BudgetExceeded('numeric all-model budget exceeded')
    n=1 << m
    supports=tuple(combinations(range(m),k))
    best_prefix=best_suffix=1
    for left in supports:
        for right in supports:
            for template in cp.TEMPLATES:
                a=first_inconsistent(model_weights(m,table,left,right,template))
                if a==n+1:
                    return n,n  # Full table itself belongs to the center family.
                b=first_inconsistent(model_weights(m,table,left,right,template,True))
                best_prefix=max(best_prefix,a)
                best_suffix=max(best_suffix,b)
    return best_prefix-1,best_suffix-1


class FoldingBuilder(tp.Builder):
    """Ordinary gates with local Boolean identities and exact-node sharing only."""
    def __init__(self,inputs: int,max_gates=2_000_000,max_word_calls=2_000_000):
        super().__init__(inputs)
        self.max_gates=max_gates
        self.max_word_calls=max_word_calls
        self.requests=0
        self.word_calls=0
        self.cache={}
        self.words={}

    def gate(self,op: str,*args: int) -> int:
        self.requests+=1
        if op not in ('AND','OR','NOT') or len(args)!=(1 if op=='NOT' else 2):
            raise ValueError('ordinary gate basis/arities only')
        available=self.inputs+2+len(self.gates)
        if any(type(x) is not int or not 0<=x<available for x in args):
            raise ValueError('invalid or forward wire')
        zero,one=self.inputs,self.inputs+1
        if op=='NOT':
            a=args[0]
            if a in (zero,one):
                return one if a==zero else zero
            if a>=self.inputs+2 and self.gates[a-self.inputs-2].op=='NOT':
                return self.gates[a-self.inputs-2].inputs[0]
        else:
            a,b=sorted(args)
            args=(a,b)
            if a==b:
                return a
            if op=='AND':
                if zero in args:
                    return zero
                if one in args:
                    return b if a==one else a
            else:
                if one in args:
                    return one
                if zero in args:
                    return b if a==zero else a
        key=(op,args)
        if key in self.cache:
            return self.cache[key]
        if len(self.gates)>=self.max_gates:
            raise tp.BudgetExceeded('allocated ordinary gate budget exceeded')
        wire=super().gate(op,*args)
        self.cache[key]=wire
        return wire

    def word(self,value: int,width: int) -> tuple[int,...]:
        if not 0<=value<(1 << width):
            raise ValueError('constant word out of range')
        return tuple(self.inputs+((value>>i)&1) for i in range(width))

    def word_constant(self,bits) -> int | None:
        if all(x in (self.inputs,self.inputs+1) for x in bits):
            return sum((x==self.inputs+1) << i for i,x in enumerate(bits))
        return None

    def less(self,a,b) -> int:
        if not a or len(a)!=len(b):
            raise ValueError('equal nonempty word widths required')
        out=self.inputs
        for x,y in zip(a,b):
            previous=out
            out=self.gate('OR',self.gate('AND',self.gate('NOT',x),self.gate('OR',y,previous)),
                          self.gate('AND',y,previous))
        return out

    def extremum(self,a,b,maximum: bool) -> tuple[int,...]:
        a,b=tuple(a),tuple(b)
        if not a or len(a)!=len(b):
            raise ValueError('word widths differ')
        self.word_calls+=1
        if self.word_calls>self.max_word_calls:
            raise tp.BudgetExceeded('word-operation budget exceeded')
        if a==b:
            return a
        if b<a:
            a,b=b,a
        key=(maximum,a,b)
        if key in self.words:
            return self.words[key]
        x,y=self.word_constant(a),self.word_constant(b)
        full=(1 << len(a))-1
        if x is not None and y is not None:
            result=self.word(max(x,y) if maximum else min(x,y),len(a))
        elif maximum and (x==full or y==full):
            result=self.word(full,len(a))
        elif not maximum and (x==0 or y==0):
            result=self.word(0,len(a))
        elif maximum and (x==0 or y==0):
            result=b if x==0 else a
        elif not maximum and (x==full or y==full):
            result=b if x==full else a
        else:
            choose=self.less(a,b)
            negative=self.gate('NOT',choose)
            low,high=(b,a) if maximum else (a,b)
            result=tuple(self.gate('OR',self.gate('AND',choose,x),self.gate('AND',negative,y))
                         for x,y in zip(low,high))
        self.words[key]=result
        return result

    def minimum(self,a,b):
        return self.extremum(a,b,False)

    def maximum(self,a,b):
        return self.extremum(a,b,True)


def add_words(builder: tp.Builder,a,b) -> tuple[int,...]:
    if not a or len(a)!=len(b):
        raise ValueError('equal nonempty word widths required')
    carry=builder.inputs
    result=[]
    for x,y in zip(a,b):
        parity=tp.xor_gate(builder,x,y)
        result.append(tp.xor_gate(builder,parity,carry))
        carry=builder.gate('OR',builder.gate('AND',x,y),builder.gate('AND',parity,carry))
    return tuple(result+[carry])


def conditional_time(builder: FoldingBuilder,not_bad: int,time: int,width: int):
    # Infinity is the largest unsigned word; finite event times are <= N.
    return tuple(builder.inputs+1 if (time>>i)&1 else not_bad for i in range(width))


def compile_first_failure(builder: FoldingBuilder,m: int,left,right,template,reverse=False):
    n,width=1 << m,m+1
    half=1 << len(left)
    vertices=4*half
    inf=builder.word((1 << width)-1,width)
    zero=builder.word(0,width)
    reach=[[zero if i==j else inf for j in range(vertices)] for i in range(vertices)]
    op,alpha,beta=template
    for address,(a,b,parity) in enumerate(address_features(m,left,right)):
        bit=address
        not_bit=builder.gate('NOT',bit)
        time=n-address if reverse else address+1
        for u,v in product((0,1),repeat=2):
            expected=cp.bool_op(op,u^(alpha&parity),v^(beta&parity))
            not_bad=not_bit if expected==0 else bit
            event=conditional_time(builder,not_bad,time,width)
            x,y=2*a+u,2*(half+b)+(1-v)
            reach[x][y]=builder.minimum(reach[x][y],event)
            x,y=2*(half+b)+v,2*a+(1-u)
            reach[x][y]=builder.minimum(reach[x][y],event)
    for pivot in range(vertices):
        old=reach
        reach=[[builder.minimum(old[i][j],builder.maximum(old[i][pivot],old[pivot][j]))
                for j in range(vertices)] for i in range(vertices)]
    failures=[builder.maximum(reach[2*i][2*i+1],reach[2*i+1][2*i]) for i in range(vertices//2)]
    result=failures[0]
    for value in failures[1:]:
        result=builder.minimum(result,value)
    # A fully extendable table has failure time N+1, not the unsigned infinity.
    return builder.minimum(result,builder.word(n+1,width))


def splice_gate_bound(m: int,k: int) -> dict:
    tp.parameters(m,k,0)
    n,width=1 << m,m+1
    variables=1 << (k+1)
    vertices=2*variables
    models=len(cp.TEMPLATES)*comb(m,k)**2
    extremum=8*width+1
    per_model=8*n*extremum+(16*width+2)*vertices**3+(2*variables)*extremum
    total=n+2*(models*per_model+(models-1)*extremum)+11*width+2*(width+1)+1
    return {'N':n,'word_width':width,'models':models,'literal_vertices':vertices,
            'unoptimized_gate_upper_bound':total,'word_extremum_gate_bound':extremum,
            'asymptotic_expression':'O(binomial(m,k)^2*(m+1)*(N+2^(3k)))'}


@dataclass(frozen=True)
class SpliceRecognizer:
    circuit: tp.Circuit
    bound: dict
    construction: dict


def build_splice_recognizer(m: int,k: int,legacy_radius: int | None=None,
                           max_gates=2_000_000,max_logical_gates=25_000_000) -> SpliceRecognizer:
    bound=splice_gate_bound(m,k)
    if m>8 or bound['unoptimized_gate_upper_bound']>max_logical_gates:
        raise tp.BudgetExceeded('logical construction budget exceeded')
    if legacy_radius is not None:
        cp.check_regime(m,k,legacy_radius)
    builder=FoldingBuilder(1 << m,max_gates=max_gates)
    supports=tuple(combinations(range(m),k))
    best=[]
    for reverse in (False,True):
        result=None
        for left in supports:
            for right in supports:
                for template in cp.TEMPLATES:
                    current=compile_first_failure(builder,m,left,right,template,reverse)
                    result=current if result is None else builder.maximum(result,current)
        best.append(result)
    total=add_words(builder,best[0],best[1])
    output=builder.gate('NOT',tp.leq_constant(builder,total,(1 << m)+1))
    splice_allocated=len(builder.gates)
    legacy_allocated=0
    if legacy_radius is not None:
        old=cp.build_recognizer(m,k,legacy_radius,max_gates=max_gates).circuit
        legacy_allocated=old.size
        mapping=list(range(old.inputs+2))
        for gate in old.gates:
            mapping.append(builder.gate(gate.op,*(mapping[i] for i in gate.inputs)))
        output=builder.gate('OR',output,mapping[old.output])
    circuit=builder.finish(output)
    allowed=bound['unoptimized_gate_upper_bound']+legacy_allocated+(legacy_radius is not None)
    if circuit.size>allowed:
        raise AssertionError('gate upper bound violated')
    return SpliceRecognizer(circuit,bound,{'ordinary_gates':circuit.size,'splice_allocated_gates':splice_allocated,
        'copied_legacy_literal_gates':legacy_allocated,'gate_requests':builder.requests,
        'word_calls':builder.word_calls,'exact_node_sharing':True,'legacy_radius':legacy_radius})


def inner_splice(m: int,cut: int,joint: cp.SharedInner,left: int,right: int):
    if joint.m!=m or not 0<=cut<=1 << m:
        raise ValueError('invalid inner splice')
    b=joint.builder
    original_left=cp.reachable_gates(b,left)
    original_right=cp.reachable_gates(b,right)
    before=len(b.gates)
    condition=tp.leq_constant(b,tuple(range(m)),cut-1)
    output=b.gate('OR',b.gate('AND',condition,left),b.gate('AND',b.gate('NOT',condition),right))
    circuit=b.finish(output)
    metadata={'left_reachable':len(original_left),'right_reachable':len(original_right),
              'shared_reachable':len(original_left&original_right),'new_gates':len(b.gates)-before,
              'selector_bound':2*m+4,'reachable_total':len(cp.reachable_gates(b,output))}
    if metadata['new_gates']>2*m+4:
        raise AssertionError('address comparator/selector bound failed')
    return circuit,metadata


def connected_components(n: int,accepted: set[int]) -> int:
    if n>16:
        raise tp.BudgetExceeded('finite hypercube connectivity budget exceeded')
    remaining=set(accepted)
    components=0
    while remaining:
        components+=1
        start=remaining.pop()
        stack=[start]
        while stack:
            x=stack.pop()
            for i in range(n):
                y=x^(1 << i)
                if y in remaining:
                    remaining.remove(y)
                    stack.append(y)
    return components


def cardinal_log_bound(m: int,k: int,radius: int) -> dict:
    tp.parameters(m,k,radius)
    # An integer upper bound on log2 |D1|, using M <= 2^m.
    ell=6+2*m+(1 << (k+1))
    noise_log=ell+radius*m+(radius+1).bit_length()
    splice_log=m+1+2*ell
    return {'center_log_bound':ell,'noise_log_bound':noise_log,'splice_log_bound':splice_log,
            'accepted_log_bound':1+max(noise_log,splice_log)}


def fixed_beta_sample(m: int,beta: Fraction,epsilon: Fraction,c=1) -> dict:
    previous=cp.fixed_beta_sample(m,beta,epsilon,c)
    k=previous['k']
    radius=previous['output_radius']
    source=splice_gate_bound(m,k)
    legacy=cp.size_estimate(m,k,radius)
    upper=source['unoptimized_gate_upper_bound']+legacy['gates']+1
    budget=4*tp.center_size_bound(m,k)+2*m+12
    exponent=(1+epsilon)*m
    if exponent.denominator!=1:
        raise ValueError('nonintegral sample exponent')
    count=cardinal_log_bound(m,k,radius)
    return {'m':m,'beta':str(beta),'epsilon':str(epsilon),'c':c,'k':k,'radius':radius,
        's1':previous['s1'],'s2':previous['s2'],'splice_inner_bound':budget,
        'splices_are_YES_by_bound':budget<=previous['s1'],
        'old_noisy_inputs_are_YES_by_bound':previous['all_accepted_are_YES_by_bound'],
        'ordinary_gate_upper_bound':upper,'upper_bound_bit_length':upper.bit_length(),
        'outer_bound_below_target':upper<(1 << exponent.numerator),
        'cardinality_log_bound':count,'cardinality_below_counting_target':count['accepted_log_bound']<4*previous['s2'],
        'materialized':False}


def run_experiment(seed=11205) -> dict:
    rng=random.Random(seed)
    complete=[]
    for m,k,radius in ((3,0,0),(3,1,0),(4,0,2)):
        n=1 << m
        centers=cp.binary_centers(m,k)
        spliced=explicit_splices(n,centers)
        old={x for x in range(1 << n) if min((x^c).bit_count() for c in centers)<=radius}
        accepted=spliced|old
        network=build_splice_recognizer(m,k,radius)
        output=tp.evaluate_packed(network.circuit,max_inputs=16)
        expected=sum(1 << x for x in accepted)
        if output!=expected or connected_components(n,accepted)!=1:
            raise AssertionError(('full connected recognizer failed',m,k,radius))
        complete.append({'m':m,'k':k,'radius':radius,'centers':len(centers),
            'splice_tables':len(spliced),'old_noisy_tables':len(old),'accepted_tables':len(accepted),
            'accepted_components':1,'all_input_comparisons':1 << n,
            'construction':network.construction,'circuit_sha256':cp.circuit_hash(network.circuit)})
    # Numeric all-model implementation, independently compared with explicit centers.
    numeric=[]
    for m,k in ((3,1),(6,1),(7,1)):
        n=1 << m
        centers=cp.binary_centers(m,k)
        for _ in range(5):
            table=splice(n,rng.randrange(n+1),rng.choice(centers),rng.choice(centers))
            expected=brute_match_lengths(n,table,centers)
            observed=numeric_match_lengths(m,k,table)
            if observed!=expected:
                raise AssertionError('bottleneck matching lengths failed')
            numeric.append({'m':m,'k':k,'prefix':observed[0],'suffix':observed[1],
                            'is_splice':sum(observed)>=n})
        for _ in range(3):
            table=rng.getrandbits(n)
            expected=brute_match_lengths(n,table,centers)
            observed=numeric_match_lengths(m,k,table)
            if observed!=expected:
                raise AssertionError('arbitrary matching lengths failed')
            numeric.append({'m':m,'k':k,'prefix':observed[0],'suffix':observed[1],
                            'is_splice':sum(observed)>=n})
    # Adding splice paths invalidates the old dimension <= radius theorem.
    # For R=2, the first-three-coordinate cube consists of old weight<=2 points
    # and the prefix step 111000... . It is a 3-dimensional accepted subcube.
    c=cp.binary_centers(4,0)
    s=explicit_splices(16,c)
    a=s|{x for x in range(65536) if min((x^z).bit_count() for z in c)<=2}
    if not set(range(8))<=a:
        raise AssertionError('post-splicing radius-bound counterexample failed')
    dimension_control={'m':4,'k':0,'old_radius':2,'free_coordinates':[0,1,2],
                       'accepted_completions':list(range(8)),'dimension':3}
    witnesses=[]
    for m in (6,7):
        n=1 << m
        table=sum((sum((a>>i)&1 for i in range(3))%2) << a for a in range(n))
        centers=cp.binary_centers(m,1)
        lengths=brute_match_lengths(n,table,centers)
        witness={'m':m,'k':1,'target':'parity on the three lowest address bits','prefix':lengths[0],
                 'suffix':lengths[1],'is_exact_splice':sum(lengths)>=n,
                 'distance_from_old_centers':min((table^c).bit_count() for c in centers),
            'distance_from_exact_splices':brute_splice_distance(n,table,centers)}
        if m==6 and not witness['is_exact_splice']:
            raise AssertionError('old Phase 4 counterexample was not repaired')
        if m==7 and witness['is_exact_splice']:
            raise AssertionError('new parity witness unexpectedly covered')
        witnesses.append(witness)
    inner=[]
    for _ in range(32):
        m=6
        joint=cp.SharedInner(m)
        a=joint.atom((rng.randrange(m),),rng.randrange(4),bool(rng.randrange(2)))
        b=joint.atom((rng.randrange(m),),rng.randrange(4),bool(rng.randrange(2)))
        f,_=joint.compose(a,b,rng.choice(cp.TOPS))
        a=joint.atom((rng.randrange(m),),rng.randrange(4),bool(rng.randrange(2)))
        b=joint.atom((rng.randrange(m),),rng.randrange(4),bool(rng.randrange(2)))
        g,_=joint.compose(a,b,rng.choice(cp.TOPS))
        cut=rng.randrange(65)
        circuit,info=inner_splice(m,cut,joint,f.output,g.output)
        if circuit.truth_table()!=splice(64,cut,f.truth_table(),g.truth_table()):
            raise AssertionError('inner splice circuit failed')
        inner.append(info|{'m':m,'cut':cut})
    parameters=[fixed_beta_sample(m,beta,eps) for m,beta,eps in
        ((512,Fraction(1,16),Fraction(3,4)),(1536,Fraction(1,32),Fraction(1,2)),(3072,Fraction(1,64),Fraction(1,3)))]
    if not all(x['splices_are_YES_by_bound'] and x['old_noisy_inputs_are_YES_by_bound'] and
               x['outer_bound_below_target'] and x['cardinality_below_counting_target'] for x in parameters):
        raise AssertionError('symbolic parameter check failed')
    return {'schema_version':1,'seed':seed,
        'scope':'Old noisy binary-center tubes UNION exact prefix splices of centers; NOT noisy splices or iterated closure.',
        'complete_outer_replays':complete,'all_input_comparisons':sum(x['all_input_comparisons'] for x in complete),
        'numeric_matching_checks':numeric,'parity_witnesses':witnesses,'inner_splice_checks':inner,
        'old_dimension_bound_counterexample':dimension_control,
        'symbolic_parameters':parameters,'failures':[]}


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
        print(f'Wrote {args.output}: {result["all_input_comparisons"]} full input comparisons.')
    elif args.check:
        if json.loads(args.check.read_text())!=json.loads(text):
            raise SystemExit('saved splice experiment differs from exact replay')
        print('Exact splice replay matches.')
    else:
        print(text,end='')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
