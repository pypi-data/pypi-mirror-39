#!/usr/bin/env bash

VENV=${VENV:-venv}

pip3 install invoke
pip3 install virtualenv

rm -rf venv
virtualenv -p python3.7 ${VENV}
. ${VENV}/bin/activate
pip3 install -r requirements.txt
