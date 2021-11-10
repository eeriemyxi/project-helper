import os
import pathlib
import shutil
from itertools import tee
from utils.color_print import Color

print = Color().print


def showdir(attrs):
    path = pathlib.Path(attrs.ins.current_directory)
    print(
        "green",
        "You may use the `finfo` command to get information of a file/directory.",
    )
    files, files2 = tee(path.iterdir())
    if not list(files2):
        print("red", "This directory is empty.")
        return
    for file in files:
        print("yellow", "DIR" if path.joinpath(file).is_dir() else "FILE", end=" > ")
        print("green", file.name)


def finfo(attrs, name: str):
    path = str(pathlib.PurePath(attrs.ins.current_directory))
    for file in pathlib.Path(path).iterdir():
        if name.lower() == file.name.lower():
            stats = file.stat()
            stat_list = [
                ("INODE NUMBER OR FILE INDEX", stats.st_ino),
                ("SIZE", f"{stats.st_size/1000000} MB | {stats.st_size} Bytes"),
            ]
            for property_name, value in stat_list:
                print("yellow", property_name, end=" > ")
                print("green", value)
            return
    print("red", "Not found.")


def copy(attrs, filename, path):
    projectpath = pathlib.Path(attrs.ins.project_path)
    cwd = pathlib.Path(attrs.ins.current_directory)
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
    cwd = pathlib.Path(attrs.ins.current_directory)
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
    cwd = pathlib.Path(attrs.ins.current_directory)
    full_path = cwd.joinpath(foldername)
    if full_path.exists():
        print("red", f"A folder named `{foldername}` already exists.")
        return
    os.mkdir(full_path)


def cd(attrs, path):
    cwd = attrs.ins.current_directory
    full_path = pathlib.PurePath(cwd).joinpath(path)
    if pathlib.Path(full_path).exists():
        attrs.ins.current_directory = full_path
    else:
        print("red", "Path doesn't exist.")


def cd_back(attrs):
    cwd = attrs.ins.current_directory
    new_path = pathlib.PurePath(cwd).parent
    if not attrs.db.get("path") in str(new_path):
        print(
            "red",
            "You are trying to change the current working directory to the parent directory of your specified project path.",
        )
    else:
        attrs.ins.current_directory = new_path


def rmdir(attrs, foldername):
    path = pathlib.Path(attrs.ins.cwd).joinpath(foldername)
    if path.exists():
        os.rmdir(path)
        print("green", "Directory removed.")
    else:
        print("red", "Directory not found.")


def rm(attrs, filename):
    path = pathlib.Path(attrs.ins.cwd).joinpath(filename)
    if path.exists():
        os.remove(path)
        print("green", "File removed.")
    else:
        print("red", "File not found.")


def touch(attrs, filename):
    cwd = pathlib.Path(attrs.ins.cwd)
    path = cwd.joinpath(filename)
    if not path.exists():
        try:
            path.touch()
            print("green", "File has been created.")
        except FileExistsError:
            print("red", "File already exists.")


def setup(handler):
    handler.add_command(
        instance=showdir,
        description="Shows all the files and directories present in the current working directory.",
        alias=["dir"],
    )
    handler.add_command(
        instance=finfo,
        description="Shows information about a file or folder.\nI am not satisfied with this command yet so I might remove or update it later.",
        alias=["fi"],
        usage="[path]",
    )
    handler.add_command(
        instance=copy,
        description="Copies a file from one directory to another.\nThe specified path will be joined with project path and then the file will be copied in the joined path.",
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
