# -*- coding: utf-8 -*-
import re
from collections import namedtuple

from django.conf import settings
from slugify import Slugify
import os

FORMAT_EXT = {
    "GPKG": '.gpkg',
    "KML": '.kml',
    "GeoJSON": '.json',
    "GML": '.gml',
    "GPX": '.gpx',
    "GPSTrackMaker": ".gmt",
    "ESRI Shapefile": ".shp"
}
PG_REGEX = re.compile(r"^\s?PG:\s?.*$")
WORLD_PERMISSION = 0o777
USER_GROUP_PERMISSION = 0o775
DEFAULT_WORKSPACE = settings.DEFAULT_WORKSPACE
SLUGIFIER = Slugify(separator='_')
STYLES_TABLE = "layer_styles"
ICON_REL_PATH = "workspaces/{}/styles".format(DEFAULT_WORKSPACE)
LayerPostgisOptions = namedtuple(
    'LayerPostgisOptions', ['skipfailures', 'overwrite', 'append', 'update'])
POSTGIS_OPTIONS = LayerPostgisOptions(True, True, False, False)
TEMP_DIR_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'tmp_generator')
DOWNLOADS_DIR_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'downloads')
