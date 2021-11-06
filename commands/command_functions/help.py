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


def help_command(attrs):
    color = attrs.instance.color
    longest_line_len = len(longest_line(attrs.instance.commands))
    for command in attrs.instance.commands:
        fancy_line = "-" * len(command.name)
        alias_string = "| " + " | ".join(command.alias) if command.alias else ""
        color.print("white", "=" * longest_line_len)
        color.print("yellow", command.name, alias_string)
        color.print("blue", fancy_line, ">", "Description:")
        color.print("blue", command.description)
        color.print("white", "=" * longest_line_len)


def setup(handler):
    handler.add_command(
        ins=help_command, name="help", description="Shows this message."
    )
