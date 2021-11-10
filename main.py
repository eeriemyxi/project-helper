from utils._logging import Logger
from utils.color_print import Color
from utils.database import Database
from commands.command_handling import CommandHandler
from startup import Startup


db = Database('database.db', auto_dump=True)
startup = Startup(db)
command_handler = CommandHandler(db)
color = Color()

def main():
    color.print("green", "Welcome.")
    startup.start()
    color.print('green', 'Type `help` for help.')
    command_handler.start()

if __name__ == "__main__":
    main()
