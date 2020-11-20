# Stage 1
FROM node:10-alpine
RUN apk --update add git less openssh && \
    rm -rf /var/lib/apt/lists/* && \
    rm /var/cache/apk/*
RUN git clone https://github.com/sartography/star-drive.git
WORKDIR star-drive/frontend/
RUN npm install -g @angular/cli
RUN npm install
CMD ng serve
