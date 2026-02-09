import serial
import time
import struct

PORT = '/dev/ttyUSB0'
BAUD = 9600

# Command IDs
CMD_GET_ATTITUDE = 0x84 
CMD_GET_RATES = 0x85

def parse_telemetry(data):
    # Assuming standard CubeSpace 16-bit signed integer format scaled by 0.01 or similar
    # You must adjust 'hhh' (3 signed shorts) hhh for INT and HHH for UINT. There are multiple. I am not sure which one
    if len(data) >= 6:
        x, y, z = struct.unpack('<hhh', data[0:6])
        return x, y, z
    return 0, 0, 0

def monitor_adcs():
    ser = serial.Serial(PORT, BAUD, timeout=0.5)
    print("[INFO] Starting Telemetry Monitor (Press Ctrl+C to stop)...")

    try:
        while True:
            # 1. Request Attitude
            ser.write(struct.pack('B', CMD_GET_ATTITUDE))
            time.sleep(0.05)
            att_raw = ser.read(6)
            roll, pitch, yaw = parse_telemetry(att_raw)

            # 2. Request Rates
            ser.write(struct.pack('B', CMD_GET_RATES))
            time.sleep(0.05)
            rate_raw = ser.read(6)
            wx, wy, wz = parse_telemetry(rate_raw)

            # Print formatted output (overwrite line for clean look)
            print(f"\rATT: [R:{roll:5} P:{pitch:5} Y:{yaw:5}] | RATES: [X:{wx:5} Y:{wy:5} Z:{wz:5}]", end="")
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n[INFO] Stopping monitor.")
        ser.close()

if __name__ == "__main__":
    monitor_adcs()
