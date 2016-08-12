from exoduscli import cli

NOTIFICATION_INFO = 'info'
NOTIFICATION_WARNING = 'warning'
NOTIFICATION_ERROR = 'error'

class ListItem(object):
    def __init__(self, label='', label2='', iconImage='', thumbnailImage='', path=''):
        self.props = {}
        self.cm_items = []
        self.label = label
        self._path = path

    def setInfo(self, type, infoLabels):
        self.type = type
        self.infoLabels = infoLabels.copy()

    def setProperty(self, key, value):
        self.props[key.lower()] = value

    def getProperty(self, key):
        return self.props.get(key.lower(), '')

    def addContextMenuItems(self, items, replaceItems=False):
        if replaceItems:
            self.cm_items = list(items)
        else:
            self.cm_items += items

    def getLabel(self):
        return self.label

    def setArt(self, dictionary):
        pass


_window_props = {}
class Window(object):
    def __init__(self, windowId=-1):
        if windowId not in _window_props:
            _window_props[windowId] = {}
        self.props = _window_props[windowId]

    def getProperty(self, key):
        return self.props.get(key.lower(), '')

    def setProperty(self, key, value):
        self.props[key.lower()] = value

    def clearProperty(self, key):
        if key in self.props:
            del self.props[key]


class DialogProgress(object):
    def create(self, heading, line1='', line2='', line3=''):
        self.heading = heading
        for l in [line1, line2, line3]:
            if l:
                cli.message('%s: %s' % (heading, l))

    def update(self, percent, line1='', line2='', line3=''):
        for l in [line1, line2, line3]:
            if l:
                cli.message('%s: %s' % (self.heading, l))
        cli.message('%s: %s%%' % (self.heading, percent))

    def close(self):
        pass

    def iscanceled(self):
        return False


class DialogProgressBG(object):
    pass

class Dialog(object):
    def notification(self, heading, message, icon=NOTIFICATION_INFO, time=5000, sound=True):
        pass

class WindowDialog(object):
    pass

class ControlButton(object):
    pass

class ControlImage(object):
    pass
