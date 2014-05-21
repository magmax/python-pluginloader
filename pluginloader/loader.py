# -*- coding: utf-8 -*-
# import os


class PluginLoader(object):
    def __init__(self):
        self.plugins = {}

    def load_file(self, filename):
        context = {}
        with open(filename) as fd:
            exec(fd.read(), context)

        for name, clazz in context.iteritems():
            if isinstance(clazz, type):
                self.plugins[name] = clazz()
