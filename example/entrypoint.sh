#!/bin/sh
export PYTHONPATH="$PYTHONPATH:/workspace/commons:/workspace"

# launch jupyter
jupyter lab --port=8888 --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='' &

# dagit
cd /opt/dagster/conf
dagster dev -f /workspace/repos.py -h "0.0.0.0" -p "3000"
