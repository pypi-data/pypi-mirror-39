"""
arun.rs
6th December 2018
"""
import re

def sanitize_urlparams(url):
    """
    :summary: Replace url params with <params> string
    :param url: URL
    :return: Sanitized URL
    """
    return re.sub("\=(.*?)(\&|$)", "=<params>&", url)
