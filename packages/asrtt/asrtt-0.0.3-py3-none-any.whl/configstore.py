import os
from os.path import join
import sys
import json
import utils


class ConfigStore:

    def __init__(self, name, defaults={}, globalConfigPath=False):
        self.name = name
        self.defaults = defaults
        self.globalConfigPath = globalConfigPath

        self.configDir = utils.getConfigDir()

        if self.globalConfigPath:
            self.pathPrefix = join(name, 'config.json')
            pathEntry = name
        else:
            self.pathPrefix = join('configstore', '{}.json'.format(name))
            pathEntry = 'configstore'

        self.path = join(self.configDir, self.pathPrefix)
        # self.all = {}
        utils.createConfig(self.path, self.defaults, pathEntry=pathEntry)
        self.Object = utils.loadConfigs(self.path)
        self.size = utils.getConfigSize(self.path)

    def all(self, Object=None):
        if Object:
            self.set(Object)

        jsonConfigs = utils.loadConfigs(self.path)
        return jsonConfigs

    def get(self, key):
        value = utils.getConfigs(self.path, key)
        return value

    def set(self, key, value=None):
        if isinstance(key, dict):
            setObject = key
            utils.setConfigs(self.path, Object=setObject)
        else:
            if not value:
                raise KeyError("KeyError: param value not provided")

            utils.setConfigs(self.path, key=key, value=value)

    def has(self, key):
        return utils.hasConfigs(self.path, key)

    def delete(self, key):
        utils.deleteConfigs(self.path, key)

    def clear(self):
        utils.clearConfigs(self.path)
