# Battery Monitor

Battery Monitor is a Python script designed to monitor your laptop's battery level and trigger an alarm when it falls below a specified threshold. The script logs the battery status and other relevant information to a log file and stops monitoring once the battery is charged beyond a specified limit.

## Features

- Monitors battery percentage and triggers an alarm when below a threshold.
- Log battery status, remaining time, and power source to a log file.
- Stops the alarm once the power source is connected or the battery level is above the threshold.
- Configurable battery thresholds, check intervals and log file location.

## Requirements

- Python 3.x
- `psutil` library
- `pygame` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/battery-monitor.git
    ```

2. Install the required packages:

    ```sh
    pip install requirements.txt
    ```

3. Ensure the alarm audio file is in the specified path (`./audio/piano-chilled-melody.wav`).

## Usage

Run the script using Python 3:

```sh
python3 battery_monitor.py
```
