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
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name)

        self.assertEquals(['Foo'], sut.plugins.keys())
        self.assertIsInstance(sut.plugins['Foo'], object)
        self.assertEquals('Foo', sut.plugins['Foo'].__class__.__name__)

    def test_ignorable_classes(self):
        self.plugin_file.write('class Foo(object): pass')
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name, onlyif=lambda x, y: False)

        self.assertEquals({}, sut.plugins)

    def test_ignorable_classes_with_variable_false(self):
        self.plugin_file.write('class Foo(object): pass')
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name, onlyif=False)

        self.assertEquals([], sut.plugins.keys())

    def test_ignorable_classes_with_variable_true(self):
        self.plugin_file.write('class Foo(object): pass')
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name, onlyif=True)

        self.assertEquals(['Foo'], sut.plugins.keys())

    def test_parameters_for_constructor(self):
        self.plugin_file.write(
            'class Foo(object):\n'
            '  def __init__(self, a):\n'
            '    self.a = a'
            )
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name, args=[5])

        self.assertEquals(5, sut.plugins['Foo'].a)

    def test_named_parameters_for_constructor(self):
        self.plugin_file.write(
            'class Foo(object):\n'
            '  def __init__(self, a):\n'
            '    self.a = a'
            )
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name, kwargs={'a': 5})

        self.assertEquals(5, sut.plugins['Foo'].a)

    def test_adding_vars_to_globals(self):
        self.plugin_file.write(
            'class Foo(object):\n'
            '  def __init__(self):\n'
            '    self.a = b'
            )
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name, global_env={'b': 8})

        self.assertEquals(8, sut.plugins['Foo'].a)
