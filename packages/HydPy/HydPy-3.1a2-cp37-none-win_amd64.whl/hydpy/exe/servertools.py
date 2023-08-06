# -*- coding: utf-8 -*-
"""



>>> from hydpy.core.examples import prepare_full_example_1
>>> prepare_full_example_1()

>>> from hydpy import run_subprocess, TestIO
>>> import subprocess
>>> with TestIO():
...     process = subprocess.Popen(
...         'hyd.py start_server 8080 LahnH 1996-01-01 1996-01-06 1d',
...         shell=True)
...     run_subprocess('hyd.py await_server 8080 10', verbose=False)

>>> from urllib import request
>>> from hydpy import Date, print_values
>>> t0 = Date('1996-01-01')
>>> def test(id_, time_, alpha):
...     content = (f"alpha= [{alpha}] \\n"
...                f"firstdate = {t0+f'{int(time_[0])}d'}\\n"
...                f"lastdate = {t0+f'{int(time_[2])}d'}\\n"
...                f"dill.discharge=[0.0] \\n"
...                f"lahn_1.discharge=[0.0]").encode('utf-8')
...     for methodname in (
...             'simperiod', 'parameteritems', 'load_conditionvalues',
...             'conditionitems', 'simulate', 'save_conditionvalues',
...             'seriesitems'):
...         url = f'http://localhost:8080/{methodname}?id={id_}'
...         if methodname in ('simperiod', 'parameteritems', 'conditionitems'):
...             response = request.urlopen(url, data=content)
...         else:
...             response = request.urlopen(url)
...         result = response.read()
...     lines = str(result, encoding='utf-8').split('\\n')
...     for line in lines:
...         if line.startswith('dill.discharge'):
...             values = eval(line.split('=')[1])
...             print_values(values)

Single simulation run:

>>> test(id_='workingdir1', time_=[0.0,1.0,5.0], alpha=2.0)
35.250827, 7.774062, 5.035808, 4.513706, 4.251594

Multiple interlockingsimulation runs:

>>> test(id_='workingdir2', time_=[0.0,1.0,1.0], alpha=2.0)
35.250827

>>> test(id_='workingdir3', time_=[0.0,1.0,3.0], alpha=2.0)
35.250827, 7.774062, 5.035808

>>> test(id_='workingdir2', time_=[1.0,1.0,5.0], alpha=2.0)
7.774062, 5.035808, 4.513706, 4.251594

Parallel runs with different parameterisations:

>>> test(id_='workingdir4', time_=[0.0,1.0,3.0], alpha=2.0)
35.250827, 7.774062, 5.035808

>>> test(id_='workingdir5', time_=[0.0,1.0,3.0], alpha=1.0)
11.658511, 8.842278, 7.103614

>>> test(id_='workingdir4', time_=[3.0,1.0,5.0], alpha=2.0)
4.513706, 4.251594

>>> test(id_='workingdir5', time_=[3.0,1.0,5.0], alpha=1.0)
6.00763, 5.313751

>>> test(id_='workingdir1', time_=[0.0, 1.0, 5.0], alpha=1.0)
11.658511, 8.842278, 7.103614, 6.00763, 5.313751


>>> _ = request.urlopen('http://localhost:8080/close_server')
>>> process.kill()
>>> _ = process.communicate()
"""
# import...
# ...from standard library
import collections
import http.server
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict
# ...from HydPy
from hydpy import pub
from hydpy.core import autodoctools
from hydpy.core import objecttools
from hydpy.core import hydpytools


class ServerState(object):

    def __init__(self):
        self.hp: hydpytools.HydPy = None
        self.conditions: collections.defaultdict = None
        self.init_conditions: dict = None
        self.id_: str = None
        self.idx1: int = None
        self.idx2: int = None
        self.inputs: Dict[str, str] = None
        self.outputs: Dict[str, Any] = None

    def initialize(self, projectname):
        self.hp = hydpytools.HydPy(projectname)
        hp = self.hp
        pub.options.printprogress = False
        hp.prepare_network()
        hp.init_models()
        hp.prepare_simseries()
        hp.prepare_modelseries()
        hp.load_inputseries()
        hp.load_conditions()
        self.conditions = collections.defaultdict(lambda: {})
        self.init_conditions = hp.conditions


