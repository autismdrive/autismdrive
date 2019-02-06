#!/bin/bash

# Start Angular
# --------------------------------------------------------------------------
# Set the home directory
export HOME_DIR=`pwd`
FRONTEND_PATH="${HOME_DIR}/frontend"

echo -e '\n\n*** Starting frontend app... ***\n\n'
cd $FRONTEND_PATH
ng serve & NG_PID=$! # Save the process ID

echo -e '\n\n*** frontend app running at http://localhost:4200 ***\n\n'
wait $NG_PID
