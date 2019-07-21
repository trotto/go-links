#!/bin/bash

CURRENT_DIR=$(pwd)

dev_appserver.py --port=9095 --admin_port=8095 \
                 --storage_path="$CURRENT_DIR"/local_db \
                 --enable_console=true \
                 src
