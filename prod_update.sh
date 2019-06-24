#!/bin/bash

# Run the basic operations to update a production setup after a code change.
# This script should be executed by a post_receive git hook after completing
# a checkout.
# --------------------------------------------------------------------------

# Move the configuration file into place.
mkdir -p ./backend/instance
cp /home/ubuntu/star_config.py ./backend/instance/config.py
cp /home/ubuntu/api-keys.ts ./frontend/src/api-keys.ts

if [ "$1" == "prod" ]; then
    echo "Building for production."
elif [ "$1" == "private" ]; then
    echo "Building for private staging server."
elif [ "$1" == "staging" ]; then
    echo "Building for staging."
else
    echo "Please specify environment (prod/private/staging)"
    exit
fi

export ENV=$1

export FLASK_APP=./backend/app/__init__.py

# Set the home directory
export HOME_DIR=`pwd`
echo "Running from ${HOME_DIR}"

# activate the pip environment we are running inside of, and upgrade any
# library dependencies.
source ./backend/python-env/bin/activate
export FLASK_APP=${HOME_DIR}/backend/app/__init__.py
eval 'cd ${HOME_DIR}/backend && pip3 install -r requirements.txt'

# Load up the staging environment
if [ "$ENV" == "staging" ]; then
eval 'cd ${HOME_DIR}/backend && /home/ubuntu/.local/bin/flask resourcereset'
fi

eval 'cd ${HOME_DIR}/backend && /home/ubuntu/.local/bin/flask db upgrade'


# clear and rebuild the index
eval 'cd ${HOME_DIR}/backend && /home/ubuntu/.local/bin/flask clearindex'
eval 'cd ${HOME_DIR}/backend && /home/ubuntu/.local/bin/flask initindex'

# Rebuild the front end.
eval 'cd ${HOME_DIR}/frontend && npm install'
if [ "$1" == "prod" ]; then
    eval 'cd ${HOME_DIR}/frontend && ng build --prod -c production'
else
    eval 'cd ${HOME_DIR}/frontend && ng build -c ${ENV}'
fi
# Reload apache
echo "Reloading Apache"
sudo service apache2 reload

