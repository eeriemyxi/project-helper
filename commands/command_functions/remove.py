# import os
import shutil


def remove(attrs, project_name: str) -> None:
    log = attrs.log.info
    log(
        "Checking if %s exists. If it exists, it will be removed as requested.",
        project_name,
    )
    if attrs.db.dexists("projects", project_name):
        path = attrs.db.dget_from_project(project_name, "path")
        log("Path was found: %s", path)
        shutil.rmtree(path)
        attrs.db.dpop("projects", project_name)
        log("Project `%s` has been removed.", project_name)
        attrs.ins.color.print("green", "Removed project: ", end="")
        attrs.ins.color.print("cyan", project_name)
    else:
        log("Project doesn't exist.")
        attrs.ins.color.print("red", "Project not found.")


def setup(handler):
    handler.add_command(
        instance=remove, description="Remove a project.", usage="<project-name>"
    )
