#!/usr/bin/env python3
"""Opt-in, time-bounded seven-eighths verification in an isolated source copy.

Downloads pinned dependencies only inside a fresh temporary directory (and may
use normal tool caches). Never alters the working checkout's Lean directory.
The temporary copy is retained for inspection or continuation. This is NOT run
by the unit-test suite. Pass --run to authorize the build workflow.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
from datetime import datetime, timezone


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true', help='perform network/setup/build operations')
    parser.add_argument('--seconds', type=int, default=900, help='total wall-clock limit after source extraction')
    args = parser.parse_args()
    if not args.run:
        parser.error('This downloads/builds dependencies. Use --run explicitly.')
    if args.seconds < 1:
        parser.error('--seconds must be positive')
    repo = Path(__file__).resolve().parents[2]
    output = repo / 'research_notes/results'
    output.mkdir(exist_ok=True)
    report_file = output / 'comparator_attempt.json'
    log_file = output / 'comparator_attempt.log'
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
    isolated = Path(tempfile.mkdtemp(prefix='rh-comparator-'))
    report = {
        'status': 'preparing isolated source',
        'source_revision': revision,
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'isolated_directory': str(isolated),
        'time_limit_seconds_after_extraction': args.seconds,
        'checkout_lean_directory_modified': False,
        'stages': [],
        'comparator_completed_successfully': False,
    }

    def save():
        report_file.write_text(json.dumps(report, indent=2) + '\n')

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    save()
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
    # Bound inherited CPU affinity without changing machine-wide settings.
    if hasattr(os, 'sched_getaffinity'):
        cpus = sorted(os.sched_getaffinity(0))[:8]
        os.sched_setaffinity(0, set(cpus))
        report['cpu_affinity'] = cpus
    with log_file.open('w') as log:
        log.write(f'Source: {revision}\nIsolated copy: {isolated}\n')
        log.flush()
        archive = subprocess.Popen(['git', 'archive', revision, 'lean'], cwd=repo,
                                   stdout=subprocess.PIPE, stderr=log)
        extraction = subprocess.run(['tar', '-x', '-C', str(isolated)], stdin=archive.stdout,
                                    stdout=log, stderr=log)
        archive.stdout.close()
        archive_code = archive.wait()
        if archive_code or extraction.returncode:
            report['status'] = 'source extraction failed'
            save()
            return 1
        lean = isolated / 'lean'
        before = (lean / 'lake-manifest.json').read_bytes()
        report['initial_manifest_sha256'] = hashlib.sha256(before).hexdigest()
        report['lakefile_sha256'] = digest(lean / 'lakefile.lean')
        report['toolchain'] = (lean / 'lean-toolchain').read_text().strip()
        deadline = time.monotonic() + args.seconds
        stages = [
            ('dependency setup', ['lake', 'update']),
            ('dependency cache', ['lake', 'exe', 'cache', 'get']),
            ('comparator', ['lake', 'env', 'comparator', 'ComparatorChallenges/QuasiRiemannHypothesis.json']),
        ]
        for name, command in stages:
            remaining = int(deadline - time.monotonic())
            if remaining <= 0:
                report['status'] = f'time limit reached before {name}'
                break
            report['status'] = f'running {name}'
            save()
            log.write(f'\nSTAGE {name}: {command!r}; remaining seconds: {remaining}\n')
            log.flush()
            started = time.monotonic()
            result = subprocess.run(['timeout', '--signal=TERM', '--kill-after=10s', f'{remaining}s', *command],
                                    cwd=lean, env=env, stdout=log, stderr=log)
            stage = {'name': name, 'command': command, 'exit_code': result.returncode,
                     'elapsed_seconds': round(time.monotonic() - started, 3)}
            report['stages'].append(stage)
            log.write(f'END STAGE: {stage!r}\n')
            log.flush()
            report['final_manifest_sha256'] = digest(lean / 'lake-manifest.json')
            report['manifest_changed'] = (lean / 'lake-manifest.json').read_bytes() != before
            if result.returncode:
                report['status'] = (f'{name} timed out; proof NOT verified' if result.returncode == 124
                                    else f'{name} failed; proof NOT verified')
                break
            if name == 'comparator':
                report['comparator_completed_successfully'] = True
                report['status'] = 'comparator exited successfully; inspect log and statement/axiom evidence'
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save()
    print(json.dumps(report, indent=2))
    return 0 if report['comparator_completed_successfully'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
