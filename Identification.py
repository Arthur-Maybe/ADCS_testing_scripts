import serial
import time

# CONFIGURATION
PORT = 'COM3' 
BAUD = 115200  # Standard for CubeSpace; try 921600 if 115200 fails (HIL default)
TIMEOUT = 1

def send_kiss_cmd(ser, cmd_byte):
    # KISS Frame: [FEND, Command/Port, Data, FEND]
    # 0xC0 is the FEND (Frame End) marker
    # 0x00 is usually the 'Data' port for ADCS commands
    packet = bytearray([0xC0, 0x00, cmd_byte, 0xC0])
    
    print(f"Sending KISS Packet: {packet.hex().upper()}")
    ser.write(packet)

def run_test():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
        print(f"Connected to {PORT} at {BAUD} baud.")
        
        # We try CMD 0x80 (Identification)
        send_kiss_cmd(ser, 0x80)
        
        time.sleep(0.5)
        
        if ser.in_waiting > 0:
            resp = ser.read(ser.in_waiting)
            print(f"RESPONSE RECEIVED: {resp.hex().upper()}")
        else:
            print("No response. The ADCS TX line is still silent.")
            
        ser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_test()
