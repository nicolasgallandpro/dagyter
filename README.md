# Dagyter
The goal of this projet is to easily schedule pipelines of Jupyter notebooks using Dagster.  
toml file...  
Logger...  


# Installation
clone...  
docker-compose up -d  
  
# Configuration
## .env
#--- Dagyter  
COMPOSE_PROJECT_NAME=PROD  
DAGY_PORT=8082  
WORKSPACE_DIR=./example-workspace  
  
#--- Dagster  
DAGSTER_PORT=3004  
DAGSTER_PERSISTANCE_DIR=../persistance/  
DAGSTER_URL=https://dagster.domain.com  
  
#--- Jupyter  
JUPYTER_PORT=8887  
JUPYTER_URL=https://jupyter.domain.com   
  
#--- Streamlit  
STREAMLIT_URL=https://streamlit.domain.com  
STREAMLIT_PORT=8501  
  

