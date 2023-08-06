from stdplus._readfile import readfile
from stdplus._sshConfig import *
from stdplus._writefile import writefile
from stdplus._fexecvp import fexecvp
from stdplus._fnmatches import fnmatches
from stdplus._removeRoot import removeRoot
from stdplus._run_cmd import *
from stdplus._defaultify import *
from stdplus._isInt import *
from stdplus._isString import *

import re

__all__ = [
    'contains',
    'defaultify',
    'defaultify',
    'defaultifyDict',
    'defaultifyDict',
    'elipsifyMiddle',
    'fexecvp',
    'fnmatches',
    'getSshHost',
    'isInt',
    'isIp',
    'isString',
    'keyscanHost',
    'readSshConfig',
    'readfile',
    'removeKnownHosts',
    'removeRoot',
    'resetKnownHost',
    'resetKnownHosts',
    'run',
    'run_cmd',
    'writefile'
]

def contains(small, big):
    for i in xrange(len(big)-len(small)+1):
        for j in xrange(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return i, i+len(small)
    return False

def isIp(string):
    return None != re.match("^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",string)

def elipsifyMiddle(s, n):
    if len(s) <= n:
        # string is already short-enough
        return s
    # half of the size, minus the 3 .'s
    n_2 = round(int(n) / 2 - 3)
    # whatever's left
    n_1 = round(n - n_2 - 3)
    return '{0}...{1}'.format(s[:n_1], s[-n_2:])
