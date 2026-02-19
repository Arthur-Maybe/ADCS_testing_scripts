import serial
import time

PORT = 'COM3'
BAUD_RATES = [9600, 38400, 115200, 921600] # Focus on the most likely ones

def run_power_scan():
    # 0x55 is the standard sync/calibration byte
    sync_pulse = b'\x55\x55\x55\x55'
    
    # Common CSP/KISS packet for Identification (Node 1, Port 0)
    # [FEND, CSP_HEADER_4BYTES, DATA_0x80, FEND]
    # This is a 'best guess' at a default CSP header
    csp_packet = bytearray([0xC0, 0x01, 0x00, 0x00, 0x00, 0x80, 0xC0])
    raw_packet = bytearray([0xC0, 0x00, 0x80, 0xC0])

    print(f"--- Starting Advanced Sync/CSP Scan ---")

    for baud in BAUD_RATES:
        print(f"\n[TESTING] {baud} baud...")
        try:
            ser = serial.Serial(PORT, baud, timeout=0.5)
            ser.setDTR(True)
            ser.setRTS(True)
            
            # 1. Send Sync Pulse
            ser.write(sync_pulse)
            time.sleep(0.05)
            
            # 2. Try Raw KISS
            ser.write(raw_packet)
            time.sleep(0.1)
            
            # 3. Try CSP-style KISS
            ser.write(csp_packet)
            time.sleep(0.2)

            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting)
                print(f"!!! SUCCESS !!! -> {response.hex().upper()}")
                return
            
            ser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_power_scan()
