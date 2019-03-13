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

echo -e '\n\n*** backend reset. Start tests in frontend with "ng e2e" ***\n\n'
cd $FRONTEND_PATH
ng e2e --dev-server-target=
