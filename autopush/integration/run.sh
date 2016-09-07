#!/bin/bash

FIREFOX_BINARY=$1

npm install

virtualenv venv
. venv/bin/activate
pip install -r requirements.txt

./run.py --binary $FIREFOX_BINARY 
