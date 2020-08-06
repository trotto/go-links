#!/bin/bash

export PLATFORM=app_engine
export DATABASE=cloud_datastore
export ENVIRONMENT=dev

# see https://cloud.google.com/datastore/docs/tools/datastore-emulator#manually_setting_the_variables
export DATASTORE_DATASET=trotto-test
export DATASTORE_EMULATOR_HOST=localhost:8081
export DATASTORE_EMULATOR_HOST_PATH=localhost:8081/datastore
export DATASTORE_HOST=http://localhost:8081
export DATASTORE_PROJECT_ID=trotto-test

cd src
export FLASK_APP=main.py
export FLASK_RUN_PORT=9095
export FLASK_ENV=development
flask run
