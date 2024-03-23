FROM python:3.11.8-slim-bullseye

RUN apt-get update && apt-get install curl gnupg2 libpq-dev gcc -y

# from https://cloud.google.com/sdk/docs/install#deb
ENV CLOUDSDK_PYTHON=/usr/local/bin/python
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y

WORKDIR /usr/src/app

COPY server/src/requirements.txt server/src/requirements.txt
RUN pip install -r server/src/requirements.txt

COPY server server

CMD [ "./server/scripts/run.sh" ]
