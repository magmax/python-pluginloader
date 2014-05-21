import unittest
import os
import shutil
import tempfile

from pluginloader.loader import PluginLoader


class plugins_in_file(unittest.TestCase):
    def setUp(self):
        self.plugin_file = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.plugin_file.close()

    def test_load_empty_file(self):
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name)

        self.assertEquals({}, sut.plugins)

    def test_base_case(self):
        self.plugin_file.write('class Foo(object): pass')
        self.plugin_file.flush()
        self.plugin_file.seek(0)
        print self.plugin_file.read()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name)

        self.assertEquals(['Foo'], sut.plugins.keys())


@unittest.skip('Not ready yet')
class plugins_in_directory(unittest.TestCase):
    def setUp(self):
        self.plugin_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.plugin_dir)

    def test_load_file(self):
        sut = PluginLoader()

        sut.load_all()
