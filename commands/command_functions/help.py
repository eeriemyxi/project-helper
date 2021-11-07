from typing import List


def longest_line(commands: List) -> str:
    longest = str()
    for command in commands:
        desc = command.description
        lines = desc.splitlines()
        for line in lines:
            if len(line) > len(longest):
                longest = line
    return longest

def sort_commands(commands: List) -> List:
    return sorted(commands, key=lambda command: command.name)

def help_command(attrs):
    color = attrs.instance.color
    commands = sort_commands(attrs.ins.commands)
    longest_line_len = len(longest_line(commands))
    for command in commands:
        fancy_line = "-" * len(command.name)
        alias_string = ("| " + " | ".join(command.alias)) if command.alias else ""
        color.print("white", "=" * longest_line_len)
        color.print("yellow", command.name, alias_string, end=' ')
        color.print("LIGHTRED_EX", command.usage)
        color.print("cyan", fancy_line, ">", "Description:")
        color.print("cyan", command.description)
        color.print("white", "=" * longest_line_len)


def setup(handler):
    handler.add_command(
        ins=help_command, name="help", description="Shows this message."
    )
