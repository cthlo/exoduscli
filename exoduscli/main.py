'''Load and start Exodus with XBMC stub
'''

import sys
import threading
import runpy
import os
import base64
from os import path
from itertools import count
from urlparse import urlparse

from lib import webbrowser
from exoduscli import config, addons, cli
from fakexbmc import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs

def _run_exodus(*args):
    '''Run a Exodus using runpy
    '''
    fullpath = path.join(config.addonsdir, config.exodus['id'], config.exodus['entryfile'])
    entrypath, entryfile = path.split(fullpath)
    if entrypath not in sys.path:
        sys.path.insert(0, entrypath)
    module, _ = path.splitext(entryfile)

    # Exodus assumes thread names start at 1
    # and gets provider names from the thread name
    c = threading._counter = count().next
    c() # consume 0

    sys.argv = list(args)
    # note: cannot use __import__ because Exodus spawns threads that do import
    # so that would cause deadlock
    runpy.run_module(module)


def _dir_select(handle):
    '''List items of a handle from xbmcplugin._dirs
    Return handle and the index of the selected item in the directory
    '''
    _dirs = xbmcplugin._dirs

    # if Exodus didn't add any item to directory
    if handle not in _dirs:
        _dirs[handle] = []

    if handle > 0:
        options = ['<< Back']
    else:
        options = ['<< Exit']
        # explicitly remove these options from the index page
        _dirs[handle] = [i for i in _dirs[handle] if i[1].getLabel() not in ['Tools', 'Channels']]

    for _, listitem, isfolder in _dirs[handle]:
        options.append('%s' % listitem.getLabel())

    idx = cli.select(options)
    if idx > 0:
        return (handle, idx-1)
    else:
        if handle == 0: # index page
            _exit(0)
        _dirs[handle] = [] # clear current directory
        return _dir_select(handle-1) # previous directory


def _determine_args(handle, index):
    '''Return arguments tuple (used for calling Exodus) based on selected item
    Return None if it is a special item or is unsupported
    '''
    url, listitem, isfolder = xbmcplugin._dirs[handle][index]
    urlparts = urlparse(url)
    scheme = urlparts.scheme

    if scheme == 'plugin':
        base = '%s://%s' % (scheme, urlparts.netloc)
        query = '?%s' % urlparts.query
        return (base, handle+1, query)

    elif scheme == 'browser':
        url = base64.b64decode(urlparts.netloc)
        try:
            webbrowser.get().open(url)
        except webbrowser.Error:
            cli.message('Failed to open URL in browser')
        return None

    elif scheme == 'print':
        url = base64.b64decode(urlparts.netloc)
        cli.message(url)
        return None

    else:
        cli.message('Unsupported item')
        return None


def _exit(status):
    cli.message('\nBye\n')
    sys.exit(status)


def _setup_paths():
    '''Add dependency lib paths (used by Exodus)
    '''
    for dependency in config.libs:
        libpath = path.join(config.addonsdir, dependency['id'], dependency['libpath'])
        sys.path.insert(0, libpath)


def _inject_xbmc():
    sys.modules['xbmc'] = xbmc
    sys.modules['xbmcaddon'] = xbmcaddon
    sys.modules['xbmcgui'] = xbmcgui
    sys.modules['xbmcplugin'] = xbmcplugin
    sys.modules['xbmcvfs'] = xbmcvfs


def _clear_log():
    if path.isfile(config.logfile):
        os.remove(config.logfile)


def main():
    try:
        addons.download_addons()
    except Exception as e:
        cli.message('Failed to load Exodus: %s' % str(e))
        _exit(-1)

    _setup_paths()
    _inject_xbmc()
    _clear_log()

    args = ('plugin://plugin.video.exodus', 0, '')
    while True:
        t = threading.Thread(target=_run_exodus, args=args)
        t.daemon = True
        cli.message('Loading...')
        t.start()
        t.join()

        handle = args[1]

        while True:
            try:
                selected = _dir_select(handle)
            except KeyboardInterrupt:
                _exit(0)
            args = _determine_args(*selected)
            if args: break


if __name__ == '__main__':
    main()
