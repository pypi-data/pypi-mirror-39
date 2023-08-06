from re      import sub
from os      import walk, mkdir
from sys     import stderr
from shutil  import rmtree
from os.path import isfile, isdir, join, basename, splitext, exists
from filecmp import dircmp

import mekpie.debug    as debug
import mekpie.messages as messages

# Debug
# ---------------------------------------------------------------------------- #

def panic(message=None):
    if message is None:
        exit(1)
    errprint(f'\n{message.strip()}\n\n')
    raise Exception('Debug') if debug.debug else exit(1)

def log(message):
    errprint(f' -- {tab(str(message)).strip()}\n') if debug.debug else None
    return message

def errprint(string):
    stderr.write(string)
    stderr.flush()

# Collections
# ---------------------------------------------------------------------------- #

def empty(collection):
    return len(collection) == 0

def car(collection):
    if not empty(collection):
        return collection[0]

def last(collection):
    if not empty(collection):
        return collection[-1]

def cdr(collection):
    if not empty(collection):
        return collection[1:]

def cons(item, collection):
    return [item] + collection

def shift(collection, n=1):
    for _ in range(n):
        if not empty(collection):
            collection.pop(0)

def flatten(collection):
    return sum(collection, [])

def split(collection, item):
    if item not in collection:
        return collection, []
    index  = collection.index(item)
    first  = collection[:index]
    second = collection[index + 1:] 
    return first, second


# Strings
# ---------------------------------------------------------------------------- #

def tab(string, spaces=4):
    return sub(r'^|\n', '\n' + (spaces * ' '), string)

def underline(element, collection):
    top    = ' '.join(collection)
    bottom = ' '.join(underlined_collection(element, collection))
    return f'{top}\n{bottom}'

def underlined_collection(underlined_element, collection):
    def underline_or_hide(element):
        rep = '^' if element == underlined_element else ' '
        return sub(r'.', rep, str(element))
    return map(underline_or_hide, collection)

# Files
# ---------------------------------------------------------------------------- #

def smkdir(path):
    if not exists(path):
        mkdir(path)

def srmtree(path):
    if exists(path):
        rmtree(path)

def list_files(path, with_filter=None, with_ext=None, recursive=False):
    if with_filter is None:
        with_filter = lambda _ : True
    if with_ext is not None:
        with_filter = lambda filename : filename.endswith(with_ext)
    return list(filter(with_filter, list_all_files(path)))

def list_all_files(path):
    return flatten([[join(pre, post)
            for post
            in posts]
        for (pre, _, posts)
        in walk(path)
    ])

def filename(path):
    return splitext(basename(path))[0]

def file_as_str(path):
    log(f'Reading the contents of {path}...')
    with open(path) as resource:
        return resource.read()

def remove_contents(path):
    log(f'Deleting the contents of {path}...')
    srmtree(path)
    smkdir(path)

def check_is_file(path):
    if isfile(path):
        return path
    panic(messages.file_not_found.format(path))

def check_is_dir(path):
    if isdir(path):
        return path
    panic(messages.directory_not_found.format(path))

def same_dir(dir1, dir2):
    def recursive(dcmp):
        if dcmp.diff_files:
            return False
        return all([recursive(sub_dcmp)
            for sub_dcmp
            in dcmp.subdirs.values()
        ])
    return recursive(dircmp(dir1, dir2))

def exec_str(source, handle, ctx={}):
    try:
        exec(source, ctx)
    except Exception as err:
        panic(messages.execution_error.format(handle, tab(str(err))))
    return ctx

def exec_file(path, ctx={}):
    return exec_str(file_as_str(path), path, ctx)

# Types
# ---------------------------------------------------------------------------- #

def type_name(x):
    return type(x).__name__
