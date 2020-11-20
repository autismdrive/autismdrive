# Stage 1
FROM sartography/cr-connect-angular-base
COPY ./ /star-drive
WORKDIR /star-drive/frontend/
RUN npm install -g @angular/cli
RUN npm install
CMD ng serve --host 0.0.0.0
