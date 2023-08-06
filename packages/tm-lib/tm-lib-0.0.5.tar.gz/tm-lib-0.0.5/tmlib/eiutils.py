import functools

from mongoengine import DoesNotExist

from bson import json_util


def toJson(data):
    """Convert Mongo object(s) to JSON"""
    return json_util.dumps(data)


"""
Decorators
"""


def get_or_404(fn):
    """
    404 as response if document doesn't exists
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except DoesNotExist:
            return "Does not exists", 404
    return wrapper
