# -*- coding: utf-8 -*-
"""This module implements some main features for using *HydPy* from
your command line tools via script |hyd|."""
# import...
# ...from standard library
from typing import IO
import contextlib
import datetime
import inspect
import os
import sys
# ...from hydpy
from hydpy import pub
from hydpy.core import autodoctools
from hydpy.core import objecttools


def exec_commands(commands, *, logfile: IO, **parameters) -> None:
    """Execute the given Python commands.

    Function |exec_commands| is thought for testing purposes only (see
    the main documentation on module |hyd|).  Seperate individual commands
    by semicolons and replaced whitespaces with underscores:

    >>> from hydpy.exe.commandtools import exec_commands
    >>> import sys
    >>> exec_commands("x_=_1+1;print(x)", logfile=sys.stdout)
    Start to execute the commands ['x_=_1+1', 'print(x)'] for testing purposes.
    2

    |exec_commands| interprets double underscores as a single underscores:

    >>> exec_commands("x_=_1;print(x.____class____)", logfile=sys.stdout)
    Start to execute the commands ['x_=_1', 'print(x.____class____)'] \
for testing purposes.
    <class 'int'>

    |exec_commands| evaluates additional keyword arguments before it
    executes the given commands:

    >>> exec_commands("e=x==y;print(e)", x=1, y=2, logfile=sys.stdout)
    Start to execute the commands ['e=x==y', 'print(e)'] for testing purposes.
    False
    """
    cmdlist = commands.split(';')
    logfile.write(
        f'Start to execute the commands {cmdlist} for testing purposes.\n')
    for par, value in parameters.items():
        exec(f'{par} = {value}')
    for command in cmdlist:
        command = command.replace('__', 'temptemptemp')
        command = command.replace('_', ' ')
        command = command.replace('temptemptemp', '_')
        exec(command)


pub.scriptfunctions['exec_commands'] = exec_commands


def print_latest_logfile(dirpath='.'):
    """Print the latest log file in the current or the given working directory.

    See the main documentation on module |hyd| for more information.
    """
    filenames = []
    for filename in os.listdir(dirpath):
        if filename.startswith('hydpy_') and filename.endswith('.log'):
            filenames.append(filename)
    if not filenames:
        raise FileNotFoundError(
            f'Cannot find a HydPy log file in directory '
            f'{os.path.abspath(dirpath)}.')
    with open(sorted(filenames)[-1]) as logfile:
        print(logfile.read())


def prepare_logfile(filename=None):
    """Prepare an empty log file and return its absolute path.

    If not given, |prepare_logfile| generates a filename containing
    the actual date and time:

    >>> from hydpy.exe.commandtools import prepare_logfile
    >>> from hydpy import repr_, TestIO
    >>> from hydpy.core.testtools import mock_datetime_now
    >>> from datetime import datetime
    >>> with TestIO():
    ...     with mock_datetime_now(datetime(2000, 1, 1, 12, 30, 0)):
    ...         filepath = prepare_logfile()
    >>> import os
    >>> os.path.exists(filepath)
    True
    >>> repr_(filepath)    # doctest: +ELLIPSIS
    '...hydpy/tests/iotesting/hydpy_2000-01-01_12-30-00.log'

    To given filenames,  |prepare_logfile| does not add any date or time
    information:
    >>> with TestIO():
    ...     with mock_datetime_now(datetime(2000, 1, 1, 12, 30, 0)):
    ...         filepath = prepare_logfile('my_log_file.txt')
    >>> os.path.exists(filepath)
    True
    >>> repr_(filepath)    # doctest: +ELLIPSIS
    '...hydpy/tests/iotesting/my_log_file.txt'
    """
    if filename is None:
        filename = datetime.datetime.now().strftime(
            'hydpy_%Y-%m-%d_%H-%M-%S.log')
    with open(filename, 'w'):
        pass
    return os.path.abspath(filename)


