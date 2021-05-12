# Dagyter
The goal of this projet is to easily schedule pipelines of Jupyter notebooks using Dagster.  
toml file...  
Logger...  


# Installation
- git clone...  
- copy workspace-example in another directory. You can add directories named "not_versionned" in any directory, they will be ignored
- create .env file  
- docker-compose up -d 
then you can use bindou to make a clean installation 

## .env example 
COMPOSE_PROJECT_NAME=PROD  
WORKSPACE_DIR=./example-workspace  
DAGSTER_PERSISTANCE_DIR=../persistance/  

