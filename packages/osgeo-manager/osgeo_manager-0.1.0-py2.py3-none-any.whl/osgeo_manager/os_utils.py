import os
import time
from uuid import uuid4

from log import get_logger

logger = get_logger(__name__)
WORLD_PERMISSION = 0o777
USER_GROUP_PERMISSION = 0o775


def create_direcotry(path, mode=WORLD_PERMISSION):
    # please read the following section
    # https://docs.python.org/2/library/os.html#mkdir-modebits
    if not os.path.exists(path):
        try:
            previous_mask = os.umask(0)
            os.makedirs(path, mode=mode)
        except OSError as e:
            logger.error(e.message)
        finally:
            # set the previous mask back
            os.umask(previous_mask)


def get_new_dir(base_dir=None):
    if not base_dir:
        from .constants import TEMP_DIR_PATH
        base_dir = TEMP_DIR_PATH
    rand_str = uuid4().__str__().replace('-', '')[:8]
    timestr = time.strftime("%Y/%m/%d/%H/%M/%S")
    target = os.path.join(base_dir, timestr, rand_str)
    create_direcotry(target)
    return target
