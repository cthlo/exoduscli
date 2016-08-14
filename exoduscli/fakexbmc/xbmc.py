import re
import sys
import runpy
import os.path
from urlparse import parse_qsl, urlparse, urljoin
from time import sleep as _sleep

from exoduscli import config, cli
from exoduscli.fakexbmc import xbmcplugin

PLAYLIST_VIDEO = 1
ENGLISH_NAME = 2
LOGDEBUG = 0
LOGERROR = 4
LOGFATAL = 6
LOGINFO = 1
LOGNONE = 7
LOGNOTICE = 2
LOGSEVERE = 5
LOGWARNING = 3
abortRequested = False

def getInfoLabel(infotag):
    if infotag == 'ListItem.Title':
        return ''

    if infotag == 'Container.PluginName':
        return config.exodus['id']

    if infotag == 'Container.FolderPath':
        base = sys.argv[0]
        query = sys.argv[2]
        return urljoin(base, query)

    if infotag == 'ListItem.FileName':
        return '' # unsure when it should be non-empty

    raise NotImplementedError


_re_container_content = re.compile(r'Container.Content\(([^\)]+)\)')
_re_has_addon = re.compile(r'System.HasAddon\(([^\)]+)\)')
def getCondVisibility(condition):
    if condition == 'Window.IsActive(virtualkeyboard)':
        return False
    if condition == 'Window.IsActive(yesnoDialog)':
        return False

    m = _re_has_addon.match(condition)
    if m:
        addon = m.group(1)
        hasaddon = addon in [config.exodus['id']]+[d['id'] for d in config.libs]
        return hasaddon

    m = _re_container_content.match(condition)
    if m:
        content = m.groups()[0]
        handle = sys.argv[1]
        return content == xbmcplugin._contents[handle]

    raise NotImplementedError


def executeJSONRPC(jsonrpccommand):
    raise NotImplementedError


def sleep(time):
    _sleep(time/1000.0)


_re_notification = re.compile(r'Notification\(([^\),]*),([^\),]*)(?:,([^\),]+))?(?:,([^\),]+))?\)')
_re_update = re.compile(r'Container\.Update\(([^\)]+)\)')
def executebuiltin(function):
    m = re.match(_re_notification, function)
    if m:
        header, message, time, image = m.groups()
        cli.message('%s: %s' % (header.strip(), message.strip()))
        try:
            t = int(time)
            cli.message('(resume in %s seconds)' % round(t/1000.0))
        except TypeError:
            t = 0
        sleep(t)
        return

    m = re.match(_re_update, function)
    if m:
        # this is completely different from how Kodi deals with Container.Update
        # Kodi creates new addon process to run the url, here we're making assumptions
        # on how Exodus works, and run Exodus again in the same thread from the entry
        # point with the query string supplied from the Container.Update call
        url = m.group(1)
        parts = urlparse(url)
        if parts.scheme == 'plugin' and parts.netloc == config.exodus['id']:
            qs = parts.query
            kv = dict(parse_qsl(qs))
            if kv['action'] in ['addItem', 'moviePersons', 'movies', 'tvPersons', 'tvshows']:
                exodus, _ = os.path.splitext(config.exodus['entryfile'])
                old_argv = sys.argv[:]
                sys.argv[2] = '?' + qs
                runpy.run_module(exodus)
                sys.argv = old_argv
                return
        raise NotImplementedError

    if function == 'Dialog.Close(virtualkeyboard)':
        return

    if function == 'Dialog.Close(yesnoDialog)':
        return

    if function == 'Dialog.Close(busydialog)':
        return

    if function == 'Container.SetViewMode(500)':
        return

    if function == 'Container.SetViewMode(504)':
        return

    raise NotImplementedError


def getSkinDir():
    return 'skin.confluence'


def translatePath(path):
    urlparts = urlparse(path)
    if urlparts.scheme == 'special':
        if urlparts.netloc == 'skin':
            return os.path.join(config.specialroot, 'skins', getSkinDir(), urlparts.path)

    elif urlparts.scheme == '':
        return urlparts.geturl()

    raise NotImplementedError


def getLanguage(format=ENGLISH_NAME, region=False):
    if format == ENGLISH_NAME and not region:
        return 'en'
    raise NotImplementedError


def log(msg, level=LOGNOTICE):
    lvl = {
          LOGDEBUG: 'DEBUG',
           LOGINFO: 'INFO',
         LOGNOTICE: 'NOTICE',
        LOGWARNING: 'WARNING',
          LOGERROR: 'ERROR',
         LOGSEVERE: 'SEVERE',
          LOGFATAL: 'FATAL',
           LOGNONE: 'NONE'
    }[level]
    with open(config.logfile, 'a+') as f:
        f.write('%s: %s\n' % (lvl, msg))


def getLocalizedString(id):
    if id == 19033:
        return 'Information' # https://github.com/xbmc/xbmc/blob/master/addons/resource.language.en_gb/resources/strings.po
    raise NotImplementedError


class Keyboard(object):
    def __init__(self, default='', heading='', hidden=False):
        self.default = default
        self.prompt = heading + (' [%s]: ' % default if default else ': ')
        self.hidden = hidden
        self.confirmed = False

    def doModal(self):
        try:
            self.input = cli.input(self.prompt, self.hidden)
            self.input = self.input or self.default
            self.confirmed = True
        except (KeyboardInterrupt, EOFError) as e:
            pass

    def getText(self):
        return self.input

    def isConfirmed(self):
        return self.confirmed


class Player(object):
    def __init__(self):
        pass

    def play(self, item='', listitem=None, windowed='false', startpos=-1):
        pass


class PlayList(object):
    def __init__(self, playList):
        pass

    def clear(self):
        pass
