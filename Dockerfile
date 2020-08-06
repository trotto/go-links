FROM python:3.7-buster

WORKDIR /usr/src/app
COPY server server
COPY client_secrets.json server/src/config/client_secrets.json
COPY app.yml server/src/config/app.yml
RUN pip install -r server/src/requirements.txt

CMD [ "sh", "server/scripts/run.sh" ]
