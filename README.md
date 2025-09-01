# wifi-penetration

This is a Python tool for scanning WiFi networks, blocking networks, and getting WiFi passwords. 
⚠️Disclaimer: This tool is developed for **educational purposes only** and should only be used on networks you own or have explicit permission to test.

-----

## Features
- Detects wireless interfaces on your system
- Scans nearby WiFi networks and lists SSID/BSSID/Channel
- Captures handshake packets for further analysis
- Blocks clients' access to the network like a jammer
- Cracks the handshake and show password
- After completing the task, it will restore all network card settings to their original state.
- Demonstrates use of Python 'subprocess', 'CSV', and system commands

-----

## Requirements
- Linux-based system
- Python 3.x
- 'aircrack-ng' suite installed
- The network card must also have packet injection capability
- Your password list must be named 'pass.txt'(It exists by default)

-----

## Usage
\\\bash
- sudo apt update
- sudo apt install aircrack-ng
- git clone https://github.com/DevALIGhasemi/wifi-penetration.git
- cd wifi-penetration/
- sudo python3 run.py
