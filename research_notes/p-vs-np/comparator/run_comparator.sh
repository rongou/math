#!/usr/bin/env bash
# Independently re-check the P-vs-NP-relevant Lean results of the OpenAI math
# release with Comparator, in an isolated snapshot of the pinned commit.
#
# Never modifies the repository: the build happens in a `git archive` snapshot
# under /tmp, and logs go to this script's directory.
#
# Usage: run_comparator.sh <snapshot-root> <challenge>...

set -uo pipefail

REPO=/home/rou/src/math
COMMIT=fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb
OUT="$(cd "$(dirname "$0")" && pwd)"
ROOT="$1"; shift
LEAN_DIR="$ROOT/lean"
export GIT_TERMINAL_PROMPT=0
# The README's mmap workaround for large builds.
export GLIBC_TUNABLES=glibc.malloc.mmap_max=0:glibc.malloc.arena_max=1

log() { printf '[%s] %s\n' "$(date -u +%H:%M:%S)" "$*" | tee -a "$OUT/progress.log"; }

if [ ! -d "$LEAN_DIR" ]; then
  log "snapshot $COMMIT -> $ROOT"
  mkdir -p "$ROOT"
  git -C "$REPO" archive "$COMMIT" lean | tar -x -C "$ROOT"
fi

cd "$LEAN_DIR"
if [ ! -d .lake/packages/mathlib ]; then
  log "lake update (fetch pinned deps + apply compatibility patches)"
  lake update > "$OUT/00_lake_update.log" 2>&1 || { log "lake update FAILED"; exit 1; }
fi
if [ ! -f .lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ]; then
  log "lake exe cache get"
  lake exe cache get > "$OUT/01_cache_get.log" 2>&1 || { log "cache get FAILED"; exit 1; }
fi

printf 'challenge\tbuild\tcomparator\tbuild_s\tcomparator_s\n' > "$OUT/summary.tsv"
for c in "$@"; do
  sol=$(python3 -c "import json;print(json.load(open('ComparatorChallenges/$c.json'))['solution_module'])")
  log "build $c ($sol)"
  t0=$(date +%s)
  lake build "+$sol" "+ComparatorChallenges.$c" > "$OUT/build_$c.log" 2>&1
  b=$?; t1=$(date +%s)
  if [ $b -ne 0 ]; then
    log "  build FAILED ($((t1-t0))s)"
    printf '%s\tFAIL\tSKIP\t%s\t-\n' "$c" "$((t1-t0))" >> "$OUT/summary.tsv"
    continue
  fi
  log "  built in $((t1-t0))s; running comparator"
  timeout 3600 lake env comparator "ComparatorChallenges/$c.json" > "$OUT/comparator_$c.log" 2>&1
  r=$?; t2=$(date +%s)
  if [ $r -eq 0 ]; then v=PASS; else v="FAIL($r)"; fi
  log "  comparator $v ($((t2-t1))s)"
  printf '%s\tOK\t%s\t%s\t%s\n' "$c" "$v" "$((t1-t0))" "$((t2-t1))" >> "$OUT/summary.tsv"
done
log "done"
