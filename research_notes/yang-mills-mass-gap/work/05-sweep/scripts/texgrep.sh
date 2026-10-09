#!/bin/bash
# Usage: texgrep.sh "regex" [min]  -- list preprint dirs whose build TeX matches regex (case-insensitive, ERE), with hit counts >= min
min=${2:-1}
cd /home/rou/src/math/preprints
grep -rEic --include="*.tex" "$1" */build 2>/dev/null | awk -F: '$2>0 {split($1,a,"/"); n[a[1]]+=$2} END {for (d in n) printf "%6d %s\n", n[d], d}' | awk -v m=$min '$1>=m' | sort -rn
