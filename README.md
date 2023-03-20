# Dagyter
The goal of this projet is to easily schedule pipelines of Jupyter notebooks using Dagster (and Dagstermill).  

## Examples
An example with a simple dag
![dag](https://github.com/nicolasgallandpro/dagyter/blob/main/img/simple.png?raw=true)

An example with a more complex dag
![dag](https://github.com/nicolasgallandpro/dagyter/blob/main/img/complex.png?raw=true)

## Getting started
You can call the "create_definitions" function of dagyter.py with the toml file as argument :  
defs = create_definitions("/workspace/pipelines_and_scheduling.toml")  
  
You can find a full docker example in the "example" directory.
