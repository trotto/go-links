emulator_process=$(lsof -t -i:8082)
if [ -n "$emulator_process" ]; then
  kill -9 $emulator_process
fi

gcloud config set project trotto-test
sh test_datastore_emulator_start.sh > /dev/null 2>&1 &

export PLATFORM=app_engine
export DATABASE=cloud_datastore
export ENVIRONMENT=test_env

# see https://cloud.google.com/datastore/docs/tools/datastore-emulator#manually_setting_the_variables
export DATASTORE_DATASET=trotto-test
export DATASTORE_EMULATOR_HOST=localhost:8082
export DATASTORE_EMULATOR_HOST_PATH=localhost:8082/datastore
export DATASTORE_HOST=http://localhost:8082
export DATASTORE_PROJECT_ID=trotto-test

python run_tests.py $1 --logging-level INFO
