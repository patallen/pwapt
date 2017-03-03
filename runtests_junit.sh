#!/bin/bash
set -e

. ~/.virtualenvs/python2.7/bin/activate

pip install -r requirements/testing.txt

py.test --junitxml junit_test_output/results_$(date +"%Y%m%d%H%M").xml
