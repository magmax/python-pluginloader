# -*- coding: utf-8 -*-
# import os


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

    def load_directory(self, path):
        pass

    def _apply_condition(self, condition, *args, **kwargs):
        if callable(condition):
            return condition(*args, **kwargs)
        return condition

    def _default_condition(self, name, clazz):
        return isinstance(clazz, type)
