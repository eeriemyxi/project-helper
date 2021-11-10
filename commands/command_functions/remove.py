import os


def remove(attrs, project_name: str) -> None:
    if attrs.db.dexists("projects", project_name):
        path = attrs.db.dget_from_project(project_name, 'path')
        os.rmdir(path)
        attrs.db.dpop("projects", project_name)
        attrs.ins.color.print('green', "Removed project: ", end='')
        attrs.ins.color.print('cyan', project_name)
    else:
        attrs.ins.color.print('red', "Project not found.")

def setup(handler):
    handler.add_command(
        instance=remove,
        description='Remove a project.',
        usage='<project-name>'
    )
