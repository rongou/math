"""Independent finite checks of composition, 2-CSP, and literal gate circuits."""
from contextlib import redirect_stderr
from fractions import Fraction
from itertools import product, combinations
import io
import json
from pathlib import Path
import random
import unittest
from unittest.mock import patch

import composition_probe as cp


def packed_labels(value,rows,cols):
    return tuple(tuple(((value >> (2*(r*cols+c)))&1,(value >> (2*(r*cols+c)+1))&1)
                       for c in range(cols)) for r in range(rows))


def standalone_constraint_circuit(rows,cols,template):
    b=cp.tp.Builder(2*rows*cols)
    bad=tuple(tuple(cp.label_bad_wires(b,(2*(r*cols+c),2*(r*cols+c)+1))
                    for c in range(cols)) for r in range(rows))
    return b.finish(cp.compile_slice_sat(b,bad,template))


class BooleanCompositionTests(unittest.TestCase):
    def test_all_sixteen_operations_have_canonical_representations(self):
        # Four unary functions of each independent argument, then AND/NAND/XOR.
        unary_left=(0,15,12,3)
        unary_right=(0,15,10,5)
        generated={cp.top_table(op,a,b,4) for op in cp.TOPS for a in unary_left for b in unary_right}
        self.assertEqual(generated,set(range(16)))
        for code in range(16):
            for u,v in product((0,1),repeat=2):
                self.assertEqual(cp.apply_binary(code,u,v,1),(code >> (2*u+v))&1)

    def test_all_sixteen_top_functions_compile_in_at_most_four_gates(self):
        for code in range(16):
            b=cp.tp.Builder(2)
            circuit=b.finish(cp.binary_gate(b,code,0,1))
            self.assertLessEqual(circuit.size,4)
            for x in range(4):
                self.assertEqual(circuit.evaluate(x),bool((code >> (2*(x&1)+((x>>1)&1)))&1))
        with self.assertRaises(ValueError):
            cp.binary_gate(cp.tp.Builder(2),16,0,1)

    def test_binary_center_enumeration_against_all_sixteen_operations(self):
        atoms=cp.tp.center_tables(3,1)
        expected={cp.apply_binary(code,a,b,8) for code in range(16) for a in atoms for b in atoms}
        self.assertEqual(set(cp.binary_centers(3,1)),expected)
        self.assertEqual(len(expected),72)
        self.assertTrue(set(atoms)<=expected)
        self.assertIn(136,expected)  # The AND that Phase 3 missed.
        self.assertNotIn(120,expected)  # (x0 AND x1) XOR x2.

    def test_hamming_errors_add_for_every_small_operation_and_input(self):
        for code in range(16):
            for x,y,a,b in product(range(8),repeat=4):
                actual=(cp.apply_binary(code,x,y,3)^cp.apply_binary(code,a,b,3)).bit_count()
                self.assertLessEqual(actual,(x^a).bit_count()+(y^b).bit_count())

    def test_radius_doubling_cannot_be_omitted(self):
        atoms=cp.tp.center_tables(6,1)
        centers=cp.binary_centers(6,1)
        a,b=1,2  # One error each around the all-zero center.
        self.assertEqual(min((a^c).bit_count() for c in atoms),1)
        self.assertEqual(min((b^c).bit_count() for c in atoms),1)
        x=a^b
        self.assertEqual(min((x^c).bit_count() for c in centers),2)


