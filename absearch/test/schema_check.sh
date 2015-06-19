#!/bin/bash
# Read the config.schema.json and validates against config.json
python $PROJECT_DIR/setup.py develop
absearch-check
