#!/usr/bin/env bash
set -e
echo " --- Start YML configuration reading test ..."
clone_dir="$(pwd)/../.."
yml_path="$(readlink -f $clone_dir/baroque.yml)"
venv="$(readlink -f $(date +%s)_brq_yml_reading_test)"
virtualenv "$venv" && cd "$venv" && source bin/activate
echo " --- Created virtualenv: $venv ..."
pip install baroque
echo " --- Installed baroque via pip ..."
python3 -c "from baroque import Baroque; brq = Baroque(configfile='$yml_path')"
echo " --- Test was OK ..."
deactivate
rm -rf "$venv"
exit 0