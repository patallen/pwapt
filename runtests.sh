#!/bin/bash
set -e

. ~/.virtualenvs/python2.7/bin/activate

pip install -r requirements/testing.txt

python -m unittest discover
