#! /bin/bash
sleep 30
flask db init
sleep 5
flask db migrate
sleep 5
flask db upgrade
sleep 5
flask initdb
sleep 5
flask run --host 0.0.0.0
