#!/bin/bash

# Start Postgres
# --------------------------------------------------------------------------
DATABASE_PATH="/usr/local/var/postgres"

echo -e '\n\n*** Starting postgresql... ***\n\n'
pg_ctl start -D $DATABASE_PATH -W & POSTGRES_PID=$! # Save the process ID

echo -e '\n\n*** postgres running. ***\n\n'
wait $POSTGRES_PID
