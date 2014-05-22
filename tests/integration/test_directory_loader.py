import unittest
import os
import shutil
import tempfile

from pluginloader.loader import PluginLoader


class plugins_in_directory(unittest.TestCase):
    def setUp(self):
        self.plugin_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.plugin_dir)

    def test_empty_directory(self):
        sut = PluginLoader()

        sut.load_directory(self.plugin_dir)

        self.assertEqual({}, sut.plugins)
