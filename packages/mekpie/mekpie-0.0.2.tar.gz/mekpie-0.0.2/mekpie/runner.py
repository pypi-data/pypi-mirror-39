from sys        import stdout, stderr
from subprocess import run, PIPE

import mekpie.messages as messages

from .util import panic, log

def lrun(args, quiet=False, error=True):
    log('Running...\n' + serialize_command(args))
    try:
        if quiet:
            if run(args, stdout=PIPE, stderr=PIPE).returncode != 0:
                raise OSError
        else:
            if run(args).returncode != 0:
                raise OSError
    except KeyboardInterrupt:
        exit()
    except OSError:
        if error:
            panic(messages.failed_program_call.format(serialize_command(args)))

def serialize_command(args):
    return '$ ' + ' '.join(args)
