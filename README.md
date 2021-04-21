# Dagyter
The goal of this projet is to easily schedule pipelines of Jupyter notebooks using Dagster.  
toml file...  
Logger...  


# Installation
- git clone...  
- copy workspace-example in another directory  
- create .env file  
- docker-compose up -d  

## .env file example
#--- Dagyter  
COMPOSE_PROJECT_NAME=PROD  
DAGY_PORT=127.0.0.1:8082  
WORKSPACE_DIR=./example-workspace  
  
#--- Dagster  
DAGSTER_PORT=127.0.0.1:3004  
DAGSTER_PERSISTANCE_DIR=../persistance/  
DAGSTER_URL=https://dagster.domain.com  
  
#--- Jupyter  
JUPYTER_PORT=127.0.0.1:8887  
JUPYTER_URL=https://jupyter.domain.com   
  
#--- Streamlit  
STREAMLIT_URL=https://streamlit.domain.com  
STREAMLIT_PORT=127.0.0.1:8501  
  
## .env local example  
#--- Dagyter  
COMPOSE_PROJECT_NAME=DEV  
DAGY_PORT=8082  
WORKSPACE_DIR=./example-workspace  
  
#--- Dagster  
DAGSTER_PORT=3004  
DAGSTER_PERSISTANCE_DIR=../persistance/  
DAGSTER_URL=http://localhost:3004  
  
#--- Jupyter  
JUPYTER_PORT=8887  
JUPYTER_URL=http://localhost:8887  
  
#--- Streamlit  
STREAMLIT_URL=http://localhost:8501  
STREAMLIT_PORT=8501  
