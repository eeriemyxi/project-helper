def settings(attrs, setting: str, *, value: str) -> None:
    attrs.log.info("Checking if setting `%s exists.", setting)
    if attrs.db.exists(setting.lower()):
        attrs.db.set(setting.lower(), value)
        attrs.log.info("Setting `%s` was set to `%s`", setting, value)
        attrs.ins.color.print(
            "magenta", f"Settings for `{setting}` has been set to `{value}`."
        )
    else:
        attrs.log.info("Setting `%s` was not found", setting)
        attrs.ins.color.print("red", f"Setting `{setting}` not found.")


def setup(handler):
    handler.add_command(
        instance=settings,
        description="Change settings.",
        usage="<setting_name> <value>",
    )
