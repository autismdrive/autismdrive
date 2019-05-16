#!/bin/bash

# Clear and re-seed the database, then run all frontend end-to-end tests.
# --------------------------------------------------------------------------

# Set the home directory
export HOME_DIR=`pwd`
BACKEND_PATH="${HOME_DIR}/backend"
FRONTEND_PATH="${HOME_DIR}/frontend"
DATABASE_PATH="/usr/local/var/postgres"

echo -e '\n\n*** Clearing and re-seeding database... ***\n\n'
cd $BACKEND_PATH
source python-env/bin/activate
export FLASK_APP=./app/__init__.py
flask reset

echo -e '\n\n*** backend reset. Starting tests in frontend with "ng e2e --dev-server-target=" ***\n\n'
cd $FRONTEND_PATH
ng e2e --dev-server-target= & TESTING_PID=$!

wait $TESTING_PID

TESTING_DONE="End-to-end testing is complete."
if command -v say >/dev/null 2>&1; then
  say "$TESTING_DONE"
else
  if command -v spd-say >/dev/null 2>&1; then
    spd-say "$TESTING_DONE"
  else
    echo -e "\07\07"
  fi
fi