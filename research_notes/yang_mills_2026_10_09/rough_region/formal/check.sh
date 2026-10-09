#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
env -u LEAN_PATH -u LEAN_SRC_PATH \
  /home/rou/.elan/toolchains/leanprover--lean4---v4.34.1/bin/lean \
  --trust=0 IncidenceBounds.lean
