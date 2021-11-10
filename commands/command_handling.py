import importlib.util
import inspect
from dataclasses import dataclass
from pkgutil import iter_modules
from typing import Callable, Dict, List, Tuple

from utils._logging import Logger
from utils.color_print import Color
from utils.database import Database
from utils.tools import tools


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
    db: Database
    user_input: str
    get_user_input: tools.get_user_input
    inp: str  # Alias of `user_input`
    instance: object
    ins: object  # Alias of `instance`


class CommandHandler:
    def __init__(self, db) -> None:
        self.db = db
        self.logger = Logger(name="commands.log")
        self.log = self.logger.log
        self.color = Color()
        self.commands: List[CommandInfo] = list()
        self.current_directory = self.db.get("path")
        self.get_user_input = tools.get_user_input

    def add_command(
        self,
        instance: Callable = None,
        ins: Callable = None,
        description: str = "Not specified",
        desc: str = "Not specified",
        usage: str = "",
        name: str = None,
        alias: List[str] = [],
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

    def _join_aliases_and_command(self, command: CommandInfo) -> List | Tuple:
        return command.alias + [command.name]

    def _parse_arguments(self, args: list, command: CommandInfo) -> Tuple[List, Dict]:
        self.log.info("Parsing arguments of %s", command.name)
        signature = inspect.signature(command.instance)
        found = 0
        for param in signature.parameters.values():
            if param.kind == param.KEYWORD_ONLY and param.default is param.empty:
                found = 1
                values = list(signature.parameters.values())
                index = values.index(param)
                kwargs = {param.name: " ".join(args[index - 1 :])}
                if not kwargs[param.name]:
                    kwargs = dict()
                if len(args) > 1:
                    args = args[: len(values) - 2]
                else:
                    args = []
                self.log.info(
                    "Parsed arguments:\n*args: %s\n**kwargs: %s",
                    repr(args),
                    repr(kwargs),
                )
                return args, kwargs
        if not found:
            return args, {}

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
            self._handle_user_input()

    def _handle_user_input(self) -> None:
        user_input = self.get_user_input()
        user_input_command_name = user_input.split()[0]
        args = user_input.split()[1:]
        self.log.info("User input: %s", user_input)
        for command in self.commands:
            command_with_aliases = self._join_aliases_and_command(command)
            for command_name in command_with_aliases:
                if command_name.lower().startswith(user_input_command_name.lower()):
                    if (
                        command.shortening
                        or command.shortening is False
                        and user_input_command_name.lower() == command_name.lower()
                    ):
                        try:
                            args, kwargs = self._parse_arguments(args, command)
                            attrs = CommandAttrs(
                                log=self.log,
                                db=self.db,
                                user_input=user_input,
                                get_user_input=self.get_user_input,
                                inp=user_input,
                                instance=self,
                                ins=self,
                            )
                            command.instance(attrs, *args, **kwargs)
                            self.log.info("Command invoked: %s", command.name)
                            return
                        except TypeError as error:
                            self.log.info(
                                "While trying to call the function `%s` it raised an error:",
                                command.instance.__name__,
                            )
                            self.log.exception(error)
                            self.color.print(
                                "red",
                                text := "`{0}` command is missing the argument(s) {1}. Please type `help {0}` in the command line to know how to use this command.".format(
                                    command.name,
                                    error.args[0].split(":")[1].strip(),
                                ),
                            )
                            self.log.info(
                                "The error was handled by printing:\n%s", text
                            )
