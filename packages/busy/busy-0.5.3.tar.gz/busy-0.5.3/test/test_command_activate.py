from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.task import Task
from busy.commander import Commander
from busy.system import System

class TestCommandActivate(TestCase):

    def test_activate(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'plan.txt')
            p.write_text('2018-09-04|a\n')
            c = Commander(root=t)
            c.handle('activate','1')
            self.assertEqual(p.read_text(), '')
            p2 = Path(t, 'todo.txt')
            self.assertEqual(p2.read_text(), 'a\n')

    def test_activate_with_today_option(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'plan.txt')
            p.write_text('2018-09-04|a\n2019-03-25|b\n')
            c = Commander(root=t)
            with mock.patch('busy.future.today', lambda : Date(2019,2,11)):
                c.handle('activate','--today')
                self.assertEqual(p.read_text(), '2019-03-25|b\n')
                p2 = Path(t, 'todo.txt')
                self.assertEqual(p2.read_text(), 'a\n')
