from unittest import TestCase
from genty import genty, genty_dataset
from mock import MagicMock, call, patch, sentinel
from zcli import ui


class UI_CLASSES_tests (TestCase):
    def test_existing_verbosity(self):
        i = ui.make_ui('standard')
        self.assertIsInstance(i, ui.standard)

    def test_unknown_verbosity(self):
        self.assertRaises(KeyError, ui.make_ui, 'blorgleflorg')


class output_format_tests (TestCase):
    @patch('time.strftime')
    @patch('sys.stderr')
    def test_write_line(self, m_stderr, m_strftime):
        m_strftime.return_value = '{<strftime>}'

        m_tmpl = MagicMock()
        m_tmpl.format.return_value = '{<tmpl>}'

        result = ui._write_line(
            m_tmpl,
            sentinel.a,
            sentinel.b,
            key=sentinel.v,
        )

        self.assertIsNone(result)

        self.assertEqual(
            m_strftime.mock_calls,
            [
                call('%Y-%m-%d %H:%M:%S%z'),
            ],
        ),

        self.assertEqual(
            m_tmpl.mock_calls,
            [
                call.format(
                    sentinel.a,
                    sentinel.b,
                    key=sentinel.v,
                ),
            ],
        )

        self.assertEqual(
            m_stderr.mock_calls,
            [
                call.write('{<strftime>} {<tmpl>}\n'),
            ],
        )


@genty
class verbosity_tests (TestCase):
    @genty_dataset(
        quiet=('quiet', [
                'timestamp FAILURE: message\n',
        ]),
        standard=('standard', [
                'timestamp FAILURE: message\n',
                'timestamp message\n',
        ]),
        debug=('debug', [
                'timestamp FAILURE: message\n',
                'timestamp message\n',
                'timestamp debug: message\n',
        ]),
    )
    def test_verbosity(self, verb, msgs):
        uicb = ui.make_ui(verb)

        with patch('time.strftime') as m_strftime:
            m_strftime.return_value = 'timestamp'

            with patch('sys.stderr') as m_stderr:
                uicb.handle_failure('message')
                uicb.status('message')
                uicb.debug('message')

                self.assertEqual(
                    m_stderr.mock_calls,
                    [
                        call.write(msg)
                        for msg in msgs
                    ],
                )
