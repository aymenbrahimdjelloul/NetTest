"""

@author: Aymen Brahim Djelloul
@version : 0.1
@date : 22.07.2025
@license : MIT License


"""

# IMPORTS
import sys
import socket
import platform
import requests
import datetime
from typing import Any, Optional
from dataclasses import dataclass


# Define global variables
VERSION: str = "0.1"
PLATFORM_NAME: str = platform.platform()
TIMEOUT: int = 5



@dataclass
class TestResult:

    success: bool = False
    internet_connected: Optional[bool] = False
    interface_type: Optional[str] = None
    gateway_ip: Optional[str] = None
    machine_ip: Optional[str] = None
    network_latency: Optional[float] = None
    internet_ping: Optional[int] = None

    public_ip: Optional[str] = None
    isp: Optional[str] = None
    bandwidth_down_mbps: Optional[float] = None
    bandwidth_up_mbps: Optional[float] = None
    timestamp: datetime = datetime.datetime.now()



class NetTest(object):

    def __init__(self, dev_mode: bool = False) -> None:

        self._dev_mode = dev_mode

    def is_connected(self, timeout: float = 3.0, host: str = "8.8.8.8", port: int = 53) -> bool:
        """
        Checks internet connectivity by attempting a socket connection.
        Uses `traceback` for detailed debug logs in dev_mode.

        Args:
            timeout (float): Socket timeout in seconds.
            host (str): Remote host to test (default: Google DNS).
            port (int): Port to connect to (default: 53).

        Returns:
            bool: True if connected, False otherwise.
        """
        try:
            socket.setdefaulttimeout(timeout)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            sock.close()
            return True
        except Exception as e:
            if self._dev_mode:
                # Log full traceback instead of just printing
                import traceback
                traceback.print_exc()  # Detailed error in dev

            return False

    def get_gateway_ip(self) -> str:
        """ This method will retrive the GateWay ip address in cross-platform"""

    def get_machine_ip(self) -> str:
        """ This method will retrive the machine ip address in cross-platform"""

    def get_interface_type(self) -> str:
        """ This method will get the interface name string Wi-Fi or Ethernet from cross-platform"""

    def measure_network_latency(self) -> float:
        """ This method will get the network latency measure in cross-platform"""

    def measure_internet_ping(self) -> int:
        """ This method will get the internet ping measure in ms"""

    def get_public_ip(self) -> str:
        """ This method will retrive the public ip address in cross-platform"""

    def get_isp_name(self) -> str:
        """ This method will determine the isp name string"""

    def measure_down_bandwidth(self, friendly: bool = False) -> float:
        """ This method will measure the download bandwidth speed"""

    def measure_up_bandwidth(self, friendly: bool = False) -> float:
        """ This method will measure the upload bandwidth speed"""


    def run_test(self) -> TestResult:
        """ This method will run the whole test and return the result"""

        try:
            return TestResult(
                success=True,
                internet_connected=self.is_connected(),
                interface_type=self.get_interface_type(),
                gateway_ip=self.get_gateway_ip(),
                machine_ip=self.get_machine_ip(),
                network_latency=self.measure_network_latency(),
                internet_ping=self.measure_internet_ping(),

                public_ip=self.get_public_ip(),
                isp=self.get_isp_name(),
                bandwidth_down_mbps=self.measure_down_bandwidth(friendly=True),
                bandwidth_up_mbps=self.measure_up_bandwidth(friendly=True),
            )

        except Exception:

            if self._dev_mode:
                import traceback
                traceback.print_exc()

            return TestResult(
                success=False
            )

    def __str__(self) -> str:
        pass


if __name__ == '__main__':
    sys.exit(0)
