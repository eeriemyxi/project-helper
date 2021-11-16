import os
from contextlib import suppress


def exec_command(attrs, *, command):
    os.chdir(str(attrs.ins.cwd))
    with suppress(KeyboardInterrupt):
        os.system(command)

def setup(handler):
    handler.add_command(
        instance=exec_command,
        name='exec',
        description="Execute terminal command.",
        usage="<command>",
        alias=["ex"],
        shortening=False,
    )
