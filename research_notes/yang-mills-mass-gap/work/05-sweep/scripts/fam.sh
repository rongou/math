#!/bin/bash
# Usage: fam.sh NNN [NNN ...]  -- print CONTENTS.md entry for each family, stripped of HTML table tags
C=/home/rou/src/math/CONTENTS.md
for f in "$@"; do
  start=$(grep -n "^\*\*$f\. " $C | head -1 | cut -d: -f1)
  if [ -z "$start" ]; then echo "NO FAMILY $f"; continue; fi
  next=$(awk -v s=$start 'NR>s && /^\*\*[0-9][0-9][0-9]\. /{print NR; exit}' $C)
  [ -z "$next" ] && next=$(wc -l < $C)
  echo "===== FAMILY $f (CONTENTS.md lines $start-$((next-1))) ====="
  sed -n "${start},$((next-1))p" $C | grep -v '^</\?t[dr]>\|^<tbody>\|^</tbody>\|^$' | sed 's#</tbody><tbody><tr>##; s#</td>##; s#<td>##'
done
