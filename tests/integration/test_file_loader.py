import unittest
import os
import shutil
import tempfile

from pluginloader import PluginLoader


class plugins_in_file(unittest.TestCase):
    def setUp(self):
        self.plugin_file = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.plugin_file.close()

    def _write_file(self, content):
        self.plugin_file.write(content.encode('utf-8'))

    def test_load_empty_file(self):
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name)

        self.assertEquals({}, sut.plugins)

    def test_base_case(self):
        self._write_file('class Foo(object): pass')
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name)

        self.assertEquals(['Foo'], list(sut.plugins.keys()))
        self.assertIsInstance(sut.plugins['Foo'], object)
        self.assertEquals('Foo', sut.plugins['Foo']().__class__.__name__)

    def test_ignorable_classes(self):
        self._write_file('class Foo(object): pass')
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name, onlyif=lambda x, y: False)

        self.assertEquals({}, sut.plugins)

    def test_ignorable_classes_with_variable_false(self):
        self._write_file('class Foo(object): pass')
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name, onlyif=False)

        self.assertEqual([], list(sut.plugins.keys()))

    def test_ignorable_classes_with_variable_true(self):
        self._write_file('class Foo(object): pass')
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name, onlyif=True)

        self.assertEqual(sorted(['__builtins__', 'Foo']),
                         sorted(list(sut.plugins.keys())))

    def test_parameters_for_constructor(self):
        self._write_file(
            'class Foo(object):\n'
            '  def __init__(self, a):\n'
            '    self.a = a'
            )
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name)

        plugin = sut.plugins['Foo'](5)
        self.assertEqual(5, plugin.a)

    def test_named_parameters_for_constructor(self):
        self._write_file(
            'class Foo(object):\n'
            '  def __init__(self, a):\n'
            '    self.a = a'
            )
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name)

        plugin = sut.plugins['Foo'](a=5)

        self.assertEqual(5, plugin.a)

    def test_two_plugins_in_a_file(self):
        self._write_file(
            'class Foo(object):\n'
            '  pass\n'
            'class Bar(object):\n'
            '  pass\n'
            )
        self.plugin_file.flush()
        sut = PluginLoader()

        sut.load_file(self.plugin_file.name)

        self.assertEqual(sorted(['Foo', 'Bar']),
                         sorted(list(sut.plugins.keys())))
        self.assertEqual('Foo', sut.plugins['Foo']().__class__.__name__)
        self.assertEqual('Bar', sut.plugins['Bar']().__class__.__name__)
