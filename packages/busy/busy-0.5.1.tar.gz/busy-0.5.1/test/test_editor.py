from unittest import TestCase
import busy
from unittest import mock
from pathlib import Path

class MockSubprocess:

    def run(arg):
        Path(arg[1]).write_text('v')

class TestEditor(TestCase):

    def test_editor(self):
        with mock.patch('busy.subprocess', MockSubprocess):
            x = busy.editor('a')
            self.assertEqual(x, 'v')
