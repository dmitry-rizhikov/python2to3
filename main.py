import logging
import sys

from diff_files import Diff
from utils import Utils
from run_futurize import Futurize
from run_pylint import Pylint

if __name__ == '__main__':
    path_utils = Utils()

    pylint2 = Pylint('venv2/bin/pylint')

    pylint3 = Pylint('venv/bin/pylint')

    diff = Diff()

    futurize = Futurize()

    logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    path = '/home/dmitry/zeev-stxnet/Tools_new'
    exclude = ['External', 'AutoTestVW/VWAutomatedTesting/WorkspaceEnum/Lib']

    path_utils.add_folders_to_path(dirname=path, exclude_dirs=exclude)

    pylint2.run_pylint(dirname=path, out_file='pylint2_old.txt', exclude_dirs=exclude)

    futurize.run_futurize(dirname=path, out_file='futurize.txt', exclude_dirs=exclude)

    futurize.validate_output(file='futurize.txt')

    pylint2.run_pylint(dirname=path, out_file='pylint2_new.txt', exclude_dirs=exclude)

    diff.diff_files(from_file='pylint2_old.txt', to_file='pylint2_new.txt', out_file='pylint2_diff.txt')

    pylint3.run_pylint(dirname=path, out_file='pylint3_new.txt', exclude_dirs=exclude)

    diff.diff_files(from_file='pylint2_new.txt', to_file='pylint3_new.txt', out_file='pylint3_diff.txt')
    
