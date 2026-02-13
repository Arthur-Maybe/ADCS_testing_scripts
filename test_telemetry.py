import serial
import time
import struct

# CONFIGURATION
PORT = '/dev/ttyUSB0'
BAUD = 9600

# ==========================================
# UPDATED COMMAND IDS FROM YOUR HEADER FILE
# ==========================================
# From #define ESTIMATED_ATTITUDE_ANGLES (0x92)
CMD_GET_ATTITUDE = 0x92 

# From #define ESTIMATED_ANGULAR_RATES (0x93)
# Note: You could also use RATE_SENSOR_RATES (0x9B) for raw gyro data
CMD_GET_RATES = 0x93    

def parse_telemetry(data):
    # '<' = Little Endian
    # 'h' = Signed Short (2 bytes). We use signed because angles/rates can be negative.
    # 'H' = Unsigned Short. Used for Voltages, Currents, Temperatures (Kelvin).
    
    if len(data) >= 6:
        # Unpack 3 signed integers (2 bytes each = 6 bytes total)
        val1, val2, val3 = struct.unpack('<hhh', data[0:6])
        
        # Scaling Factor: CubeSpace usually scales angles by 0.01 or 0.001
        # Example: Raw 4500 -> 45.00 degrees. Adjust '0.01' if your manual says otherwise.
        scale = 0.01 
        return val1 * scale, val2 * scale, val3 * scale
        
    return 0, 0, 0

def monitor_adcs():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=0.5)
        print(f"[INFO] Opened {PORT}. Starting Telemetry Monitor...")
        print("[INFO] Press Ctrl+C to stop.")
    except Exception as e:
        print(f"[ERROR] Could not open port: {e}")
        return

    try:
        while True:
            # --- 1. Request Attitude (Roll/Pitch/Yaw) ---
            ser.write(struct.pack('B', CMD_GET_ATTITUDE))
            time.sleep(0.1) # Wait for processing
            att_raw = ser.read(6)
            
            if len(att_raw) == 6:
                roll, pitch, yaw = parse_telemetry(att_raw)
            else:
                roll, pitch, yaw = (0, 0, 0) # Timeout/Error

            # --- 2. Request Rates (X/Y/Z) ---
            ser.write(struct.pack('B', CMD_GET_RATES))
            time.sleep(0.1) # Wait for processing
            rate_raw = ser.read(6)
            
            if len(rate_raw) == 6:
                wx, wy, wz = parse_telemetry(rate_raw)
            else:
                wx, wy, wz = (0, 0, 0) # Timeout/Error

            # Print output (Overwrites the line for a clean dashboard look)
            # \033[K clears the rest of the line
            print(f"\rATT(deg): [R:{roll:6.2f} P:{pitch:6.2f} Y:{yaw:6.2f}] | RATE(deg/s): [X:{wx:6.2f} Y:{wy:6.2f} Z:{wz:6.2f}]\033[K", end="")
            
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n[INFO] Stopping monitor.")
        ser.close()

if __name__ == "__main__":
    monitor_adcs()
