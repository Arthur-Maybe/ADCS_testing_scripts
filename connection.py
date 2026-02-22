import serial
import time

# --- Configuration based on your C code ---
PORT = 'COM3'         # Update to your actual COM port
BAUD_RATE = 115200    # Common for CubeSpace, check your config headers
TIMEOUT = 2           # Seconds

# Command IDs (These should be defined in your CubeSpaceADCS.h)
# From ioRead logic: Telemetry commands must be > 127
IDENTIFICATION_CMD = 0x80  # Example ID for IDENTIFICATION
IDENTIFICATION_SIZE = 10   # Example size; check CUBESPACEADCS_IDENTIFICATION_SIZE

def test_adcs_telemetry(cmd_id, expected_len):
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"Connected to ADCS on {PORT}")

        # 1. Send the Command (ioRead logic: ru8_Data[0] = u8_Command)
        print(f"Sending Telemetry Request: {hex(cmd_id)}")
        ser.write(bytes([cmd_id]))
        
        # 2. Delay (t_Delay in your C code)
        time.sleep(0.1) 

        # 3. Read the Frame (pu8_Frame in your C code)
        data = ser.read(expected_len)

        if data:
            print(f"Received {len(data)} bytes:")
            print(f"HEX: {data.hex(' ')}")
            try:
                print(f"STR: {data.decode('ascii', errors='ignore')}")
            except:
                pass
        else:
            print("No data received. Check baud rate or Command ID.")

        ser.close()
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    # Test Identification
    test_adcs_telemetry(IDENTIFICATION_CMD, IDENTIFICATION_SIZE)