state = ServerState()

        
class HydPyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """ToDo

    >>> from hydpy.core.examples import prepare_full_example_1
    >>> prepare_full_example_1()
    >>> from hydpy import run_subprocess, TestIO
    >>> import subprocess
    >>> with TestIO():
    ...     process = subprocess.Popen(
    ...         'hyd.py start_server 8080 LahnH 1996-01-01 1996-01-06 1d',
    ...         shell=True)
    ...     run_subprocess('hyd.py await_server 8080 10', verbose=False)

    >>> from urllib import request
    >>> def test(methodname, data=None):
    ...     url = f'http://localhost:8080/{methodname}?id=ID'
    ...     if data is not None:
    ...         data = bytes(data, encoding='utf-8')
    ...     print(str(request.urlopen(url, data=data).read(), encoding='utf-8'))
    >>> test('status')
    status = ready

    >>> test('parameteritemtypes')
    alpha = DoubleItem1D(1)
    >>> test('conditionitemtypes')
    lz = DoubleItem0D()
    >>> test('seriesitemtypes')
    dill = DoubleItem1D(5)
    lahn_1 = DoubleItem1D(5)

    >>> test('inittimegrid')
    firstdate = 1996-01-01 00:00:00
    lastdate = 1996-01-06 00:00:00
    stepsize = 1d

    >>> test('simperiod',
    ...      ('firstdate = 1996-01-01 00:00:00\\n'
    ...       'lastdate = 1996-01-02 00:00:00'))
    <BLANKLINE>

    >>> test('parameteritems', 'alpha = [3.0]')
    <BLANKLINE>
    >>> test('conditionitems', 'lz = [10.0]')
    <BLANKLINE>
    >>> test('seriesitems',
    ...      'dill.discharge = [5.0]\\n'
    ...      'lahn_1.discharge = [6.0]')
    <BLANKLINE>

    >>> test('parameteritems')
    alpha = [3.0]
    >>> test('conditionitems')
    lz = [10.0]
    >>> test('seriesitems')
    dill.discharge = [5.0]
    lahn_1.discharge = [6.0]

    >>> test('close_server')
    shutting down server
    >>> process.kill()
    >>> _ = process.communicate()
    """

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    @staticmethod
    def bstring2dict(bstring: bytes) -> Dict[str, str]:
        """Parse the given bytes string into an |collections.OrderedDict|
        and return it.

        Different items must be separated by newline characters; keys and
        values must be seperated by "="; an arbitrary number of
        whitespaces is allowed:

        >>> from hydpy.exe.servertools import HydPyHTTPRequestHandler
        >>> HydPyHTTPRequestHandler.bstring2dict(b'var1 = 1\\nvar2=  [2]\\n')
        OrderedDict([('var1', '1'), ('var2', '[2]')])
        """
        inputs = collections.OrderedDict()
        for line in str(bstring, encoding='utf-8').split('\n'):
            line = line.strip()
            if line:
                key, value = line.split('=')
                inputs[key.strip()] = value.strip()
        return inputs

    @staticmethod
    def dict2bstring(dict_: Dict[str, Any]) -> bytes:
        """Unparse the given dictionary into a bytes string and return it.

        See the following example and the documentation on method
        |HydPyHTTPRequestHandler.bstring2dict|:

        >>> from hydpy.exe.servertools import HydPyHTTPRequestHandler
        >>> HydPyHTTPRequestHandler.dict2bstring(
        ...     dict([('var1', '1'), ('var2', '[2]')]))
        b'var1 = 1\\nvar2 = [2]'
        """
        output = '\n'.join(f'{key} = {value}' for key, value
                           in dict_.items())
        return bytes(output, encoding='utf-8')

    def do_GET(self):
        try:
            self._set_headers()
            externalname = urllib.parse.urlparse(self.path).path[1:]
            internalname = f'get_{externalname}'
            state.outputs = collections.OrderedDict()
            try:
                state.id_ = urllib.parse.parse_qsl(self.path)[0][1]
            except IndexError:
                state.id_ = None
            try:
                method = getattr(self, internalname)
            except AttributeError:
                raise AttributeError(
                    f'No GET method for property `{externalname}` available.')
            try:
                method()
            except BaseException:
                objecttools.augment_excmessage(
                    f'While trying execute the GET method '
                    f'of property {externalname}')
            if method is not self.get_close_server:
                self.wfile.write(self.dict2bstring(state.outputs))
        except BaseException as exc:
            self.wfile.write(bytes(f'{type(exc)}: {exc}', encoding='utf-8'))

    def do_POST(self):
        try:
            self._set_headers()
            externalname = urllib.parse.urlparse(self.path).path[1:]
            internalname = f'post_{externalname}'
            content_length = int(self.headers['Content-Length'])
            state.id_ = urllib.parse.parse_qsl(self.path)[0][1]
            state.inputs = self.bstring2dict(self.rfile.read(content_length))
            state.outputs = {}
            try:
                method = getattr(self, internalname)
            except AttributeError:
                raise AttributeError(
                    f'No POST method for property `{externalname}` available.')
            try:
                method()
            except BaseException:
                objecttools.augment_excmessage(
                    f'While trying execute the POST method '
                    f'of property {externalname}')
            if method is not self.get_close_server:
                self.wfile.write(self.dict2bstring(state.outputs))
        except BaseException as exc:
            self.wfile.write(bytes(f'{type(exc)}: {exc}', encoding='utf-8'))

    def get_status(self):
        state.outputs['status'] = 'ready'

    def get_close_server(self):
        self.wfile.write(b'shutting down server')
        shutter = threading.Thread(target=self.server.shutdown)
        shutter.deamon = True
        shutter.start()

    def post_process_input(self):
        self.post_simperiod()
        self.post_parameteritems()
        self.get_load_conditionvalues()
        self.post_conditionitems()
        self.get_simulate()
        self.get_save_conditionvalues()
        self.get_parameteritems()
        self.get_conditionitems()
        self.get_seriesitems()

    def get_parameteritemtypes(self):
        state.outputs['alpha'] = 'DoubleItem1D(1)'

    def get_conditionitemtypes(self):
        state.outputs['lz'] = 'DoubleItem0D()'

    def get_seriesitemtypes(self):
        state.outputs['dill'] = 'DoubleItem1D(5)'
        state.outputs['lahn_1'] = 'DoubleItem1D(5)'

    def get_inittimegrid(self):
        init = pub.timegrids.init
        state.outputs['firstdate'] = init.firstdate
        state.outputs['lastdate'] = init.lastdate
        state.outputs['stepsize'] = init.stepsize

    def post_simperiod(self):
        init = pub.timegrids.init
        sim = pub.timegrids.sim
        sim.firstdate = state.inputs['firstdate']
        sim.lastdate = state.inputs['lastdate']
        state.idx1 = init[sim.firstdate]
        state.idx2 = init[sim.lastdate]

    def post_parameteritems(self):
        alpha = state.inputs.get('alpha', None)
        if alpha is not None:
            for element in state.hp.elements.catchment:
                getattr(
                    element.model.parameters.control, 'alpha')(eval(alpha)[0])

    def post_conditionitems(self):
        lz = state.inputs.get('lz', None)
        if lz is not None:
            element = state.hp.elements.land_lahn_1
            element.model.sequences.states.lz(eval(lz)[0])

    def post_seriesitems(self):
        state.hp.nodes.dill.sequences.sim.series[state.idx1:state.idx2] = \
            eval(state.inputs['dill.discharge'])
        state.hp.nodes.lahn_1.sequences.sim.series[state.idx1:state.idx2] = \
            eval(state.inputs['lahn_1.discharge'])

    def get_load_conditionvalues(self):
        if not state.idx1:
            state.hp.conditions = state.init_conditions
        else:
            state.hp.conditions = state.conditions[state.id_][state.idx1]

    def get_save_conditionvalues(self):
        state.conditions[state.id_][
            state.idx2] = state.hp.conditions

    def get_simulate(self):
        state.hp.doit()

    def get_parameteritems(self):
        state.outputs['alpha'] = \
            [state.hp.elements.land_dill.model.parameters.control.alpha.value]

    def get_conditionitems(self):
        state.outputs['lz'] = \
            [state.hp.elements.land_lahn_1.model.sequences.states.lz.value]

    def get_seriesitems(self):
        state.outputs['dill.discharge'] = \
            list(state.hp.nodes.dill.sequences.sim.series
                 [state.idx1:state.idx2])
        state.outputs['lahn_1.discharge'] = \
            list(state.hp.nodes.lahn_1.sequences.sim.series
                 [state.idx1:state.idx2])


