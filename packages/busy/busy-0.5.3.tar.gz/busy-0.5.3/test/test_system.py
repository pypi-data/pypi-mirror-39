from unittest import TestCase
import datetime

from busy.system import System
from busy.task import Task

class TestSystem(TestCase):

    def test_get(self):
        q = System()
        q.add(Task('a'))
        t = q.todos.get()
        self.assertEqual(str(t),'a')

    def test_list(self):
        s = System()
        s.add(Task('a'))
        s.add(Task('b'))
        i = s.todos.list()
        self.assertEqual(len(i), 2)
        self.assertEqual(i[1][0], 2)
        self.assertEqual(str(i[0][1]), 'a')
        self.assertIsInstance(i[1][1], Task)

    def test_defer(self):
        s = System()
        s.add(Task('a'))
        d = datetime.date(2018,12,25)
        s.defer(d)
        self.assertEqual(s.plans.count(), 1)
        self.assertEqual(s.plans.get(1).plan_date.year, 2018)

    def test_pop(self):
        s = System()
        t1 = Task('a')
        t2 = Task('b')
        s.add(t1)
        s.add(t2)
        s.pop()
        i = s.todos.list()
        self.assertEqual(len(i), 2)
        self.assertEqual(str(i[0][1]), 'b')

    def test_by_number(self):
        s = System()
        s.add(Task('a'))
        s.add(Task('b'))
        t = s.todos.get(2)
        self.assertEqual(str(t), 'b')

    def test_create_with_string(self):
        s = System()
        s.add('a')
        self.assertEqual(str(s.todos.get()), 'a')
        self.assertIsInstance(s.todos.get(), Task)

    def test_create_with_multiple_strings(self):
        s = System('a','b','c')
        self.assertIsInstance(s.todos.get(), Task)
        self.assertEqual(s.todos.count(), 3)
        self.assertEqual(str(s.todos.get(2)), 'b')

    def test_select_multiple(self):
        s = System('a','b','c')
        t = s.todos.select(1,3)
        self.assertEqual(len(t), 2)

    def test_list_plans(self):
        s = System('a','b')
        s.defer((2018,12,4))
        self.assertEqual(s.plans.count(), 1)

    def test_defer_by_index(self):
        s = System('a','b')
        s.defer((2018,12,4),2)
        t = s.todos.get()
        self.assertEqual(s.plans.count(),1)
        self.assertEqual(str(t), 'a')

    def test_defer_multiple(self):
        s = System('a','b','c')
        s.defer((2018,12,5),1,3)
        p = s.plans.get(2)
        self.assertEqual(str(p), 'c')

    def test_list_by_criteria(self):
        s = System('a','b','c')
        i = s.todos.list(2,3)
        self.assertEqual(len(i), 2)
        self.assertEqual(str(i[1][1]), 'c')

    def test_drop(self):
        s = System('a','b','c')
        s.drop()
        self.assertEqual(str(s.todos.get()), 'b')
        self.assertEqual(str(s.todos.get(3)), 'a')

    def test_drop_by_criteria(self):
        s = System('a','b','c','d')
        s.drop('2-3')
        self.assertEqual(str(s.todos.get(1)), 'a')
        self.assertEqual(str(s.todos.get(2)), 'd')
        self.assertEqual(str(s.todos.get(3)), 'b')
        self.assertEqual(str(s.todos.get(4)), 'c')
