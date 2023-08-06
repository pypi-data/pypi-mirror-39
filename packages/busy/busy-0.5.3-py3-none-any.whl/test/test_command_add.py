from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.task import Task
from busy.commander import Commander
from busy.system import System

class TestCommandAdd(TestCase):

    def test_add_by_input(self):
        with TemporaryDirectory() as t:
            c = Commander(root=t)
            with mock.patch('sys.stdin', StringIO('g')):
                c.handle('add')
                x = Path(t, 'todo.txt').read_text()
                self.assertEqual(x, 'g\n')
