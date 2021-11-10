import pathlib
import shutil
from itertools import tee
from utils.color_print import Color

print = Color().print


def showdir(attrs):
    path = attrs.ins.cwd
    files, files2 = tee(path.iterdir())
    if not list(files2):
        print("red", "This directory is empty.")
        return
    for file in files:
        print('cyan', str(file.stat().st_size/1000000)+' MB', end=" | ")
        print("yellow", "DIR" if path.joinpath(file).is_dir() else "FILE", end=" > ")
        print("green", file.name)


def copy(attrs, filename, path):
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


def move(attrs, filename, path):
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


def mkdir(attrs, foldername):
    cwd = attrs.ins.cwd
    full_path = cwd.joinpath(foldername)
    if full_path.exists():
        print("red", f"A folder named `{foldername}` already exists.")
        return
    full_path.mkdir()


def cd(attrs, path):
    cwd = attrs.ins.cwd
    full_path = cwd.joinpath(path)
    if full_path.exists():
        attrs.ins.cwd = full_path
    else:
        print("red", "Path doesn't exist.")


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


def rmdir(attrs, foldername):
    path = attrs.ins.cwd.joinpath(foldername)
    if path.exists():
        shutil.rmtree(path)
        print("green", "Directory removed.")
    else:
        print("red", "Directory not found.")


def rm(attrs, filename):
    path = attrs.ins.cwd.joinpath(filename)
    if path.exists() and path.is_file():
        path.unlink()
        print("green", "File removed.")
    else:
        print("red", "File not found.")


def touch(attrs, filename):
    cwd = attrs.ins.cwd
    path = cwd.joinpath(filename)
    if not path.exists():
        try:
            path.touch()
            print("green", "File has been created.")
        except FileExistsError:
            print("red", "File already exists.")


def ren(attrs, filename: str, filename_new: str) -> None:
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
    handler.add_command(
        instance=showdir,
        description="Shows all the files and directories present in the current working directory.",
        alias=["dir"],
    )
    handler.add_command(
        instance=copy,
        description="Copies a file from one directory to another.\nThe specified path will be joined with project path and then the file will be copied to the joined path.",
        alias=["cp"],
        usage="<filename> <path>",
    )
    handler.add_command(
        instance=move,
        description="Works just like the `copy` command but instead moves it.",
        alias=["mv"],
        usage="<filename> <path>",
    )
    handler.add_command(
        instance=mkdir,
        description="Make a new directory in the current working directory.",
    )
    handler.add_command(
        instance=cd,
        description="Change the current working directory",
        usage="<path>",
        shortening=False,
    )
    handler.add_command(
        instance=cd_back,
        description="Switch to the parent path of current working directory",
        name="cd..",
        shortening=False,
    )
    handler.add_command(
        instance=rmdir,
        description="Remove a folder from the current working directory",
        usage="<folder_name>",
        shortening=False,
    )
    handler.add_command(
        instance=rm,
        description="Remove a file from the current working directory",
        usage="<file_name>",
    )
    handler.add_command(
        instance=touch,
        description="Create a file in the current working directory",
        usage="<file_name>",
    )
    handler.add_command(
        instance=ren,
        description="Rename a file/directory in the current working directory",
        usage="<file_name>",
    )
