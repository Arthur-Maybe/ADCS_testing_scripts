ADCS Integration Testing Scripts
This collection of Python scripts is designed to verify the connection, sensors, and logic flow of the CubeSpace ADCS unit integration without needing to flash the Flight Software (FSW) repeatedly.

#Prerequisites
1. PySerial library installed:
  - pip install pyserial
2. Hardware Connection
  - Connect the ADCS Engineering Model to your PC using a USB-to-UART (TTL) adapter.
  - TX on Adapter goes to RX on ADCS.
  - RX on Adapter goes to TX on ADCS.
  - GND must be common.

#Configuration
Before running any script, open it and update the PORT variable to match your system:
- Windows: COM3, COM4, etc. (Check Device Manager)
- Linux/Mac: /dev/ttyUSB0, /dev/tty.usbserial, etc.
Default Baud Rate: 9600
