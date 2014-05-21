# -*- coding: utf-8 -*-
# import os


class PluginLoader(object):
    def __init__(self):
        self.plugins = {}

    def load_file(self, filename, onlyif=True, args=None, kwargs=None):
        args = args or []
        kwargs = kwargs or {}
        context = {}
        with open(filename) as fd:
            exec(fd.read(), context)

        for name, clazz in context.iteritems():
            if (isinstance(clazz, type)
                    and self._apply_condition(onlyif, name, clazz)):
                self.plugins[name] = clazz(*args, **kwargs)

    def _apply_condition(self, condition, *args, **kwargs):
        if callable(condition):
            return condition(*args, **kwargs)
        return condition
