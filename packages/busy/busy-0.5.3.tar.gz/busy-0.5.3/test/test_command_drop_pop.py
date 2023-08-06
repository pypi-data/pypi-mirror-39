from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.task import Task
from busy.commander import Commander
from busy.system import System

class TestCommandDrop(TestCase):

    def test_drop(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(root=t)
            c.handle('drop','2','4')
            o = p.read_text()
            self.assertEqual(o, 'a\nc\nb\nd\n')

    def test_pop(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(root=t)
            c.handle('pop','2','4')
            o = p.read_text()
            self.assertEqual(o, 'b\nd\na\nc\n')
