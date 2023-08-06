from os.path import join

import mekpie.messages as messages

from .definitions import Config
from .util        import panic, tab, check_is_file, check_is_dir, type_name, exec_file
from .structure   import get_main_path, get_mekpy_path

def get_config(options):
    return config_from_dict(exec_file(get_mekpy_path(), { 'options': options }), options)

def config_from_dict(config_dict, options):
    return check_config(Config(
        name                   = config_dict.get('name',                   None),
        main                   = config_dict.get('main',                   None),
        libs                   = config_dict.get('libs',                   []),
        cc                     = config_dict.get('cc',                     'gcc/clang'),
        cmd                    = config_dict.get('cmd',                    'cc'),
        dbg                    = config_dict.get('dbg',                    'gdb'),
        flags                  = config_dict.get('flags',                  []),
        override_debug_flags   = config_dict.get('override_debug_flags',   None),
        override_release_flags = config_dict.get('override_release_flags', None),
        options                = options,
    ))

def check_config(config):
    check_name(config.name)
    check_main(config)
    check_libs(config.libs)
    check_cc(config.cc)
    check_cmd(config.cc)
    check_dbg(config.dbg)
    check_flags(config.flags)
    check_override_debug_flags(config.override_debug_flags)
    check_override_release_flags(config.override_release_flags)
    return config

def check_name(name):
    check_type('name', name, str)

def check_main(config):
    check_type('main', config.main, str)
    check_is_file(get_main_path(config.main))

def check_libs(libs):
    check_type('libs', libs, list)
    for lib in libs:
        check_type('libs', lib, str)

def check_cc(cc):
    check_type('cc', cc, str)

def check_cmd(cmd):
    check_type('cmd', cmd, str)

def check_dbg(dbg):
    check_type('dbg', dbg, str)

def check_flags(flags):
    check_type('flags', flags, list)
    for flag in flags:
        check_type('flags', flag, str)

def check_override_debug_flags(flags):
    if flags is not None:
        check_type('override_debug_flags', flags, list)
        for flag in flags:
            check_type('override_debug_flags', flag, str)

def check_override_release_flags(flags):
    if flags is not None:
        check_type('override_release_flags', flags, list)
        for flag in flags:
            check_type('override_release_flags', flag, str)

def check_type(name, value, *expected_types):
    if all([type(value) != exp for exp in expected_types]):
        panic(messages.type_error.format(
            name,
            ' or '.join([exp.__name__ for exp in expected_types]),
            type_name(value),
            tab(get_description(name))
        ))

def get_description(name):
    return {
        'name'                   : '`name` specifies the name of the project',
        'main'                   : '`main` specifies the .c file continaing `main`',
        'libs'                   : '`libs` speicfies and libraries to load',
        'cc'                     : '`cc` specifies the c compiler configuration to use',
        'cmd'                    : '`cmd` specified the c compiler command',
        'dbg'                    : '`dbg` specifies the debugger to use',
        'flags'                  : '`flags` specifies additional compiler flags',
        'override_debug_flags'   : '`override_debug_flags` overrides debug flags',
        'override_release_flags' : '`override_release_flags` overrides release flags',
    }[name]