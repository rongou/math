#!/usr/bin/env bash
# Second batch, started after the first batch finishes (same snapshot).
OUT="$(cd "$(dirname "$0")" && pwd)"
while pgrep -f "run_comparator.sh $(cat "$OUT/snapshot_root.txt")" > /dev/null; do sleep 20; done
cp "$OUT/summary.tsv" "$OUT/summary_batch1.tsv"
exec "$OUT/run_comparator.sh" "$(cat "$OUT/snapshot_root.txt")" BinPackingGap KMedianThreshold DirectedFeedback ParityLifts VariableWL WLIdentification TwoWayComplementation SensitivitySeparation GotsmanLinial MatrixMultiplication
