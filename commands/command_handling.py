from typing import Callable, List
from utils.color_print import Color
from utils._logging import Logger
from dataclasses import dataclass
from pkgutil import iter_modules
import importlib.util


@dataclass(init=True)
class CommandInfo:
    name: str
    description: str
    usage: str
    alias: List[str]
    instance: Callable
    shortening: bool


@dataclass(init=True)
class CommandAttrs:
    log: Logger.log
    user_input: str
    instance: object


class CommandHandler:
    def __init__(self) -> None:
        self.logger = Logger(name="commands.log")
        self.log = self.logger.log
        self.color = Color()
        self.commands: List[CommandInfo] = list()

    def get_user_input(self) -> str:
        self.color.print("green", ">>> ", end="")
        return input()

    def add_command(
        self,
        instance: Callable = None,
        ins: Callable = None,
        description: str = "Not specified",
        desc: str = "Not specified",
        usage: str = "Not specified",
        name: str = None,
        alias: List[str] = None,
        shortening: bool = True,
    ) -> None:
        """
        Add `instance` as a command.

        Parameters
        ----------
        instance or ins
            - The function to call when the command is invoked.

        description or desc
            - Description for the command.
              It is shown in the help command.

        usage
            - Arguments the command accepts.

        name
            - Name of the command. If it's `None`, the function name is used.

        alias
            - Aliases of the command.

        shortening
            - Normally the command line searches for the closest match to the user input.
              It iterates through all the commands and searches for the closest match by name.
              If this parameter is False, It will not be triggered unless the user types out
              the entire name.


        Aliases
        -------
        description
            - desc

        instance
            - ins

        """
        not_specified = "Not specified"
        instance = ins or instance
        name = name or instance.__name__
        description = description if desc == not_specified else desc
        self._add_command(
            instance=instance,
            description=description,
            usage=usage,
            name=name,
            alias=alias,
            shortening=shortening,
        )

    def _add_command(
        self,
        instance: Callable,
        description: str,
        usage: str,
        name: str,
        alias: List[str],
        shortening: bool,
    ) -> None:
        self.commands.append(
            CommandInfo(
                name=name,
                description=description,
                usage=usage,
                alias=alias,
                instance=instance,
                shortening=shortening,
            )
        )
        self.log.info("Added command: %s", name)

    def _load_command_from_spec(self, spec) -> None:
        self.log.info("Importing: %s", spec.name)
        lib = importlib.util.module_from_spec(spec)
        self.log.info("Successfully imported: %s", spec.name)
        self.log.info("Executing: %s", spec.name)
        spec.loader.exec_module(lib)
        self.log.info("Executed: %s", spec.name)
        self.log.info("Checking for setup function of %s", spec.name)
        if hasattr(lib, "setup"):
            self.log.info("Setup function found.")
            setup = getattr(lib, "setup")
            setup(self)
            self.log.info("Successfully called setup function.")

    def load_commands(self) -> int:
        """
        Loads all the commands from commands.command_functions.

        Returns
        ------
        `int`:
            Count of commands.
        """
        commands = iter_modules(["commands/command_functions"])
        count = 0
        for command in commands:
            package_path = f"commands.command_functions.{command.name}"
            spec = importlib.util.find_spec(package_path)
            self._load_command_from_spec(spec)
            count += 1
        return count

    def start(self) -> None:
        """
        This method starts the handler.
        """
        self.log.info("Starting CommandHandler.")
        self.log.info("Loading commands.")
        count = self.load_commands()
        self.log.info("Loading commands successful. Total commands: %s.", count)
        self.log.info("Starting main loop.")
        while True:
            user_input = self.get_user_input()
            self.log.info("User input: %s", user_input)
            for command in self.commands:
                if command.name.lower().startswith(user_input.lower()):
                    if (
                        command.shortening
                        or command.shortening is False
                        and user_input.lower() == command.name.lower()
                    ):
                        command.instance(
                            CommandAttrs(
                                log=self.log, user_input=user_input, instance=self
                            )
                        )

                    self.log.info("Command invoked: %s", command.name)
