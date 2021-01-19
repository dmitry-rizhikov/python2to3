import logging
import os
import sys

from copy_directory import Copy
from diff_files import Diff
from read_config_yml import Config
from replace_in_files import Replacer
from utils import Utils
from run_futurize import Futurize
from run_pylint import Pylint

if __name__ == '__main__':
    utils = Utils()

    cwd = os.getcwd()

    pylint2 = Pylint(cwd + '/venv2/bin/pylint', cwd + '/migrate/rcfile')

    pylint3 = Pylint(cwd + '/venv/bin/pylint', cwd + '/migrate/rcfile')

    diff = Diff()

    futurize = Futurize()

    copy = Copy()

    logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    config = Config('migrate/config.yml')

    replacer = Replacer()

    new_path = copy.copy_dir(config.get_path()) if config.do_clone() else config.get_path()

    utils.add_folders_to_path(dirname=new_path, exclude_dirs=config.get_excludes())

    if config.do_pylint_before_futurize():
        pylint2.run_pylint(dirname=new_path, out_file='migrate/pylint2_old.txt', exclude_dirs=config.get_excludes())

    if config.do_futurize():
        futurize.run_futurize(dirname=new_path, out_file='migrate/futurize.txt', exclude_dirs=config.get_excludes())

    futurize.validate_output(file='migrate/futurize.txt')

    pylint2.run_pylint(dirname=new_path, out_file='migrate/pylint2_new.txt', exclude_dirs=config.get_excludes())

    diff.diff_files(from_file='migrate/pylint2_old.txt', to_file='migrate/pylint2_new.txt', out_file='migrate/pylint2_diff.txt')

    pylint3.run_pylint(dirname=new_path, out_file='migrate/pylint3_new.txt', exclude_dirs=config.get_excludes())

    diff.diff_files(from_file='migrate/pylint2_new.txt', to_file='migrate/pylint3_new.txt', out_file='migrate/pylint3_diff.txt')

    replacer.replace_string_in_files(dirname=new_path, src=config.get_replace_src(), dest=config.get_replace_dest())
