"""
author: arun.rs
21st September 2018
"""
import uuid

class TraceRequest(object):
    """
    Maintains a UID for every application request
    """
    __trace_id = ""
    __parent_id = ""
    __child_id = ""

    def __init__(self):
        pass

    def get_trace_id(self, renew=False):
        """
        :Brief: This method is used in every place to get the already generated request ID or
        generate new request ID and sent off
        """
        if not TraceRequest.__trace_id or renew:
            self.set_trace_id(str(uuid.uuid1()))
        return TraceRequest.__trace_id + "|" + TraceRequest.__parent_id + "|" + TraceRequest.__child_id

    def set_trace_id(self, trace_id, parent_id="", child_id=""):
        """
        :Brief: This method is used by entry points where the incoming HTTP request has the
        request ID in its headers
        """
        TraceRequest.__trace_id = trace_id
        TraceRequest.__parent_id = parent_id
        TraceRequest.__child_id = child_id

    def get_root_id(self):
        """
        :summary:
        :return:
        """
        return TraceRequest.__trace_id

    def get_parent_id(self):
        """

        :return:
        """
        return TraceRequest.__parent_id

    def get_child_id(self):
        """
        :summary:
        :return:
        """
        return TraceRequest.__child_id

    def get_all_ids(self):
        """

        :return:
        """
        if not TraceRequest.__trace_id:
            self.set_trace_id(str(uuid.uuid1()))
        return TraceRequest.__trace_id, TraceRequest.__parent_id, TraceRequest.__child_id
