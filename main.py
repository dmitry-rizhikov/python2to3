import logging
import sys

from copy_directory import Copy
from diff_files import Diff
from read_config_yml import Config
from utils import Utils
from run_futurize import Futurize
from run_pylint import Pylint

if __name__ == '__main__':
    utils = Utils()

    pylint2 = Pylint('venv2/bin/pylint')

    pylint3 = Pylint('venv/bin/pylint')

    diff = Diff()

    futurize = Futurize()
    
    copy = Copy()

    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    
    config = Config('config.yml')

    new_path = copy.copy_dir(config.get_path()) if config.do_clone() else config.get_path()

    utils.add_folders_to_path(dirname=new_path, exclude_dirs=config.get_excludes())

    pylint2.run_pylint(dirname=new_path, out_file='pylint2_old.txt', exclude_dirs=config.get_excludes())

    futurize.run_futurize(dirname=new_path, out_file='futurize.txt', exclude_dirs=config.get_excludes())

    futurize.validate_output(file='futurize.txt')

    pylint2.run_pylint(dirname=new_path, out_file='pylint2_new.txt', exclude_dirs=config.get_excludes())

    diff.diff_files(from_file='pylint2_old.txt', to_file='pylint2_new.txt', out_file='pylint2_diff.txt')

    pylint3.run_pylint(dirname=new_path, out_file='pylint3_new.txt', exclude_dirs=config.get_excludes())

    diff.diff_files(from_file='pylint2_new.txt', to_file='pylint3_new.txt', out_file='pylint3_diff.txt')
