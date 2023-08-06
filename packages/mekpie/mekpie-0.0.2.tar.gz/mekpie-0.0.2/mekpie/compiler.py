from os.path     import join
from collections import namedtuple

import mekpie.messages as messages

from .util         import panic, list_files, remove_contents, filename
from .runner       import lrun
from .structure    import (
    get_test_path,
    get_target_path,
    get_target_debug_path,
    get_target_release_path,
    get_main_path,
    get_src_path,
    get_includes_path,
)

def command_clean(cfg):
    remove_contents(get_target_debug_path())
    remove_contents(get_target_release_path())
    if not cfg.options.quiet:
        print(messages.clean.strip())

def command_build(cfg):
    command_clean(cfg)
    sources = get_sources(cfg)
    mains   = [get_main_path(cfg.main), *list_files(get_test_path(), with_ext='.c')]
    for main in mains:
        compiler_configs[cfg.cc](cfg, sources, main)
    if not cfg.options.quiet:
        print(messages.build_succeeded.strip())

def command_run(cfg):
    command_build(cfg)
    lrun([get_bin_path(cfg, get_main_path(cfg.main))] + cfg.options.programargs)

def command_debug(cfg):
    if cfg.options.release:
        panic(messages.release_debug)
    command_build(cfg)
    lrun([cfg.dbg, get_bin_path(cfg, get_main_path(cfg.main))])

def command_test(cfg):
    command_build(cfg)
    for test in get_tests(cfg):
        lrun([get_bin_path(cfg, test)])

def get_tests(cfg):
    return list_files(get_test_path(), with_filter=lambda test : 
        test.endswith('.c')  and 
        (filename(test) in cfg.options.commandargs or len(cfg.options.commandargs) == 0)
    )

def get_bin_path(cfg, main):
    root = get_target_release_path() if cfg.options.release else get_target_debug_path()
    return join(root, filename(main))

def get_sources(cfg):
    sources = list_files(get_src_path(), with_ext='.c')
    sources.remove(get_main_path(cfg.main))
    return sources

# Compiler Configs
# ---------------------------------------------------------------------------- #

def gcc_clang_config(cfg, sources, main):
    sources = sources + [main]
    debug_flags = (['-g'] 
        if cfg.override_debug_flags is None 
        else cfg.override_debug_flags)
    release_flags = (['-O'] 
        if cfg.override_release_flags is None      
        else cfg.override_release_flags)
    flags = cfg.flags + (release_flags 
        if cfg.options.release 
        else debug_flags)
    flags = flags + (['-v']        
        if cfg.options.verbose 
        else [])
    libs = ['-l' + lib for lib in cfg.libs]
    lrun([
        cfg.cmd, 
        *sources,
        *flags, 
        *libs,
        '-I' + get_includes_path(), 
        '-o', get_bin_path(cfg, main)
    ])

compiler_configs = {
    'gcc/clang' : gcc_clang_config,
}