def execute_scriptfunction():
    """Execute a HydPy script function.

    Function |execute_scriptfunction| is indirectly applied and
    explained in the documentation on module |hyd|.
    """
    try:
        args_given = []
        kwargs_given = {}
        for arg in sys.argv[1:]:
            try:
                key, value = parse_argument(arg)
                kwargs_given[key] = value
            except ValueError:
                args_given.append(arg)
        logfilepath = prepare_logfile(kwargs_given.pop('logfile', None))
        logstyle = kwargs_given.pop('logstyle', 'plain')
        try:
            funcname = str(args_given.pop(0))
        except IndexError:
            raise ValueError(
                'The first positional argument defining the function '
                'to be called is missing.')
        try:
            func = pub.scriptfunctions[funcname]
        except KeyError:
            raise ValueError(
                f'There is no `{funcname}` function callable by `hyd.py`.  '
                f'Choose one of the following instead: '
                f'{objecttools.enumeration(pub.scriptfunctions.keys())}')
        args_required = inspect.getfullargspec(func).args
        nmb_args_required = len(args_required)
        nmb_args_given = len(args_given)
        if nmb_args_given != nmb_args_required:
            enum_args_given = ''
            if nmb_args_given:
                enum_args_given = (
                    f' ({objecttools.enumeration(args_given)})')
            enum_args_required = ''
            if nmb_args_required:
                enum_args_required = (
                    f' ({objecttools.enumeration(args_required)})')
            raise ValueError(
                f'Function `{funcname}` requires `{nmb_args_required:d}` '
                f'positional arguments{enum_args_required}, but '
                f'`{nmb_args_given:d}` are given{enum_args_given}.')
        try:
            with open(logfilepath, 'a') as logfile:
                sys.stdout = LogFileInterface(logfile, logstyle, 'info')
                sys.stderr = LogFileInterface(logfile, logstyle, 'warning')
                func(*args_given, **kwargs_given, logfile=sys.stdout)
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
    except BaseException as exc:
        with open(logfilepath, 'a') as logfile:
            if logstyle not in LogFileInterface.style2infotype2string:
                logstyle = 'plain'
            interface = LogFileInterface(logfile, logstyle, 'exception')
            arguments = ', '.join(sys.argv)
            interface.write(
                f'Invoking hyd.py with arguments `{arguments}` '
                f'resulted in the following error:\n{str(exc)}\n')


class LogFileInterface(object):
    """Wraps a usual file object, exposing all its methods while modifying
    only the `write` method.

    At the moment, class |LogFileInterface| only supports only two log
    styles, as explained in the documentation on module |hyd|.  The
    following example shows its basic usage:

    >>> from hydpy import TestIO
    >>> from hydpy.exe.commandtools import LogFileInterface
    >>> with TestIO():
    ...     logfile = open('test.log', 'w')
    >>> lfi = LogFileInterface(
    ...     logfile, logstyle='prefixed', infotype='exception')
    >>> lfi.write('a message\\n')
    >>> lfi.write('another message\\n')
    >>> lfi.close()
    >>> with TestIO():
    ...     with open('test.log', 'r') as logfile:
    ...         print(logfile.read())
    error: a message
    error: another message
    <BLANKLINE>

    The class member `style2infotype2string` defines the currently
    available log styles.
    """

    style2infotype2string = {
        'plain': {'info': '',
                  'warning': '',
                  'exception': ''},
        'prefixed': {'info': 'info: ',
                     'warning': 'warning: ',
                     'exception': 'error: '}}

    def __init__(self, logfile: IO, logstyle: str, infotype: str):
        self.logfile = logfile
        try:
            stdtype2string = self.style2infotype2string[logstyle]
        except KeyError:
            styles = objecttools.enumeration(
                sorted(self.style2infotype2string.keys()))
            raise ValueError(
                f'The given log file style {logstyle} is not available.  '
                f'Please choose one of the following: {styles}.')
        self._string = stdtype2string[infotype]

    def write(self, string):
        self.logfile.write('\n'.join(
            f'{self._string}{substring}' if substring else ''
            for substring in string.split('\n')))

    def __getattr__(self, name):
        return getattr(self.logfile, name)


def parse_argument(string):
    """Return a single value for a string understood as a positional
    argument or a |tuple| containing a keyword and its value for a
    string understood as a keyword argument.

    |parse_argument| is intended to be used as a helper function for
    function |execute_scriptfunction| only.  See the following
    examples to see which types of keyword arguments |execute_scriptfunction|
    covers:

    >>> from hydpy.exe.commandtools import parse_argument
    >>> parse_argument('x=3')
    ('x', '3')
    >>> parse_argument('"x=3"')
    '"x=3"'
    >>> parse_argument("'x=3'")
    "'x=3'"
    >>> parse_argument('x="3==3"')
    ('x', '"3==3"')
    >>> parse_argument("x='3==3'")
    ('x', "'3==3'")
    """
    idx_equal = string.find('=')
    if idx_equal == -1:
        return string
    idx_quote = idx_equal+1
    for quote in ('"', "'"):
        idx = string.find(quote)
        if -1 < idx < idx_quote:
            idx_quote = idx
    if idx_equal < idx_quote:
        return string[:idx_equal], string[idx_equal+1:]
    return string


autodoctools.autodoc_module()
