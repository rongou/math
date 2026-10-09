#!/usr/bin/env bash
# Reproduce this bounded phase; previous artifacts are read-only.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
study=$(dirname -- "$here")
repo=$(cd -- "$study/../.." && pwd)
if [[ $# -gt 1 ]]; then
  printf 'Usage: %s [built-pinned-Lean-project-with-Mathlib]\n' "$0" >&2
  exit 2
fi
project=
if [[ $# == 1 ]]; then
  project=$(cd -- "$1" && pwd)
  if [[ ! -f "$project/lean-toolchain" ]] || [[ $(tr -d '\r\n' < "$project/lean-toolchain") != 'leanprover/lean4:v4.34.1' ]]; then
    printf 'Expected Lean 4.34.1.\n' >&2
    exit 2
  fi
fi
cd -- "$repo"
check_prior() {
python3 -B - "$here/prior_manifest.json" <<'PY'
from pathlib import Path
import hashlib,json,sys
manifest=json.loads(Path(sys.argv[1]).read_text())
bad=[name for name,h in manifest.items() if not Path(name).is_file() or hashlib.sha256(Path(name).read_bytes()).hexdigest()!=h]
if bad:
    raise SystemExit('Previous artifacts changed: '+repr(bad))
print(f'Previous artifacts preserved: {len(manifest)} files, including uncommitted Phases 3 and 4.')
PY
}
check_prior
python3 -B -m unittest discover -s "$study/experiments" -p 'test_*.py' -v
python3 -B "$study/experiments/splice_probe.py" --check "$study/experiments/splice_results.json"
if [[ -n "$project" ]]; then
  helper=$(mktemp -d "${TMPDIR:-/tmp}/phase5-splice-check.XXXXXXXX")
  # Retain this fresh directory; never delete existing build artifacts or caches.
  printf '\nTemporary proof artifacts retained in %s\n' "$helper"
  phase2="$repo/research_notes/p_vs_np_2026_10_09_phase2/validation"
  phase3="$repo/research_notes/p_vs_np_2026_10_09_phase3/validation"
  (
    cd -- "$project"
    env -u LEAN_PATH -u LEAN_SRC_PATH lake env lean --trust=0 --error=warning -j1 -M16384 \
      --root="$phase2" -o "$helper/PromiseCounting.olean" "$phase2/PromiseCounting.lean"
    env -u LEAN_SRC_PATH LEAN_PATH="$helper" lake env lean --trust=0 --error=warning -j1 -M16384 \
      --root="$phase3" -o "$helper/SeparatedTubes.olean" "$phase3/SeparatedTubes.lean"
    env -u LEAN_SRC_PATH LEAN_PATH="$helper" lake env lean --trust=0 --error=warning -j1 -M16384 \
      --root="$here" "$here/PrefixSplicing.lean"
  ) 2>&1 | tee "$helper/proof.log"
  python3 -B - "$helper/proof.log" <<'PY'
from pathlib import Path
import re,sys
text=Path(sys.argv[1]).read_text()
expected={'minmax_threshold','splice_zero','splice_last','splice_adjacent','mem_spliceSet','card_spliceSet_le','splice_of_matching_prefix_suffix','accepted_subcube_count_bound'}
rows=re.findall(r"^'PrefixSplicing\.([^']+)' depends on axioms: \[([^\]]*)\]$",text,re.M)
if len(rows)!=8 or {name for name,_ in rows}!=expected:
    raise SystemExit('Missing or duplicate new theorem reports')
for name,axioms in rows:
    if {a.strip() for a in axioms.split(',') if a.strip()}-{'propext','Classical.choice','Quot.sound'}:
        raise SystemExit('Unapproved axioms: '+name)
if 'error:' in text:
    raise SystemExit('Compiler errors are not accepted')
print('Eight new splicing/counting lemmas checked; standard permitted axioms only.')
PY
else
  printf '\nNOT RUN: PrefixSplicing.lean (supply a built pinned Mathlib project).\n'
fi
check_prior
printf '\nPhase 5 checks complete. This is not a full GapMCSP correctness or lower-bound proof.\n'
