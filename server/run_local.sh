#!/bin/bash

export ENVIRONMENT=dev

cd src

export FLASK_APP=main.py
export FLASK_RUN_PORT=9095
export FLASK_ENV=development

flask db upgrade

flask run
