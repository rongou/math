from fractions import Fraction
from itertools import combinations,product
import json
from pathlib import Path
import random
import unittest
from unittest.mock import patch

import splice_probe as sp


def truth_value(circuit,x):
    return int(circuit.evaluate(x))


def numeric_prefix_boundaries(n,table,centers):
    p=max(j for j in range(n+1) if any(((table^c)&((1 << j)-1))==0 for c in centers))
    q=max(j for j in range(n+1) if any(((table^c)>> (n-j))==0 for c in centers))
    return p,q


def template_tables(m,left,right,template):
    op,alpha,beta=template
    a_count=1 << len(left)
    b_count=1 << len(right)
    if a_count+b_count>10:
        raise ValueError('bounded literal template enumeration only')
    values=set()
    for f,g in product(range(1 << a_count),range(1 << b_count)):
        value=0
        for address,(a,b,p) in enumerate(sp.address_features(m,left,right)):
            value|=sp.cp.bool_op(op,((f>>a)&1)^(alpha&p),((g>>b)&1)^(beta&p)) << address
        values.add(value)
    return tuple(values)


class WordAndFoldingTests(unittest.TestCase):
    def test_unsigned_min_max_less_all_words_through_width_four(self):
        for width in range(1,5):
            for maximum in (False,True):
                b=sp.FoldingBuilder(2*width)
                a=tuple(range(width))
                c=tuple(range(width,2*width))
                result=b.extremum(a,c,maximum)
                self.assertLessEqual(b.requests,8*width+1)
                circuits=[b.finish(bit) for bit in result]
                for x,y in product(range(1 << width),repeat=2):
                    value=x|(y << width)
                    got=sum(truth_value(c,value) << i for i,c in enumerate(circuits))
                    self.assertEqual(got,max(x,y) if maximum else min(x,y))
            b=sp.FoldingBuilder(2*width)
            less=b.finish(b.less(tuple(range(width)),tuple(range(width,2*width))))
            for x,y in product(range(1 << width),repeat=2):
                self.assertEqual(less.evaluate(x|(y << width)),x<y)

    def test_full_width_addition_carry_and_bound(self):
        for width in range(1,5):
            b=sp.FoldingBuilder(2*width)
            bits=sp.add_words(b,tuple(range(width)),tuple(range(width,2*width)))
            self.assertLessEqual(b.requests,11*width)
            circuits=[b.finish(bit) for bit in bits]
            for x,y in product(range(1 << width),repeat=2):
                value=x|(y << width)
                got=sum(truth_value(c,value) << i for i,c in enumerate(circuits))
                self.assertEqual(got,x+y)

    def test_conditional_times_and_unsigned_infinity(self):
        for m in range(1,5):
            width=m+1
            for time in range(1,(1 << m)+1):
                b=sp.FoldingBuilder(1)
                not_bad=b.gate('NOT',0)
                bits=sp.conditional_time(b,not_bad,time,width)
                circuits=[b.finish(bit) for bit in bits]
                for bad in (0,1):
                    got=sum(truth_value(c,bad) << i for i,c in enumerate(circuits))
                    self.assertEqual(got,time if bad else (1 << width)-1)

    def test_local_folding_matches_an_independent_unfolded_circuit(self):
        rng=random.Random(17)
        for _ in range(64):
            folded=sp.FoldingBuilder(3)
            raw=sp.tp.Builder(3)
            translated=list(range(5))
            for step in range(32):
                op=rng.choice(('AND','OR','NOT'))
                args=tuple(rng.randrange(len(translated)) for _ in range(1 if op=='NOT' else 2))
                old=raw.gate(op,*args)
                new=folded.gate(op,*(translated[x] for x in args))
                self.assertEqual(old,len(translated))
                translated.append(new)
            a=raw.finish(old)
            b=folded.finish(new)
            self.assertEqual(sp.tp.evaluate_packed(a),sp.tp.evaluate_packed(b))
            self.assertLessEqual(b.size,a.size)
        b=sp.FoldingBuilder(2)
        x=b.gate('AND',0,1)
        self.assertEqual(x,b.gate('AND',1,0))
        self.assertEqual(b.gate('NOT',b.gate('NOT',0)),0)

    def test_word_and_node_limits_are_enforced(self):
        with self.assertRaises(sp.tp.BudgetExceeded):
            sp.FoldingBuilder(2,max_gates=0).gate('AND',0,1)
        with self.assertRaises(sp.tp.BudgetExceeded):
            sp.FoldingBuilder(2,max_word_calls=0).minimum((0,),(1,))
        with self.assertRaises(ValueError):
            sp.FoldingBuilder(2).gate('AND',0,4)
        with self.assertRaises(ValueError):
            sp.FoldingBuilder(2).less((),())


