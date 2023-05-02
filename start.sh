#!/bin/bash

cd csi_fe
nohup npm start > /dev/null &
cd ..
cd CSI_BE
. configure.sh
. secrets.sh
. venv/bin/activate
nohup gunicorn --chdir app -w 2 --threads 2 run:app -b 0.0.0.0:5000 > /dev/null &

