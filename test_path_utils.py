import logging
import os
import shutil
import sys
from unittest import TestCase

from diff_files import Diff
from utils import Utils
from run_futurize import Futurize
from run_pylint import Pylint


class Test(TestCase):
    path_utils = Utils()

    pylint2 = Pylint('venv2/bin/pylint')

    pylint3 = Pylint('venv/bin/pylint')

    diff = Diff()

    futurize = Futurize()

    logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    @classmethod
    def setUpClass(cls):
        shutil.rmtree('folder', ignore_errors=True)

        # create folder structure
        path1 = 'folder/subfolder1/xxx'
        path2 = 'folder/subfolder2/yyy'
        os.makedirs(path1)
        os.makedirs(path2)

        with open("folder/file1.py", "w") as file:
            file.write("file1")
        with open(path1 + "/file2.py", "w") as file:
            file.write("file2")

    def test_complete_scenario(self):
        self.path_utils.add_folders_to_path(dirname='folder', exclude_dirs=[])

        self.assertIsNotNone(sys.path.index('folder'))
        self.assertIsNotNone(sys.path.index('folder/subfolder1'))
        self.assertIsNotNone(sys.path.index('folder/subfolder2'))
        self.assertIsNotNone(sys.path.index('folder/subfolder1/xxx'))
        self.assertIsNotNone(sys.path.index('folder/subfolder2/yyy'))

        self.pylint2.run_pylint(dirname='folder', out_file='pylint2_old.txt', exclude_dirs=[])

        self.assertGreater(os.path.getsize('pylint2_old.txt'), 0)

        self.futurize.run_futurize(dirname='folder', exclude_dirs=[], out_file='futurize.txt')

        self.pylint2.run_pylint(dirname='folder', out_file='pylint2_new.txt', exclude_dirs=[])

        self.assertGreater(os.path.getsize('pylint2_new.txt'), 0)

        self.diff.diff_files(from_file='pylint2_old.txt', to_file='pylint2_new.txt', out_file='pylint2_diff.txt')

        self.assertGreater(os.path.getsize('pylint2_diff.txt'), 0)

        self.pylint3.run_pylint(dirname='folder', out_file='pylint3_new.txt', exclude_dirs=[])

        self.diff.diff_files(from_file='pylint2_new.txt', to_file='pylint3_new.txt', out_file='pylint3_diff.txt')

        self.assertGreater(os.path.getsize('pylint3_diff.txt'), 0)
