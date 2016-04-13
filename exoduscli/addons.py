'''Download XBMC addons including Exodus and its dependencies
'''

import shutil
import hashlib
import zipfile
import base64
import urllib2
from StringIO import StringIO
from os import path, makedirs

from exoduscli import config, cli

def _download(id, b64url, zipmd5):
    '''Download one addon from base64 encoded url
    Checks md5
    Loads zip contents into addons directory
    '''
    dir = path.join(config.addonsdir, id)
    if path.isdir(dir):
        return
    cli.message('Retrieving %s...' % id)

    url = base64.b64decode(b64url)
    resp = urllib2.urlopen(url)
    s = resp.read(5*1000*1000) # should not be larger than 5MB

    m = hashlib.md5(s)
    if m.hexdigest() != zipmd5:
        raise Exception('Invalid md5 for %s', id)

    f = StringIO(s)
    try:
        with zipfile.ZipFile(f) as z:
            z.extractall(config.addonsdir)
    except:
        shutil.rmtree(dir)
    finally:
        f.close()
    cli.message('Loaded %s' % id)


def download_addons():
    '''Download all necessary addons according to config
    '''
    if not path.isdir(config.addonsdir):
        makedirs(config.addonsdir)

    _download(config.exodus['id'], config.exodus['b64url'], config.exodus['zipmd5'])
    for dependency in config.libs:
        _download(dependency['id'], dependency['b64url'], dependency['zipmd5'])
