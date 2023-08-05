import os

file_suffix = "-jupygit___.ipynb"

def add_gitignore_entry(path):
    suffix = "*" + file_suffix
    gitignore_path = os.path.join(path, ".gitignore")
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as w:
            w.write("# jupygit file \"extension\"\n")
            w.write(suffix)
    else:
        with open(gitignore_path, "r") as r:
            entries = set([s.strip() for s in r.readlines()])
        if suffix not in entries:
            with open(gitignore_path, "a") as w:
                w.write("\n# jupygit file \"extension\"\n")
                w.write(suffix)