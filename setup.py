import sys
from setuptools import setup

if sys.version_info < (2, 6) or sys.version_info >= (3, ):
    print('Python2 (>= 2.6) is required')
    sys.exit(1)

setup(
    name         = 'exoduscli',
    version      = '0.0.0',
    url          = 'https://github.com/cthlo/exoduscli',
    author       = 'cthlo',
    license      = 'MIT',
    packages     = ['exoduscli', 'exoduscli.fakexbmc', 'exoduscli.lib'],
    entry_points = {
        'console_script': [
            'exoduscli = exoduscli.main:main'
        ]
    }
)
