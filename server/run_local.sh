#!/bin/bash

export DATABASE=postgres
export ENVIRONMENT=dev

cd src

flask db upgrade

export FLASK_APP=main.py
export FLASK_RUN_PORT=9095
export FLASK_ENV=development

flask run
