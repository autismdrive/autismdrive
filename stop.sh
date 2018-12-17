#!/bin/bash

# Stop Angular, Postgres, Elasticsearch, and Flask (and kill any associated processes).
# --------------------------------------------------------------------------

# Set the home directory
export HOME_DIR=`pwd`
BACKEND_PATH="${HOME_DIR}/backend"
DATABASE_PATH="/usr/local/var/postgres"

# Stop Angular
echo -e '\n\n*** Stopping frontend app... ***\n\n'
lsof -t -i tcp:4200 -s tcp:listen | xargs kill

# Stop PostgreSQL
echo -e '\n\n*** Stopping postgresql... ***\n\n'
pkill -f postgres
pg_ctl stop -m immediate -D $DATABASE_PATH

# Stop ElasticSearch
echo -e '\n\n*** Stopping elasticsearch... ***\n\n'
pkill -f elasticsearch

# Kill any remaining server processes
echo -e '\n\n*** Stopping backend app... ***\n\n'
lsof -t -i tcp:5000 -s tcp:listen | xargs kill
lsof -t -i tcp:9200 -s tcp:listen | xargs kill
lsof -t -i tcp:5432 -s tcp:listen | xargs kill