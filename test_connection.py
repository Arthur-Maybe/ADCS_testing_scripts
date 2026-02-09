import serial
import time
import struct

# CONFIGURATION
PORT = '/dev/ttyUSB0'  # Adjust this to your COM port
BAUD = 115200

def test_connection():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        print(f"[INFO] Opened {PORT} successfully.")
    except Exception as e:
        print(f"[ERROR] Could not open port: {e}")
        return

    # CubeSpace command to get Identification (ID: 128 / 0x80 usually, check your ICD)
    # This is a generic example. You must check 'CubeSpaceADCS_MAS_package.h' for the actual ID.
    CMD_ID_IDENTIFICATION = 0x80 
    
    # Send Command
    print("[INFO] Sending Ping (Get Identification)...")
    ser.write(struct.pack('B', CMD_ID_IDENTIFICATION))
    
    # Wait for response (CubeSpace usually returns a header + data)
    time.sleep(0.1)
    response = ser.read(10) # Read up to 10 bytes

    if len(response) > 0:
        print(f"[SUCCESS] Received {len(response)} bytes: {response.hex()}")
        print("Hardware link is ACTIVE.")
    else:
        print("[FAIL] No response received. Check wiring (RX/TX swapped?) or Baud rate.")
    
    ser.close()

if __name__ == "__main__":
    test_connection()
