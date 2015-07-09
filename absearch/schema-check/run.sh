#!/bin/bash
# Read the config.schema.json and validates against config.json
# $1: github project name
rm -rf $1
git clone http://github.com/mozilla-services/$1
python $1/setup.py develop
absearch-check
