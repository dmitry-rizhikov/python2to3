import logging
import os
import sys


class Utils:
    logger = logging.getLogger(__name__)

    def get_subfolders(self, dirname):
        if os.path.isdir(dirname):
            subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
            for dirname in subfolders:
                subfolders.extend(self.get_subfolders(dirname))
                self.logger.info('scanning path %s', dirname)

            return subfolders
        else:
            logging.info('invalid path %s', dirname)
            return None

    def add_folders_to_path(self, dirname):
        folders = self.get_subfolders(dirname)

        if folders is not None:
            folders.append(dirname)
            for subfolder in list(folders):
                self.logger.info('appending to system path %s', subfolder)
                sys.path.append(subfolder)

    def join_exclude_dirs(self, dirs, dirname):
        result = ''
        separator = '/'
        if not dirs is None and isinstance(dirs, list):
            for directory in dirs:
                if not str(directory).startswith(dirname):
                    if str(dirname).endswith('/') or str(directory).startswith('/'):
                        separator = ''
                    directory = dirname + separator + directory
                result += ' -path %s -prune -o' % directory

        return result
