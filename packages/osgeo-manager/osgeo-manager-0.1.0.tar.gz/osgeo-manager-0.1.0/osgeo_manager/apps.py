from django.apps import AppConfig

from .constants import DOWNLOADS_DIR_PATH, TEMP_DIR_PATH
from .os_utils import create_direcotry

create_direcotry(TEMP_DIR_PATH)
create_direcotry(DOWNLOADS_DIR_PATH)


class OSGEOManagerConfig(AppConfig):
    name = 'osgeo_manager'
    verbose_name = "osgeo_manager"
