import dagstermill,sys

class logger:
    def info(*args):
        if (dagstermill.get_context()).logging_tags['pipeline'] == 'ephemeral_dagstermill_pipeline':
            print(*args)
        else:
            (dagstermill.get_context()).log.info(" ".join(str(s) for s in args))
    def error(*args):
        if (dagstermill.get_context()).logging_tags['pipeline'] == 'ephemeral_dagstermill_pipeline':
            print(*args, file=sys.stderr)
        else:
            (dagstermill.get_context()).log.error(" ".join(str(s) for s in args))

logger.info("Dagyter Loaded ! Please user logger.info() and logger.error() instead of print() in  order to see your output both in jupyter and dagster") 
