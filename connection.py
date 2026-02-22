import serial
import time

# --- Configuration ---
PORT = 'COM3'        # Change to your port
BAUD_RATE = 115200   # Common for CubeSpace
TIMEOUT = 2

# --- Command ID Map from your Header ---
CMDS = {
    "IDENTIFICATION": 0x80,
    "ESTIMATED_ATTITUDE": 0x92,
    "RAW_MAGNETOMETER": 0xAA,
    "ADCS_TEMPERATURES": 0xAE,
    "TELECOMMAND_ACK": 0xF0
}

# --- Expected Sizes from your .c source calls ---
SIZES = {
    0x80: 10,  # IDENTIFICATION
    0x92: 6,   # ESTIMATED_ATTITUDE_ANGLES (Roll, Pitch, Yaw as int16)
    0xAA: 6,   # RAW_MAGNETOMETER (X, Y, Z as int16)
    0xAE: 6,   # ADCS_TEMPERATURES
    0xF0: 4    # TELECOMMAND_ACKNOWLEDGE
}

def run_telemetry_test(name, cmd_id):
    expected_len = SIZES.get(cmd_id, 6) # Default to 6 if unknown
    
    try:
        with serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
            print(f"--- Requesting {name} ({hex(cmd_id)}) ---")
            
            # 1. Send Command (u8_Command)
            ser.write(bytes([cmd_id]))
            
            # 2. Wait for processing (t_Delay)
            time.sleep(0.1) 
            
            # 3. Read Frame (pu8_Frame)
            data = ser.read(expected_len)
            
            if data:
                print(f"Success! Received {len(data)} bytes")
                print(f"Hex Dump: {data.hex(' ')}")
                
                # Optional: Simple parser for 16-bit signed integers (common in ADCS)
                if len(data) >= 6:
                    import struct
                    # '<hhh' means 3 Little-Endian Signed Shorts
                    try:
                        vals = struct.unpack('<hhh', data[:6])
                        print(f"Parsed Values: {vals}")
                    except:
                        pass
            else:
                print("Error: No data received (Timeout).")
            print("-" * 40)

    except Exception as e:
        print(f"Serial Error: {e}")

if __name__ == "__main__":
    print(f"Starting ADCS Test on {PORT}...")
    
    # Run tests
    run_telemetry_test("Identification", CMDS["IDENTIFICATION"])
    run_telemetry_test("Magnetometer", CMDS["RAW_MAGNETOMETER"])
    run_telemetry_test("Temperatures", CMDS["ADCS_TEMPERATURES"])