class ConstraintEncodingTests(unittest.TestCase):
    def test_all_small_label_matrices_against_literal_assignments(self):
        checked=0
        for rows,cols in ((1,1),(1,2),(2,1),(2,2)):
            for template in cp.TEMPLATES:
                circuit=standalone_constraint_circuit(rows,cols,template)
                actual=cp.tp.evaluate_packed(circuit)
                expected=0
                for value in range(1 << (2*rows*cols)):
                    labels=packed_labels(value,rows,cols)
                    literal=cp.brute_slice_witness(labels,template) is not None
                    self.assertEqual(cp.slice_sat(labels,template),literal)
                    expected |= int(literal) << value
                    checked+=1
                self.assertEqual(actual,expected)
                variables=rows+cols
                self.assertEqual(circuit.size,6*rows*cols+16*variables**3+3*variables-1)
        self.assertEqual(checked,3504)

    def test_larger_constraint_circuits_on_positive_and_arbitrary_samples(self):
        rng=random.Random(74)
        rows,cols=4,4
        for template in cp.TEMPLATES:
            samples=[]
            for _ in range(8):
                a,b=rng.randrange(16),rng.randrange(16)
                value=0
                for r in range(rows):
                    for c in range(cols):
                        x,y=cp.template_label(template,(a>>r)&1,(b>>c)&1)
                        value|=x << (2*(r*cols+c))
                        value|=y << (2*(r*cols+c)+1)
                samples.append(value)
            samples.extend(rng.getrandbits(32) for _ in range(16))
            circuit=standalone_constraint_circuit(rows,cols,template)
            actual=cp.evaluate_samples(circuit,tuple(samples))
            expected=tuple(cp.brute_slice_witness(packed_labels(x,rows,cols),template) is not None for x in samples)
            self.assertEqual(actual,expected)
            self.assertTrue(all(actual[:8]))

    def test_template_must_be_global_across_common_coordinate_slices(self):
        labels=tuple((((a,b),),) for a,b in product((0,1),repeat=2))
        self.assertTrue(all(any(cp.slice_sat(block,t) for t in cp.TEMPLATES) for block in labels))
        self.assertFalse(any(all(cp.slice_sat(block,t) for block in labels) for t in cp.TEMPLATES))
        # Compile the same condition: all four labels occur on different common assignments.
        b=cp.tp.Builder(8)
        bad=[cp.label_bad_wires(b,(2*i,2*i+1)) for i in range(4)]
        answers=[]
        for template in cp.TEMPLATES:
            answers.append(b.fold('AND',[cp.compile_slice_sat(b,((bad[i],),),template) for i in range(4)]))
        circuit=b.finish(b.fold('OR',answers))
        value=sum(bit << (2*i+j) for i,(a,c) in enumerate(product((0,1),repeat=2)) for j,bit in enumerate((a,c)))
        self.assertFalse(circuit.evaluate(value))

    def test_invalid_label_domains_and_brute_budgets(self):
        for labels in ((),((),),(((0,2),),),(((0,0),),((1,0),(0,1)))):
            with self.assertRaises(ValueError):
                cp.validate_labels(labels)
        with self.assertRaises(cp.tp.BudgetExceeded):
            cp.brute_slice_witness(tuple(tuple((0,0) for _ in range(9)) for _ in range(9)),cp.TEMPLATES[0])


