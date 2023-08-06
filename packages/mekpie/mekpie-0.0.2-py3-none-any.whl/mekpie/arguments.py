import mekpie.debug    as debug
import mekpie.messages as messages

from .create      import command_new, command_init
from .definitions import Options, Option

from .util import (
    car,
    cdr,
    tab,
    split,
    empty,
    panic,
    underline,
)
from .compiler import (
    command_run,
    command_test,
    command_clean,
    command_build,
    command_debug,
)

def command_help(cfg):
    print(messages.usage)

def command_version(cfg):
    print(messages.version)

def pre_config_commands():
    return [
        command_help,
        command_version,
        command_new,
        command_init,
    ]

def default_options():
    return Options(
        quiet       = False,
        verbose     = False,
        release     = False,
        developer   = False,
        changedir   = False,
        command     = None,
        commandargs = [],
        programargs = [],
    )

def available_options():
    return [
        flag('quiet',            ['-q', '--quiet']),
        flag('verbose',          ['-v', '--verbose']),
        flag('release',          ['-r', '--release']),
        flag('developer',        ['-d', '--developer']),
        flag('changedir',        ['-c', '--changedir'], 2),
        command(command_help,    ['-h', '--help', 'help']),
        command(command_version, ['-V', '--version', 'version']),
        command(command_new,     ['new']),
        command(command_init,    ['init']),
        command(command_clean,   ['clean']),
        command(command_build,   ['build']),
        command(command_run,     ['run']),
        command(command_test,    ['test']),
        command(command_debug,   ['debug']),
    ]

def parse_arguments(args):
    argsall = args[:]
    options = default_options()._asdict()
    args, programargs = split(args, '--')
    options['programargs'] = programargs
    while not empty(args):
        arg = car(args)
        for names, nargs, handler in available_options():
            if arg in names:
                handler(options, args[:nargs], argsall)
                args = args[nargs:] if nargs else []
                break
        else:
            argument_error(messages.unknown_argument, car(args), argsall)
    return Options(**options)

def flag(name, aliases, nargs=1):

    def handle_flag(options, args, argsall):
        if options[name]:
            argument_error(messages.repeated_option.format(name), name, argsall)
        else:
            options[name] = cdr(args) or True

    return Option(
        names   = aliases,
        nargs   = nargs,
        handler = handle_flag,
    )

def command(command, aliases):

    def handle_command(options, args, argsall):
        if options['command']:
            argument_error(messages.too_many_arguments, command, argsall)
        else:
            options['commandargs'] = cdr(args)
            options['command']    = command

    return Option(
        names   = aliases,
        nargs   = None,
        handler = handle_command,
    )

def argument_error(message, arg, args):
    args = ['mekpie'] + args
    panic(f'{message}\n{tab(underline(arg, args))}')