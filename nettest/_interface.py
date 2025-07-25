"""

@author : Aymen Brahim Djelloul
@version : 0.1
@date : 23.07.2025
@license : MIT License

"""

# IMPORTS
import os
import sys
import shutil
from nettest import NetTest


try:

    from colorama import Fore, Style, init

    init(autoreset=True)

    class Colors:
        pass

except ImportError:

    colorama: bool = False

    class Colors:
        pass


class _Const:

    version: str = "0.1"
    name = f"NetTest - v{version}"


class Interface:

    def __init__(self) -> None:

        # Define the NetTest object
        self.nettest = NetTest()

        # Print the header
        self._print_header()

    def _print_header(self) -> None:
        """ This method will print the software header"""

    def _print_help(self) -> None:
        """ This method will print the help message"""

    def run(self) -> None:
        """ This method will run the command-line interface """



def main():
    """ This main function is the entry point to run this software"""

    try:

        cli = Interface()
        cli.run()

    except KeyboardInterrupt:
        sys.exit(0)

    except Exception:

        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    sys.exit(0)