class BottleneckTests(unittest.TestCase):
    def test_thresholding_min_max_matches_boolean_reachability(self):
        rng=random.Random(25)
        for vertices in range(2,7):
            for _ in range(12):
                weights=tuple(tuple(0 if i==j else rng.randrange(1,6) for j in range(vertices)) for i in range(vertices))
                result=sp.bottleneck_closure(weights)
                for time in range(6):
                    for source in range(vertices):
                        seen={source}
                        todo=[source]
                        while todo:
                            x=todo.pop()
                            for y in range(vertices):
                                if weights[x][y]<=time and y not in seen:
                                    seen.add(y)
                                    todo.append(y)
                        self.assertEqual({j for j in range(vertices) if result[source][j]<=time},seen)

    def test_model_failure_times_against_literal_functions_and_real_gates(self):
        checked=0
        m=2
        n=4
        for left in ((0,),(1,)):
            for right in ((0,),(1,)):
                for template in sp.cp.TEMPLATES:
                    centers=template_tables(m,left,right,template)
                    builder=sp.FoldingBuilder(n)
                    forward=sp.compile_first_failure(builder,m,left,right,template)
                    backward=sp.compile_first_failure(builder,m,left,right,template,True)
                    fc=[builder.finish(bit) for bit in forward]
                    bc=[builder.finish(bit) for bit in backward]
                    for table in range(16):
                        p,q=numeric_prefix_boundaries(n,table,centers)
                        self.assertEqual(sp.first_inconsistent(sp.model_weights(m,table,left,right,template)),p+1)
                        self.assertEqual(sp.first_inconsistent(sp.model_weights(m,table,left,right,template,True)),q+1)
                        got_p=sum(truth_value(c,table) << i for i,c in enumerate(fc))
                        got_q=sum(truth_value(c,table) << i for i,c in enumerate(bc))
                        self.assertEqual((got_p,got_q),(p+1,q+1))
                        checked+=1
        self.assertEqual(checked,768)

    def test_no_contradiction_is_clamped_to_N_plus_one(self):
        b=sp.FoldingBuilder(8)
        words=sp.compile_first_failure(b,3,(),(),('AND',0,0))
        circuits=[b.finish(bit) for bit in words]
        # All-zero and all-one tables are both constant centers for this model.
        for x in (0,255):
            got=sum(truth_value(c,x) << i for i,c in enumerate(circuits))
            self.assertEqual(got,9)
            self.assertNotEqual(got,15)

    def test_model_union_does_not_choose_a_different_template_at_each_address(self):
        # The whole-model threshold is taken before maximizing over templates.
        centers=sp.cp.binary_centers(3,0)
        table=0b01010101
        p,q=sp.numeric_match_lengths(3,0,table)
        self.assertEqual((p,q),sp.brute_match_lengths(8,table,centers))
        self.assertLess(p+q,8)


