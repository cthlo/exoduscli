from os import path
__dir__ = path.abspath(path.dirname(__file__))

specialroot = path.join(__dir__, 'fakexbmc', 'special')
addonsdir = path.join(__dir__, 'addons')
logfile = path.join(__dir__, 'fakexbmc.log')
exodus = dict(
    id = 'plugin.video.exodus',
    b64url = 'aHR0cHM6Ly9vZmZzaG9yZWdpdC5jb20vZXhvZHVzL3BsdWdpbi52aWRlby5leG9kdXMvcGx1Z2luLnZpZGVvLmV4b2R1cy0xLjMuMC56aXA=',
    zipmd5 = 'b7d6e9dbf5041425eb3261d9261f37f0',
    entryfile = 'default.py',
    version = '1.3.0'
)
libs = [
    dict(
        id = 'script.module.urlresolver',
        b64url = 'aHR0cHM6Ly9vZmZzaG9yZWdpdC5jb20vdHZhcmVzb2x2ZXJzL3R2YS1jb21tb24tcmVwb3NpdG9yeS9yYXcvbWFzdGVyL3ppcHMvc2NyaXB0Lm1vZHVsZS51cmxyZXNvbHZlci9zY3JpcHQubW9kdWxlLnVybHJlc29sdmVyLTMuMC4wLnppcA==',
        zipmd5 = 'a72aea526e516d12dffecfe7a981aa3c',
        libpath = 'lib',
        version = '3.0.0'
    )
]
