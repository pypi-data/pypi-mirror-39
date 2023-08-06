from unittest import TestCase
from mock import MagicMock, call, patch, sentinel
from zcli import operations
from zcli.tests.utils import FAKE_OPID


class ZcashOperations_tests (TestCase):
    def setUp(self):
        self.m_ui = MagicMock()
        self.m_cli = MagicMock()
        self.ops = operations.ZcashOperations(self.m_cli)

    @patch('logging.root')
    @patch('time.sleep')
    def test_wait_on_opids_basic(self, m_sleep, m_root):
        interval = 42

        opres = [
            {
                'id': FAKE_OPID,
                'status': 'success',
                'result': {'txid': sentinel.TXID_0},
            },
        ]

        self.m_cli.z_getoperationstatus.return_value = opres
        self.m_cli.z_getoperationresult.return_value = opres
        self.m_cli.gettransaction.return_value = {
            'confirmations': operations.MINCONF,
        }

        result = self.ops.wait(self.m_ui, [FAKE_OPID], interval=interval)
        self.assertTrue(result)

        self.assertEqual(
            m_sleep.mock_calls,
            [call(interval)],
        )

        self.assertEqual(
            m_root.mock_calls,
            [],
        )

        self.assertEqual(
            self.m_ui.handle_failure.mock_calls,
            [],
        )

        self.assertEqual(
            self.m_ui.status.mock_calls,
            [call(
                ('Waiting {} seconds for {} incomplete operations '
                 'and {} unconfirmed transactions.'),
                interval,
                1,
                0),
             call(
                 'Operation {} transition: {!r} -> {!r}',
                 FAKE_OPID,
                 'unknown',
                 'success'),
             call(
                 'Transaction {!r} final ({} >= {} confirmations)',
                 sentinel.TXID_0,
                 6,
                 6)])