class SplicingTests(unittest.TestCase):
    def test_prefix_suffix_criterion_for_arbitrary_small_center_sets(self):
        rng=random.Random(72)
        for n in range(1,6):
            for _ in range(16):
                centers=tuple(sorted(rng.sample(range(1 << n),min(4,1 << n))))
                splices=sp.explicit_splices(n,centers)
                for table in range(1 << n):
                    p,q=sp.brute_match_lengths(n,table,centers)
                    self.assertEqual((p,q),numeric_prefix_boundaries(n,table,centers))
                    self.assertEqual(p+q>=n,table in splices)

    def test_all_splice_paths_have_single_coordinate_steps(self):
        for n in range(5):
            for f,g in product(range(1 << n),repeat=2):
                path=[sp.splice(n,j,f,g) for j in range(n+1)]
                self.assertEqual(path[0],g)
                self.assertEqual(path[-1],f)
                self.assertTrue(all((x^y).bit_count()<=1 for x,y in zip(path,path[1:])))

    def test_exact_splice_distance_by_independent_enumeration(self):
        centers=(0,3,12,15)
        splices=sp.explicit_splices(4,centers)
        for table in range(16):
            self.assertEqual(sp.brute_splice_distance(4,table,centers),min((table^s).bit_count() for s in splices))

    def test_inner_selector_gates_and_all_cut_endpoints(self):
        for m in range(1,5):
            for cut in range((1 << m)+1):
                joint=sp.cp.SharedInner(m)
                f=joint.atom((0,),2,False)
                g=joint.atom((m-1,),1,True)
                left=joint.builder.finish(f).truth_table()
                right=joint.builder.finish(g).truth_table()
                circuit,cost=sp.inner_splice(m,cut,joint,f,g)
                self.assertEqual(circuit.truth_table(),sp.splice(1 << m,cut,left,right))
                self.assertLessEqual(cost['new_gates'],2*m+4)
                self.assertLessEqual(cost['reachable_total'],cost['left_reachable']+cost['right_reachable']-cost['shared_reachable']+2*m+4)

    def test_connected_union_retains_noise_and_breaks_the_old_radius_bound(self):
        centers=sp.cp.binary_centers(4,0)
        old={x for x in range(65536) if min((x^c).bit_count() for c in centers)<=2}
        splices=sp.explicit_splices(16,centers)
        union=old|splices
        self.assertEqual(len(old),548)
        self.assertEqual(len(splices),112)
        self.assertEqual(len(union),616)
        self.assertEqual(sp.connected_components(16,old),4)
        self.assertEqual(sp.connected_components(16,union),1)
        self.assertTrue(set(range(8))<=union)  # Three free coordinates, larger than R=2.

    def test_old_parity_witness_is_repaired_but_a_larger_one_is_not(self):
        for m,expected in ((6,True),(7,False)):
            n=1 << m
            table=sum((sum((a>>i)&1 for i in range(3))%2) << a for a in range(n))
            centers=sp.cp.binary_centers(m,1)
            lengths=sp.brute_match_lengths(n,table,centers)
            self.assertEqual(sp.numeric_match_lengths(m,1,table),lengths)
            self.assertEqual(sum(lengths)>=n,expected)
            distance=sp.brute_splice_distance(n,table,centers)
            if m==6:
                self.assertEqual(distance,0)
            else:
                self.assertGreaterEqual(distance,n//4)
                self.assertGreater(min((table^c).bit_count() for c in centers),2)


class ReproductionTests(unittest.TestCase):
    def test_compiler_does_not_enumerate_centers_or_cuts(self):
        with (patch.object(sp.cp,'binary_centers',side_effect=AssertionError('center enumeration')),
              patch.object(sp,'explicit_splices',side_effect=AssertionError('cut enumeration'))):
            network=sp.build_splice_recognizer(3,0)
        centers=sp.cp.binary_centers(3,0)
        expected=sp.explicit_splices(8,centers)
        result=sp.tp.evaluate_packed(network.circuit)
        self.assertEqual(result,sum(1 << x for x in expected))
        self.assertLessEqual(network.circuit.size,network.bound['unoptimized_gate_upper_bound'])

    def test_parameter_samples_remain_symbolic(self):
        for m,beta,eps in ((512,Fraction(1,16),Fraction(3,4)),(1536,Fraction(1,32),Fraction(1,2)),(3072,Fraction(1,64),Fraction(1,3))):
            with patch.object(sp,'build_splice_recognizer',side_effect=AssertionError('must not materialize')):
                row=sp.fixed_beta_sample(m,beta,eps)
            self.assertFalse(row['materialized'])
            self.assertTrue(row['outer_bound_below_target'])
            self.assertTrue(row['splices_are_YES_by_bound'])
            self.assertTrue(row['old_noisy_inputs_are_YES_by_bound'])
            self.assertTrue(row['cardinality_below_counting_target'])

    def test_budgets_and_invalid_inputs(self):
        with self.assertRaises(sp.tp.BudgetExceeded):
            sp.build_splice_recognizer(3,1,max_logical_gates=10)
        with self.assertRaises(sp.tp.BudgetExceeded):
            sp.explicit_splices(8,(0,255),budget=1)
        with self.assertRaises(ValueError):
            sp.splice(4,5,0,0)
        with self.assertRaises(ValueError):
            sp.bottleneck_closure(((0,1),(2,)))
        with self.assertRaises(ValueError):
            sp.brute_match_lengths(4,0,())

    def test_saved_report_replays(self):
        actual=sp.run_experiment()
        saved=json.loads(Path(__file__).with_name('splice_results.json').read_text())
        self.assertEqual(json.loads(json.dumps(actual)),saved)
        self.assertEqual(actual['all_input_comparisons'],66048)
        self.assertEqual(len(actual['numeric_matching_checks']),24)
        self.assertEqual(len(actual['inner_splice_checks']),32)
        self.assertEqual(actual['old_dimension_bound_counterexample']['dimension'],3)
        self.assertEqual(actual['failures'],[])


if __name__=='__main__':
    unittest.main()
