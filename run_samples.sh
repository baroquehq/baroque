#!/usr/bin/env bash
set -e
echo " --- Start running samples ..."
clone_dir="$(pwd)"
venv="$(date +%s)_brq_samples_test"
virtualenv "$venv" && cd "$venv" && source bin/activate
echo " --- Created virtualenv: $venv ..."
pip install baroque
echo " --- Installed baroque via pip ..."
cd "$clone_dir/samples"
for s in *.py; do python3 "$s"; done
echo " --- Samples run OK ..."
deactivate
exit 0