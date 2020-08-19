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

    def add_folders_to_path(self, dirname, exclude_dirs):
        folders = self.get_subfolders(dirname)

        if folders is not None:
            folders.append(dirname)
            for subfolder in list(folders):
                if self.is_not_empty(exclude_dirs) \
                        and self.join_path(local_path=subfolder, absolut_path=dirname) in exclude_dirs:
                    continue

                self.logger.info('appending to system path %s', subfolder)
                sys.path.append(subfolder)

    def is_not_empty(self, dir_list):
        return not dir_list is None and isinstance(dir_list, list)

    def join_exclude_dirs(self, dirs, dirname):
        result = ''
        if self.is_not_empty(dirs):
            for directory in dirs:
                if not str(directory).startswith(dirname):
                    directory = self.join_path(directory, dirname)
                result += ' -path %s -prune -o' % directory

        return result

    def join_path(self, local_path, absolut_path):
        separator = '/'
        if not str(absolut_path).endswith(separator) and not str(local_path).startswith(separator):
            return absolut_path + separator + local_path
        return absolut_path + local_path
