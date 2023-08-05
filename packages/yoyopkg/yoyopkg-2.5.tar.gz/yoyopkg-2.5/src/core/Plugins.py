from abc import ABC, abstractmethod
from src.core.Steps import Steps
import sys
import os
from importlib import util
from typing import Dict


class Plugin:
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def author(self):
        pass

    @abstractmethod
    def steps(self):
        pass

    @abstractmethod
    def onStep(self, step):
        pass

    @abstractmethod
    def requirements(self):
        pass

    def __str__(self):
        return self.name() + '\tby: ' + self.author()

    # TODO pass before


class PluginStore:
    def __init__(self, config):
        self.config = config
        self.plugins = dict()  # type: Dict[str, Plugin]
        self.paths = []

    def addPath(self, path):
        self.paths.append(path)

    def refresh(self):
        for p in self.paths:
            self.refreshOne(p)

    def refreshOne(self, path):
        old_path = sys.path
        sys.path = sys.path[:]
        sys.path.insert(0, path)

        for filename in os.listdir(path):
            if '__' in filename:
                continue

            if not filename.endswith('.py'):
                continue

            spec = util.spec_from_file_location(path + '/' + filename, path + '/' + filename)
            plugin = util.module_from_spec(spec)
            spec.loader.exec_module(plugin)

            tmpPlugin = plugin.get(self.config)
            self.plugins[tmpPlugin.name()] = tmpPlugin

        sys.path = old_path

    def delPath(self, path):
        if path in self.paths:
            self.paths.remove(path)

    def getAll(self) -> Dict[str, Plugin]:
        return self.plugins

    def __getitem__(self, item):
        return self.plugins[item]

    def run(self, step: Steps):
        for p in self.plugins:
            if step in self.plugins[p].steps():
                self.plugins[p].onStep(step)

    def __str__(self):
        out = 'paths:\n'
        for p in self.paths:
            out += '\t' + p + '\n'
        out += '\nplugins:\n'
        for p in self.plugins:
            out += '\t' + str(str(self.plugins[p]) + '\n')

        return out
