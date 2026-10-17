#!/usr/bin/env bash
# The continuing reading: 24 screen founders x four views and 12 P1 founders, six recipes in each
# job, one runner process per view (or P1) and founder, at most WORKERS at a time.
# usage: run_continuing.sh ROOT OUT WORKERS   (ROOT holds stone-age/ and cadence/ with src/)
set -u
ROOT=$1; OUT=$2; WORKERS=$3
export PYTHONPATH=$ROOT/cadence/src
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
PY=${PY:-python}
HERE=$ROOT/stone-age/benchmarks/sequence_v1
mkdir -p "$OUT/logs"
jobs=$OUT/jobs.txt
: > "$jobs"
for seed in $(seq 1001 1012); do echo "p1 $seed protocol-continuing-p1.json" >> "$jobs"; done
for view in hidden invisible visible consecutive; do
  for seed in $(seq 202001 202024); do echo "screen-$view $seed protocol-continuing-screen-$view.json" >> "$jobs"; done
done
run_one() {
  reading=$1; seed=$2; protocol=$3
  [ -e "$OUT/$reading/s$seed/metrics.json" ] && return 0
  rm -rf "$OUT/$reading/s$seed"
  log=$OUT/logs/$reading-s$seed.log
  echo "$(date -u '+%FT%TZ') start $reading $seed; $(uptime)" > "$log"
  (cd "$HERE" && $PY runner.py --protocol "$protocol" --out "$OUT/$reading/s$seed" --seeds "$seed" \
     --recipes founder recall base keep pred keep_pred) >> "$log" 2>&1
  echo "$(date -u '+%FT%TZ') done $reading $seed exit $?; $(uptime)" >> "$log"
}
export -f run_one
export OUT HERE PY
xargs -P "$WORKERS" -L 1 bash -c 'run_one "$@"' _ < "$jobs"
(cd "$HERE" && $PY continuing_reading.py "$OUT") > "$OUT/logs/reading.log" 2>&1
echo "$(date -u '+%FT%TZ') all done" >> "$OUT/logs/reading.log"
