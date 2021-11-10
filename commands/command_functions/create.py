from utils.tools import tools


def create(attrs, *, name: str):
    name = tools.fix_folder(name)
    attrs.log.info("Creating a new project, `%s`. Checking if it already exists.", name)
    if not attrs.db.dexists("projects", name):
        path = attrs.ins.project_path.joinpath(name)
        if path.is_dir():
            attrs.ins.color.print("red", "Path already exists.")
            return
        else:
            path.mkdir()
            attrs.db.dset(f"projects.{name}", {"path": str(path)})
            attrs.ins.color.print("green", "Project created successfully.")
            attrs.log.info("Project created.")
    else:
        attrs.ins.color.print("red", "Project with that name already exists.")


def setup(handler):
    handler.add_command(
        instance=create, usage="<name>", description="Create a new project."
    )
