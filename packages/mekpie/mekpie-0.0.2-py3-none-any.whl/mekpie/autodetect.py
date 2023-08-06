from os     import name
from shutil import which

import mekpie.messages as messages

from .util        import panic, log
from .definitions import CC_CMDS

def autodetect_compiler():
    for cmd in CC_CMDS.keys():
        if defined(cmd):
            return CC_CMDS[cmd]
    panic(messages.failed_autodetect)

def defined(name):
    return which(name) is not None