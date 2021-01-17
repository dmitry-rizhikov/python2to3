import logging
import subprocess
from migrate.utils import Utils


class Pylint:
    logger = logging.getLogger(__name__)

    args = ['--rcfile=rcfile',
            '--disable=I,R,C,W',
            '--disable=mixed-indentation,bad-indentation,unused-wildcard-import,wildcard-import']

    command = 'find %s %s -name "*.py" -exec %s "{}" +'

    def __init__(self, pylint_exec):
        self.pylint_exec = pylint_exec

    def run_pylint(self, dirname, out_file, exclude_dirs):

        f = open(out_file, 'w')

        command = self.command % (dirname,
                                  Utils().join_exclude_dirs(dirs=exclude_dirs, dirname=dirname),
                                  self.pylint_exec + ' ' + ' '.join(self.args))
        self.logger.info('executing %s', command)
        pylint_proc = subprocess.Popen(command, stdout=f, stderr=subprocess.STDOUT, shell=True)
        pylint_proc.wait()
        f.close()
