from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.task import Task
from busy.commander import Commander
from busy.system import System

class TestCommandDefer(TestCase):

    def test_defer(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(root=t)
            c.handle('defer','2','--to','2019-09-06')
            o = p.read_text()
            self.assertEqual(o, 'a\nc\nd\n')
            o2 = Path(t, 'plan.txt').read_text()
            self.assertEqual(o2, '2019-09-06|b\n')

    def test_defer_for(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(root=t)
            c.handle('defer','2','--for','2019-09-06')
            o = p.read_text()
            self.assertEqual(o, 'a\nc\nd\n')
            o2 = Path(t, 'plan.txt').read_text()
            self.assertEqual(o2, '2019-09-06|b\n')

    def test_defer_days(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\nc\nd')
            with mock.patch('busy.future.today', lambda : Date(2019,2,11)):
                c = Commander(root=t)
                c.handle('defer','2','--for','1 day')
                o = p.read_text()
                self.assertEqual(o, 'a\nc\nd\n')
                o2 = Path(t, 'plan.txt').read_text()
                self.assertEqual(o2, '2019-02-12|b\n')

    def test_defer_d(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\nc\nd')
            with mock.patch('busy.future.today', lambda : Date(2019,2,11)):
                c = Commander(root=t)
                c.handle('defer','2','--for','5d')
                o = p.read_text()
                self.assertEqual(o, 'a\nc\nd\n')
                o2 = Path(t, 'plan.txt').read_text()
                self.assertEqual(o2, '2019-02-16|b\n')

    def test_defer_with_input(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\n')
            c = Commander(root=t)
            with mock.patch('sys.stdin', StringIO('2019-08-24')):
                c.handle('defer')
                o = p.read_text()
                self.assertEqual(o, 'b\n')
                o2 = Path(t, 'plan.txt').read_text()
                self.assertEqual(o2, '2019-08-24|a\n')

    def test_defer_without_date_raises_error(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'todo.txt')
            p.write_text('a\nb\n')
            c = Commander(root=t)
            with mock.patch('sys.stdin', None):
                with self.assertRaises(RuntimeError):
                    c.handle('defer')
