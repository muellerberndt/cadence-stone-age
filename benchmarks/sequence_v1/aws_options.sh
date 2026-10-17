#!/usr/bin/env bash
# The recall memory's four options on the screen (48 founders, four views) and on P1 (24
# founders): one runner process per view (or P1) and founder, every recipe in each.
# usage: aws_options.sh ROOT OUT WORKERS
#   ROOT holds stone-age/ (this repository) and cadence/ (the library tree with src/)
set -u
ROOT=$1; OUT=$2; WORKERS=$3
export PYTHONPATH=$ROOT/cadence/src
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
PY=${PY:-python}
HERE=$ROOT/stone-age/benchmarks/sequence_v1
mkdir -p "$OUT/logs"
jobs=$OUT/jobs.txt
: > "$jobs"
for view in hidden invisible visible consecutive; do
  for seed in $(seq 202001 202048); do
    echo "screen-$view $seed protocol-options-screen-$view.json" >> "$jobs"
  done
done
for seed in $(seq 1001 1024); do
  echo "p1 $seed protocol-options-p1.json" >> "$jobs"
done
run_one() {
  reading=$1; seed=$2; protocol=$3
  log=$OUT/logs/$reading-s$seed.log
  echo "$(date -u '+%FT%TZ') start $reading $seed; $(uptime)" > "$log"
  (cd "$HERE" && $PY runner.py --protocol "$protocol" --out "$OUT/$reading/s$seed" --seeds "$seed" \
     --recipes founder recall aroused rewarded improved) >> "$log" 2>&1
  status=$?
  echo "$(date -u '+%FT%TZ') done $reading $seed exit $status; $(uptime)" >> "$log"
  echo "$reading $seed $status" >> "$OUT/status.txt"
}
export -f run_one
export OUT HERE PY
xargs -P "$WORKERS" -L 1 bash -c 'run_one "$@"' _ < "$jobs"
(cd "$HERE" && $PY options_reading.py "$OUT") > "$OUT/logs/reading.log" 2>&1
echo "$(date -u '+%FT%TZ') all done" >> "$OUT/status.txt"
