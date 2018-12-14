#!/bin/bash

# Start Postgres & Elasticsearch, then run all backend unit tests.
# --------------------------------------------------------------------------
pause_for () {
  for (( c=1; c<=$1; c++ ))
  do
     sleep 1 && echo "."
  done
}

# Set the home directory
export HOME_DIR=`pwd`
BACKEND_PATH="${HOME_DIR}/backend"
# FRONTEND_PATH="${HOME_DIR}/frontend"
DATABASE_PATH="/usr/local/var/postgres"

# Pause for 3 seconds
pause_for 3

echo -e '\n\n*** Stopping currently-running services... ***\n\n'
./stop.sh

# Pause for 3 seconds to allow stop script to finish
pause_for 3

echo "Running from ${HOME_DIR}"

echo -e '\n\n*** Starting postgresql and elasticsearch... ***\n\n'
pg_ctl start -D $DATABASE_PATH -W &
POSTGRES_PID=$! # Save the process ID

# Pause for 3 seconds to allow Postgres to start
pause_for 3

elasticsearch -d &
ELASTIC_PID=$! # Save the process ID

# Pause for 10 seconds to allow Elasticsearch to start
pause_for 15

# echo -e '\n\n*** Running backend tests... ***\n\n'
# cd $BACKEND_PATH
# source python-env/bin/activate
# export FLASK_APP=./app/__init__.py
# python tests.py

echo -e '\n\n*** postgres & elastic running. ***\n\n'
wait $POSTGRES_PID $ELASTIC_PID
