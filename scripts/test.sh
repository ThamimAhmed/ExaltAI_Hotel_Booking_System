#!/bin/bash
set -e

if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
elif [ -f .venv/Scripts/activate ]; then
  source .venv/Scripts/activate
fi

export PYTHONPATH=.

pytest --cov=src --cov-report=term-missing > pytest.log
tail -n 20 pytest.log

# Extract overall coverage percentage
COV=$(grep 'TOTAL' pytest.log | awk '{print $NF}' | tr -d '%')
COV=${COV:-0}

if command -v pyre >/dev/null 2>&1; then
  if [ -d .venv/Lib/site-packages ]; then
    PYRE_EXTRA="--search-path=.venv/Lib/site-packages"
  else
    PYRE_EXTRA=""
  fi
  pyre --noninteractive $PYRE_EXTRA || true
else
  echo "pyre not installed"
fi

if [ "${COV%.*}" -lt 70 ]; then
  echo "Coverage below 70%"
  exit 1
fi
