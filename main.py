from utils.color_print import Color
from utils.database import Database
from commands.command_handling import CommandHandler
from startup import Startup


color = Color()
db = Database("database.db", auto_dump=True)
startup = Startup(db)


def main():
    color.print("green", "Welcome.")
    startup.start()
    command_handler = CommandHandler(db)
    color.print("green", "Type `help` for help.")
    command_handler.start()


if __name__ == "__main__":
    main()
