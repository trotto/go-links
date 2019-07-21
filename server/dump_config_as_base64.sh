#!/bin/bash

cd src
zip -r ../config.zip config/
base64 ../config.zip