def start_server(
        socket, projectname, firstdate, lastdate, stepsize,
        *, logfile=None) -> None:
    pub.timegrids = firstdate, lastdate, stepsize
    state.initialize(projectname)
    server = http.server.HTTPServer(('', int(socket)), HydPyHTTPRequestHandler)
    server.serve_forever()


def await_server(port, seconds):
    """

    >>> from hydpy import run_subprocess, TestIO
    >>> with TestIO():    # doctest: +ELLIPSIS
    ...     run_subprocess('hyd.py await_server 8080 0.1')
    Invoking hyd.py with arguments `...hyd.py, await_server, 8080, 0.1` \
resulted in the following error:
    <urlopen error Waited for 0.1 seconds without response on port 8080.>
    ...

    >>> import subprocess
    >>> from hydpy.core.examples import prepare_full_example_1
    >>> prepare_full_example_1()
    >>> with TestIO():
    ...     process = subprocess.Popen(
    ...         'hyd.py start_server 8080 LahnH 1996-01-01 1996-01-06 1d',
    ...         shell=True)
    ...     run_subprocess('hyd.py await_server 8080 10')

    >>> from urllib import request
    >>> _ = request.urlopen('http://localhost:8080/close_server')
    >>> process.kill()
    >>> _ = process.communicate()
    """
    now = time.perf_counter()
    end = now + float(seconds)
    while now <= end:
        try:
            urllib.request.urlopen(f'http://localhost:{port}/status')
            break
        except urllib.error.URLError:
            time.sleep(0.1)
            now = time.perf_counter()
    else:
        raise urllib.error.URLError(
            f'Waited for {seconds} seconds without response on port {port}.')


pub.scriptfunctions['start_server'] = start_server
pub.scriptfunctions['await_server'] = await_server


autodoctools.autodoc_module()
