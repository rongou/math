#!/usr/bin/env bash
# Reproduce Phase 3 without rewriting saved experiments or previous phases.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
study=$(dirname -- "$here")
repo=$(cd -- "$study/../.." && pwd)
if [[ $# -gt 1 ]]; then
  printf 'Usage: %s [built-Lean-4.34.1-project-with-Mathlib]\n' "$0" >&2
  exit 2
fi
project=
if [[ $# == 1 ]]; then
  project=$(cd -- "$1" && pwd)
  if [[ ! -f "$project/lean-toolchain" ]] || [[ $(tr -d '\r\n' < "$project/lean-toolchain") != 'leanprover/lean4:v4.34.1' ]]; then
    printf 'Expected a built Lean 4.34.1 project.\n' >&2
    exit 2
  fi
fi
cd -- "$repo"
check_prior() {
  python3 -B - "$here/prior_manifest.json" <<'PY'
from pathlib import Path
import hashlib, json, sys
manifest = json.loads(Path(sys.argv[1]).read_text())
bad = [name for name, expected in manifest.items()
       if not Path(name).is_file() or hashlib.sha256(Path(name).read_bytes()).hexdigest() != expected]
if bad:
    raise SystemExit('Previous research files changed: ' + repr(bad))
print(f'Previous phases preserved: {len(manifest)} tracked files match.')
PY
}
check_prior
python3 -B -m unittest discover -s "$study/experiments" -p 'test_*.py' -v
python3 -B "$study/experiments/tube_probe.py" --check "$study/experiments/tube_results.json"
if [[ -n "$project" ]]; then
  helper=$(mktemp -d "${TMPDIR:-/tmp}/phase3-certificate-check.XXXXXXXX")
  trap 'rm -rf -- "$helper"' EXIT
  previous="$repo/research_notes/p_vs_np_2026_10_09_phase2/validation"
  (
    cd -- "$project"
    env -u LEAN_PATH -u LEAN_SRC_PATH lake env lean --trust=0 --error=warning -j1 -M16384 \
      --root="$previous" -o "$helper/PromiseCounting.olean" "$previous/PromiseCounting.lean"
    env -u LEAN_SRC_PATH LEAN_PATH="$helper" lake env lean --trust=0 --error=warning -j1 -M16384 \
      --root="$here" "$here/SeparatedTubes.lean"
  ) 2>&1 | tee "$helper/proof.log"
  python3 -B - "$helper/proof.log" <<'PY'
from pathlib import Path
import re, sys
text = Path(sys.argv[1]).read_text()
expected = {
    'hammingDist_le_one', 'subcube_step_induction', 'adjacent_centers_eq',
    'accepting_subcube_one_center', 'free_card_le_of_subcube_in_ball',
    'accepting_subcube_free_card_le', 'relative_certificate_free_budget',
    'center_subcube_accepted', 'disagreement_contains_subcube',
    'supported_distance_lower_bound', 'junta_distance_lower_bound',
}
rows = re.findall(r"^'SeparatedTubes\.([^']+)' depends on axioms: \[([^\]]*)\]$", text, re.M)
if len(rows) != len(expected) or {name for name, _ in rows} != expected:
    raise SystemExit('Unexpected/missing theorem axiom reports')
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
for name, axioms in rows:
    actual = {a.strip() for a in axioms.split(',') if a.strip()}
    if not actual <= allowed:
        raise SystemExit(f'Unapproved axioms for {name}: {actual - allowed}')
if 'error:' in text:
    raise SystemExit('Compiler errors are not accepted')
print(f'Lean verification: {len(rows)} theorems; only standard permitted axioms.')
PY
else
  printf '\nNOT RUN: SeparatedTubes.lean (supply a built pinned Mathlib project).\n'
fi
check_prior
printf '\nPhase 3 checks completed. This does not verify the external magnification theorem or prove full GapMCSP hardness.\n'
