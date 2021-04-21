FROM nicogalland/python-base-data-eng-light:latest

RUN mkdir /root/.ssh

#------------ jupyter
RUN pip install jupyterlab jupyterlab-git toml

#------------- dagster
RUN pip install \
    dagster \
    dagster-graphql \
    dagit \
    dagster-postgres \
    dagstermill \ 
    pycountry \ 
    pandas-profiling[notebook] \
    streamlit \ 
    pyecharts \ 
    plotly \
    pyecharts \
    streamlit-echarts 
 

ENV DAGSTER_HOME=/opt/dagster/dagster_home

RUN mkdir -p $DAGSTER_HOME
COPY dagster/dagster.yaml $DAGSTER_HOME
RUN mkdir /dagyter
COPY dagyter.py /dagyter
ENV PYTHONSTARTUP=/dagyter/dagyter.py

#------------ start

#workdir /workspace/output in order to have dagster put output notebooks in this directory (didn't fount another way to configure it
WORKDIR /workspace/output  
ENV PYTHONPATH "${PYTHONPATH}:/workspace"

COPY entrypoint.sh /opt/dagster/
RUN chmod +x /opt/dagster/entrypoint.sh
ENTRYPOINT ["/opt/dagster/entrypoint.sh"]
