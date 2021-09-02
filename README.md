# Dagyter
The goal of this projet is to easily schedule pipelines of Jupyter notebooks using Dagster.  


# How it works
Dagyter includes:
- a Dagster installation (port 3000)
- a Jupyter notebook (port 8888)
- a Streamlit (port 5001)

All your codes (notebooks, dagster dags conf, python files, ...) must be mounted in the /workspace directory of the container.
The Dagster DAGs (pipelines) are configured with a small toml file : /workspace/pipelines_and_scheduling.toml
You can find examples of Dagyter configurations (local and server) here : https://github.com/nicolasgallandpro/dagyter_examples

# Features
Dagyter offers some features :
- a pre-configured Dagster / Dagstermill / Jupyter / Streamlit
- a simplified way to schedule notebooks via a toml file
- a logger class to make it easier to log in the same time in the notebook AND in dagster logs (you just have to use logger.info() or logger.error() instead of print() in the notebooks and the output will be visible in the notebooks AND in dagster logs)


# Installation
The simple way is to start from one of the examples you can find here :  https://github.com/nicolasgallandpro/dagyter_examples
and then execute : docker-compose up -d 

