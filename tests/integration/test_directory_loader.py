import unittest
import os
import shutil
import tempfile

from pluginloader import PluginLoader


class plugins_in_directory(unittest.TestCase):
    def setUp(self):
        self.plugin_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.plugin_dir)

    def _create(self, filename, content, path=None):
        path = (self.plugin_dir
                if path is None
                else os.path.join(self.plugin_dir, path))
        with open(os.path.join(path, filename), 'w+') as fd:
            fd.write(content)

    def _create_dir(self, path):
        os.makedirs(os.path.join(self.plugin_dir, path))

    def test_empty_directory(self):
        sut = PluginLoader()

        sut.load_directory(self.plugin_dir)

        self.assertEqual({}, sut.plugins)

    def test_load_simple_file(self):
        self._create('foo.py', 'class Foo(object): pass')
        sut = PluginLoader()

        sut.load_directory(self.plugin_dir)

        self.assertEqual(['Foo'], sut.plugins.keys())

    def test_ignorable_classes(self):
        self._create('foo.py', 'class Foo(object): pass')
        sut = PluginLoader()

        sut.load_directory(self.plugin_dir, onlyif=lambda x, y: False)

        self.assertEquals({}, sut.plugins)

    def test_containing_directories(self):
        self._create_dir('foo')
        sut = PluginLoader()

        sut.load_directory(self.plugin_dir)

        self.assertEquals({}, sut.plugins)

    def test_recursive_mode(self):
        self._create_dir('foo')
        self._create('bar.py', 'class Bazz(object): pass', 'foo')
        sut = PluginLoader()

        sut.load_directory(self.plugin_dir, recursive=True)

        self.assertEquals(['Bazz'], sut.plugins.keys())

    def test_recursive_mode_off(self):
        self._create_dir('foo')
        self._create('bar.py', 'class Bazz(object): pass', 'foo')
        sut = PluginLoader()

        sut.load_directory(self.plugin_dir, recursive=False)

        self.assertEquals({}, sut.plugins)

    def test_link_recursive(self):
        os.symlink(self.plugin_dir, os.path.join(self.plugin_dir, 'foo'))

        sut = PluginLoader()

        sut.load_directory(self.plugin_dir, recursive=True)

        self.assertEquals({}, sut.plugins)
