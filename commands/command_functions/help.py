from shutil import get_terminal_size
from textwrap import dedent

# def longest_line(commands: list) -> str:
#     longest = str()
#     for command in commands:
#         desc = command.description
#         lines = desc.splitlines()
#         for line in lines:
#             if len(line) > len(longest):
#                 longest = line
#     return longest


def sort_commands(commands: list) -> list:
    return sorted(commands, key=lambda command: command.name)


def help_command(attrs, command_name: str = None):
    color = attrs.instance.color
    commands = sort_commands(attrs.ins.commands)
    found = False
    if command_name is None: color.print('green', 'You can do `help [command_name]` for more information about a command.')
    for command in commands:
        if command_name is not None:
            if not command_name.lower() in (
                [i.lower() for i in command.alias] + [command.name.lower()]
            ):
                continue
            else:
                found = True
        fancy_line = "-" * len(command.name)
        alias_string = (" | " + " | ".join(command.alias)) if command.alias else ""
        print(f"{color.yellow}{command.name}{alias_string} {color.lightred_ex}{command.usage}")
        if command_name is not None: print(f"{color.cyan}{fancy_line} > Description:\n{command.description}")
    if command_name is not None and found is False:
        attrs.ins.color.print("red", "Command not found.")


def setup(handler):
    handler.add_command(
        ins=help_command, name="help", description="Shows this message."
    )
