# Linux Status Monitor
## For home servers running Samba

Collects statistics into a message in order to be displayed.

Intended to be used with the [stm32-status-monitor-usb](https://github.com/marcosatti/stm32-status-monitor-usb) project.

Requirements:
- Running Linux
- Running on an Intel CPU (uses Intel RAPL - maybe it works on AMD/other?).
- Python (+ dependencies, see `requirements.txt`)

Systemd service unit file included for automatic start up. 
