# PC Control Center

A desktop system monitoring application built with Python and PySide6.

## Features

- CPU usage monitoring
- CPU core usage
- CPU frequency monitoring
- CPU and GPU temperature monitoring
- RAM usage, total and available memory
- Disk usage, used and free space
- Real-time CPU usage graph
- Automatic system metrics updates every 2 seconds

## Technologies

- Python 3.14
- PySide6
- psutil
- Linux hardware monitoring (`/sys/class/hwmon/`)

## Project Structure

```text
pc_control_center/
├── core/
│   ├── __init__.py
│   ├── system_monitor.py
│   └── temperature_monitor.py
├── gui.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/brkln61-beep/pc_control_center.git
cd pc_control_center
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Author


Developed as a personal Python project to explore system monitoring, desktop application development and modular code organization.
