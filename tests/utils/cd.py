"""Change directory using context manager syntax ('with').

Based on https://stackoverflow.com/questions/431684/how-do-i-cd-in-python

EXAMPLE:
with CD("/tmp"):
    print(os.getcwd())

"""
import os
import pathlib


class CD:
    """Change directory using context manager syntax ('with')."""

    def __init__(self, new_pwd):
        """Save future pwd."""
        self.new_pwd = pathlib.Path(new_pwd).expanduser()
        self.old_pwd = None

    def __enter__(self):
        """Save old pwd and change directory."""
        self.old_pwd = os.getcwd()
        os.chdir(self.new_pwd)

    def __exit__(self, etype, value, traceback):
        """Change back to old pwd."""
        os.chdir(self.old_pwd)
