# -*- coding: utf-8 -*-
# import os


class PluginLoader(object):
    def __init__(self):
        self.plugins = {}

    def load_file(self, filename, onlyif=None, args=None, kwargs=None,
                  global_env=None):
        args = args or []
        kwargs = kwargs or {}
        onlyif = self._default_condition if onlyif is None else onlyif
        context = {}
        with open(filename) as fd:
            exec(fd.read(), global_env, context)

        for name, clazz in context.iteritems():
            if (self._apply_condition(onlyif, name, clazz)):
                self.plugins[name] = clazz(*args, **kwargs)

    def _apply_condition(self, condition, *args, **kwargs):
        if callable(condition):
            return condition(*args, **kwargs)
        return condition

    def _default_condition(self, name, clazz):
        return isinstance(clazz, type)
