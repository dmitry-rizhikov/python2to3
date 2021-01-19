import logging
import subprocess

from utils import Utils


class Futurize:
    logger = logging.getLogger(__name__)

    command = 'find %s %s -name "*.py" -exec %s "{}" +'

    futurize_exec = 'venv2/bin/futurize -auwn0 --no-diffs'

    def run_futurize(self, dirname, out_file, exclude_dirs):
        f = open(out_file, 'w')

        command = self.command % (dirname, Utils().join_exclude_dirs(dirs=exclude_dirs, dirname=dirname), self.futurize_exec)
        self.logger.info('executing %s', command)
        pylint_proc = subprocess.Popen(command, stdout=f, stderr=subprocess.STDOUT, shell=True)
        pylint_proc.wait()
        f.close()

    def validate_output(self, file='futurize.txt'):
        with open(file, 'r+') as f:
            for line in f:
                if 'Traceback' in line:
                    raise Exception('Futurize failed. Check output file %s' % file)