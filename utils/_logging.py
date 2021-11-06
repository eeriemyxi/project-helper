import logging
import os


class Logger:
    def __init__(self, name: str, ensure=True) -> None:
        self.logger_name = name
        self.log_folder_name = "./logs"
        self.log_file_path = os.path.join(self.log_folder_name, name)
        if ensure:
            self._ensure()
        self.logger = logging.getLogger(name)
        self.formatter = logging.Formatter(
            fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p"
        )
        self.file_handler = logging.FileHandler(filename=self.log_file_path)
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    @property
    def log(self) -> logging.Logger:
        return self.logger

    def _ensure(self):
        '''
        Ensures all files are as it should be.
        '''
        self.log_folder_create(self.log_folder_name)
        self.delete_log_if_exists(self.logger_name)

    def log_folder_create(self, name: str) -> None:
        """
        If the `logs` folder doesn't exist, it creates it.
        """
        if not os.path.exists(name):
            os.mkdir(name)
    
    def delete_log_if_exists(self, name: str) -> None:
        '''
        This will delete the log file if it exists.
        '''
        path = os.path.join(self.log_folder_name, name)
        if os.path.exists(path):
            os.remove(path)

    def close(self) -> None:
        '''
        Close the logger.
        '''
        self.logger.handlers[0].flush()
        logging.shutdown()