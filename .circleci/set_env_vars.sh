echo 'export PYTHONPATH=${HOME}/google_appengine:$PYTHONPATH' >> $BASH_ENV
echo 'export SERVER_CODE_ROOT=server' >> $BASH_ENV
echo 'export SERVER_SRC_ROOT=server/src' >> $BASH_ENV
echo 'export FRONTEND_ROOT=frontend' >> $BASH_ENV
echo "export NEW_TROTTO_VERSION_ID=$(date +%s)" >> $BASH_ENV
