#!/bin/bash -e

# Use for tagging services-test

if (( $# != 1 )); then
    echo "Please specify the tag"
    exit 1;
fi

HOME_DIR=$(basename $(pwd))
TAG=$1

echo "Tagging..."
git tag -a $1 -m "Release $1"

echo "Pushing new tags..."
git push --tags

