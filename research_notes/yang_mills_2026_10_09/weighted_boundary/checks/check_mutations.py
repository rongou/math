#!/usr/bin/env python3
"""Reproduce the fourth-pass diagnostic mutation controls.

Runs the original suite under -O, then four deliberately corrupted copies.
Only temporary files are written; they are removed before this program returns.
This validates finite diagnostics, not the mathematical theorems.
"""
from pathlib import Path
import hashlib
import os
import subprocess
import sys
import tempfile

MUTATIONS = (
    ('Cell-incidence budget 8n -> 7n',
     'self.assertLessEqual(len(touched), 8*n)',
     'self.assertLessEqual(len(touched), 7*n)',
     'test_gauge_invariance_and_bounded_cell_edit_cost'),
    ('Omit inversion of reflected normal links',
     'qinv(value) if sign == -1 and invert else value',
     'value',
     'test_exact_noncommuting_Q8_reflections_and_wrong_orientation_control'),
    ('Replace normalized projected density by one',
     'ratio = [num/(mass*mean) for num, mass in zip(numerator, marginal)]',
     'ratio = [F(1) for _ in marginal]',
     'test_exterior_tilt_defeats_edit_stability_exactly'),
    ('Confuse output weight with source weight in the literal integral',
     'model.mu[i]*sum(k*q for k, q in zip(model.kernel[i], weight))',
     'model.mu[i]*weight[i]',
     'test_output_weighted_integral_is_not_a_weighted_probability'),
)


def main():
    source = Path(__file__).with_name('check_weighted_boundary.py')
    text = source.read_text()
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    print('Fourth-pass finite-diagnostic mutation validation.', flush=True)
    print('Source SHA-256:', hashlib.sha256(source.read_bytes()).hexdigest(), flush=True)
    original = subprocess.run([sys.executable, '-O', str(source)], env=environment,
                              capture_output=True, text=True)
    if original.returncode:
        raise RuntimeError('Original optimized suite failed:\n'+original.stdout+original.stderr)
    print('Original suite under python -O: PASS', flush=True)
    for line in original.stderr.splitlines():
        if line.startswith(('Ran ', 'OK')):
            print(line, flush=True)
    with tempfile.TemporaryDirectory(prefix='ym-weighted-mutations-') as tmp:
        for i, (name, old, new, expected_failure) in enumerate(MUTATIONS):
            if text.count(old) != 1:
                raise RuntimeError('Mutation target is not unique: '+name)
            path = Path(tmp)/f'mutated_{i}.py'
            path.write_text(text.replace(old, new))
            result = subprocess.run([sys.executable, str(path)], env=environment,
                                    capture_output=True, text=True)
            if not result.returncode or 'FAIL: '+expected_failure not in result.stderr:
                raise RuntimeError('Mutation was not rejected in the expected test: '+name+
                                   '\n'+result.stdout+result.stderr)
            print(f'REJECTED as expected: {name}; exit={result.returncode}', flush=True)
            for line in result.stderr.splitlines():
                if line.startswith(('FAIL:', 'FAILED')):
                    print('  '+line, flush=True)
    print('All four mutations rejected; temporary copies removed.', flush=True)
    print('Scope: finite checks only, not independent review, analytic certification, or RG closure.', flush=True)


if __name__ == '__main__':
    main()
