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

    def _create(self, filename, content):
        with file(os.path.join(self.plugin_dir, filename), 'w+') as fd:
            fd.write(content)

    def test_empty_directory(self):
        sut = PluginLoader()

        sut.load_directory(self.plugin_dir)

        self.assertEqual({}, sut.plugins)

    def test_load_simple_file(self):
        self._create('foo.py', 'class Foo(object): pass')
        sut = PluginLoader()

        sut.load_directory(self.plugin_dir)

        self.assertEqual(['Foo'], sut.plugins.keys())
