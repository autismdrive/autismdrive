#!/bin/bash

# Start Postgres and Elasticsearch servers
# --------------------------------------------------------------------------
pause_for () {
  for (( c=1; c<=$1; c++ ))
  do
     sleep 1 && echo "."
  done
}

DATABASE_PATH="/usr/local/var/postgres"

echo -e '\n\n*** Starting Postgres... ***\n\n'
pg_ctl start -D $DATABASE_PATH -W & POSTGRES_PID=$! # Save the process ID

# Pause for 3 seconds to allow Postgres to start
pause_for 3
echo -e '\n\n*** Postgres running. ***\n\n'

echo -e '\n\n*** Starting Elasticsearch... ***\n\n'
elasticsearch -d & ELASTIC_PID=$! # Save the process ID

# Pause for 10 seconds to allow Elasticsearch to start
pause_for 15
echo -e '\n\n*** Elasticsearch running. ***\n\n'

wait $POSTGRES_PID $ELASTIC_PID
