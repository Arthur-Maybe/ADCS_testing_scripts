import serial
import time

# Use the exact settings we discussed
ser = serial.Serial('COM3', 115200, timeout=0.1)
ser.setDTR(True) 
ser.setRTS(True)

print("Starting Low-Latency Loopback...")

try:
    for i in range(50):
        ser.write(b'X')
        time.sleep(0.01)
        if ser.in_waiting:
            char = ser.read(ser.in_waiting)
            print(f"Iter {i}: SUCCESS! Received {char}")
            break
    else:
        print("Still nothing. The hardware is ignoring the loopback.")
finally:
    ser.close()
