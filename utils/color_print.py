from colorama import Fore, Style, init


class Color:
    """
    This class exists to make printing colored text easier.
    """

    def __init__(self) -> None:
        init()
        self.colors = [color for color in dir(Fore) if not color.startswith("_")]

    def print(self, color: str, *objects, **kwargs) -> None:
        """
        Color prints text using the module `colorama`.

        Parameters
        ----------
        color: `str`
            - Set the color to print the text with.

        *objects:
            - Objects to print.

        **kwargs
            - Other parameters of `print` built-in function.
        """
        color = color.upper()
        assert hasattr(
            Fore, color
        ), "Invalid color. It must be one of these: %s" % ", ".join(self.colors)
        print(getattr(Fore, color), end="")
        print(*objects, end="")
        print(Fore.RESET, **kwargs)
