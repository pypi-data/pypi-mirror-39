from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date
import unittest
from unittest.mock import Mock

from busy.task import Task
from busy.commander import Commander
from busy.system import System

class TestCommandManage(TestCase):

    def test_manage_launches_editor(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\n')
            with mock.patch('busy.editor', lambda x: 'b\n'):
                c = Commander(root=t)
                o = c.handle('manage')
                f = p.read_text()
                self.assertEqual(f, 'b\n')

    def test_manage_includes_newline_at_end(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\n')
            m = Mock()
            m.return_value = 'b\n'
            with mock.patch('busy.editor', m):
                c = Commander(root=t)
                o = c.handle('manage')
                m.assert_called_with('a\n')
