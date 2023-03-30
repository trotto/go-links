FROM python:3.10.10-slim-bullseye

ENV CLOUDSDK_PYTHON=/usr/local/bin/python
RUN apt-get update && apt-get install curl gnupg2 libpq-dev gcc -y

WORKDIR /usr/src/app
COPY server server

# from https://cloud.google.com/sdk/docs/install#deb
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y
RUN pip install -r server/src/requirements.txt

CMD [ "./server/scripts/run.sh" ]
