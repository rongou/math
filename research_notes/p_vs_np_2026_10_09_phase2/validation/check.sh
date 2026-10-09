#!/usr/bin/env bash
# Reproduce the new Phase 2 artifacts, not the external literature or phase1.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
study=$(dirname -- "$here")
repo=$(cd -- "$study/../.." && pwd)
if [[ $# -gt 1 ]]; then
  printf 'Usage: %s [built-Lean-project-with-Mathlib]\n' "$0" >&2
  exit 2
fi
project=
if [[ $# == 1 ]]; then
  project=$(cd -- "$1" && pwd)
  if [[ ! -f "$project/lean-toolchain" ]] || [[ $(tr -d '\r\n' < "$project/lean-toolchain") != 'leanprover/lean4:v4.34.1' ]]; then
    printf 'Expected a Lean 4.34.1 project.\n' >&2
    exit 2
  fi
fi
cd -- "$repo"
python3 -B -m unittest discover -s "$study/experiments" -p 'test_*.py' -v
python3 -B "$study/experiments/sharing_probe.py" --output "$study/experiments/sharing_results.json"
python3 -B "$study/experiments/promise_atlas.py" --check
python3 -B "$study/experiments/certificate_controls.py" --output "$study/experiments/certificate_results.json"
# This finite all-input network proof exceeds a 4 GiB kernel allocation cap.
lean +leanprover/lean4:v4.34.1 --trust=0 -j1 -M16384 --error=warning "$here/ZeroGateControl.lean"
lean +leanprover/lean4:v4.34.1 --trust=0 -j1 -M4096 --error=warning "$here/AtlasWitness.lean"
if [[ -n "$project" ]]; then
  (
    cd -- "$project"
    env -u LEAN_PATH -u LEAN_SRC_PATH lake env lean \
      --root="$here" --trust=0 --error=warning "$here/PromiseCounting.lean"
  )
else
  printf '\nNOT RUN: PromiseCounting.lean (supply a built Mathlib project).\n'
fi
python3 -B - "$here/phase1_manifest.json" <<'PY'
from pathlib import Path
import hashlib,json,sys
manifest=json.loads(Path(sys.argv[1]).read_text())
changed=[]
for name,expected in manifest.items():
    p=Path(name)
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
        changed.append(name)
if changed:
    raise SystemExit('Phase1 manifest differs: '+repr(changed))
print(f'Phase1 preservation: {len(manifest)} recorded files unchanged.')
PY
printf '\nPhase2 artifact checks completed. External source theorems and general DAG normalization are not checked by this script.\n'
