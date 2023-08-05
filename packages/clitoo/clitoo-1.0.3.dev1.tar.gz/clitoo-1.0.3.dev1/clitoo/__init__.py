'''Clitoo makes your python callbacks work on CLI too !

This CLI can execute python callbacks with parameters.

Clitoo recognizes 4 types of command line arguments:

- lone arguments are passed as args
- arguments with = are passed as kwargs
- dashed arguments like -f arrive in context.args
- dashed arguments like -foo=bar arrive in context.kwargs

It doesn't matter how many dashes you put in the front, they are all
removed.

To use the context in your callback just import the clitoo context::

    from clitoo import context
    print(context.args, context.kwargs)

Clitoo provides 2 builtin commands: help and debug. Any other first
argument will be considered as the dotted path to the callback to import
and execute.

Examples:

clitoo help your.mod.funcname
    Print out the function docstring.

clitoo debug your.func -a --b --something='to see' how it=parses
    Dry run of your.mod with arguments, dump out actual calls.

clitoo your.mod.funcname with your=args
    Call your.mod.funcname('with', your='args').
'''

import inspect
import importlib
from pkg_resources import iter_entry_points
import traceback
import sys

import colored


class Context:
    """Args/kwargs starting with dash go in context."""

    def __init__(self, *args, **kwargs):
        self.args = list(args)
        self.kwargs = kwargs
        self.argv = []
        self.default_module = __name__

    @classmethod
    def factory(cls, argvs):
        context = cls()

        for argv in argvs:
            if not argv.startswith('-'):
                continue

            if argv == '--':
                context.args.append(sys.stdin.read().strip())
                continue

            context.argv.append(argv)
            argv = argv.lstrip('-')

            if '=' in argv:
                key, value = argv.split('=', 1)
                if value == '-':
                    value = sys.stdin.read().strip()
                context.kwargs[key] = value

            else:
                context.args.append(argv)

        return context

    def take(self, *names, **kwargs):
        """Pop argument or kwarg."""
        for name in names:
            if name in self.kwargs:
                return self.kwargs.pop(name)

            elif name in self.args:
                i = self.args.index(name)
                if i >= 0:
                    self.args.pop(i)
                    return True

        if 'default' in kwargs:
            return kwargs['default']


context = Context.factory(sys.argv)


class Callback:
    def __init__(self):
        self.path = None
        self.module = None
        self.modname = None
        self.funcname = None
        self.parts = None
        self.cb = None
        self.callables = None

    @classmethod
    def factory(cls, path, try_default=True):
        self = cls()
        self.path = path
        self.parts = self.path.split('.')

        for i, part in enumerate(self.parts):
            modname = '.'.join(self.parts[:i + 1])
            if not modname:
                return

            try:
                self.module = importlib.import_module(modname)
            except ImportError:
                break
            else:
                self.modname = modname

        ret = self.module
        for part in self.parts[i:]:
            if isinstance(ret, dict) and part in ret:
                ret = ret.get(part)
            elif isinstance(ret, list) and part.isnumeric():
                ret = ret[int(part)]
            else:
                ret = getattr(ret, part, None)

        if ret != self.module:
            self.cb = ret

        self.callables = [
            i[0]
            for i in inspect.getmembers(self.module)
            if callable(getattr(self.module, i[0]))
            and not isinstance(getattr(self.module, i[0]), type)
            and not i[0].startswith('_')
        ]

        if try_default and not self.cb:
            other_path = f'{context.default_module}.{path}'
            other = cls.factory(other_path, False)
            if other.cb:
                return other

        return self

    @property
    def filename(self):
        if self.modname:
            return importlib.find_loader(self.modname).get_filename()
        return False

    def __call__(self, *args, **kwargs):
        setup = getattr(self.module, '_clitoo_setup', None)
        if setup:
            setup()
        result = self.cb(*args, **kwargs)
        clean = getattr(self.module, '_clitoo_clean', None)
        if clean:
            clean()
        return result


