import pathlib
import shutil
from itertools import tee, count
from utils.color_print import Color


class Decorator:
    def __init__(self) -> None:
        self.commands = []

    def add_command(self, **kwargs):
        """
        A decorator to add commands
        """

        def inner(func):
            self.commands.append(dict(instance=func, **kwargs))

        return inner

def colon_split(text: str) -> list[str, str]:
    try:
        one, two = tuple(map(lambda x: x.strip(), text.split(':')[:2]))
    except ValueError:
        print('red', 'Please split both arguments by a colon, `:`.')
        return False, False
    return one, two

decorator = Decorator()
command = decorator.add_command
print = Color().print


@command(
    description="Shows all the files and directories present in the current working directory.",
    alias=["dir"],
)
def showdir(attrs):
    path = attrs.ins.cwd
    files, files2 = tee(path.iterdir())
    if not list(files2):
        print("red", "This directory is empty.")
        return
    for dir_index, dir_name in enumerate(files):
        print('red', dir_index, end=' | ')
        print("cyan", str(dir_name.stat().st_size / 1000000) + " MB", end=" | ")
        print("yellow", "DIR" if path.joinpath(dir_name).is_dir() else "FILE", end=" > ")
        print("green", dir_name.name)


@command(
    description="Copies a file from one directory to another.\nThe specified path will be joined with project path and then the file will be copied to the joined path.\nYou have to seperate both paths by a colon, `:`.",
    alias=["cp"],
    usage="<filename> : <path>",
)
def copy(attrs, *, filename_path):
    filename, path = colon_split(filename_path)
    if not all((filename, path)):
        return
    projectpath = pathlib.Path(attrs.ins.project_path)
    cwd = attrs.ins.cwd
    full_path_filename = cwd.joinpath(filename)
    full_path_copy = projectpath.joinpath(path)
    if full_path_copy.exists():
        print(
            "red",
            f"Could not copy. A file named `{filename}` already exists in `{path}`",
        )
        return
    if not full_path_filename.exists():
        print("red", f"`{filename}` not found.")
        return
    shutil.copyfile(full_path_filename, full_path_copy)


@command(
    description="Works just like the `copy` command but instead moves it.",
    alias=["mv"],
    usage="<filename> <path>",
)
def move(attrs, *, filename_path):
    filename, path = colon_split(filename_path)
    if not all((filename, path)):
        return
    projectpath = pathlib.Path(attrs.ins.project_path)
    cwd = attrs.ins.cwd
    full_path_filename = cwd.joinpath(filename)
    full_path_move = projectpath.joinpath(path)
    if full_path_move.exists():
        print(
            "red",
            f"Could not move. A file named `{filename}` already exists in `{path}`",
        )
        return
    if not full_path_filename.exists():
        print("red", f"`{filename}` not found.")
        return
    shutil.move(full_path_filename, full_path_move)


@command(
    description="Make a new directory in the current working directory.",
)
def mkdir(attrs, *, foldername):
    cwd = attrs.ins.cwd
    full_path = cwd.joinpath(foldername)
    if full_path.exists():
        print("red", f"A folder named `{foldername}` already exists.")
        return
    full_path.mkdir()


@command(
    description="Change the current working directory. You may also enter the index shown by the `showdir` command.",
    usage="<path> | .<index>",
    shortening=False,
)
def cd(attrs, *, path):
    cwd = attrs.ins.cwd
    full_path = cwd.joinpath(path)
    if path.startswith('.'):
        if path[1:].isnumeric():
            files = cwd.iterdir()
            files_dict = {str(index):name for index, name in enumerate(files)}
            index = path[1:]
            full_path = files_dict.get(index)
            if full_path is not None and full_path.is_dir():
                attrs.ins.cwd = full_path
                return
            else:
                print("red", "Path doesn't exist or it is a file.")
                return
    if full_path.exists() and full_path.is_dir():
        attrs.ins.cwd = full_path
        return
    else:
        print("red", "Path doesn't exist or it is a file..")
        return

@command(
    description="Switch to the parent path of current working directory",
    name="cd..",
    shortening=False,
)
def cd_back(attrs):
    cwd = attrs.ins.cwd
    new_path = cwd.parent
    if not attrs.db.get("path") in str(new_path):
        print(
            "red",
            "You are trying to change the current working directory to the parent directory of your specified project path.",
        )
    else:
        attrs.ins.cwd = new_path


@command(
    description="Remove a folder from the current working directory",
    usage="<folder_name>",
    shortening=False,
)
def rmdir(attrs, *, foldername):
    path = attrs.ins.cwd.joinpath(foldername)
    if path.exists():
        shutil.rmtree(path)
        print("green", "Directory removed.")
    else:
        print("red", "Directory not found.")


@command(
    description="Remove a file from the current working directory",
    usage="<file_name>",
)
def rm(attrs, *, filename):
    path = attrs.ins.cwd.joinpath(filename)
    if path.exists() and path.is_file():
        path.unlink()
        print("green", "File removed.")
    else:
        print("red", "File not found.")


@command(
    description="Create a file in the current working directory",
    usage="<file_name>",
)
def touch(attrs, *, filename):
    cwd = attrs.ins.cwd
    path = cwd.joinpath(filename)
    if not path.exists():
        try:
            path.touch()
            print("green", "File has been created.")
        except FileExistsError:
            print("red", "File already exists.")


@command(
    description="Rename a file/directory in the current working directory. You have to seperate both paths by a colon, `:`.",
    usage="<file_name> : <new_file_name>",
)
def ren(attrs, *, filenames: str) -> None:
    filename, filename_new = colon_split(filenames)
    if not all((filename, filename_new)):
        return
    cwd = attrs.ins.cwd
    full_path = cwd.joinpath(filename)
    full_path_new = cwd.joinpath(filename_new)
    if not full_path.exists():
        print("red", "Original path does'nt exist.")
        return
    if full_path_new.exists():
        print("red", "New path already exists.")
        return
    full_path.rename(full_path_new)
    print("green", "File has been renamed.")


def setup(handler):
    for kwargs in decorator.commands:
        handler.add_command(**kwargs)