"""
author: arun.rs
created: 10th October 2018
"""
import logging.config
from trace_request import TraceRequest
from logger_settings import LOG_SETTINGS

class Logger(logging.LoggerAdapter):
    """
    :summary:
    """
    def __init__(self, logger):
        """
        :summary: Initiallizes the logger with the supplied log name
        :param logger: Logger name
        """
        self.logger = logger

    def process(self, msg, kwargs):
        """
        :summary: Overrides the default process method to append UUID to the logs
        :param msg: Message to be logger
        :param kwargs: Keyword arguments
        :return: Message with the request id and msg data
        """
        return '%s|%s' % (TraceRequest().get_trace_id(), msg), kwargs

class CustomLogger(object):
    """
    :summary: Custom logger with the supplied log settings
    """
    def __init__(self, log_setting=None):
        """
        :summary: Initiallizes logging module with the value passed, else sets default log settings
        :param log_setting: Logging settings
        :return: None
        """
        if log_setting:
            logging.config.dictConfig(log_setting)
        # else:
            # logging.basicConfig(filename='/logs/default.log', level=logging.DEBUG)
            # logging.config.dictConfig(LOG_SETTINGS)

    def get_logger(self, logger_val):
        """
        :summary: Validates the logger_instance and returns the same
        :param logger_val: Logger Value
        :return: Logger Instance
        """
        if isinstance(logger_val, str):
            logger_instance = logging.getLogger(logger_val)
        elif isinstance(logger_val, logging.LoggerAdapter):
            logger_instance = logger_val.logger
        elif isinstance(logger_val, logging.Logger):
            logger_instance = logger_val
        else:
            raise ValueError("Invalid Input")
        return Logger(logger_instance)

    def renew_request_id(self, value=None):
        """
        :summary: Renews the request id
        :param value: Sets the value as request id
        :return: None
        """
        if value:
            TraceRequest().set_trace_id(value)
        else:
            TraceRequest().get_trace_id(renew=True)
