#!/bin/bash

# Start Postgres, Flask, and Angular servers
# --------------------------------------------------------------------------
pause_for () {
  for (( c=1; c<=$1; c++ ))
  do
     sleep 1 && echo "."
  done
}

echo -e '\n\n*** Stopping currently-running services... ***\n\n'
./stop.sh

# Pause for 3 seconds to allow stop script to finish
pause_for 3

./start-db.sh & POSTGRES_PID=$!

# Pause for 5 seconds to allow Postgres to start
pause_for 5

./start-backend.sh & FLASK_PID=$!

# Pause for 5 seconds to allow Flask to start
pause_for 5

./start-frontend.sh & NG_PID=$!

wait $POSTGRES_PID $FLASK_PID $NG_PID
