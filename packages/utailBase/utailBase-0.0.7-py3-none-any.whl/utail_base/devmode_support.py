def set_for_run_this_singular(logFilePath):
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
    os.chdir(parent_path)

    import utail_base
    import logging
    # setup logging
    utail_base.setup_logging(default_level=logging.INFO)
    utail_base.setup_logging_root(loggingLv=logging.DEBUG, filePath=logFilePath)