class FeatureAndDecoderTests(unittest.TestCase):
    def test_parity_fibers_are_uniform_and_partition_the_cube(self):
        for m in range(1,7):
            for size in range(min(3,m-1)+1):
                for union in combinations(range(m),size):
                    blocks=cp.feature_blocks(m,union)
                    self.assertEqual(len(blocks),1 << (size+1))
                    self.assertEqual(sorted(i for block in blocks for i in block),list(range(1 << m)))
                    for index,block in enumerate(blocks):
                        self.assertEqual(len(block),1 << (m-size-1))
                        for a in block:
                            projected=sum(((a>>i)&1) << j for j,i in enumerate(union))
                            self.assertEqual(index,2*projected+(a.bit_count()&1))

    def test_overlap_layouts_cover_each_union_assignment_once(self):
        for left,right in (((0,),(1,)),((0,),(0,)),((0,1),(1,2)),((0,1),(0,1)),((),())):
            layout=cp.slice_layout(left,right)
            union=set(left)|set(right)
            common=set(left)&set(right)
            self.assertEqual(len(layout),1 << len(common))
            flat=[i for block in layout for row in block for i in row]
            self.assertEqual(sorted(flat),list(range(1 << len(union))))

    def test_semantic_recognizer_all_eight_bit_inputs(self):
        for k in (0,1):
            expected=set(cp.binary_centers(3,k))
            for table in range(256):
                self.assertEqual(cp.semantic_recognize(3,k,0,table),table in expected)

    def test_small_atlas_has_full_input_certificates(self):
        centers=set(cp.binary_centers(3,1))
        self.assertEqual(cp.tp.minimum_distance(tuple(centers)),2)
        profile=cp.tp.cube_profile(8,centers)
        self.assertEqual(profile['subcubes_examined'],6561)
        self.assertEqual(profile['maximum_accepting_dimension'],0)
        self.assertEqual(profile['minimum_certificate_histogram'],{8:72})

    def test_noisy_round_membership_and_center_separation(self):
        rng=random.Random(38)
        centers=cp.binary_centers(6,1)
        atoms=cp.tp.center_tables(6,1)
        self.assertEqual(len(centers),616)
        self.assertEqual(cp.tp.minimum_distance(centers),16)
        for _ in range(24):
            a,b=rng.choice(atoms),rng.choice(atoms)
            x,y=a^(1 << rng.randrange(64)),b^(1 << rng.randrange(64))
            table=cp.apply_binary(rng.randrange(16),x,y,64)
            self.assertLessEqual(min((table^c).bit_count() for c in centers),2)
            self.assertTrue(cp.semantic_recognize(6,1,2,table))
        for _ in range(16):
            table=rng.getrandbits(64)
            self.assertEqual(cp.semantic_recognize(6,1,2,table),min((table^c).bit_count() for c in centers)<=2)

    def test_decoder_guard_rejects_unsupported_radius_and_missing_parity_bit(self):
        for args in ((2,1,0),(5,1,2),(3,1,1),(6,1,-1)):
            with self.assertRaises(ValueError):
                cp.check_regime(*args)
        with self.assertRaises(cp.tp.BudgetExceeded):
            cp.feature_blocks(3,(0,1,2))
        with self.assertRaises(ValueError):
            cp.feature_blocks(3,(1,0))


class ActualSharingTests(unittest.TestCase):
    def test_repeated_atom_is_not_charged_twice(self):
        joint=cp.SharedInner(6)
        a=joint.atom((0,),2,True)
        b=joint.atom((0,),2,True)
        self.assertEqual(a,b)
        circuit,cost=joint.compose(a,b,'AND')
        self.assertEqual(cost['left_gates'],24)
        self.assertEqual(cost['shared_gates'],24)
        self.assertEqual(cost['reachable_composition_gates'],25)
        self.assertGreater(circuit.size,cost['reachable_composition_gates'])  # an unused NOT is allocated

    def test_two_distinct_roots_share_the_full_parity_computation(self):
        joint=cp.SharedInner(6)
        a=joint.atom((0,),2,True)
        b=joint.atom((1,),2,True)
        circuit,cost=joint.compose(a,b,'XOR')
        self.assertEqual(cost['shared_gates'],20)
        self.assertEqual(cost['reachable_composition_gates'],32)
        self.assertEqual(cost['union_gates'],28)
        # Parity shifts cancel semantically, but the literal network is not optimized away.
        expected=sum((((x>>0)^(x>>1))&1) << x for x in range(64))
        self.assertEqual(circuit.truth_table(),expected)

    def test_disjoint_gates_and_fresh_top_nodes(self):
        joint=cp.SharedInner(4)
        a=joint.atom((0,1),8)
        b=joint.atom((2,3),8)
        for op,extra in (('AND',1),('NAND',2),('XOR',4)):
            circuit,cost=joint.compose(a,b,op)
            self.assertEqual(cost['shared_gates'],0)
            self.assertEqual(cost['reachable_composition_gates'],cost['left_gates']+cost['right_gates']+extra)

    def test_one_more_affordable_xor_round_is_missed(self):
        joint=cp.SharedInner(6)
        a,b,c=(joint.atom((i,),2) for i in range(3))
        first,cost1=joint.compose(a,b,'XOR')
        second,cost2=joint.compose(first.output,c,'XOR')
        centers=cp.binary_centers(6,1)
        self.assertIn(first.truth_table(),centers)
        self.assertEqual(cost1['reachable_composition_gates'],4)
        self.assertEqual(cost2['reachable_composition_gates'],8)
        self.assertEqual(min((second.truth_table()^x).bit_count() for x in centers),32)
        self.assertFalse(cp.semantic_recognize(6,1,2,second.truth_table()))

    def test_symbolic_cost_counts_ordered_pairs_and_overlap(self):
        for m,k,r in ((3,0,0),(3,1,0),(4,1,0),(6,1,2),(8,2,1)):
            estimate=cp.size_estimate(m,k,r)
            self.assertEqual(sum(row['ordered_support_pairs'] for row in estimate['by_overlap']),estimate['ordered_pairs'])
            self.assertLessEqual(estimate['gates'],estimate['simple_gate_upper_bound'])
        with patch.object(cp,'binary_centers',side_effect=AssertionError('must not enumerate centers')):
            circuit=cp.build_recognizer(3,0,0)
            self.assertEqual(circuit.circuit.size,1932)


