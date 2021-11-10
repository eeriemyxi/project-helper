import os

from utils._logging import Logger
from utils.color_print import Color
from utils.database import Database
from utils.tools import tools


class Startup:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.status = 0
        self.color = Color()
        self.logger = Logger('startup.log')
        self.log = self.logger.log
        self.get_user_input = tools.get_user_input

    def before_startup(self) -> None:
        self.log.info('Setup started.')

    def setup_projects(self) -> None:
        self.db.dcreate("projects")

    def after_startup(self) -> None:
        self.log.info('Startup complete')

    def start(self) -> None:
        self.before_startup()
        self.log.info("Check if path key already exists in database. If True, the user will not be considered new.")
        if not self.db.exists('path'):
            self.welcome()
            self.setup_projects()
        else:
            self.log.info("User has already completed the setup.")
        self.after_startup()
        return

    def welcome(self) -> None:
        def on_exit():
            if self.status == 1:
                exit()
            else:
                os.remove('database.db')
                exit()
        self.log.info('The user is new.')
        self.log.info('Welcoming the user.')
        self.color.print('green', "Oh I see you're a new user.")
        self.color.print('green', "So now I will ask you a few questions. Please answer them correctly!")
        self.color.print('magenta', 'You can exit by typing `exit` anytime.')
        self.color.print('green', "What's your name? Don't worry it's stored locally only.")
        self.log.info('Asking user their name.')
        name = self.get_user_input(
            "Name must be > 3 and < 20", 
            lambda x: len(x) >= 3 and len(x) < 20, 
            "Your entered name must be atleast 3 characters long and shorter than 20 characters.",
            lambda x: x.title(),
            )
        self.log.info('User chose `%s` as their name.', name)
        self.db.set('name', name)
        self.log.info('Asking for path.')
        self.color.print('green', f"Alright {name}, time for a serious one. Where do you want to create your projects? Enter the path below")
        path = self.get_user_input(
            "Please choose an empty folder if possible", 
            lambda x: os.path.isdir(x),
            "Either the path doesn't exist or it is not pointing to a directory.",
            confirm=True,
            restart=(self.welcome, None),
            on_exit=on_exit
            )
        self.log.info('User chose `%s` as their path.', path)
        self.db.set('path', path)
        self.status = 1
        self.color.print('green','Alright. Setup complete. It was easy right?\nRemember, you can always change these settings later by using the following commands:')
        self.color.print('magenta','\t- To change the path, use: `settings path <path>`')
        self.color.print('magenta','\t- To change the name, use: `settings name <name>`')
