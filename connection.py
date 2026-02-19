import serial
import time

ser = serial.Serial('COM3', 115200, timeout=0.5)

while True:
    ser.write(b'A') # Keep sending 'A'
    time.sleep(0.1)
    if ser.in_waiting:
        print("I HEAR IT!")
        break
    else:
        print("Still nothing on RX...")
