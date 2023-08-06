from .queue import TodoQueue
from .queue import PlanQueue
from .task import Task

import busy.future
import busy

class System:

    def __init__(self, *items, todos=None, plans=None):
        self.todos = todos if todos else TodoQueue()
        self.plans = plans if plans else PlanQueue()
        self.add(*items)

    def add(self, *items):
        self.todos.add(*items)

    def pop(self, *criteria):
        self.todos.pop(*criteria)

    def drop(self, *criteria):
        self.todos.drop(*criteria)

    def defer(self, date, *criteria):
        indices = self.todos.select(*(criteria or [1]))
        plans = [self.todos.get(i+1).as_plan(date) for i in indices]
        self.plans.add(*plans)
        self.todos.delete_by_indices(*indices)

    def activate(self, *criteria, today=False):
        if today:
            func = lambda t: t.plan_date <= busy.future.today()
            indices = self.plans.select(func)
        else:
            indices = self.plans.select(*criteria)
        tasks = [self.plans.get(i+1).as_todo() for i in indices]
        self.todos.add(*tasks)
        self.plans.delete_by_indices(*indices)

    def manage(self, *criteria):
        tasklist = self.todos.list(*criteria)
        indices = [i[0]-1 for i in tasklist]
        body_start = ''.join([str(i[1])+'\n' for i in tasklist])
        body_after = busy.editor(body_start).split('\n')
        new_tasks = [Task(i) for i in body_after if i]
        self.todos.delete_by_indices(*indices)
        self.add(*new_tasks)
