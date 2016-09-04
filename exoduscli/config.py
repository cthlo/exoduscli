from os import path
from lib import appdirs

_appdir = appdirs.user_data_dir('exoduscli')

specialroot = path.join(_appdir, 'fakexbmc', 'special')
addonsdir = path.join(_appdir, 'addons')
logfile = path.join(_appdir, 'fakexbmc.log')
exodus = dict(
    id = 'plugin.video.exodus',
    b64url = 'aHR0cHM6Ly9vZmZzaG9yZWdpdC5jb20vZXhvZHVzL3BsdWdpbi52aWRlby5leG9kdXMvcGx1Z2luLnZpZGVvLmV4b2R1cy0yLjAuOC56aXA=',
    zipmd5 = 'd1bf483d48be348c916fb95750b30e61',
    entryfile = 'exodus.py',
    version = '2.0.8'
)
libs = [
    dict(
        id = 'script.module.urlresolver',
        b64url = 'aHR0cHM6Ly9vZmZzaG9yZWdpdC5jb20vdHZhcmVzb2x2ZXJzL3R2YS1jb21tb24tcmVwb3NpdG9yeS9yYXcvbWFzdGVyL3ppcHMvc2NyaXB0Lm1vZHVsZS51cmxyZXNvbHZlci9zY3JpcHQubW9kdWxlLnVybHJlc29sdmVyLTMuMC4xOS56aXA=',
        zipmd5 = '4b78acc8d1f61cc7765071bbcbb8e09a',
        libpath = 'lib',
        version = '3.0.19'
    )
]
