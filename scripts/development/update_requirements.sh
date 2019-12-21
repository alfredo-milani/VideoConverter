#!/usr/bin/env bash

# Go to project root
# cd ../..
echo "- Current directory: $(pwd)"

# Update requirements.txt file with libs from requirements.in
echo "- Updating requirements.txt file"
pip-compile --output-file=requirements.txt requirements.in

# Sync libs
echo "- Syncing libs"
pip-sync
