# NetTest

A simple and straightforward tool to test network connection and performance measures with integrated CLI.

## 🌐 Overview

NetTest is a lightweight, pure Python network testing utility designed to help you quickly assess network connectivity and performance. Built with simplicity in mind, it provides essential network diagnostics through an intuitive command-line interface.

## ✨ Features

- **Connection Testing**: Verify connectivity to hosts and services
- **Performance Measurement**: Test network speed and latency
- **Network Diagnostics**: Comprehensive network status information
- **Integrated CLI**: Simple, user-friendly command-line interface
- **Pure Python**: No external dependencies required
- **Cross-Platform**: Works on Windows, Linux, and macOS

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/aymenbrahimdjelloul/NetTest.git
cd NetTest
```

## 📖 Usage

Run NetTest using the main script:

```bash
python run.py [options]
```

### Basic Commands

Test basic connectivity:
```bash
python run.py --test
```

Measure network performance:
```bash
python run.py --performance
```

Run full diagnostics:
```bash
python run.py --full
```

### Command-Line Options

```
--test          Test network connectivity
--performance   Measure network speed and latency
--host <url>    Specify target host
--port <port>   Specify target port
--timeout <sec> Set connection timeout
--verbose       Enable detailed output
--help          Show help message
```

## 📋 Requirements

- Python 3.6 or higher
- No external dependencies (uses Python standard library only)

## 🛠️ Project Structure

```
NetTest/
├── nettest/          # Core module files
├── tests/            # Test suite
├── run.py            # Main entry point
├── LICENSE           # MIT License
└── README.md         # This file
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues

If you encounter any issues or have suggestions, please [open an issue](https://github.com/aymenbrahimdjelloul/NetTest/issues) on GitHub.

## 📊 Release History

* 0.1 - Initial release (August 2025)

## ⭐ Show Your Support

If you find this tool helpful, please consider giving it a star on GitHub!
