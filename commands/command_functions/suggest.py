from discord_webhook import DiscordWebhook, DiscordEmbed
from commands.command_handling import CommandAttrs
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/874346590234615848/xBYVKyNxziJzrsnhzY1zW5OCgQR_0vmNEhQ8SKsuHDKZSbW3vwZVILw2NgcJoEyq_J3D"


def suggest(attrs: CommandAttrs, *, message: str) -> None:
    print(message)
    name = attrs.db._dget("name")
    attrs.ins.color.print(
        "green",
        f"Hello {name}, I see you want to suggest me something! I am thankful for your time.\nIf you want me to respond back to you, you have to tell me how to contact you.",
    )
    embed = DiscordEmbed(title="New suggestion!", description=message)
    embed.set_author(name=name)
    embed.set_footer(text="Time: {}".format(datetime.now().strftime("%c")))
    response = attrs.get_user_input(
        "YES or NO",
        lambda x: x.lower() in ("yes", "no"),
        wrong="Your answer should either be `yes` or `no`.",
        process=lambda x: dict(yes=True, no=False)[x.lower()],
    )
    if response:
        contact_info = attrs.get_user_input(
            "Please enter something that would help me contact you",
            process=lambda x: x or "Not specified",
        )
        embed.add_embed_field(name="Contact info", value=contact_info)
    webhook = DiscordWebhook(url=WEBHOOK_URL)
    webhook.add_embed(embed)
    webhook.execute()
    attrs.ins.color.print("green", "Thanks.")


def setup(handler) -> None:
    handler.add_command(
        instance=suggest, description="Suggest me something.", usage="<message>"
    )
