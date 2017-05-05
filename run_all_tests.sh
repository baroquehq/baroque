#!/usr/bin/env bash
set -e
cd tests/runners
bash run_unit_tests.sh
bash run_installation_test.sh
bash run_test_yml_reading.sh
bash run_samples.sh