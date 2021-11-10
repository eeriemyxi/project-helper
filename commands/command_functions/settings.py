def settings(attrs, setting: str, *, value: str) -> None:
    if attrs.db.exists(setting.lower()):
        attrs.db.set(setting.lower(), value)
        attrs.ins.color.print('magenta', f'Settings for `{setting}` has been set to `{value}`.')
    else:
        attrs.ins.color.print('red', f'Setting `{setting}` not found.')


def setup(handler):
    handler.add_command(
        instance=settings,
        description='Change settings.',
        usage='<setting_name> <value>'
    )