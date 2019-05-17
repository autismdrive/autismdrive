#!/bin/bash

# Run all backend tests.
# --------------------------------------------------------------------------

# Set the home directory
export HOME_DIR=`pwd`
BACKEND_PATH="${HOME_DIR}/backend"

echo -e '\n\n*** Starting tests in backend with nose2 ***\n\n'
cd $BACKEND_PATH
source python-env/bin/activate
export FLASK_APP=./app/__init__.py
nose2 -v & TESTING_PID=$!

wait $TESTING_PID

TESTING_DONE="Back-end testing is complete."
if command -v say >/dev/null 2>&1; then
  say "$TESTING_DONE"
else
  if command -v spd-say >/dev/null 2>&1; then
    spd-say "$TESTING_DONE"
  else
    echo -e "\07\07"
  fi
fi