def expand(*argv):
    """
    Extract args/kwargs not starting with dash.

    This will return a tuple of args and kwargs, making an arg of every argv
    that is passed alone, and a kwarg of any argv that contains = sign.

    For example:

        args, kwargs = expand('a', 'b=2', '-c', '--d=1')
        assert args == ['a']
        assert kwargs == {'b': '2'}

    """
    args, kwargs = list(), dict()

    for arg in argv:
        if arg == '-':
            args.append(sys.stdin.read().strip())
            continue

        if arg.startswith('-'):
            continue

        if '=' in arg:
            name, value = arg.split('=', 1)
            if value == '-':
                value = sys.stdin.read().strip()
            kwargs[name] = value
        else:
            args.append(arg)

    return args, kwargs


def filedoc(filepath):
    """Return the documentation for a file."""
    co = compile(open(filepath).read(), filepath, 'exec')
    if co.co_consts and isinstance(co.co_consts[0], str):
        docstring = co.co_consts[0]
    else:
        docstring = None
    return docstring


def help(cb=None):
    """
    Get help for a callable, or list callables for a module.

    Example::

        $ clitoo help foo.bar
    """
    cb = Callback.factory(cb or context.default_module)

    def _modhelp():
        if cb.filename:
            moddoc = filedoc(cb.filename)

        if moddoc:
            print(moddoc)
        else:
            print(f'{colored.fg(208)}'
                  f'No module docstring found for {cb.path}'
                  f'{colored.attr(0)}')

        try:
            importlib.import_module(cb.modname)
        except ImportError:
            traceback.print_exc()
            print(f'Could not import module: {cb.modname}')
        else:
            if cb.callables:
                print(f'{colored.fg(208)}'
                      f'[Callables in {cb.filename}]'
                      f'{colored.attr(0)}\n')

                for i in cb.callables:
                    print(f'{colored.fg(2)}- {i}{colored.attr(0)}')

                print(f'\n{colored.fg(208)}Try {sys.argv[0].split("/")[-1]}'
                      f' help callable_name{colored.attr(0)}')
            else:
                print(f'No callable found in {cb.filename}')

        if not moddoc and not cb.callables:
            print('No help found')

    if cb.cb:
        funcdoc = inspect.getdoc(cb.cb)

        if funcdoc:
            print(funcdoc)
        else:
            print(f'No docstring found for {cb.path}')
            _modhelp()
    else:
        _modhelp()


def debug(*args, **kwargs):
    """Print debug output for a command line.

    The debug function is made to dump the result of the clilabs parser.
    It will show what callable and arguments it will use.
    You will see that the following are not the same, as stated in the
    tutorial::

        clitoo debug your.func -x 12
        clitoo debug your.func -x=12
    """
    if not args:
        return print('Argument argument required ie. clilabs debug your.func')

    cb = Callback.factory(args[0])
    if not cb.cb:
        print(f'Could not import {args[0]} nor {cb.path}')
    else:
        print(f'Callable: {cb.cb}')
        print(f'Callable path: {cb.cb.__code__.co_filename}')

    print(f'Args: {args[1:]}')
    print(f'Kwargs: {kwargs}')
    print(f'Context args: {context.args}')
    print(f'Context kwargs: {context.kwargs}')


def main(argv=None, default_path=None):
    argv = argv if argv is not None else sys.argv[1:]
    path = argv[0] if argv else default_path or 'clitoo.help'
    default_path = default_path or 'clitoo.help'

    # hack allowing the caller to not define it in their module
    if path == 'help':
        path = 'clitoo.help'

    callback = Callback.factory(path)
    if not callback.cb:
        callback = Callback.factory(default_path)

    args, kwargs = expand(*argv[1:])
    return callback(*args, **kwargs)


def console_script(*argv):
    argv = argv or sys.argv
    entry_point = argv[0].split('/')[-1]
    callback = None
    for i in iter_entry_points(entry_point):
        entry_parts = i.name.split(' ')
        entry_count = len(entry_parts)
        if entry_parts == [entry_point] + argv[1:entry_count]:
            callback = Callback.factory(f'{i.module_name}.{".".join(i.attrs)}')
            break

    if not callback:
        for i in iter_entry_points(entry_point):
            entry_parts = i.name.split(' ')
            return help(i.module_name)

    if not callback.cb:
        raise Exception(f'notfound {callback}')

    args, kwargs = expand(*argv[entry_count:])
    return callback(*args, **kwargs)
