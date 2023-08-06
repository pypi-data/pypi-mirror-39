from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.task import Task
from busy.commander import Commander
from busy.system import System

class TestCommandDelete(TestCase):

    def test_delete(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(root=t)
            c.handle('delete','--yes','3-')
            o = p.read_text()
            self.assertEqual(o, 'a\nb\n')

    def test_delete_with_input_confirmation_yes(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(root=t)
            with mock.patch('sys.stdin', StringIO('Y')):
                c.handle('delete','3-')
                o = p.read_text()
                self.assertEqual(o, 'a\nb\n')

    def test_delete_with_input_confirmation_no(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(root=t)
            with mock.patch('sys.stdin', StringIO('no')):
                c.handle('delete','3-')
                o = p.read_text()
                self.assertEqual(o, 'a\nb\nc\nd')

    def test_delete_outputs_before_confirmation(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\n')
            c = Commander(root=t)
            o = StringIO()
            with mock.patch('sys.stdin', StringIO('Y')):
                with mock.patch('sys.stdout', o):
                    c.handle('delete', '1')
                    self.assertEqual(o.getvalue(), 'a\nDelete? (Y/n) ')

    def test_delete_defaults_to_first_task_only(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\n')
            c = Commander(root=t)
            with mock.patch('sys.stdin', StringIO('Y')):
                c.handle('delete')
                o = p.read_text()
                self.assertEqual(o, 'b\n')
