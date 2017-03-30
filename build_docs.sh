#!/bin/bash

# Have sphinxcontrib-napoleon read google-styled docstrings and generate
# RST files that can be read by Sphinx
# (http://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html)
sphinx-apidoc -f -o docs . tests setup.py sample.py

# Run Sphinx and get HTML files
cd docs/
make clean
make html