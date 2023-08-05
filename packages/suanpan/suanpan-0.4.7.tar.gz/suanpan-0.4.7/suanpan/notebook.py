# coding=utf-8
from __future__ import print_function

from suanpan.components import Component


class Notebook(object):
    def __init__(self, component=Component, name="Notebook", runFunc=None):
        def defaultRunFunc(*args, **kwargs):
            pass

        self.name = name
        self.componentClass = component
        self.runFunc = runFunc or defaultRunFunc
        self.runFunc.__name__ = self.name
        self.component = self.componentClass(self.runFunc)

    def init(self):
        return self.component.init()

    def save(self, context, results):
        return self.component.save(context, results)

    def arg(self, *args, **kwargs):
        decorator = self.componentClass.arg(*args, **kwargs)
        self.component = decorator(self.component)
        return self.component

    def input(self, *args, **kwargs):
        decorator = self.componentClass.input(*args, **kwargs)
        self.component = decorator(self.component)
        return self.component

    def output(self, *args, **kwargs):
        decorator = self.componentClass.output(*args, **kwargs)
        self.component = decorator(self.component)
        return self.component

    def param(self, *args, **kwargs):
        decorator = self.componentClass.param(*args, **kwargs)
        self.component = decorator(self.component)
        return self.component

    def column(self, *args, **kwargs):
        decorator = self.componentClass.column(*args, **kwargs)
        self.component = decorator(self.component)
        return self.component
