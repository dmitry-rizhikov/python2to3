import logging
import os
import shutil
from pathlib import Path
from unittest import TestCase


# Find code directory relative to our directory
import sys
from os.path import dirname

from migrate.copy_directory import Copy
from migrate.diff_files import Diff
from migrate.read_config_yml import Config
from migrate.replace_in_files import Replacer
from migrate.run_futurize import Futurize
from migrate.run_pylint import Pylint
from migrate.utils import Utils


class Test(TestCase):
    utils = Utils()

    cwd = os.getcwd()

    pylint2 = Pylint(cwd + '/venv2/bin/pylint', cwd + '/test/rcfile')

    pylint3 = Pylint(cwd + '/venv/bin/pylint', cwd + '/test/rcfile')

    diff = Diff()

    futurize = Futurize()

    copy = Copy()

    replacer = Replacer()

    logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    @classmethod
    def setUpClass(cls):
        for p in Path().glob("test/folder*"):
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

        self.replacer.replace_string_in_files(dirname=new_path, src='file', dest='replaced')

        self.assertEqual(Path(new_path + '/subfolder1/xxx/file2.py').read_text(), 'replaced2')
        self.assertEqual(Path(new_path + '/file1.py').read_text(), 'replaced1')

        self.replacer.replace_string_in_files(config.get_path(), config.get_replace_src(), config.get_replace_dest())

        self.assertEqual(Path('test/folder/subfolder1/xxx/file2.py').read_text(), 'file2')
        self.assertEqual(Path('test/folder/file1.py').read_text(), 'file1')

    def test_is_excluded(self):
        self.assertFalse(self.utils.is_excluded('aaaa/bbbbb', None, 'aaaa'))
        self.assertFalse(self.utils.is_excluded('aaaa/bbbbb', [], 'aaaa'))
        self.assertFalse(self.utils.is_excluded('aaaa/bbbbb', ['xxxxx', 'yyyyyy'], 'aaaa'))
        self.assertTrue(self.utils.is_excluded('aaaa/xxxxx/', ['xxxxx/', 'yyyyyy'], 'aaaa/'))
        self.assertTrue(self.utils.is_excluded('aaaa/xxxxx/', ['xxxxx', 'yyyyyy'], 'aaaa/'))
        self.assertTrue(self.utils.is_excluded('aaaa/xxxxx', ['xxxxx/', 'yyyyyy'], 'aaaa/'))
        self.assertTrue(self.utils.is_excluded('aaaa/xxxxx/', ['xxxxx', 'yyyyyy'], 'aaaa'))
        self.assertTrue(self.utils.is_excluded('aaaa/xxxxx/yyyyyy', ['xxxxx/yyyyyy'], 'aaaa/'))
