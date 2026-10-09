#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
python3 checks/check_finite_volume.py
python3 checks/check_su2_interface.py
./formal/check.sh
./rough_region/check.sh
./boundary_cost/check.sh
./weighted_boundary/check.sh
./exact_marginal/check.sh
