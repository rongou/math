#!/usr/bin/env bash
# Check only this investigation's new artifacts. Optionally supply a fully built
# Lean project directory to check PredicateRestriction against its OAI imports.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
study=$(dirname -- "$here")
repo=$(cd -- "$study/../.." && pwd)
project=${1:-}
if [[ $# -gt 1 ]]; then
  printf 'Usage: %s [built-lean-project-directory]\n' "$0" >&2
  exit 2
fi
cd -- "$repo"
python3 -B -m unittest discover -s "$study/experiments" -p 'test_*.py' -v
# The default exact experiment checks all its documented bounded cases.
python3 -B "$study/experiments/restriction_check.py" \
  --output "$study/experiments/restriction_results.json"
python3 -B "$study/experiments/locality_probe.py" \
  --output "$study/experiments/locality_results.json"
lean +leanprover/lean4:v4.34.1 --trust=0 --error=warning \
  "$here/LocalPredicateCNF.lean"
lean +leanprover/lean4:v4.34.1 --trust=0 -j1 -M4096 --error=warning \
  "$here/ParityCertificate.lean"
if [[ -n "$project" ]]; then
  project=$(cd -- "$project" && pwd)
  helper=$(mktemp -d "${TMPDIR:-/tmp}/predicate-restriction-check.XXXXXXXX")
  # Remove only this script's fresh directory, never any project's build cache.
  trap 'rm -rf -- "$helper"' EXIT
  (
    cd -- "$project"
    lake env lean --trust=0 --error=warning --root="$here" \
      -o "$helper/LocalPredicateCNF.olean" "$here/LocalPredicateCNF.lean"
    env LEAN_PATH="$helper${LEAN_PATH:+:$LEAN_PATH}" lake env lean \
      --trust=0 --error=warning --root="$here" "$here/PredicateRestriction.lean"
  )
else
  printf '\nNOT RUN: PredicateRestriction.lean (supply a built OAI Lean project).\n'
fi
printf '\nInvestigation artifact checks completed; this script does not rerun the family112 comparator.\n'
