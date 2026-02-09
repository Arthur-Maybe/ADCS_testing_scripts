import serial
import time
import struct

# CONFIGURATION
PORT = '/dev/ttyUSB0'
BAUD = 9600     

def test_connection():
    try:
        # Open the serial port
        ser = serial.Serial(PORT, BAUD, timeout=1)
        print(f"[INFO] Opened {PORT} at {BAUD} baud successfully.")
    except Exception as e:
        print(f"[ERROR] Could not open port: {e}")
        return

    # CubeSpace command to get Identification
    CMD_ID_IDENTIFICATION = 0x80 
    
    # Send Command
    print("[INFO] Sending Ping (Get Identification)...")
    ser.write(struct.pack('B', CMD_ID_IDENTIFICATION))
    
    # Wait for response
    time.sleep(0.2) 
    
    # Read response
    response = ser.read(10) # Read up to 10 bytes

    if len(response) > 0:
        print(f"[SUCCESS] Received {len(response)} bytes: {response.hex()}")
        print("Hardware link is ACTIVE.")
    else:
        print("[FAIL] No response received.")
        print("   - Check wiring (RX connected to TX?)")
        print("   - Verify ADCS is powered on")
    
    ser.close()

if __name__ == "__main__":
    test_connection()
