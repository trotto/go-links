#!/bin/bash

dir_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )

# create empty database (and drop any pre-existing one)
psql -f "$dir_path/db_create.sql" postgres

# add tables
cd "$dir_path/../../src"

export FLASK_SECRET=testing
export DATABASE_URL="postgresql://admin:testing@/testing_trotto_core"
export FLASK_APP=main.py

flask db upgrade
