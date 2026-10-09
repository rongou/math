#!/usr/bin/env python3
"""Read-only static inventory of the repository's quasi-RH solution imports.

Not a Lean parser, elaborator, axiom audit, build, or comparator run.  Traverses
ordinary single-line import statements and scans local source after masking
nested comments and ordinary string literals.  Imported external packages and
generated declarations are not inspected.  No dependencies are downloaded.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path


def mask_comments_and_strings(text: str) -> str:
    """Keep offsets/newlines while masking nested Lean comments and strings."""
    output = list(text)
    depth = 0
    in_string = False
    i = 0
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                output[i:i + 2] = [' ', ' ']
                depth += 1
                i += 2
            elif text.startswith('-/', i):
                output[i:i + 2] = [' ', ' ']
                depth -= 1
                i += 2
            else:
                output[i] = '\n' if text[i] == '\n' else ' '
                i += 1
        elif in_string:
            if text[i] == '\\' and i + 1 < len(text):
                output[i] = ' '
                output[i + 1] = '\n' if text[i + 1] == '\n' else ' '
                i += 2
            elif text[i] == '"':
                output[i] = ' '
                in_string = False
                i += 1
            else:
                output[i] = '\n' if text[i] == '\n' else ' '
                i += 1
        elif text.startswith('/-', i):
            output[i:i + 2] = [' ', ' ']
            depth = 1
            i += 2
        elif text.startswith('--', i):
            end = text.find('\n', i)
            if end < 0:
                end = len(text)
            output[i:end] = [' '] * (end - i)
            i = end
        elif text[i] == '"':
            output[i] = ' '
            in_string = True
            i += 1
        else:
            i += 1
    if depth or in_string:
        raise ValueError("unterminated comment or ordinary string")
    return ''.join(output)


def imports_in(clean: str) -> list[str]:
    imports = []
    for line in clean.splitlines():
        match = re.match(r'^\s*(?:public\s+)?import\s+(.*)$', line)
        if match:
            imports.extend(match.group(1).split())
    return imports


def command_output(command: list[str], cwd: Path) -> str:
    try:
        result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"unavailable: {error}"
    if result.returncode:
        return f"exit {result.returncode}: {result.stderr.strip()}"
    return result.stdout.strip()


def inventory(repo: Path) -> dict:
    lean = repo / 'lean'
    config_path = lean / 'ComparatorChallenges/QuasiRiemannHypothesis.json'
    config = json.loads(config_path.read_text())
    pending = [config['solution_module']]
    local = {}
    external = set()
    flags = []
    while pending:
        module = pending.pop()
        if module in local or module in external:
            continue
        path = lean.joinpath(*module.split('.')).with_suffix('.lean')
        if not path.is_file():
            external.add(module)
            continue
        text = path.read_text()
        clean = mask_comments_and_strings(text)
        imports = imports_in(clean)
        local[module] = {'lines': len(text.splitlines()), 'imports': imports}
        pending.extend(imports)
        for match in re.finditer(r'\b(?:sorry|admit|axiom|unsafe|native_decide|sorryAx)\b', clean):
            flags.append({'file': str(path.relative_to(repo)),
                          'line': clean.count('\n', 0, match.start()) + 1,
                          'token': match.group()})
    groups = Counter('.'.join(module.split('.')[:4]) for module in local)
    return {
        'status': 'static inventory only; this script does not build Lean or run the comparator',
        'date': date.today().isoformat(),
        'repository_revision': command_output(['git', 'rev-parse', 'HEAD'], repo),
        'config': str(config_path.relative_to(repo)),
        'solution_module': config['solution_module'],
        'target_declarations': config['theorem_names'],
        'permitted_axioms_in_config': config['permitted_axioms'],
        'enable_nanoda_in_config': config['enable_nanoda'],
        'toolchain_pin': (lean / 'lean-toolchain').read_text().strip(),
        'installed_lean': command_output(['lean', '--version'], lean),
        'tool_paths': {name: shutil.which(name) for name in ('lake', 'comparator', 'landrun', 'lean4export')},
        'lake_directory_present': (lean / '.lake').is_dir(),
        'local_module_count': len(local),
        'local_source_line_count': sum(item['lines'] for item in local.values()),
        'external_import_count': len(external),
        'external_import_roots': dict(sorted(Counter(module.split('.')[0] for module in external).items())),
        'largest_local_groups': dict(groups.most_common(12)),
        'lexical_review_flags': sorted(flags, key=lambda row: (row['file'], row['line'])),
        'limitations': [
            'Module-import closure is not declaration-level proof dependency analysis.',
            'External packages, macros, raw strings, and generated declarations are not audited.',
            'No marker hits does not certify soundness or identify all axioms.',
            'The comparator challenge stub is not in the solution import closure.',
        ],
    }


if __name__ == '__main__':
    repository = Path(__file__).resolve().parents[2]
    print(json.dumps(inventory(repository), indent=2))
