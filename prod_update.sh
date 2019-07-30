#!/bin/bash

# Run the basic operations to update a production setup after a code change.
# This script should be executed by a post_receive git hook after completing
# a checkout.
# --------------------------------------------------------------------------

# Move the configuration file into place.
mkdir -p ./backend/instance
cp /home/ubuntu/star_config.py ./backend/instance/config.py

if [ "$1" == "prod" ]; then
    echo "Building for production."
elif [ "$1" == "mirror" ]; then
    echo "Building for mirroring server."
elif [ "$1" == "staging" ]; then
    echo "Building for staging."
else
    echo "Please specify environment (prod/mirror/staging)"
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
eval 'cd ${HOME_DIR}/backend && flask resourcereset'
fi

eval 'cd ${HOME_DIR}/backend && flask db upgrade'

# clear and rebuild the index
eval 'cd ${HOME_DIR}/backend && flask clearindex'
eval 'cd ${HOME_DIR}/backend && flask initindex'

# Copy the frontend config file into the proper place.
declare -a arr=("" ".staging" ".prod")
for NAME in "${arr[@]}"
do
    eval 'cp /home/ubuntu/environment${NAME}.ts ${HOME_DIR}/frontend/src/environments/environment${NAME}.ts'
done

# Rebuild the front end.
eval 'cd ${HOME_DIR}/frontend && npm install'

if [ "$1" == "prod" ]; then
    eval 'cd ${HOME_DIR}/frontend && ng build --prod -c production'
elif [ "$1" == "mirror" ]; then
    eval 'cd ${HOME_DIR}/frontend && ng build -c staging'
else
    eval 'cd ${HOME_DIR}/frontend && ng build -c ${ENV}'
fi
# Reload apache
echo "Reloading Apache"
sudo service apache2 reload
