#!/usr/bin/env bash
# The 0.90 candidate against 0.89.0: one runner process per library, reading, recipe and founder,
# at most WORKERS at a time, one BLAS thread each. LIB_R089 and LIB_C090 name each library's
# directory, put first on PYTHONPATH; the 0.89.0 runs also record the published wheel's SHA-256.
# usage: LIB_R089=... LIB_C090=... run_m090.sh OUT WORKERS   (OUT/jobs.txt from memory_090.py jobs)
set -u
OUT=$1; WORKERS=$2; JOBS=$OUT/jobs.txt
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
PY=${PY:-python}
HERE=$(cd "$(dirname "$0")" && pwd)
WHEEL=7b27009d0affd2235026ca5f7b4776ba545c15d5c5a14a61c75e52b6df65b786
mkdir -p "$OUT/logs"
run_one() {
  library=$1; reading=$2; protocol=$3; recipe=$4; seed=$5; arm=$6
  target=$OUT/$library/$reading/$recipe/s$seed
  [ -f "$target/metrics.json" ] && return 0
  rm -rf "$target"; mkdir -p "$(dirname "$target")"
  log=$OUT/logs/$library-$reading-$recipe-s$seed.log
  if [ "$library" = R089 ]; then lib=$LIB_R089; wheel=(--wheel-sha256 "$WHEEL"); else lib=$LIB_C090; wheel=(); fi
  (cd "$HERE" && PYTHONPATH="$lib" $PY runner.py --protocol "$protocol" --out "$target" --seeds "$seed" \
     --recipes "$recipe" --arms "$arm" "${wheel[@]}") > "$log" 2>&1
  echo "$library $reading $recipe $seed $?" >> "$OUT/status.txt"
}
export -f run_one
export OUT HERE PY WHEEL LIB_R089 LIB_C090
xargs -P "$WORKERS" -L 1 bash -c 'run_one "$@"' _ < "$JOBS"
(cd "$HERE" && $PY memory_090.py analyze "$OUT") > "$OUT/logs/analysis.log" 2>&1
echo "all done $(date -u '+%FT%TZ')" >> "$OUT/status.txt"
