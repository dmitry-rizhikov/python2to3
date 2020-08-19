import logging
import os
import shutil
import sys
from pathlib import Path
from unittest import TestCase

from copy_directory import Copy
from diff_files import Diff
from read_config_yml import Config
from utils import Utils
from run_futurize import Futurize
from run_pylint import Pylint


class Test(TestCase):
    utils = Utils()

    pylint2 = Pylint('venv2/bin/pylint')

    pylint3 = Pylint('venv/bin/pylint')

    diff = Diff()

    futurize = Futurize()

    copy = Copy()

    logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    @classmethod
    def setUpClass(cls):
        for p in Path("test").glob("folder*"):
            shutil.rmtree(p, ignore_errors=True)

        # create folder structure
        path1 = 'test/folder/subfolder1/xxx'
        path2 = 'test/folder/subfolder2/yyy'
        os.makedirs(path1)
        os.makedirs(path2)

        with open("test/folder/file1.py", "w") as file:
            file.write("file1")
        with open(path1 + "/file2.py", "w") as file:
            file.write("file2")

    def test_complete_scenario(self):
        config = Config('test/test_config.yml')
        self.assertEqual(config.get_path(), 'test/folder')
        self.assertEqual(['subpath1', 'subpath2'], config.get_excludes())

        new_path = self.copy.copy_dir(src_path=config.get_path())
        self.assertTrue(os.path.isdir(new_path), 'Directory is not created: %s' % new_path)

        self.utils.add_folders_to_path(dirname=new_path, exclude_dirs=config.get_excludes())

        self.assertIsNotNone(sys.path.index(new_path))
        self.assertIsNotNone(sys.path.index(new_path + '/subfolder1'))
        self.assertIsNotNone(sys.path.index(new_path + '/subfolder2'))
        self.assertIsNotNone(sys.path.index(new_path + '/subfolder1/xxx'))
        self.assertIsNotNone(sys.path.index(new_path + '/subfolder2/yyy'))

        self.pylint2.run_pylint(dirname=new_path, out_file='test/pylint2_old.txt', exclude_dirs=config.get_excludes())

        self.assertGreater(os.path.getsize('test/pylint2_old.txt'), 0)

        self.futurize.run_futurize(dirname=new_path, exclude_dirs=config.get_excludes(), out_file='futurize.txt')

        self.pylint2.run_pylint(dirname=new_path, out_file='test/pylint2_new.txt', exclude_dirs=config.get_excludes())

        self.assertGreater(os.path.getsize('test/pylint2_new.txt'), 0)

        self.diff.diff_files(from_file='test/pylint2_old.txt', to_file='test/pylint2_new.txt',
                             out_file='test/pylint2_diff.txt')

        self.assertGreater(os.path.getsize('test/pylint2_diff.txt'), 0)

        self.pylint3.run_pylint(dirname=new_path, out_file='test/pylint3_new.txt', exclude_dirs=config.get_excludes())

        self.diff.diff_files(from_file='test/pylint2_new.txt', to_file='test/pylint3_new.txt',
                             out_file='test/pylint3_diff.txt')

        self.assertGreater(os.path.getsize('test/pylint3_diff.txt'), 0)

    def test_is_excluded(self):
        self.assertFalse(self.utils.is_excluded('aaaa/bbbbb', None, 'aaaa'))
        self.assertFalse(self.utils.is_excluded('aaaa/bbbbb', [], 'aaaa'))
        self.assertFalse(self.utils.is_excluded('aaaa/bbbbb', ['xxxxx', 'yyyyyy'], 'aaaa'))
        self.assertTrue(self.utils.is_excluded('aaaa/xxxxx/', ['xxxxx/', 'yyyyyy'], 'aaaa/'))
        self.assertTrue(self.utils.is_excluded('aaaa/xxxxx/', ['xxxxx', 'yyyyyy'], 'aaaa/'))
        self.assertTrue(self.utils.is_excluded('aaaa/xxxxx', ['xxxxx/', 'yyyyyy'], 'aaaa/'))
        self.assertTrue(self.utils.is_excluded('aaaa/xxxxx/', ['xxxxx', 'yyyyyy'], 'aaaa'))
        self.assertTrue(self.utils.is_excluded('aaaa/xxxxx/yyyyyy', ['xxxxx/yyyyyy'], 'aaaa/'))
