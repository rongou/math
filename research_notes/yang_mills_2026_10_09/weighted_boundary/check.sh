#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
PYTHONDONTWRITEBYTECODE=1 python3 checks/check_weighted_boundary.py
PYTHONDONTWRITEBYTECODE=1 python3 checks/check_mutations.py
