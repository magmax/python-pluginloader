import unittest
import os
import shutil
import tempfile

from pluginloader.loader import PluginLoader


@unittest.skip('Not ready yet')
class plugins_in_directory(unittest.TestCase):
    def setUp(self):
        self.plugin_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.plugin_dir)

    def test_load_file(self):
        sut = PluginLoader()

        sut.load_directory()
