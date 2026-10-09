#!/bin/bash
# Usage: kw.sh "regex" -- list families whose CONTENTS.md block matches regex (case-insensitive), with hit counts
C=/home/rou/src/math/CONTENTS.md
awk -v pat="$1" 'BEGIN{IGNORECASE=1}
/^\*\*[0-9][0-9][0-9]\. /{fam=substr($0,3,3); title=$0; sub(/\*\*[0-9]+\. /,"",title); sub(/\*\*.*/,"",title); titles[fam]=title}
{ if (fam!="" && $0 ~ pat) { n[fam]++ } }
END{ for (f in n) printf "%s (%d) %s\n", f, n[f], titles[f] }' $C | sort
