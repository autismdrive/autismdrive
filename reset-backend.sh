#!/bin/bash

# Start Flask
# --------------------------------------------------------------------------
# Set the home directory
export HOME_DIR=`pwd`
BACKEND_PATH="${HOME_DIR}/backend"

echo -e '\n\n*** Resetting backend app... ***\n\n'
cd $BACKEND_PATH
source python-env/bin/activate
export FLASK_APP=./app/__init__.py
flask db upgrade
flask initdb
