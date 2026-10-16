#!/bin/zsh
# The follow-up reading (RECALL_PROTOCOL.md, "Follow-up reading: context in the key"): the two
# context recipes on three views, two queues, at most two runner processes; the founder and
# recall rows are the first reading's retained runs (rs-<view>) and are not rerun.
# usage: run_recall_context.sh <queue 1|2> <runs dir> <library src dir>
set -u
QUEUE=$1
RUNS=$2
export PYTHONPATH=$3
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
PY=/Users/muellerberndt/Projects/oph-meta/.venv-cadence/bin/python
HERE=${0:a:h}
cd $HERE
SEEDS=(202001 202025)
if [[ $QUEUE == 1 ]]; then
  VIEWS=(hidden visible)
else
  VIEWS=(invisible)
fi
for view in $VIEWS; do
  echo "$(date '+%F %T') start context $view; $(uptime)"
  $PY runner.py --protocol protocol-recall-context-$view.json --out $RUNS/rc-$view --seeds ${SEEDS[@]} --recipes recall_ctx05 recall_ctx10 > $RUNS/rc-$view.log 2>&1
  echo "$(date '+%F %T') done context $view (exit $?)"
done
echo "$(date '+%F %T') context queue $QUEUE finished; $(uptime)"
# P1 on founder 1001 for the better context recipe runs separately after the screen's analysis:
#   runner.py --protocol protocol-recall-context-p1.json --out $RUNS/rc-p1 --seeds 1001 --recipes <better>
