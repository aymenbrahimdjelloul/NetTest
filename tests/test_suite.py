import unittest
import time
from nettest import NetTest
from typing import Optional


class TestNetTest(unittest.TestCase):
    """Comprehensive test suite for NetTest functionality."""

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize the NetTest instance once for all tests."""
        cls.nettest = NetTest()
        cls.start_time = time.perf_counter()

    @classmethod
    def tearDownClass(cls) -> None:
        """Print the total test execution time."""
        end_time = time.perf_counter()
        print(f"\nTotal Test Suite Execution Time: {end_time - cls.start_time:.3f} seconds")

    def test_is_connected(self) -> None:
        """Test internet connection status detection."""
        result = self.nettest.is_connected()
        self.assertIsInstance(result, bool,
                              "is_connected() should return a boolean value")

    def test_get_machine_ip(self) -> None:
        """Test machine IP address retrieval and validation."""
        ip = self.nettest.get_machine_ip()
        self._validate_ip_address(ip, "machine IP")

    def test_get_gateway_ip(self) -> None:
        """Test gateway IP address retrieval and validation."""
        ip = self.nettest.get_gateway_ip()
        if ip is not None:  # Gateway IP might be None in some cases
            self._validate_ip_address(ip, "gateway IP")

    def test_get_public_ip(self) -> None:
        """Test public IP address retrieval and validation."""
        ip = self.nettest.get_public_ip()
        if ip is not None:  # Public IP might be None if offline
            self._validate_ip_address(ip, "public IP")

    def test_get_isp_name(self) -> None:
        """Test ISP name retrieval."""
        isp = self.nettest.get_isp_name()
        self.assertIsInstance(isp, str, "ISP name should be a string")
        if not self.nettest.is_connected():
            self.assertEqual(isp, "", "ISP name should be empty when offline")

    def test_get_interface_type(self) -> None:
        """Test network interface type detection."""
        interface = self.nettest.get_interface_type()
        valid_interfaces = ['Ethernet', 'WiFi', 'Unknown']
        self.assertIn(interface, valid_interfaces,
                      f"Interface type should be one of {valid_interfaces}")

    def test_measure_network_latency(self) -> None:
        """Test network latency measurement."""
        latency = self.nettest.measure_network_latency()
        self.assertIsInstance(latency, (float, int),
                              "Latency should be a numeric value")
        self.assertGreaterEqual(latency, 0,
                                "Latency should not be negative")
        if not self.nettest.is_connected():
            self.assertEqual(latency, float('inf'),
                             "Latency should be infinite when offline")

    def _validate_ip_address(self, ip: str, description: str) -> None:
        """Helper method to validate IP address format."""
        self.assertIsInstance(ip, str,
                              f"{description} should be a string")
        self.assertRegex(ip, r'^\d{1,3}(\.\d{1,3}){3}$',
                         f"Invalid {description} format")
        # Validate each octet is between 0-255
        for octet in ip.split('.'):
            self.assertTrue(0 <= int(octet) <= 255,
                            f"Invalid octet in {description}")


if __name__ == "__main__":
    unittest.main(verbosity=2)