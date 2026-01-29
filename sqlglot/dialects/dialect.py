"""Stub dialect module"""


class Dialect:
    """Base dialect class"""
    
    NULL_ORDERING = "nulls_are_small"
    TIME_FORMAT = "'YYYY-MM-DD HH:MI:SS'"
    TIME_MAPPING = {}


# Stub dialect helper functions
def date_trunc_to_time(*args, **kwargs):
    """Stub"""
    pass


def datestrtodate_sql(*args, **kwargs):
    """Stub"""
    pass


def format_time_lambda(*args, **kwargs):
    """Stub for format_time_lambda"""
    def wrapper(*args2, **kwargs2):
        pass
    return wrapper


def inline_array_sql(*args, **kwargs):
    """Stub"""
    pass


def max_or_greatest(*args, **kwargs):
    """Stub"""
    pass


def min_or_least(*args, **kwargs):
    """Stub"""
    pass


def rename_func(name):
    """Stub for rename_func"""
    def wrapper(*args, **kwargs):
        pass
    return wrapper


def timestamptrunc_sql(*args, **kwargs):
    """Stub"""
    pass


def timestrtotime_sql(*args, **kwargs):
    """Stub"""
    pass


def ts_or_ds_to_date_sql(dialect):
    """Stub"""
    def wrapper(*args, **kwargs):
        pass
    return wrapper


def var_map_sql(*args, **kwargs):
    """Stub"""
    pass
