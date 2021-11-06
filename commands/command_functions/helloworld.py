def hello_world(attrs):
    print("It works!")
    print(attrs.user_input)


def setup(handler):
    handler.add_command(
        ins=hello_world, description="Hello world command. What else could it be huh?"
    )
