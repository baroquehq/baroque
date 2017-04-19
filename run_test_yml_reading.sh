#!/usr/bin/env bash
set -e
echo " --- Start YML configuration reading test ..."
yml_path="$(readlink -f baroque.yml)"
venv="$(date +%s)_brq_samples_test"
virtualenv "$venv" && cd "$venv" && source bin/activate
echo " --- Created virtualenv: $venv ..."
pip install baroque
echo " --- Installed baroque via pip ..."
python3 -c "from baroque import Baroque; brq = Baroque(configfile='$yml_path')"
echo " --- Test was OK ..."
deactivate
exit 0