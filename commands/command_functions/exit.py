def exit_command(attrs):
    exit()


def setup(handler):
    handler.add_command(
        ins=exit_command,
        name="exit",
        description="Exit from the script.",
        shortening=False,
    )