class ReproductionTests(unittest.TestCase):
    def test_batch_interpreter_agrees_with_scalar_outputs(self):
        circuit=cp.build_recognizer(3,0,0).circuit
        samples=tuple(range(256))
        self.assertEqual(cp.evaluate_samples(circuit,samples),tuple(circuit.evaluate(x) for x in samples))
        with self.assertRaises(ValueError):
            cp.evaluate_samples(circuit,(256,))
        with self.assertRaises(cp.tp.BudgetExceeded):
            cp.evaluate_samples(circuit,samples,max_samples=1)

    def test_construction_budgets_and_cli_are_enforced_before_work(self):
        with self.assertRaises(cp.tp.BudgetExceeded):
            cp.build_recognizer(8,2,1,max_gates=10)
        with self.assertRaises(cp.tp.BudgetExceeded):
            cp.binary_centers(3,1,max_pairs=1)
        with patch.object(cp,'run_experiment') as run,redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                cp.main(['--check','unused','--output','unused'])
            run.assert_not_called()

    def test_fixed_beta_samples_are_exact_and_symbolic(self):
        for m,beta,eps in ((512,Fraction(1,16),Fraction(3,4)),(1536,Fraction(1,32),Fraction(1,2)),(3072,Fraction(1,64),Fraction(1,3))):
            with patch.object(cp,'build_recognizer',side_effect=AssertionError('must remain symbolic')):
                row=cp.fixed_beta_sample(m,beta,eps)
            self.assertFalse(row['materialized'])
            self.assertTrue(row['all_accepted_are_YES_by_bound'])
            self.assertTrue(row['separated_tubes'])
            self.assertTrue(row['outer_size_below_target'])
            self.assertEqual(row['output_radius'],2*row['seed_radius'])
        with self.assertRaises(ValueError):
            cp.fixed_beta_sample(512,Fraction(1,4),Fraction(1,2))

    def test_saved_full_report_replays_exactly(self):
        current=cp.run_experiment()
        recorded=json.loads(Path(__file__).with_name('composition_results.json').read_text())
        self.assertEqual(json.loads(json.dumps(current)),recorded)
        self.assertEqual(current['all_input_comparisons'],66048)
        self.assertEqual(current['noisy_round_sampled_circuit']['sample_count'],193)
        self.assertEqual(len(current['inner_shared_compositions']),48)
        self.assertEqual(current['one_more_round_witness']['second_cost']['reachable_composition_gates'],8)
        self.assertEqual(current['failures'],[])


if __name__=='__main__':
    unittest.main()
