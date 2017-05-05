#!/usr/bin/env bash
echo " --- Start of installation test ..."
venv="$(readlink -f $(date +%s)_brq_install_test)"
virtualenv "$venv" && cd "$venv" && source bin/activate
echo " --- Created virtualenv: $venv ..."
pip install baroque
if [ $? -ne 0 ]; then
    echo " --- Installation through pip failed!"
    exit 1
fi
echo " --- Installation through pip was OK ..."
python3 -c "import baroque"
if [ $? -ne 0 ]; then
    echo " --- Test import of library failed!"
    exit 2
fi
echo " --- Test import of library was OK ..."
deactivate
rm -rf "$venv"
exit 0