#!/bin/bash
# Work out which directory the script is stored in
DIR="$( cd -P "$( dirname "$0" )" && pwd )"
# Change to my directory, in case we were being run from somewhere else
cd $DIR
# Run the project
python spellathon.py
