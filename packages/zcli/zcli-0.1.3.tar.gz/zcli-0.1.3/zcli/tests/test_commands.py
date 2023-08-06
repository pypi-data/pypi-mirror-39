from unittest import TestCase
from decimal import Decimal
from genty import genty, genty_dataset
from mock import MagicMock, call, patch
from zcli import commands, operations
from zcli.tests.utils import FAKE_OPID


class FakeUsageError (Exception):
    @classmethod
    def usage_error(cls, msg):
        raise cls(msg)


@genty
class send_tests (TestCase):
    @genty_dataset(
        single_zaddr=(
            ['FAKE_ZADDR', '42', 'this is the memo'],
            [{
                'address': 'FAKE_ZADDR',
                'amount': Decimal('42'),
                'memo': 'this is the memo'.encode('hex'),
            }],
        ),
        multiple=(
            [
                'FAKE_ZADDR', '42', 'this is the memo',
                'FAKE_TADDR', '23', '',
            ],
            [
                {
                    'address': 'FAKE_ZADDR',
                    'amount': Decimal('42'),
                    'memo': 'this is the memo'.encode('hex'),
                },
                {
                    'address': 'FAKE_TADDR',
                    'amount': Decimal('23'),
                }
            ],
        ),
    )
    def test_post_process_args_no_error(self, destinfo, expected):
        m_opts = MagicMock()
        m_opts.DESTINFO = destinfo

        result = commands.send.post_process_args(
            m_opts,
            FakeUsageError.usage_error,
        )

        self.assertIs(result, m_opts)
        self.assertEqual(m_opts.mock_calls, [])
        self.assertEqual(m_opts.DESTINFO, expected)

    @genty_dataset(
        empty=(
            [],
            '^At least one destination must be supplied.$',
        ),
        single_arg=(
            ['foo'],
            ('^DESTINFO must be triplets of ADDR AMOUNT MEMO; '
             'found 1 arguments.$'),
        ),
        # taddr_nonempty_memo=(
        #     ['I am a fake taddr', '42', 's:I am a nonempty memo.'],
        #     'FIXME',
        # ),
    )
    def test_post_process_args_with_error(self, destinfo, rgx):
        m_opts = MagicMock()
        m_opts.DESTINFO = destinfo

        self.assertRaisesRegexp(
            FakeUsageError,
            rgx,
            commands.send.post_process_args,
            m_opts,
            FakeUsageError.usage_error,
        )


@genty
class commands_smoketests (TestCase):
    """High level smoketests of commands."""

    dataset = dict(
        (cls.__name__, (cls, args, checkresult, expectedclicalls))
        for (cls, args, checkresult, expectedclicalls)
        in [
            (
                commands.list_balances,
                [],
                lambda _: {'total': 0, 'addresses': {}},
                None,
            ),
            (
                commands.do,
                ['help', ['getinfo']],
                lambda m: isinstance(m, MagicMock),
                [call.help('getinfo')],
            ),
            (
                commands.send,
                [
                    'z-fake-src-addr',
                    ['z-fake-dst-addr', '42.23', 's:fake memo'],
                ],
                lambda txids: isinstance(txids, list) and len(txids) == 1,
                None,
            ),
            (
                commands.wait,
                [
                    [FAKE_OPID],
                ],
                lambda txids: isinstance(txids, list) and len(txids) == 1,
                None,
            ),
        ]
    )

    @genty_dataset(**dataset)
    def test_run(self, cls, args, checkresult, expectedclicalls):
        m_cli = self._make_mock_cli()
        m_ui = MagicMock()
        ops = operations.ZcashOperations(m_cli)

        with patch('time.sleep'):
            result = cls.run(m_ui, ops, *args)

        self.assertTrue(checkresult(result), repr(result))
        if expectedclicalls is not None:
            self.assertEqual(m_cli.mock_calls, expectedclicalls)

    def test_dataset_completeness(self):
        expected = set(commands.COMMANDS.keys())
        actual = set(self.dataset.keys())
        self.assertEqual(expected, actual)

    def _make_mock_cli(self):
        m_cli = MagicMock()

        def fake_z_getop(opids):
            return [
                {
                    'id': opid,
                    'status': 'success',
                    'result': {
                        'txid': 'fake txid for {}'.format(opid)
                    },
                }
                for opid
                in opids
            ]

        m_cli.z_getoperationstatus = fake_z_getop
        m_cli.z_getoperationresult = fake_z_getop
        m_cli.z_sendmany.return_value = FAKE_OPID
        m_cli.gettransaction.return_value = {
            'confirmations': 6,
        }

        return m_cli
