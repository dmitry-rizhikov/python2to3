import logging
from datetime import datetime
from distutils.dir_util import copy_tree


class Copy:
    logger = logging.getLogger(__name__)

    def copy_dir(self, src_path):
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("-%d-%m-%Y-%H-%M-%S-%f")

        dest_path = src_path + timestampStr
        self.logger.info('clonning %s to %s',src_path, dest_path)
        copy_tree(src_path, dest_path, preserve_symlinks=1, preserve_mode=0)
        return dest_path
