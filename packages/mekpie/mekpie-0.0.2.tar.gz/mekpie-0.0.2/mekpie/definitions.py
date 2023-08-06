from collections import namedtuple

Option = namedtuple('Option', [
    'names',
    'nargs',
    'handler',
])

Options = namedtuple('Options', [
    'quiet',       # -q --quiet
    'verbose',     # -v --verbose
    'release',     # -r --release
    'developer',   # -d --developer
    'changedir',   # -c --changedir
    'command',     # new, init, clean, build, run, test, debug
    'commandargs', # <optionargs...>
    'programargs', # -- <programargs...>
])

Config = namedtuple('Config', [
    'name',                   # Project name
    'main',                   # Entry point
    'libs',                   # Libraries to link
    'cc',                     # C Compiler Configuration
    'cmd',                    # The C Compiler command
    'dbg',                    # Debugger
    'flags',                  # User compiler flags
    'override_debug_flags',   # Override config debug flags 
    'override_release_flags', # Override config release flags
    'options',                # The provided command line options
])

CC_CMDS = {
    'clang' : ('gcc/clang', 'clang', 'lldb'),
    'gcc'   : ('gcc/clang', 'gcc',   'gdb'), 
}

DEFAULT_MEKPY='''
# This is a standard configuration file for mekpie

# the name of your project
name = '{}' 
# the .c file containing `main`
main = '{}'
# any libraries to load
libs = []
# the c compiler configuration to use (gcc/clang)
cc = '{}'
# the c compiler command to use on the command line
cmd = '{}'
# the debugger to use
dbg = '{}'
# additional compiler flags
flags = ['-Wall']
# Provide a list to override the c compiler configuration default
override_debug_flags = None
# Provide a list to override the c compiler configuration default
override_release_flags = None

if options.release:
    pass # this code will only run for release builds
else:
    pass # this code will only run for debug builds
'''

MAIN = '''
#include <stdio.h>
#include <stdlib.h>

int main() {
    puts("Hello, World!");
    return EXIT_SUCCESS;
}
'''.strip()

VERSION = '0.0.1'