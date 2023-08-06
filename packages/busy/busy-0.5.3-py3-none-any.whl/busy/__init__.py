import subprocess
from tempfile import NamedTemporaryFile
from pathlib import Path

PYTHON_VERSION = (3,6,5)

def editor(arg):
    with NamedTemporaryFile() as tempfile:
        Path(tempfile.name).write_text(arg)
        subprocess.run(['sensible-editor', tempfile.name])
        return Path(tempfile.name).read_text()
