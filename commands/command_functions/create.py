import os
from utils.tools import tools


def create(attrs, *, name: str):
    name = tools.fix_folder(name)
    attrs.log.info("Creating a new project, `%s`. Checking if it already exists.", name)
    if not attrs.db.dexists("projects", name):
        path = os.path.join(attrs.ins.current_directory, name)
        if os.path.isdir(path):
            attrs.ins.color.print("red", "Path already exists.")
            return
        else:
            os.mkdir(path)
            # attrs.db.dadd_project(name, "path", path)
            attrs.db.dset(f"projects.{name}", {'path': path})
            attrs.ins.color.print("green", "Project created successfully.")
            attrs.log.info("Project created.")
    else:
        attrs.ins.color.print("red", "Project with that name already exists.")


def setup(handler):
    handler.add_command(
        instance=create, usage="<name>", description="Create a new project."
    )
