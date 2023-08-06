"""
author: arun.rs
21st September 2018
"""
import os

from logging.config import dictConfig
#Logs absoulte location
LOG_PATH = '/logs/'
#Logs Generic settings
LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
                    'standard': {'format': "%(asctime)s|%(levelname)s|%(module)s|%(lineno)s|%(funcName)s|%(message)s"},
                    'trace': {'format': "%(asctime)s|%(message)s"}
                  },

    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },

    'loggers': {
                }
}
#Module wise logs settings
LOG_SETTINGS['handlers']['application'] = {
    'class': 'cloghandler.ConcurrentRotatingFileHandler',
    'level': 'DEBUG',
    'formatter': 'standard',
    'filename': os.path.join(LOG_PATH, 'application.log'),
    'mode': 'a',
    'maxBytes': 104857600,
    'backupCount': 5,
}

LOG_SETTINGS['loggers']['application'] = {
    'handlers': [ 'application'],
    'formatter': 'standard',
    'level': 'DEBUG',
    'propagate': False
}

LOG_SETTINGS['handlers']['trace'] = {
    'class': 'cloghandler.ConcurrentRotatingFileHandler',
    'level': 'DEBUG',
    'formatter': 'trace',
    'filename': os.path.join(LOG_PATH, 'trace.log'),
    'mode': 'a',
    'maxBytes': 104857600,
    'backupCount': 5,
}

LOG_SETTINGS['loggers']['trace'] = {
    'handlers': ['trace'],
    'formatter': 'trace',
    'level': 'DEBUG',
    'propagate': False
}

dictConfig(LOG_SETTINGS)

