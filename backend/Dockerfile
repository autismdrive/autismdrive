FROM python:3.8-slim
RUN apt-get update
RUN apt-get install apache2-dev libpq-dev -y
COPY ./ /star-drive
RUN /bin/bash -c "python3 -m venv python-env \
 && source python-env/bin/activate \
 && pip3 install -r star-drive/backend/requirements.txt" 
RUN /bin/bash -c "cd /star-drive/backend/ && echo $PWD && mkdir instance && cp -r config instance/config && cp instance/config/docker.py instance/config.py"
ENV FLASK_DEBUG=1
ENV FLASK_APP=star-drive/backend/app/__init__.py
CMD /bin/bash -c "source python-env/bin/activate \
 && /star-drive/backend/containerrun.sh"
