#!/usr/bin/env bash
# The 0.89 memory readings: one runner process per reading, recipe and founder, at most WORKERS at
# a time, one BLAS thread each, cadence-net 0.89.0 from PyPI in the interpreter PY.
# usage: run_m089.sh OUT WORKERS [JOBS]   (JOBS defaults to OUT/jobs.txt, written by memory_089.py jobs)
set -u
OUT=$1; WORKERS=$2; JOBS=${3:-$OUT/jobs.txt}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
PY=${PY:-python}
HERE=$(cd "$(dirname "$0")" && pwd)
WHEEL=7b27009d0affd2235026ca5f7b4776ba545c15d5c5a14a61c75e52b6df65b786
mkdir -p "$OUT/logs"
run_one() {
  reading=$1; protocol=$2; recipe=$3; seed=$4
  target=$OUT/$reading/$recipe/s$seed
  [ -f "$target/metrics.json" ] && return 0
  rm -rf "$target"; mkdir -p "$(dirname "$target")"
  log=$OUT/logs/$reading-$recipe-s$seed.log
  (cd "$HERE" && $PY runner.py --protocol "$protocol" --out "$target" --seeds "$seed" \
     --recipes "$recipe" --wheel-sha256 "$WHEEL") > "$log" 2>&1
  echo "$reading $recipe $seed $?" >> "$OUT/status.txt"
}
export -f run_one
export OUT HERE PY WHEEL
xargs -P "$WORKERS" -L 1 bash -c 'run_one "$@"' _ < "$JOBS"
(cd "$HERE" && $PY memory_089.py analyze "$OUT") > "$OUT/logs/analysis.log" 2>&1
echo "all done $(date -u '+%FT%TZ')" >> "$OUT/status.txt"
