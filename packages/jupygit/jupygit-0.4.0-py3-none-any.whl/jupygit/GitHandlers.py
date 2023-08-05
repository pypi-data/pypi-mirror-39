import json
import os
from urllib.parse import parse_qs

from notebook.base.handlers import IPythonHandler

from .gitignore_manipulator import add_gitignore_entry
from .nb_manipulator import clean_nb

FILE_EXTENSION = ".ipynb"
FILE_SUFFIX = "-jupygit___.ipynb"
EXTENSION = slice(None, -6)


class GitRestoreHandler(IPythonHandler):

    def post(self):
        data = parse_qs(self.request.body.decode('utf8'))
        dirty_path = data["path"][0]

        clean_path = dirty_path[:-len(FILE_SUFFIX)] + FILE_EXTENSION
        os.remove(clean_path)

        self.set_status(200)


class GitCleanHandler(IPythonHandler):

    def post(self):
        data = parse_qs(self.request.body.decode('utf8'))
        clean_path = data["path"][0]
        add_gitignore_entry(os.path.dirname(clean_path))

        dirty_path = clean_path[EXTENSION] + FILE_SUFFIX

        with open(dirty_path, "r") as r:
            dirty = json.load(r)

        clean_nb(dirty)

        with open(clean_path, "w") as w:
            json.dump(dirty, w, indent=1)
            w.write("\n")  # Fix for the new line issue

        self.set_status(200)


class GitCheckRecoveryHandler(IPythonHandler):

    def get(self):
        notebook_path = self.get_argument('path')

        attempt_to_recover = False

        if notebook_path.endswith(FILE_SUFFIX):
            if os.path.exists(notebook_path.replace(FILE_SUFFIX, FILE_EXTENSION)):
                attempt_to_recover = True

        self.write({'try_to_recover': attempt_to_recover})
