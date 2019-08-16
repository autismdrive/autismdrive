#!/bin/bash

# Start Postgres and Elasticsearch servers
# --------------------------------------------------------------------------
pause_until_active () {
    loop=true
    service=$1
    while [[ "$loop" = true ]]
    do
        if (systemctl -q is-active ${service}.service)
        then
            echo -e "\n*** ${service} running. ***\n"
            loop=false
        else
            sleep 1 && echo "."
        fi
    done
}

echo -e '\n*** Starting postgresql... ***\n'
systemctl reload-or-restart postgresql.service
pause_until_active 'postgresql'

echo -e '\n*** Starting elasticsearch... ***\n'
systemctl reload-or-restart elasticsearch.service
pause_until_active 'elasticsearch'
