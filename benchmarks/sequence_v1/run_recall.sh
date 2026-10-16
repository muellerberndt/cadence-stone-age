#!/bin/zsh
# The recall-memory witness as declared in RECALL_PROTOCOL.md: two queues, at most two runner
# processes, single BLAS thread, the shared venv with the library worktree on PYTHONPATH.
# usage: run_recall.sh <queue 1|2> <runs dir> <library src dir>
set -u
QUEUE=$1
RUNS=$2
export PYTHONPATH=$3
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
PY=/Users/muellerberndt/Projects/oph-meta/.venv-cadence/bin/python
HERE=${0:a:h}
mkdir -p $RUNS
cd $HERE
SEEDS=(202001 202025)
if [[ $QUEUE == 1 ]]; then
  VIEWS=(hidden invisible)
else
  VIEWS=(visible consecutive)
fi
for view in $VIEWS; do
  echo "$(date '+%F %T') start $view; $(uptime)"
  $PY runner.py --protocol protocol-recall-screen-$view.json --out $RUNS/rs-$view --seeds ${SEEDS[@]} --recipes founder recall > $RUNS/rs-$view.log 2>&1
  echo "$(date '+%F %T') done $view (exit $?)"
done
if [[ $QUEUE == 1 ]]; then
  echo "$(date '+%F %T') start p1 founder 1001; $(uptime)"
  $PY runner.py --protocol protocol-recall-p1.json --out $RUNS/rs-p1 --seeds 1001 --recipes founder recall > $RUNS/rs-p1.log 2>&1
  echo "$(date '+%F %T') done p1 (exit $?)"
fi
echo "$(date '+%F %T') queue $QUEUE finished; $(uptime)"
