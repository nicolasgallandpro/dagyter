# Dagyter
The goal of this projet is to easily schedule pipelines of Jupyter notebooks using Dagster (and Dagstermill).  


# Features
- a container that includes : a pre-configured Dagster+Dagstermill (port 3000), a Jupyter notebook (port 8888), and Streamlit (port 5001)
- a simplified way to schedule pipelines of notebooks via a basic toml file 

All your codes (notebooks, dagster dags conf, python files, ...) must be mounted in the /workspace directory of the container.
The Dagster DAGs (pipelines) configuration is made with a small toml file : /workspace/pipelines_and_scheduling.toml
You can find examples of Dagyter configurations (local and server) here : https://github.com/nicolasgallandpro/dagyter_examples

# Installation
The simple way is to start from one of the examples you can find here :  https://github.com/nicolasgallandpro/dagyter_examples
and then execute : docker-compose up -d 

# Advanced - content of this repos
- Dockerfile - docker-compose.yaml - entrypoint.sh : docker configuration for the container
- dagster directory : dagster conf files that are injected in the container
- jupyter directory : jupyter conf files that are injected in the container
