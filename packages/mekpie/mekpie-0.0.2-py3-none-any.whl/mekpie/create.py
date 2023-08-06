from os.path import isdir, curdir, join
from os      import chdir
from os.path import basename, abspath, exists

import mekpie.messages as messages

from .util        import panic, empty, car, smkdir, exec_str
from .config      import config_from_dict
from .autodetect  import autodetect_compiler
from .definitions import DEFAULT_MEKPY, MAIN
from .structure   import (
    set_project_path,
    get_project_path,
    get_mekpy_path,
    get_src_path,
    get_main_path,
    get_test_path,
    get_includes_path,
    get_target_path,
    get_target_debug_path,
    get_target_release_path,
)

def command_new(options):
    name = project_name(options)
    check_name(name)
    create_project_directory(name)
    create_mekpy(name)
    create_src(name)
    create_tests()
    create_includes()
    create_target()
    config_from_dict(exec_str(get_mekpy_source(name), 'default mek.py', { 'options': options }), options)
    print(messages.created.format(name).strip())

def command_init(options):
    name = basename(abspath(curdir))
    check_name(name)
    create_mekpy(name)
    create_src(name)
    create_tests()
    create_includes()
    create_target()
    config_from_dict(exec_str(get_mekpy_source(name), 'default mek.py', { 'options': options }), options)
    print(messages.initialized.format(name).strip())

def check_name(name):
    if not name:
        panic(messages.name_cannot_be_empty)
    if isdir(name):
        panic(messages.name_cannot_already_exist.format(name))

def create_project_directory(name):
    set_project_path(name)
    smkdir(get_project_path())

def create_mekpy(name):
    if not exists(get_mekpy_path()):
        with open(get_mekpy_path(), 'w+') as rsc:
            rsc.write(get_mekpy_source(name))

def create_src(name):
    smkdir(get_src_path())
    if not exists(get_main_path(name + '.c')):
        with open(get_main_path(name + '.c'), 'w+') as rsc:
            rsc.write(get_main_source())

def create_tests():
    smkdir(get_test_path())

def create_includes():
    smkdir(get_includes_path())

def create_target():
    smkdir(get_target_path())
    smkdir(get_target_release_path())
    smkdir(get_target_debug_path())

def project_name(options):
    return car(options.commandargs)

def get_main_source():
    return MAIN + '\n'

def get_mekpy_source(name):
    cc, cmd, dbg = autodetect_compiler()
    return DEFAULT_MEKPY.format(name, name + '.c', cc, cmd, dbg)