#!/usr/bin/env bash
# Week 01 setup. Creates a local virtualenv and stages your data locally.
# Nothing here is committed: this repository is public and data/ is gitignored.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "Creating virtual environment in .venv/ ..."
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --quiet --upgrade pip
python -m pip install --quiet pandas tabulate

mkdir -p data
cp -n ../health_analysis/physio_clean.csv  data/physiological_cycles.csv
cp -n ../health_analysis/sleeps_clean.csv  data/sleeps.csv

echo
echo "Ready. pandas $(python -c 'import pandas; print(pandas.__version__)')"
echo "Staged: $(ls data/*.csv | wc -l | tr -d ' ') csv files in data/ (gitignored)"
echo
echo "Next:  source .venv/bin/activate && python3 specimen.py"
