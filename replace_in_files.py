import logging
import os
import sys
from re import sub


class Replacer:
    logger = logging.getLogger(__name__)

    def replace_string_in_files(self, dirname, src, dest):
        if dirname is None or src is None or dest is None:
            self.logger.info('invalid arguments to replace function: path=%s, src=%s, dest=%s', dirname, src, dest)
            return

        for root, subFolder, files in os.walk(dirname):
            for item in files:
                if item.endswith('.py'):
                    file_path = os.path.join(root, item)
                    self.logger.info('replace "%s" to "%s" in %s', src, dest, file_path)
                    self.filereplace(file_path, src, dest)

    def filereplace(self, filename, regexToReplace, replacementString):
        a = open(filename, 'r+')
        file_content = a.read()
        a.seek(0)
        a.write(sub(regexToReplace, replacementString, file_content))
        a.close()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Invalid arguments. Expected: ' + os.path.basename(__file__) + ' <path> <src> <dest>')
        exit(1)

    Replacer().replace_string_in_files(sys.argv[1], sys.argv[2], sys.argv[3])
