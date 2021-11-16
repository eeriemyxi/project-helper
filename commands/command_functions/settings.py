import pathlib


setting_dict = {
    "delete_empty": (
        "If `true`, It will delete projects that are empty on startup. Accepted values: `true`, `false`.",
        lambda v: v.lower() in ("true", "false"),
        "Input must be either `true` or `false`.",
        lambda v: dict(true=True, false=False)[v],
    ),
    "name": (
        "Change your name.",
        lambda v: 3 <= len(v) <= 20,
        "Name must be longer than 3 charaters and shorter than 20.",
        lambda v: v.title(),
    ),
    "path": (
        "Change the path",
        lambda v: pathlib.Path(v).exists(),
        "Path doesn't exist.",
        lambda v: v,
    ),
}


def settings(attrs, setting: str, *, value: str) -> None:
    attrs.log.info("Checking if setting `%s exists.", setting)
    setting = setting.lower()
    if attrs.db.exists(setting):
        if not setting_dict[setting][1](value):
            attrs.ins.color.print("red", setting_dict[setting][2])
            return
        value = setting_dict[setting][3](value)
        attrs.db.set(setting, value=value)
        attrs.log.info("Setting `%s` was set to `%s`", setting, value)
        attrs.ins.color.print(
            "green", f"Settings for `{setting}` has been set to `{value}`."
        )
    else:
        attrs.log.info("Setting `%s` was not found", setting)
        attrs.ins.color.print("red", f"Setting `{setting}` not found.")


def setup(handler):
    handler.add_command(
        instance=settings,
        description="Change settings.\n-) {}".format(
            "\n-) ".join(
                [
                    f"{name} : {desc}"
                    for name in setting_dict
                    for desc, _, _, _ in [setting_dict[name]]
                ]
            )
        ),
        usage="<setting_name> <value>",
    )
