FROM python:3.8-slim
RUN apt-get update
RUN apt-get install git apache2-dev libpq-dev -y

RUN git clone https://github.com/sartography/star-drive.git
RUN /bin/bash -c "python3 -m venv python-env \
 && source python-env/bin/activate \
 && pip3 install -r star-drive/backend/requirements.txt" 
RUN /bin/bash -c "cd star-drive && git checkout -b dockerization"
RUN /bin/bash -c "cd /star-drive/backend/ &&  mkdir instance && cp -r config instance/config && cp instance/config/docker.py instance/config.py"
RUN apt-get remove --purge git
ENV FLASK_DEBUG=1
ENV FLASK_APP=star-drive/backend/app/__init__.py
CMD /bin/bash -c "source python-env/bin/activate && flask run & FLASK_PID=$! && echo -e '\n\n*** backend running at http://localhost:5000 ***\n\n' && wait $FLASK_PID"
