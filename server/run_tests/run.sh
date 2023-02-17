#!/bin/bash

export CLEAR_POSTGRES_DB_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/postgres/clear_db.sh"

export ENVIRONMENT=test_env
export FLASK_SECRET=testing
export DATABASE_URL="postgresql://admin:testing@/testing_trotto_core"

bash "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/postgres/create_db.sh"

python run_tests/run_tests.py $1 --logging-level INFO
