from urlparse import urlparse
from exoduscli.fakexbmc import xbmcgui

_dirs = {}
_contents = {}

def addDirectoryItem(handle, url, listitem, isFolder=False, totalItems=0):
    if handle not in _dirs:
        _dirs[handle] = []
    _dirs[handle].append((url, listitem, isFolder))
    return True


def endOfDirectory(handle, succeeded=True, updateListing=False, cacheToDisc=True):
    pass


def setContent(handle, content):
    _contents[handle] = content


def setProperty(handle, key, value):
    pass


def setResolvedUrl(handle, succeeded, listitem):
    url = listitem._path
    urlparts = urlparse(url)
    scheme = urlparts.scheme

    items = []

    if scheme == 'http' or scheme == 'https':
        path = 'browser://%s' % url
        li = xbmcgui.ListItem('Open in browser', path=path)
        items.append((path, li))

    path = 'print://%s' % url
    li = xbmcgui.ListItem('Show URL', path=path)
    items.append((path, li))

    for url, item in items:
        addDirectoryItem(handle, url, item)
