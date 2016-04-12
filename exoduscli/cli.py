'''Utils for displaying stuff and getting user input
'''

import re
from getpass import getpass

_re_decorators = re.compile(r'\[B\]|\[/B\]|\[I\]|\[/I\]')

def select(items):
    '''Show list of strings
    Return index of item selected
    '''
    print '_'*(max(len(i) for i in items)+6)
    for idx, it in enumerate(items):
        it = _re_decorators.sub('', it)
        print '[% 3d] %s' % (idx, it)

    while True:
        try:
            idx = int(raw_input())
            if idx < len(items) and idx > -1:
                return idx
            raise IndexError
        except (EOFError, ValueError, IndexError):
            print 'Invalid input, try again'


def message(s):
    '''Print a string
    '''
    print _re_decorators.sub('', s)


def input(prompt, password=False):
    '''Get user input
    `password` to specify whether this is a password input
    '''
    if password:
        return getpass(prompt)
    else:
        return raw_input(prompt)
