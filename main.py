from utils._logging import Logger
from utils.color_print import Color
from commands.command_handling import CommandHandler

startup_log = Logger(name="startup.log")
command_handler = CommandHandler()
color = Color()


def main():
    color.print("red", "hello world!")
    command_handler.start()


if __name__ == "__main__":
    main()
