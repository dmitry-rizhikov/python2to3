import logging
import os
import sys


class Utils:
    logger = logging.getLogger(__name__)

    def get_subfolders(self, dirname, exclude_dirs):
        if os.path.isdir(dirname):
            subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
            for subfolder in subfolders:
                if not self.is_excluded(subfolder, exclude_dirs, dirname):
                    subfolders.extend(self.get_subfolders(subfolder, exclude_dirs))
                    self.logger.info('scanning path %s', subfolder)

            return subfolders
        else:
            logging.info('invalid path %s', dirname)
            return None
        
    def is_excluded(self, subfolder, exclude_dirs, dirname):
        if self.is_not_empty(exclude_dirs):
            for dir in exclude_dirs:
                if str(subfolder).replace(dirname, '').lstrip('/').startswith(str(dir).rstrip('/')):
                    return True

        return False

    def add_folders_to_path(self, dirname, exclude_dirs):
        folders = self.get_subfolders(dirname, exclude_dirs)

        if folders is not None:
            folders.append(dirname)
            for subfolder in list(folders):
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
