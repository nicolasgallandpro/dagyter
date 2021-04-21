#!/bin/sh

dagster-daemon run &
dagit -h "0.0.0.0" -p "3000" -w "/opt/dagster/conf/workspace.yaml" &

jupyter lab --port=8888 --no-browser --ip=0.0.0.0 --allow-root &

streamlit run /workspace/streamlitbook.py  &

python /wrapper/run.py


