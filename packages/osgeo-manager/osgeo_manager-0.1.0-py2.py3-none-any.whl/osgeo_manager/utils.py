# -*- coding: utf-8 -*-
import collections

import requests
from requests.auth import HTTPBasicAuth

from geonode.geoserver.helpers import (get_store, gs_catalog,
                                       ogc_server_settings)

from .constants import DEFAULT_WORKSPACE, PG_REGEX
from .log import get_logger

logger = get_logger(__name__)


def get_sld_body(url):
    req = requests.get(
        url,
        auth=HTTPBasicAuth(ogc_server_settings.credentials[0],
                           ogc_server_settings.credentials[1]))
    return req.text


def get_gs_store(storename=None,
                 workspace=DEFAULT_WORKSPACE):
    if not storename:
        storename = ogc_server_settings.datastore_db.get('NAME', None)
    return get_store(gs_catalog, storename, workspace)


def get_store_schema(storename=None):
    if not storename:
        storename = ogc_server_settings.datastore_db['NAME']
    store = get_store(gs_catalog, storename, DEFAULT_WORKSPACE)
    return store.connection_parameters.get('schema', 'public')


def unicode_converter(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(unicode_converter, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(unicode_converter, data))
    else:
        return data


def urljoin(*args):
    return "/".join(map(lambda x: str(x).rstrip('/'), args))


def read_in_chunks(obj, chunk_size=2048):
    if isinstance(obj, file):
        while True:
            data = obj.read(chunk_size)
            if not data:
                break
            yield data
    else:
        for i in xrange(0, len(obj), chunk_size):
            yield obj[i:i + chunk_size]


def is_postgres_source(source_path):
    return PG_REGEX.match(source_path)
