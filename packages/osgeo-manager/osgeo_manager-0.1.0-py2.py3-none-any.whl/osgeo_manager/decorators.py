# -*- coding: utf-8 -*-
from datetime import datetime
from .exceptions import FormatException
from .constants import FORMAT_EXT
from .config import LayerConfig
from .exceptions import ConfigurationException


def ensure_supported_format(func):
    def wrap(*args, **kwargs):
        format = kwargs.get('target_format', 'GPKG')
        if format in FORMAT_EXT.keys():
            return func(*args, **kwargs)
        else:
            raise FormatException("Unsupported Format")

    return wrap


def validate_config(config_obj=None):
    if not config_obj:
        config_obj = LayerConfig()
    if not isinstance(config_obj, LayerConfig):
        raise ConfigurationException(
            "Configuration object should be instance of LayerConfig")
    return config_obj


def time_it(function):
    def wrap(request, *args, **kwargs):
        start = datetime.now()
        result = function(request, *args, **kwargs)
        end = datetime.now()
        print("{} took ------>{} seconds".format(
            function.__name__, (end - start).total_seconds()))
        print("{} took ------>{} milliseconds".format(
            function.__name__, (end - start).total_seconds() * 1000))
        return result

    return wrap
