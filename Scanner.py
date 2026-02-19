import serial
import time

PORT = 'COM3'
# Common CubeSat Baud Rates
RATES = [9600, 19200, 38400, 57600, 115200]
CMD_IDENTIFY = b'\x80' # Standard CubeSpace ID command

def scan_adcs():
    for baud in RATES:
        print(f"\n--- Testing {baud} baud ---")
        try:
            ser = serial.Serial(PORT, baud, timeout=0.5)
            # Clear buffers
            ser.reset_input_buffer()
            
            # Send raw command
            ser.write(CMD_IDENTIFY)
            time.sleep(0.1)
            
            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting)
                print(f"[!] SUCCESS at {baud}: {response.hex().upper()}")
                ser.close()
                return
            else:
                print(f"[-] No response at {baud}")
            ser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    scan_adcs()
