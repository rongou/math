#!/usr/bin/env python3
"""Reproduce diagnostic negative controls in temporary copies only."""
from pathlib import Path
import hashlib
import os
import subprocess
import sys
import tempfile

MUTATIONS = (
    ('Wrong SU(2) integral normalization F(0)=1/2',
     '            return total\n', '            return total/2\n',
     'test_F_zero_and_sphere_normalization'),
    ('False local closure bound 6n -> 5n',
     'self.assertLessEqual(len(neighbors), 6*len({root}))',
     'self.assertLessEqual(len(neighbors), 5*len({root}))',
     'test_local_closure_bound_six_is_attained'),
    ('Omit integrated-star minima from the local leading energy',
     '+sum(6-qnorm(qsum(self.staples(field, e))) for e in neighbors))',
     '+0)',
     'test_fine_decomposition_and_leading_local_lift'),
    ('Drop removed-link probability-Haar normalization in finite marginal',
     'integral = (self.q**e0+self.q**e1)/2',
     'integral = self.q**e0+self.q**e1',
     'test_exact_joint_marginal_normalization_and_Haar_factors'),
    ('Double the opposite-staple mixed derivative coefficient',
     'expected = h/6*Fprime_over_F(6*h)',
     'expected = h/3*Fprime_over_F(6*h)',
     'test_opposite_staple_mixed_derivative_and_cell_additivity_failure'),
)


def main():
    path = Path(__file__).with_name('check_exact_marginal.py')
    text = path.read_text()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    print('Exact-marginal diagnostic mutation validation.', flush=True)
    print('Source SHA-256:', hashlib.sha256(path.read_bytes()).hexdigest(), flush=True)
    run = subprocess.run([sys.executable, '-O', str(path)], env=env, capture_output=True, text=True)
    if run.returncode:
        raise RuntimeError('Optimized original suite failed:\n'+run.stdout+run.stderr)
    print('Original under python -O: PASS', flush=True)
    for line in run.stderr.splitlines():
        if line.startswith(('Ran ', 'OK')):
            print(line, flush=True)
    with tempfile.TemporaryDirectory(prefix='ym-exact-mutations-') as tmp:
        for index, (name, old, new, expected) in enumerate(MUTATIONS):
            if text.count(old) != 1:
                raise RuntimeError('Nonunique mutation target: '+name)
            copy = Path(tmp)/f'mutant_{index}.py'
            copy.write_text(text.replace(old, new))
            result = subprocess.run([sys.executable, str(copy)], env=env, capture_output=True, text=True)
            if not result.returncode or 'FAIL: '+expected not in result.stderr:
                raise RuntimeError('Mutation did not fail the intended check: '+name+'\n'+result.stdout+result.stderr)
            print('REJECTED as expected:', name, flush=True)
            for line in result.stderr.splitlines():
                if line.startswith(('FAIL:', 'FAILED')):
                    print('  '+line, flush=True)
    print('Five mutations rejected; temporary variants removed.', flush=True)
    print('Scope: finite diagnostics, not a formal analytic or RG certificate.', flush=True)


if __name__ == '__main__':
    main()
