from unittest import TestCase
from pathlib2 import Path
from mock import MagicMock, call, patch, sentinel
from zcli.main import main


class main_tests (TestCase):
    @patch('sys.stdout')
    @patch('zcli.clargs.parse_args')
    @patch('zcli.zcashcli.ZcashCLI')
    @patch('zcli.operations.ZcashOperations')
    @patch('zcli.ui.make_ui')
    def test_main(
            self,
            m_make_ui,
            m_ZcashOperations,
            m_ZcashCLI,
            m_parse_args,
            m_stdout,
    ):
        m_run = MagicMock()
        m_run.return_value = ["json", "result"]

        fakedatadir = Path('fake-path')
        m_parse_args.return_value = (
            {'DEBUG': True, 'DATADIR': fakedatadir, 'VERBOSITY': 'debug'},
            m_run,
            {'fake_arg': sentinel.FAKE_ARG},
        )

        main(sentinel.ARGS)

        self.assertEqual(
            m_parse_args.mock_calls,
            [call(main.__doc__, sentinel.ARGS)])

        self.assertEqual(
            m_ZcashCLI.mock_calls,
            [call(m_make_ui.return_value, fakedatadir)])

        self.assertEqual(
            m_ZcashOperations.mock_calls,
            [call(m_ZcashCLI.return_value)])

        self.assertEqual(
            m_run.mock_calls,
            [call(
                m_make_ui.return_value,
                m_ZcashOperations.return_value,
                fake_arg=sentinel.FAKE_ARG)])

        self.assertEqual(
            m_stdout.mock_calls,
            [call.write('[\n  "json",\n  "result"\n]')])
