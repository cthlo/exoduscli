from os import path

from exoduscli import config, addonconfigs

class Addon(object):
    def __init__(self, id=None):
        self.id = 'plugin.video.exodus' if id is None else id

    def getLocalizedString(self, id):
        s = addonconfigs.strings[self.id].get(id, -1)
        if s == -1:
            raise NotImplementedError
        else:
            return s

    def getSetting(self, id):
        s = addonconfigs.settings[self.id].get(id, '')
        return s

    def setSetting(self, id, value):
        raise NotImplementedError

    def openSettings(self):
        raise NotImplementedError

    def getAddonInfo(self, id):
        if id == 'profile':
            return path.join(config.specialroot, self.id, 'profile')
        elif id == 'path':
            return path.join(config.addonsdir, self.id, 'path')
        elif id == 'name':
            return self.id.split('.')[-1].capitalize()
        elif id == 'id':
            return self.id
        elif id == 'version':
            return '0.0.0'
        raise NotImplementedError
