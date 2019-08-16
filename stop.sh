#!/bin/bash

# Stop Angular, Postgres, Elasticsearch, and Flask (and kill any associated processes).
# --------------------------------------------------------------------------
pause_until_inactive () {
    loop=true
    service=$1
    while [[ "$loop" = true ]]
    do
        if (systemctl -q is-active ${service}.service)
        then
            sleep 1 && echo "."
        else
            echo -e "\n*** ${service} stopped. ***\n"
            loop=false
        fi
    done
}

echo -e '\n\n*** Stopping frontend app... ***\n\n'
pkill 'ng serve'

echo -e '\n\n*** Stopping backend app... ***\n\n'
pkill flask

echo -e '\n\n*** Stopping postgresql... ***\n\n'
systemctl stop postgresql.service
pause_until_inactive 'postgresql'

echo -e '\n\n*** Stopping elasticsearch... ***\n\n'
systemctl stop elasticsearch.service
pause_until_inactive 'elasticsearch'
