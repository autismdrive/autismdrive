#!/bin/bash

# Start Flask
# --------------------------------------------------------------------------
# Set the home directory
export HOME_DIR=`pwd`
BACKEND_PATH="${HOME_DIR}/backend"

echo -e '\n\n*** Starting backend app... ***\n\n'
cd $BACKEND_PATH
source python-env/bin/activate
export FLASK_APP=./app/__init__.py
export FLASK_DEBUG=1
flask run & FLASK_PID=$! # Save the process ID

echo -e '\n\n*** backend running at http://localhost:5000 ***\n\n'
wait $FLASK_PID
