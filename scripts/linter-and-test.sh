#!/bin/sh

source activate mlops_project
autopep8 --in-place --aggressive --aggressive $1/src/$2.py
pylint $1/src/$2.py
pytest $1/tests/test_modules.py -vv -k test_$2
