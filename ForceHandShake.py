import serial
import time

ser = serial.Serial('COM3', 115200, timeout=1)

# FORCE THE PINS HIGH (This wakes up many converters)
ser.setDTR(True)
ser.setRTS(True)
time.sleep(0.1) 

print("Starting Loopback with Handshake...")

try:
    ser.write(b'PING')
    time.sleep(0.2)
    
    if ser.in_waiting > 0:
        data = ser.read(ser.in_waiting)
        print(f"SUCCESS! Received: {data}")
    else:
        print("Still no RX. Trying Inverted Handshake...")
        ser.setDTR(False)
        ser.setRTS(False)
        ser.write(b'PING')
        time.sleep(0.2)
        if ser.in_waiting > 0:
            print(f"SUCCESS (Inverted): {ser.read(ser.in_waiting)}")
        else:
            print("FAIL: Check if CubeSupport is still open in Task Manager.")

finally:
    ser.close()
