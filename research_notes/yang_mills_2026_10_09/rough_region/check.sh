#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
python3 checks/check_replacement.py
python3 checks/check_scalar_controls.py
./formal/check.sh
