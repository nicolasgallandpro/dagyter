from dagster import pipeline, repository, schedule, solid, daily_schedule
import dagstermill as dm
from dagster import ModeDefinition, fs_io_manager, local_file_manager, InputDefinition, Int, OutputDefinition
from dagster.utils import script_relative_path
from datetime import date, time, datetime, timedelta
from functools import reduce
import calendar
import datetime as dt
import toml

standard_dagster_name = lambda name:name.replace('-','_').replace(' ', '_')

#----------------------------- Solid
def notebook_solid(solid_name, file_name, *args):
    inputdef = list(map(lambda x:InputDefinition("i", list),args))
    s = dm.define_dagstermill_solid( \
            solid_name, \
            script_relative_path('/workspace/'+file_name),\
            required_resource_keys={'file_manager'},\
            output_defs=[OutputDefinition(str)],
            input_defs=inputdef
            )
    return s(*args)


def create_pipeline(name, conf, timezone):
    time = conf["time"] if "time" in conf else '6:00'
    (hour,minutes) = time.split(':')
    day_of_week = conf['day_of_week'] if 'day_of_week' in conf else '*'
    week_days = ['sunday','monday','tuesday','wednesday','thursday', 'friday','saturday','sunday']
    day_of_week = ','.join(list(map(lambda d: '*' if d=='*' else str(week_days.index(d.lower().strip())), day_of_week.split(','))))
    day_of_month = str(conf['day_of_month']) if 'day_of_month' in conf else '*'
    day_of_month = ','.join(list(map(lambda d:d.strip(), day_of_month.split(','))))
    
    @pipeline(
        name=name,
        mode_defs=[
            ModeDefinition(
                resource_defs={"io_manager": fs_io_manager, "file_manager": local_file_manager}
            )
        ]
    )
    def pipeline_func():
        node_name_from_file_name = lambda f : standard_dagster_name(((f.split('/'))[-1]).replace('.ipynb',''))
        dependencies = {}

        #step 1 : list all dependencies
        #for each branch defined for the dag (one line == one branch)
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

        #step 2 : create solids
        already_created = {}
        len_nodes = []
        trace = []
        def get_solid_and_dependencies(node_file):
            len_nodes.append('.')
            if len(len_nodes) > 1000:
                raise Exception("More than 1000 nodes created. Cyclic dependency ?")
            if node_file in already_created:
                return already_created[node_file]
            node_name = node_name_from_file_name(node_file)
            directory = conf['directory'] if 'directory' in conf else '.'
            directory = directory if directory[-1] == '/' else directory + '/'
            if len(dependencies[node_file]) == 0:
                node = notebook_solid(node_name, directory + node_file)
            else:
                deps = list(map(lambda d:get_solid_and_dependencies(d), dependencies[node_file]))
                node = notebook_solid(node_name, directory + node_file, deps) 
            already_created[node_file] = node
            return node

        for node_file in dependencies:
            get_solid_and_dependencies(node_file)

    @schedule(
        name="sched_"+name,
        pipeline_name=name,
        cron_schedule=f"{minutes} {hour} {day_of_month} * {day_of_week}",
        execution_timezone=timezone,
    )
    def schedule_func(_context):
        return {}
    return [pipeline_func,schedule_func]


#-------------------- repository
@repository
def notebooks_repository():
    entries = toml.loads(open("/workspace/pipelines_and_scheduling.toml",'r').read())
    out = []
    timezone = 'Etc/GMT'

    #for each pipeline defined in the toml file
    for entry_name in entries:
        #if it's a global conf
        if entry_name.lower() == 'timezone':
            timezone = entries[entry_name]
            continue
        
        #else, it's a pipeline
        pipeline,schedule = create_pipeline(standard_dagster_name(entry_name), entries[entry_name], timezone)
        out.append(pipeline)
        out.append(schedule)
    return out
