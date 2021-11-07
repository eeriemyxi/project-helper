def create(attrs, *, name: str):
    print(attrs.ins.current_directory)

def setup(handler):
    handler.add_command(
        instance=create,
        usage='<name>',
        description='Create a new project.'
    )
