import logging
import pathlib


class Logger:
    def __init__(self, name: str, ensure=True) -> None:
        self.logger_name = name
        self.log_folder_name = pathlib.Path("./logs")
        self.log_file_path = self.log_folder_name.joinpath(name)
        if ensure:
            self._ensure()
        self.logger = logging.getLogger(name)
        self.log = self.logger
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
        )
        self.file_handler = logging.FileHandler(filename=self.log_file_path)
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def _ensure(self):
        """
        Ensures all files are as it should be.
        """
        self.log_folder_create(self.log_folder_name)
        self.delete_log_if_exists(self.logger_name)

    def log_folder_create(self, name) -> None:
        """
        If the `logs` folder doesn't exist, it creates it.
        """
        if not name.exists():
            name.mkdir()

    def delete_log_if_exists(self, name: str) -> None:
        """
        This will delete the log file if it exists.
        """
        path = self.log_folder_name.joinpath(name)
        if path.exists():
            path.unlink()

    def close(self) -> None:
        """
        Close the logger.
        """
        self.logger.handlers[0].flush()
        logging.shutdown()
