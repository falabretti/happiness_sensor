#!/bin/bash

PYTHON_BIN=<PYTHON_BIN_PATH>

cd /
cd <HAPPINESS_HOME>

cd web/
npm start &

cd ../server/
source /opt/intel/openvino/bin/setupvars.sh
$PYTHON_BIN app.py

cd /
