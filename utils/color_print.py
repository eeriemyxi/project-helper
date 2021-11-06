from colorama import Fore, Style, init


class Color:
    '''
    This class exists to make printing colored text easier.
    '''
    def __init__(self) -> None:
        init()
        self.colors = [color for color in dir(Fore) if not color.startswith("_")]
        # self.colors = list(filter(lambda color: not color.startswith('_'), dir(Fore)))

    def print(self, color: str, *objects, **kwargs) -> None:
        """
        Color prints text using the module `colorama`.

        Parameters
        ----------
        color: `str`
            Set the color to print text with.
        *objects:
            Objects to print.
        """
        color = color.upper()
        assert hasattr(
            Fore, color
        ), "Invalid color. It must be one of these: %s" % ", ".join(self.colors)
        print(getattr(Fore, color), end="")
        print(*objects, end="")
        print(Fore.RESET, **kwargs)
