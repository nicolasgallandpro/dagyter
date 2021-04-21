from dagster import pipeline, repository, schedule, solid, daily_schedule
import dagstermill as dm
from dagster import ModeDefinition, fs_io_manager, local_file_manager, InputDefinition, Int, OutputDefinition
from dagster.utils import script_relative_path
from datetime import date, time, datetime, timedelta
from functools import reduce
import calendar
import datetime as dt
import toml


#----------------------------- Helpers
def generate_should_execute(schedule_days):
    def check_schedule(scheduleExecutionContext):
        """Analyse the schedule input and return True if the job has to be executed today"""
        def check_one_schedule(schedule):
            if schedule.lower() == 'everyday':
                return True
            if schedule.isdigit():
                day_of_month = dt.datetime.today().day
                return int(schedule) == day_of_month
            if (calendar.day_name[date.today().weekday()]).lower() == schedule.lower():
                return True
            return False 
        schedules = list(map(lambda x: x.strip(), schedule_days.split(',')))
        result = reduce(lambda accu, cur: accu | check_one_schedule(cur), schedules, False )
        return result
    return check_schedule



#----------------------------- Solid
def notebook_solid(solid_name, file_name, *args):
    inputdef = [InputDefinition("i", str)] if len(args)>0 else None
    s = dm.define_dagstermill_solid( \
            solid_name, \
            script_relative_path('/workspace/'+file_name),\
            required_resource_keys={'file_manager'},\
            output_defs=[OutputDefinition(str)],
            input_defs=inputdef
            )
    return s(*args)

#-------------------------- Pipelines
def create_pipeline(name, conf):
    days = conf["schedule_days"] if "schedule_days" in conf else None
    _time = conf["time"] if 'time' in conf else None
    hour = int((_time.split(':'))[0]) if _time else 6
    minute = int((_time.split(':'))[1]) if _time else 0
    should_execute = generate_should_execute(days) if days else lambda x:True 
    

    @pipeline(
        name=name,
        mode_defs=[
            ModeDefinition(
                resource_defs={"io_manager": fs_io_manager, "file_manager": local_file_manager}
            )
        ]
    )
    def pipeline_func():
        previous = None
        for notebook in conf["notebooks"]:
            name = ((notebook.split('/'))[-1]).replace('.ipynb','')
            if previous:
                step = notebook_solid(name, notebook, previous)
            else :
                step = notebook_solid(name, notebook)
            previous = step
    
    @daily_schedule(
        name="sched_"+name,
        pipeline_name=name,
        should_execute=should_execute,
        start_date=datetime(2020, 1, 1),
        execution_timezone="Europe/Paris",
        execution_time= time(hour=hour, minute=minute, second=0, microsecond=0)
    )
    def schedule_func(_context):
        return {}
    return [pipeline_func,schedule_func]


#-------------------- repository
@repository
def notebooks_repository():
    pipelines = toml.loads(open("/workspace/schedul.toml",'r').read())
    out = []
    for pip in pipelines:
        pipeline,schedule = create_pipeline(pip, pipelines[pip])
        out.append(pipeline)
        out.append(schedule)
    return out
