import subprocess
from pathlib2 import Path
from zcli import saferjson


class ZcashCLI (object):
    def __init__(self, ui, datadir, network='mainnet'):
        assert isinstance(datadir, Path), repr(datadir)
        assert network in {'mainnet', 'testnet', 'regtest'}, repr(network)

        self._ui = ui
        self._execname = 'zcash-cli'
        self._datadir = datadir
        self._network = network

    def __getattr__(self, method):
        return ZcashCLIMethod(
            self._ui,
            method,
            self._execname,
            self._datadir,
            self._network,
        )


class ZcashCLIMethod (object):
    def __init__(self, ui, method, execname, datadir, network):
        self._ui = ui
        self._method = method
        self._execname = execname
        self._datadir = datadir
        self._network = network

    def __call__(self, *args, **kwargs):
        result = self._call_raw_result(*args, **kwargs)
        if result.startswith('{') or result.startswith('['):
            result = saferjson.loads(result)
        return result

    def _call_raw_result(self, *args, **kwargs):
        prefixopts = kwargs.pop('prefixopts', [])
        assert not kwargs, ('unexpected key word args', kwargs)

        fullargs = [
            self._execname,
            '-datadir={}'.format(self._datadir),
        ]

        fullargs.extend({
            'mainnet': [],
            'testnet': ['-testnet'],
            'regtest': ['-regtest'],
        }[self._network])

        fullargs.extend(prefixopts)

        fullargs.append(self._method)
        fullargs.extend(map(saferjson.encode_param, args))

        self._ui.debug('Running: {!r}', fullargs)
        return subprocess.check_output(fullargs).rstrip()
