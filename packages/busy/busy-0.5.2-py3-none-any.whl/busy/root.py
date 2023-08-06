from pathlib import Path
from tempfile import TemporaryDirectory
import os

from .system import System
from .task import Task
from .file import TodoFile
from .file import PlanFile

class Root:

    def __init__(self, path=None):
        if path: self.path = path

    @property
    def path(self):
        if not hasattr(self, '_path'):
            env_var = os.environ.get('BUSY_ROOT')
            self._path = Path(env_var if env_var else Path.home() / '.busy')
            if not self._path.is_dir(): self._path.mkdir()
        return self._path

    @path.setter
    def path(self, value):
        assert not hasattr(self, '_path')
        path = Path(value) if isinstance(value, str) else value
        assert isinstance(path, Path) and path.is_dir()
        self._path = path

    @property
    def system(self):
        if not hasattr(self, '_system'):
            self._todo_file = TodoFile(self.path)
            self._plan_file = PlanFile(self.path)
            todos = self._todo_file.queue
            plans = self._plan_file.queue
            self._system = System(todos=todos, plans=plans)
        return self._system

    def save(self):
        self._todo_file.save()
        self._plan_file.save()
