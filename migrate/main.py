import logging
import sys

from copy_directory import Copy
from diff_files import Diff
from migrate.read_config_yml import Config
from migrate.replace_in_files import Replacer
from migrate.utils import Utils
from migrate.run_futurize import Futurize
from migrate.run_pylint import Pylint

if __name__ == '__main__':
    utils = Utils()

    pylint2 = Pylint('venv2/bin/pylint')

    pylint3 = Pylint('venv/bin/pylint')

    diff = Diff()

    futurize = Futurize()

    copy = Copy()

    logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    config = Config('../config.yml')

    replacer = Replacer()

    new_path = copy.copy_dir(config.get_path()) if config.do_clone() else config.get_path()

    utils.add_folders_to_path(dirname=new_path, exclude_dirs=config.get_excludes())

    if config.do_pylint_before_futurize():
        pylint2.run_pylint(dirname=new_path, out_file='../pylint2_old.txt', exclude_dirs=config.get_excludes())

    if config.do_futurize():
        futurize.run_futurize(dirname=new_path, out_file='../futurize.txt', exclude_dirs=config.get_excludes())

    futurize.validate_output(file='../futurize.txt')

    pylint2.run_pylint(dirname=new_path, out_file='../pylint2_new.txt', exclude_dirs=config.get_excludes())

    diff.diff_files(from_file='../pylint2_old.txt', to_file='../pylint2_new.txt', out_file='../pylint2_diff.txt')

    pylint3.run_pylint(dirname=new_path, out_file='../pylint3_new.txt', exclude_dirs=config.get_excludes())

    diff.diff_files(from_file='../pylint2_new.txt', to_file='../pylint3_new.txt', out_file='../pylint3_diff.txt')

    replacer.replace_string_in_files(dirname=new_path, src=config.get_replace_src(), dest=config.get_replace_dest())
