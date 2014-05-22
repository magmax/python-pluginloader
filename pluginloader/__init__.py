# -*- coding: utf-8 -*-

__version__ = '0.1.1'
__description__ = 'Library to manage plugins/extensions in your applications.'

import os


class PluginFactory(object):
    def __init__(self, clazz):
        self._clazz = clazz

    def __call__(self, *args, **kwargs):
        return self._clazz(*args, **kwargs)


class PluginLoader(object):
    def __init__(self):
        self.plugins = {}

    def load_file(self, filename, onlyif=None):
        onlyif = self._default_condition if onlyif is None else onlyif
        context = {}
        with open(filename) as fd:
            exec(fd.read(), context)

        for name, clazz in context.iteritems():
            if (self._apply_condition(onlyif, name, clazz)):
                self.plugins[name] = PluginFactory(clazz)

    def load_directory(self, path, onlyif=None, recursive=False):
        for filename in os.listdir(path):
            full_path = os.path.join(path, filename)

            if os.path.isfile(full_path):
                self.load_file(full_path, onlyif)
                continue
            if os.path.isdir(full_path):
                if recursive:
                    self.load_directory(full_path, onlyif, recursive)

    def _apply_condition(self, condition, *args, **kwargs):
        if callable(condition):
            return condition(*args, **kwargs)
        return condition

    def _default_condition(self, name, clazz):
        return isinstance(clazz, type)
