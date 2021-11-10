from typing import List


def longest_line(commands: list) -> str:
    longest = str()
    for command in commands:
        desc = command.description
        lines = desc.splitlines()
        for line in lines:
            if len(line) > len(longest):
                longest = line
    return longest


def sort_commands(commands: list) -> list:
    return sorted(commands, key=lambda command: command.name)


def help_command(attrs, command_name: str = None):
    color = attrs.instance.color
    commands = sort_commands(attrs.ins.commands)
    longest_line_len = len(longest_line(commands))
    found = False
    for command in commands:
        if command_name is not None:
            if not command_name.lower() in (
                [i.lower() for i in command.alias] + [command.name.lower()]
            ):
                continue
            else:
                found = True
        fancy_line = "-" * len(command.name)
        alias_string = ("| " + " | ".join(command.alias)) if command.alias else ""
        color.print("white", "=" * longest_line_len)
        color.print("yellow", command.name, alias_string, end=" ")
        color.print("LIGHTRED_EX", command.usage)
        color.print("cyan", fancy_line, ">", "Description:")
        color.print("cyan", command.description)
        color.print("white", "=" * longest_line_len)
    if command_name is not None and found is False:
        attrs.ins.color.print("red", "Command not found.")


def setup(handler):
    handler.add_command(
        ins=help_command, name="help", description="Shows this message."
    )
