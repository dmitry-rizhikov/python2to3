#!/usr/bin/env bash

# remove old virtual envs
rm -rf venv venv2

# install virtualenv
pip install --user virtualenv

# install py2 virtual env
virtualenv -p /usr/bin/python2 venv2
# upgrade pip
venv2/bin/pip install --upgrade pip
venv2/bin/pip install -r requirements2.txt

# install py3 virtual env
virtualenv -p /usr/bin/python3.7 venv
# upgrade pip
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements3.txt