echo 'export PYTHONPATH=${HOME}/google_appengine:$PYTHONPATH' >> $BASH_ENV
echo 'export SERVER_CODE_ROOT=server' >> $BASH_ENV
echo 'export SERVER_SRC_ROOT=server/src' >> $BASH_ENV
echo 'export FRONTEND_ROOT=frontend' >> $BASH_ENV
# these placeholder credentials are just so the datastore emulator can run without throwing a credentials error
echo 'export GOOGLE_APPLICATION_CREDENTIALS=${HOME}/project/.circleci/no-priv-mock-credentials.json'  >> $BASH_ENV
version=$(date +%s)
echo "export NEW_TROTTO_VERSION_ID=${version}" >> $BASH_ENV
echo "export TEST_INSTANCE_BASE=https://${version}-dot-${GCLOUD_PROJECT}.appspot.com" >> $BASH_ENV
