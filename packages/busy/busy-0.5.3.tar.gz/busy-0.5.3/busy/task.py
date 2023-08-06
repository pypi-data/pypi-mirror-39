from datetime import date as Date
from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta
import re

from .future import absolute_date

TODO_STATE = 't'
PLAN_STATE = 'p'
DONE_STATE = 'd'

class Task:

    def __init__(self, description=None, plan_date=None):
        assert isinstance(description, str)
        assert description
        self._description = description
        self._state = TODO_STATE
        if plan_date: self.as_plan(plan_date)

    def __str__(self):
        return self._description

    @property
    def description(self):
        return self._description

    def as_plan(self, date):
        self._state = PLAN_STATE
        self._plan_date = absolute_date(date)
        return self

    def as_todo(self):
        self._state = TODO_STATE
        return self

    @property
    def plan_date(self):
        return self._plan_date

    @classmethod
    def create(self, value):
        if isinstance(value, self):
            return value
        elif isinstance(value, str):
            return self(value)
        elif isinstance(value, dict):
            return self(**value)

    @property
    def tags(self):
        words = self.description.split()
        return [w[1:].lower() for w in words if w.startswith('#')]

    @property
    def project(self):
        tags = self.tags
        return tags[0] if tags else None
