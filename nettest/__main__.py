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
import argparse
from time import perf_counter

from nettest import NetTest, PLATFORM_NAME


try:
    from colorama import Fore, Style, init
    init(autoreset=True)

    class Colors:
        """ This class contains colors using colorama library """
        BOLD: str = Style.BRIGHT
        GREEN: str = Fore.GREEN
        RED: str = Fore.RED
        YELLOW: str = Fore.YELLOW
        BLUE: str = Fore.BLUE
        END: str = Style.RESET_ALL

except ImportError:
    class Colors:
        """ This Class will replace the colorama library colors variables if exception"""
        BOLD: str = '\033[1m'
        GREEN: str = ""
        RED: str = ""
        YELLOW: str = ""
        BLUE: str = ""
        END: str = ""


class _Const:
    """ This class contains constants """
    version: str = "0.1"
    caption: str = f"NetTest - v{version}"
    website: str = "https://github.com/aymenbrahimdjelloul/NetTest"


class Interface:
    def __init__(self) -> None:
        # Define the NetTest object
        self.nettest = NetTest()

        # Print the header
        self._print_header()
        # Set console title
        self._set_console_title()

    def _set_console_title(self):
        """ This method will set the console title for windows only"""
        if "Windows" == PLATFORM_NAME:
            os.system(f"title {_Const.caption}")

    def _print_header(self) -> None:
        """ This method will print the software header"""
        print(f"\n{Colors.BLUE}{_Const.caption}{Colors.END}   {_Const.website}\n")

    def _print_help(self) -> None:
        """ This method will print the help message"""
        help_text = f"""
{Colors.BOLD}NetTest Command Line Interface{Colors.END}
{Colors.BOLD}Usage:{Colors.END}
  nettest [options]

{Colors.BOLD}Options:{Colors.END}
  -h, --help            Show this help message and exit
  -v, --version         Show version information
  -l, --local           Show only local network information
  -r, --remote          Show only remote/online information
  --latency             Measure network latency
  --ping                Measure internet ping
  --ip                  Show public IP address
  --isp                 Show ISP information
  --all                 Show all information (default)
"""
        print(help_text)

    def run(self, args) -> None:
        """ This method will run the command-line interface with given arguments"""

        if args.all or (not args.local and not args.remote and not args.latency
                        and not args.ping and not args.ip and not args.isp):

            # Show all information if no specific options are provided or --all is used
            self._print_all_info()

        else:
            # Show specific information based on provided arguments
            if args.local:
                self._print_local_info()
            if args.remote:
                self._print_remote_info()
            if args.latency:
                self._print_latency()
            if args.ping:
                self._print_ping()
            if args.ip:
                self._print_public_ip()
            if args.isp:
                self._print_isp_info()

    def _print_all_info(self):
        """Print all network information"""

        s_time: float = perf_counter()

        # Print information
        self._print_local_info()
        self._print_remote_info()

        # Show execution time
        print(f"{Colors.GREEN}{Colors.BOLD} [*] Finished in : {perf_counter() - s_time:.2f} s{Colors.END}\n")

        # Wait for user input to exit
        input("Press Enter to exit..")
        sys.exit(0)

    def _print_local_info(self):
        """Print local network information"""
        print(f"{Colors.BOLD}- Local Information:{Colors.END}\n"
              f" [*] Internet Connection :  {f'{Colors.GREEN}Yes{Colors.END}' if self.nettest.is_connected() else f'{Colors.RED}No{Colors.END}'}\n"
              f" [*] Machine IP          :  {Colors.BOLD}{self.nettest.get_machine_ip()}{Colors.END}\n"
              f" [*] Gateway IP          :  {Colors.BOLD}{self.nettest.get_gateway_ip()}{Colors.END}\n"
              f" [*] Interface Type      :  {Colors.BOLD}{self.nettest.get_interface_type()}{Colors.END}\n"
              f" [*] Network Latency     :  {Colors.BOLD}{self.nettest.measure_network_latency()} ms{Colors.END}\n")

    def _print_remote_info(self):
        """Print remote/online information"""
        print(f"{Colors.BOLD}- Online Information:{Colors.END}\n"
              f" [*] Public IP           :  {Colors.BOLD}{self.nettest.get_public_ip()}{Colors.END}\n"
              f" [*] ISP Name            :  {Colors.BOLD}{self.nettest.get_isp_name()}{Colors.END}\n"
              f" [*] Internet Ping       :  {Colors.BOLD}{self.nettest.measure_internet_ping()} ms{Colors.END}\n")

    def _print_latency(self):
        """Print network latency"""
        print(f"{Colors.BOLD}Network Latency:{Colors.END} {self.nettest.measure_network_latency()}")

    def _print_ping(self):
        """Print internet ping"""
        print(f"{Colors.BOLD}Internet Ping:{Colors.END} {self.nettest.measure_internet_ping()}")

    def _print_public_ip(self):
        """Print public IP address"""
        print(f"{Colors.BOLD}Public IP:{Colors.END} {self.nettest.get_public_ip()}")

    def _print_isp_info(self):
        """Print ISP information"""
        print(f"{Colors.BOLD}ISP Name:{Colors.END} {self.nettest.get_isp_name()}")


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="NetTest - Network testing and information tool",
        add_help=False
    )

    parser.add_argument(
        "-h", "--help",
        action="store_true",
        help="Show this help message and exit"
    )

    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Show version information"
    )

    parser.add_argument(
        "-l", "--local",
        action="store_true",
        help="Show only local network information"
    )

    parser.add_argument(
        "-r", "--remote",
        action="store_true",
        help="Show only remote/online information"
    )

    parser.add_argument(
        "--latency",
        action="store_true",
        help="Measure network latency"
    )

    parser.add_argument(
        "--ping",
        action="store_true",
        help="Measure internet ping"
    )

    parser.add_argument(
        "--ip",
        action="store_true",
        help="Show public IP address"
    )

    parser.add_argument(
        "--isp",
        action="store_true",
        help="Show ISP information"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Show all information (default)"
    )

    return parser.parse_args()


def main():
    """ This main function is the entry point to run this software"""
    try:
        args = parse_arguments()

        if args.help:
            Interface()._print_help()
            sys.exit(0)

        if args.version:
            print(f"NetTest v{_Const.version}")
            sys.exit(0)

        cli = Interface()
        cli.run(args)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)

    except Exception:

        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()