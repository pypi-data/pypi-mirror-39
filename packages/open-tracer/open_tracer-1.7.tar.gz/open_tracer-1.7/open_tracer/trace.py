"""
author: arun.rs
created: 26th October 2018
"""

from datetime import datetime
from functools import wraps
from logger import CustomLogger

TRACER = CustomLogger().get_logger('trace')

def message(operation, type, resource, execution_time, status):
    """
    :summary: Concats the supplied parameters and returns them in trace format
    :param operation: Operation (MySQL/ Mongo/ ES/ API/ etc)
    :param type: Type of the Operation (SELECT/ GET/ POST/ etc)
    :param resource: URL / Query / Function name
    :param execution_time: Time taken to perform that operation
    :param status: Success or Failure
    :return: Concatinated string
    """
    return "%s|%s|%s|%s|%s" % (operation, type, resource, execution_time, status)

def execution_time(start_time, end_time):
    """
    :summary: Difference of supplied time in seconds
    :param start_time: Start time
    :param end_time: End time
    :return: Difference of supplied time in seconds
    """
    return str(((end_time-start_time).total_seconds()) * 1000)

def trace_resource(operation, type, resource, start_time, end_time, status):
    """
    :summary: Logs the information required to trace the application
    :param operation: Operation (Mysql/ Mongo/ ES/ API/ etc)
    :param type: Type of the Operation (GET/ POST/ SELECT/ INSERT/ etc)
    :param resource: URL / Query / Function name
    :param start_time: Start time of the operation
    :param end_time: End time of the operation
    :param status: Success / Failure
    :return: None
    """
    TRACER.info(message(operation, type, resource, execution_time(start_time, end_time), status))

def trace(operation, type):
    """
    :summary: Wrapper function to trace a method
    :param operation: Operation (Mysql/ Mongo/ ES/ API/ etc)
    :param type: Type of the Operation (GET/ POST/ SELECT/ INSERT/ etc)
    :return: Traced functions response
    """
    def trace(func):
        @wraps(func)
        def trace(*args, **kwargs):
            start_time = datetime.now()
            status = True
            try:
                return func(*args, **kwargs)
            except Exception as e:
                status = False
            finally:
                end_time = datetime.now()
                trace_resource(operation, type, func.__name__, start_time, end_time, status)
        return trace
    return trace


