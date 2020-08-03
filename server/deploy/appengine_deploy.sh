#!/bin/bash

set -e

python prepare_deploy.py

source src/config/.set_env_vars

gcloud app deploy --project $TROTTO_APP_ID -q -v $(date +%s) src/app.yaml src/index.yaml src/queue.yaml
