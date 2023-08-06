import unittest
from pathlib2 import Path
from genty import genty, genty_dataset
from mock import MagicMock, call, patch
from zcli.zcashcli import ZcashCLI, ZcashCLIMethod


class ZcashCLI_tests (unittest.TestCase):
    def test_getattr(self):
        f_datadir = Path('FAKE-DATADIR')
        m_ui = MagicMock()
        zcli = ZcashCLI(m_ui, f_datadir)

        m = zcli.some_method

        self.assertIs(zcli._ui, m_ui)
        self.assertIs(zcli._ui, m._ui)
        self.assertIsInstance(m, ZcashCLIMethod)
        self.assertEqual('zcash-cli', m._execname)
        self.assertEqual(f_datadir, m._datadir)


@genty
class ZcashCLIMethod_tests (unittest.TestCase):
    def setUp(self):
        self.m_ui = MagicMock()
        self.m = ZcashCLIMethod(
            self.m_ui,
            'FAKE-METHOD',
            'FAKE-EXEC',
            Path('FAKE-DATADIR'),
            'mainnet',
        )

    call_rpc_argsets = dict(
        nothing=(
            [],
            [],
        ),
        strs=(
            ['a', 'b', 'c'],
            ['a', 'b', 'c'],
        ),
        jsonstuff=(
            [u'a', ['b', {'c': 'coconut'}]],
            ['a', '["b",{"c":"coconut"}]'],
        ),
    )

    @genty_dataset(**call_rpc_argsets)
    def test_call(self, params, expectedargs):
        with patch('subprocess.check_output') as m_check_output:
            m_check_output.return_value = 'not json object or list'

            self.m(*params)

        fullexpectedargs = [
            'FAKE-EXEC',
            '-datadir=FAKE-DATADIR',
            'FAKE-METHOD',
        ] + expectedargs

        self.assertEqual(
            self.m_ui.mock_calls,
            [call.debug('Running: {!r}', fullexpectedargs)],
        )

        self.assertEqual(
            m_check_output.mock_calls,
            [
                call(fullexpectedargs),
            ],
        )

    @genty_dataset(**call_rpc_argsets)
    def test_call_json(self, params, _):
        with patch(
                'zcli.zcashcli.ZcashCLIMethod._call_raw_result'
        ) as m_crr:

            # Trigger Json parsing:
            m_crr.return_value = '[]'

            with patch('zcli.saferjson.loads') as m_loads:
                self.m(*params)

        self.assertEqual(
            m_crr.mock_calls,
            [call(*params)],
        )

        self.assertEqual(
            m_loads.mock_calls,
            [call(m_crr.return_value)],
        )
