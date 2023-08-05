from src.core.Plugins import Plugin
from src.core.Steps import Steps
import os

from src.core.Module import runCmdHide

URL = 'https://github.com/ethanquix/yoyo_ymodules_store'


class Git_Update(Plugin):

    def __init__(self, config):
        super().__init__(config)

    def name(self):
        return 'Git Update of Modules'

    def author(self):
        return 'Dimitri Wyzlic'

    def steps(self):
        return [Steps.PRE_UPDATE]

    def onStep(self, step):
        if step == Steps.PRE_UPDATE:
            plugindir = self.config.store + 'y_local/modules/'

            curdir = os.getcwd()

            if os.path.exists(plugindir + 'fromgitplugin'):
                os.chdir(plugindir + 'fromgitplugin')
                runCmdHide('git pull')
                os.chdir(curdir)
            else:
                runCmdHide('git clone ' + URL + ' ' + plugindir + 'fromgitplugin')
        else:
            print('[DEBUG] error bad step bla bla a enlever ce message')  # TODO

    def requirements(self):
        return ['git']


def get(config):
    return Git_Update(config)
