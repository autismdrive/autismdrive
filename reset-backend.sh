#!/bin/bash

# Start Flask
# --------------------------------------------------------------------------
# Set the home directory
export HOME_DIR=`pwd`
BACKEND_PATH="${HOME_DIR}/backend"

# Install updates by default
SKIP_UPDATE=0

# getopts string
# This string needs to be updated with the single character options (e.g. -f)
opts="s:"

# Gets the command name without path
cmd(){ echo `basename $0`; }

# Help command output
usage(){
echo "\
`cmd` [OPTION...]
-s, --skip_update; Skip updating dependencies
" | column -t -s ";"
}

# Error message
error(){
    echo "`cmd`: invalid option -- '$1'";
    echo "Try '`cmd` -h' for more information.";
    exit 1;
}


# Handle long and short option flags
# https://gist.github.com/shakefu/2765260
for pass in 1 2; do
    while [ -n "$1" ]; do
        case $1 in
            --) shift; break;;
            -*) case $1 in
                -s|--skip_update)  SKIP_UPDATE=1;;
                --*)           error $1;;
                -*)            if [ $pass -eq 1 ]; then ARGS="$ARGS $1";
                               else error $1; fi;;
                esac;;
            *)  if [ $pass -eq 1 ]; then ARGS="$ARGS $1";
                else error $1; fi;;
        esac
        shift
    done
    if [ $pass -eq 1 ]; then ARGS=`getopt $opts $ARGS`
        if [ $? != 0 ]; then usage; exit 2; fi; set -- $ARGS
    fi
done


echo -e '\n\n*** Resetting backend app... ***\n\n'
cd $BACKEND_PATH
source python-env/bin/activate
export FLASK_APP=./app/__init__.py

if ! $SKIP_UPDATE ; then
  pip3 install -r requirements.txt
fi

flask db upgrade
flask reset

