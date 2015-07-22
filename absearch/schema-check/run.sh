#!/bin/bash
# Read the config.schema.json and validates against config.json
# The absearch project stores it's config/schema in the absearchdata project
rm -rf absearchdata
git clone http://github.com/mozilla-services/absearchdata
make -C absearchdata/scripts/ install
make -C absearchdata/scripts/ check_config
