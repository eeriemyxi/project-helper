import pathlib
from typing import Any, Callable
from utils.color_print import Color


color = Color()


class tools:
    def fix_folder_path(path):
        path = pathlib.PurePath(path)
        fixed_folder = path.name.replace(" ", "-")
        return str(pathlib.PurePath(path.parent).joinpath(fixed_folder))

    def fix_folder(folder_name):
        return folder_name.replace(" ", "-")

    def get_user_input(
        text: str = "",
        predicate: Callable = None,
        wrong: str = None,
        process: Callable = None,
        confirm: bool = False,
        restart: list[Callable, list[Any]] = None,
        on_exit: Callable = None,
    ) -> str:
        if restart:
            assert (
                len(restart) == 2
            ), "`restart` must be a tuple of Callable and its arguments if used."

        def return_input():
            if confirm:
                color.print("red", "Your input: %s" % user_input)
                input_text("Type `confirm` to confirm")
                if input().lower() == "confirm":
                    return process(user_input) if process else user_input
                else:
                    color.print("magenta", "Restarting...")
                    color.print("white", "-" * 30)
                    return restart[0](*restart[1])
            else:
                return process(user_input) if process else user_input

        def exit_check(user_input):
            if user_input.lower() == "exit":
                on_exit() if on_exit else exit()

        input_text = lambda x=None: [
            color.print("yellow", x or text, end=" " if (x or text) else ""),
            color.print("cyan", ">>> ", end=""),
        ]
        input_text()
        user_input = input()
        exit_check(user_input)
        if predicate is not None:
            result = bool(predicate(user_input))
            if result is False:
                while result is not True:
                    color.print("red", wrong)
                    input_text()
                    user_input = input()
                    exit_check(user_input)
                    result = bool(predicate(user_input))
            return return_input()
        else:
            return return_input()

    def debug_print(*objects):
        for object in objects:
            print(object)
