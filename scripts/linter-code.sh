#!/bin/sh

source activate mlops_project
autopep8 --in-place --aggressive --aggressive $1
pylint $1
