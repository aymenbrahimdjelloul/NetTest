"""

@author: Aymen Brahim Djelloul
@version : 0.1
@date : 22.07.2025
@license : MIT License


"""

# IMPORTS
import sys
import time
import socket
import platform
import requests
import datetime
import subprocess
from typing import Any, Optional
from dataclasses import dataclass


# Define global variables
VERSION: str = "0.1"
PLATFORM_NAME: str = platform.platform(terse=True)
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
    """
    A network testing utility class that provides methods to gather network information.

    This class includes functionality to:
    - Get the public IP address
    - Get the local gateway IP address
    - Get ISP information
    - Validate IP addresses
    - Perform basic network connectivity tests

    Example usage:
        >>> tester = NetTest()
        >>> public_ip = tester.get_public_ip()
        >>> gateway_ip = tester.get_gateway_ip()
        >>> isp_info = tester.get_isp_info()

    Note: Some methods require internet connectivity and may raise exceptions if
    network services are unavailable.
    """

    _PUBLIC_IP_API: str = "https://api.ipify.org"

    def __init__(self, dev_mode: bool = False) -> None:

        # Define developer mode
        self._dev_mode = dev_mode

        # Define requests session
        self._r_session = requests.Session()

        # Define empty variables for caching
        self._public_ip: Optional[str] = None

    def is_connected(self, timeout: float = 3.0, host: str = "8.8.8.8", port: int = 53) -> bool:
        """
        Checks internet connectivity by attempting a socket connection.

        Args:
            timeout (float): Socket timeout in seconds.
            Host (str): Remote host to test (default: Google DNS).
            Port (int): Port to connect to (default: 53).

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
        """
        Returns the default gateway IP address with optimized performance.
        Fast platform-specific detection with minimal overhead.

        Returns:
            str: The gateway IP address or "Unknown" if detection fails
        """

        try:
            if "Linux" in PLATFORM_NAME:
                # Fastest: Direct /proc/net/route parsing
                try:
                    with open('/proc/net/route', 'r') as f:
                        next(f)  # Skip header
                        for line in f:
                            fields = line.split()
                            if len(fields) > 2 and fields[1] == '00000000':  # Default route
                                gateway_hex = fields[2]
                                if gateway_hex != '00000000':
                                    gateway_int = int(gateway_hex, 16)
                                    gateway_ip = socket.inet_ntoa(struct.pack('<I', gateway_int))
                                    return gateway_ip
                except (IOError, ValueError, struct.error):
                    pass

                # Fallback: ip route (faster than route -n)
                result = subprocess.run(
                    ["ip", "r", "s", "0/0"], capture_output=True, text=True, timeout=2
                )
                for line in result.stdout.split('\n'):
                    if "via" in line:
                        parts = line.split()
                        via_idx = next((i for i, x in enumerate(parts) if x == "via"), -1)
                        if via_idx != -1 and via_idx + 1 < len(parts):
                            return parts[via_idx + 1]

            elif "Windows" in PLATFORM_NAME:
                # Fast route command with specific target
                result = subprocess.run(
                    ["route", "print", "-4", "0.0.0.0"], capture_output=True, text=True, timeout=2
                )
                for line in result.stdout.split('\n'):
                    if "0.0.0.0" in line:
                        parts = line.split()
                        if len(parts) >= 3 and parts[0] == "0.0.0.0" and parts[1] == "0.0.0.0":
                            gateway = parts[2]
                            if gateway != "On-link":
                                return gateway

            elif "darwin" in PLATFORM_NAME:  # macOS
                result = subprocess.run(
                    ["route", "-n", "get", "0.0.0.0"], capture_output=True, text=True, timeout=2
                )
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if line.startswith("gateway:"):
                        return line.split(":")[1].strip()

        except (subprocess.SubprocessError, subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # Ultra-fast fallback: Derive from local IP
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(1)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]

            # Most common gateway pattern
            parts = local_ip.split('.')
            if len(parts) == 4:
                return f"{parts[0]}.{parts[1]}.{parts[2]}.1"

        except (socket.error, socket.timeout):
            pass

        return "n/a"

    def get_machine_ip(self) -> str:
        """
        Returns the machine's primary IP address (not loopback).
        Uses multiple fallback methods for maximum reliability.
        Works on Windows, Linux, and macOS.

        Returns:
            str: The primary IP address or "Unknown" if detection fails
        """

        # Method 1: Socket connection (most reliable)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(3)
                # Try multiple external hosts for redundancy
                for host in ["8.8.8.8", "1.1.1.1", "208.67.222.222"]:
                    try:
                        s.connect((host, 80))
                        ip = s.getsockname()[0]
                        if ip and not ip.startswith(('127.', '169.254.')):
                            return ip
                    except (socket.timeout, socket.error):
                        continue
        except Exception:
            pass

        # Method 2: Platform-specific system commands
        try:
            system = platform.system().lower()

            if "Windows" in PLATFORM_NAME:
                result = subprocess.run(
                    ["ipconfig"], capture_output=True, text=True, timeout=5
                )
                for line in result.stdout.split('\n'):
                    if "IPv4 Address" in line and ":" in line:
                        ip = line.split(":")[-1].strip()
                        if ip and not ip.startswith(('127.', '169.254.')):
                            return ip

            else:  # Linux/macOS
                for cmd in [["hostname", "-I"], ["ifconfig"], ["ip", "addr", "show"]]:
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

                        if cmd[0] == "hostname":
                            # hostname -I returns space-separated IPs
                            ips = result.stdout.strip().split()
                            for ip in ips:
                                if ip and not ip.startswith(('127.', '169.254.')):
                                    return ip
                        else:
                            # Parse ifconfig/ip output
                            import re
                            ips = re.findall(r'inet (?:addr:)?(\d+\.\d+\.\d+\.\d+)', result.stdout)
                            for ip in ips:
                                if ip and not ip.startswith(('127.', '169.254.')):
                                    return ip

                    except (subprocess.SubprocessError, FileNotFoundError):
                        continue

        except Exception:
            pass

        return "n/a"

    def get_interface_type(self) -> str:
        """
        Detects whether the primary network interface is Wi-Fi or Ethernet.
        Returns:
            str: 'Wi-Fi', 'Ethernet', or 'Unknown'
        """

        try:
            if "Windows" in PLATFORM_NAME:
                # Windows detection
                result = subprocess.run(
                    ["netsh", "interface", "show", "interface"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                for line in result.stdout.splitlines():
                    if "Connected" in line:
                        if "Wi-Fi" in line:
                            return "Wi-Fi"
                        elif "Ethernet" in line:
                            return "Ethernet"
                return "Unknown"

            elif "Linux" in PLATFORM_NAME:
                # Linux detection
                route_result = subprocess.run(
                    ["ip", "route", "show", "default"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                match = re.search(r'dev\s+(\w+)', route_result.stdout)
                if not match:
                    return "Unknown"

                interface = match.group(1)
                wireless_path = f"/sys/class/net/{interface}/wireless"
                if os.path.exists(wireless_path):
                    return "Wi-Fi"
                return "Ethernet"

            elif "Darwin" in PLATFORM_NAME:  # macOS
                # macOS detection
                service_result = subprocess.run(
                    ["networksetup", "-listallhardwareports"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                for line in service_result.stdout.splitlines():
                    if "Device: " in line:
                        interface = line.split(": ")[1].strip()
                        if "en" in interface:
                            if "AirPort" in service_result.stdout:
                                return "Wi-Fi"
                            return "Ethernet"
                return "Unknown"

            else:
                return "Unknown"

        except (subprocess.CalledProcessError, FileNotFoundError, Exception):
            return "Unknown"

    def measure_network_latency(self) -> float:
        """ This method will get the network latency measure in cross-platform"""
        return 1

    def measure_internet_ping(self) -> int:
        """Measure approximate internet ping in milliseconds using a TCP handshake."""
        host = "8.8.8.8"  # Google's DNS server
        port = 53  # DNS service port
        timeout = 2  # seconds

        try:
            start = time.perf_counter()
            with socket.create_connection((host, port), timeout=timeout):
                end = time.perf_counter()
            ping_ms = int((end - start) * 1000)  # convert to milliseconds
            return ping_ms
        
        except (socket.timeout, socket.error):
            return -1  # Indicates failure to connect

    def get_public_ip(self) -> str:
        """Retrieve the public IP address in a cross-platform manner.

        Returns:
            str: The public IP address as a string, or "Unknown" if the request fails.
        """

        # Check if the public ip address is cached
        if self._public_ip:
            return self._public_ip

        try:
            response = self._r_session.get(
                url=self._PUBLIC_IP_API,
                timeout=TIMEOUT
            )

            response.raise_for_status()         # Raise exception for HTTP errors
            ip: str = response.text.strip()     # Remove any whitespace

            # Cache the public ip
            self._public_ip = ip
            return ip

        except requests.exceptions.RequestException as e:
            if self._dev_mode:
                import traceback
                traceback.print_exc()
            return "n/a"

    def get_isp_name(self) -> str:
        """
        Determine the Internet Service Provider (ISP) name for the current connection.

        Returns:
            str: The ISP name (e.g., "Telecom Algeria") if available, otherwise "n/a".
        """
        try:
            response = self._r_session.get(
                url="https://ipinfo.io/json",
                timeout=TIMEOUT
            )
            response.raise_for_status()

            data = response.json()
            org = data.get("org")  # e.g., "AS36947 Telecom Algeria"
            public_ip = data.get("ip")

            # Check if public ip is cached
            if not self._public_ip:
                # so we will check for it and cache it
                if public_ip:
                    self._public_ip = public_ip

            if org:
                # Strip the AS number if present
                return org.split(" ", 1)[1] if " " in org else org

            return "n/a"

        except requests.exceptions.RequestException as e:
            if self._dev_mode:
                import logging
                logging.error(f"ISP lookup failed: {str(e)}")
            return "n/a"

    # def measure_down_bandwidth(self, friendly: bool = False) -> float:
    #     """ This method will measure the download bandwidth speed"""
    #     return "n/a"
    #
    # def measure_up_bandwidth(self, friendly: bool = False) -> float:
    #     """ This method will measure the upload bandwidth speed"""
    #     return "n/a"

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
