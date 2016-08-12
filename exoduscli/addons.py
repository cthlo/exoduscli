'''Download XBMC addons including Exodus and its dependencies
'''

import shutil
import hashlib
import zipfile
import base64
import urllib2
from StringIO import StringIO
from os import path, makedirs, remove

from exoduscli import config, cli

def _download(id, b64url, zipmd5, version):
    '''Download one addon from base64 encoded url
    Checks md5
    Loads zip contents into addons directory
    '''
    version_file = path.join(config.addonsdir, id + '.version')
    dir = path.join(config.addonsdir, id)

    if path.isfile(version_file):
        try:
            with open(version_file, 'r') as f:
                curr_version = f.read(30).strip() # version should not be more than 30 bytes
        except:
            # try to remove version file if failed to read from it
            remove(version_file)
            raise
        if curr_version == version and path.isdir(dir):
            return

    cli.message('Retrieving %s (%s)...' % (id, version))

    if path.isdir(dir):
        shutil.rmtree(dir)

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
        # try to remove directory if anything went wrong
        if path.isdir(dir):
            shutil.rmtree(dir)
        raise

    try:
        with open(version_file, 'w+') as f:
            f.write(version)
    except:
        # try to remove version file if failed to write to it
        if path.isfile(version_file):
            remove(version_file)
        raise

    cli.message('Loaded %s' % id)


def download_addons():
    '''Download all necessary addons according to config
    '''
    if not path.isdir(config.addonsdir):
        makedirs(config.addonsdir)

    _download(config.exodus['id'], config.exodus['b64url'], config.exodus['zipmd5'], config.exodus['version'])
    for dependency in config.libs:
        _download(dependency['id'], dependency['b64url'], dependency['zipmd5'], dependency['version'])
