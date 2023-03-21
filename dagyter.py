from dagstermill import define_dagstermill_asset, local_output_notebook_io_manager
from dagster import asset, AssetIn, AssetKey, Definitions, define_asset_job, ScheduleDefinition
import pandas as pd, numpy as np
from dagster.utils import script_relative_path
import toml
try:
    from jupyter_notebook_parser import JupyterNotebookParser
    notebookparser = True
except:
    notebookparser = False

#----------------------------- helpers
standard_dagster_name = lambda name:name.replace('-','_').replace(' ', '_')
asset_name_from_file_name = lambda f : standard_dagster_name(((f.split('/'))[-1]).replace('.ipynb',''))

def dag_conf_to_dependencies(conf):
    """take the toml conf of the dag and create a dependency object of this form:
    {'first_step.ipynb': [], 'second_step.ipynb': ['first_step.ipynb'], 'third_step.ipynb': ['second_step.ipynb']}"""
    dependencies = {}
    #step 1 : list all dependencies
    for line in conf['dag'].split('\n'): 
        line = line.strip()
        if line == '':
            continue
        previous = None
        for node_file in line.split('>>'):
            node_file = node_file.strip()
            if node_file not in dependencies:
                dependencies[node_file] = []
            if previous != None:
                (dependencies[node_file]).append(previous)
            previous = node_file
    return dependencies


#----------------------------- asset
def create_notebook_asset(asset_name, file_path, group_name, _ins=[]):
    """Create an asset from a notebook. _ins are input assets"""
    #print(file_name, asset_name, group_name)
    full_path = script_relative_path('/workspace/'+file_path)
    ins = {}
    for _in in _ins:
        dep_name = asset_name_from_file_name(_in)
        ins[dep_name] = AssetIn(key=AssetKey(dep_name)) 
    #print(asset_name)
    if notebookparser:
        cells = JupyterNotebookParser(full_path).get_markdown_cells() 
        description = '' if len(cells)==0 else ''.join(cells[0]['source'])
    else:
        description = 'No description markdown cell'
    return define_dagstermill_asset(
        name=asset_name,
        notebook_path=full_path,
        group_name=group_name,
        key_prefix=group_name,
        description=description,
        ins=ins)


#----------------------------- group
def create_group(name, conf, timezone):
    time = conf["time"] if "time" in conf else '6:00'
    (hour,minutes) = time.split(':')
    day_of_week = conf['day_of_week'] if 'day_of_week' in conf else '*'
    week_days = ['sunday','monday','tuesday','wednesday','thursday', 'friday','saturday','sunday']
    day_of_week = ','.join(list(map(lambda d: '*' if d=='*' else str(week_days.index(d.lower().strip())), day_of_week.split(','))))
    day_of_month = str(conf['day_of_month']) if 'day_of_month' in conf else '*'
    day_of_month = ','.join(list(map(lambda d:d.strip(), day_of_month.split(','))))

    dependencies = dag_conf_to_dependencies(conf)
    assets = []
    asset_names = []
    for file_name in dependencies:
        directory = conf['directory'] if 'directory' in conf else '.'
        directory = directory if directory[-1] == '/' else directory + '/'
        asset_name = asset_name_from_file_name(file_name)
        asset_names.append(name+'/'+asset_name)
        file_path = directory + file_name
        assets.append(create_notebook_asset(asset_name, file_path, name, dependencies[file_name]))

    job = define_asset_job(name=name, selection=asset_names)
    schedule = ScheduleDefinition(job=job, cron_schedule=f"{minutes} {hour} {day_of_month} * {day_of_week}")  
    return {'assets':assets,'jobs':[job],'schedules':[schedule]}

#----------------------------- definitions
def create_definitions(file):
    entries = toml.loads(open(file,'r').read())
    assets = []
    schedules = []
    jobs = []
    timezone = 'Etc/GMT'
    #for each group defined in the toml file
    for entry_name in entries:
        #if it's a global conf
        if entry_name.lower() == 'timezone':
            timezone = entries[entry_name]
            continue
        
        #else, it's a group
        print('----------- group:', entry_name)
        definitions = create_group(standard_dagster_name(entry_name), entries[entry_name], timezone)
        assets += definitions['assets']
        schedules += definitions['schedules']
        jobs += definitions['jobs']
    return Definitions(
        assets=assets,
        schedules=schedules,
        jobs=jobs,
        resources={  "output_notebook_io_manager": local_output_notebook_io_manager    })