# import os
# import logging
# import logging.config
# import yaml

# def setup_logging(
#     default_path='logging.yaml',
#     default_level=logging.INFO,
#     env_key='LOG_CFG'
# ):
#     """Setup logging configuration

#     """
#     path = default_path
#     value = os.getenv(env_key, None)

#     print(path)

#     if value:
#         path = value
#     if os.path.exists(path):
#         with open(path, 'rt') as f:
#             config = yaml.safe_load(f.read())
#         logging.config.dictConfig(config)
#         print('loaded yaml. path:{}'.format(path))
#     else:
#         logging.basicConfig(level=default_level)
#         print('not found configFile.')


import os
import yaml
import logging.config
import logging
import coloredlogs

def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
        print('loaded yaml. path:{}'.format(path))
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Failed to load configuration file. Using default configs')


def setup_logging_root(loggingLv=logging.DEBUG, filePath=None,handlers=None, fmtParam=None, datefmtParam=None):
    if fmtParam is None:
        fmtParam = '%(levelname)s:%(name)s: %(message)s '
        '(%(asctime)s; %(filename)s:%(lineno)d)'

    if datefmtParam is None:
        datefmtParam = "%Y-%m-%d %H:%M:%S"

    f = logging.Formatter(fmt=fmtParam, datefmt=datefmtParam)

    if handlers is None:
        handlers = [logging.StreamHandler()]

        if filePath is not None:
            handlers.append(
                logging.handlers.RotatingFileHandler(filePath, 
                encoding='utf8',
                maxBytes=100000, backupCount=1)
            )

    log = logging.getLogger()
    log.setLevel(loggingLv)
    for h in handlers:
        h.setFormatter(f)
        h.setLevel(loggingLv)
        log.addHandler(h)