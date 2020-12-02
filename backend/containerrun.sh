#! /bin/bash
timeout 300 bash -c "until curl --silent --output /dev/null http://star-drive_es_1:9200/_cat/health?h=st; do printf '.'; sleep 5; done; printf '\n'"
flask db init
sleep 5
flask db migrate
sleep 5
flask db upgrade
sleep 5
psql $(grep -i "SQLALCHEMY_DATABASE_URI" /star-drive/backend/instance/config.py | awk -F'"' '{print $2}') -lqt | cut -d \| -f 1 | grep stardrive | grep 0 && flask initdb
flask run --host 0.0.0.0
