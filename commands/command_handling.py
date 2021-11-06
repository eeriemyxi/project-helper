from utils.color_print import Color
from utils._logging import Logger


class CommandHandler:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.log = self.logger.log
        self.color = Color()
    
    def get_user_input(self) -> str:
        self.color.print('green', '>>> ', end='')
        return input()

    def start(self) -> None:
        '''
        This function starts the handler.
        '''
        while True:
            user_info = self.get_user_input()
            print(user_info)
            self.log.warn(user_info)
            if user_info == 'exit':
                self.logger.close()
                exit()