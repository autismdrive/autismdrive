#!/bin/bash

# Start Postgres, Elasticsearch, Flask, and Angular servers
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
FRONTEND_PATH="${HOME_DIR}/frontend"
DATABASE_PATH="/usr/local/var/postgres"

echo -e '\n\n*** Stopping currently-running services... ***\n\n'
./stop.sh

# Pause for 3 seconds to allow stop script to finish
pause_for 3

echo "Running from ${HOME_DIR}"

echo -e '\n\n*** Starting postgresql and elasticsearch... ***\n\n'
pg_ctl start -D $DATABASE_PATH &
POSTGRES_PID=$! # Save the process ID

# Pause for 5 seconds to allow Postgres to start
pause_for 3

elasticsearch &
ELASTIC_PID=$! # Save the process ID

# Pause for 10 seconds to allow Elasticsearch to start
pause_for 10

echo -e '\n\n*** Starting backend app... ***\n\n'
cd $BACKEND_PATH
source python-env/bin/activate
export FLASK_APP=./app/__init__.py
export FLASK_DEBUG=1
flask run &
FLASK_PID=$! # Save the process ID

# Pause for 5 seconds to allow Flask to start
pause_for 5

echo -e '\n\n*** Starting frontend app... ***\n\n'
cd $FRONTEND_PATH
ng serve &
NG_PID=$! # Save the process ID

echo -e '\n\n*** frontend app running at http://localhost:4200 ***\n\n'
wait $POSTGRES_PID $ELASTIC_PID $FLASK_PID $NG_PID
