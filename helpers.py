import logging, os, sys

def setup_logging(log_filename):

    if os.path.dirname(log_filename):
        os.system("mkdir -p " + os.path.dirname(log_filename))

    logFormatter = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)
    
    fileHandler = logging.FileHandler(log_filename + ".log", mode='w')
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.INFO)
    rootLogger.addHandler(fileHandler)
    
    fileHandler_debug = logging.FileHandler(log_filename + ".debug.log", mode='w')
    fileHandler_debug.setFormatter(logFormatter)
    fileHandler_debug.setLevel(logging.DEBUG)
    rootLogger.addHandler(fileHandler_debug)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    rootLogger.addHandler(consoleHandler)

    rootLogger.info("Logging setup")

def get_class_dir(obj):
    dir = os.path.dirname(os.path.abspath(sys.modules[obj.__class__.__module__].__file__))
    return dir