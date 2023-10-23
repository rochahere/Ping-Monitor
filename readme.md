# SCADA Ping Monitor

SCADA Ping Monitor is a Python application that allows you to monitor the availability and latency of network hosts using ICMP ping requests. This README provides an overview of the project's main components and usage.

## Table of Contents

- [SCADA Ping Monitor](#scada-ping-monitor)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Main Script (main.py)](#main-script-mainpy)
  - [Logging Configuration (log\_config.py)](#logging-configuration-log_configpy)
  - [Graphical User Interface (gui.py)](#graphical-user-interface-guipy)
  - [Getting Started](#getting-started)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

The SCADA Ping Monitor application allows you to:

- Monitor the status and latency of network hosts.
- Generate reports for multiple or selected devices.
- Add, update, and remove devices in the database.
- View and manage the device list.

## Main Script (main.py)

The `main.py` script serves as the entry point of the application. It does the following:

- Sets up logging for the application.
- Initializes the database.
- Creates the main graphical user interface using Tkinter.
- Provides a menu for generating reports, managing the database, and more.

To start the application, run:

```bash
python main.py
```

## Logging Configuration (log_config.py)

The log_config.py module configures the logging settings for the application. It allows you to control the log file, log level, and log message format. You can customize logging by calling the configure_logging function.

Example usage:

```python
from log_config import configure_logging

# Configure logging with custom settings
logger = configure_logging(log_file='ping.log', log_level=logging.DEBUG)
logger.debug("This is a debug message.")
```

## Graphical User Interface (gui.py)

The gui.py script defines the graphical user interface of the application. It provides the following features:

Ping monitoring of devices.
Device management (add, update, remove).
Display of ping results.
Report generation.
To use the graphical user interface, run the application using the main.py script. The GUI allows you to generate full reports for all devices or generate reports for selected devices.

## Getting Started

Follow these steps to get started with the SCADA Ping Monitor:

1. Clone this repository:

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

2. Install the required Python dependencies by running:

```bash
pip install -r requirements.txt
```

3. Start the application by running the main.py script:

```bash
python main.py
```

## Usage

Once you start the application, you can interact with it via the graphical user interface. You can add devices, update their details, remove them, generate reports, and more.

## Contributing

If you'd like to contribute to this project, please follow the contribution guidelines provided in the CONTRIBUTING.md file.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to customize this README to include specific details about your project or add additional sections as needed.
