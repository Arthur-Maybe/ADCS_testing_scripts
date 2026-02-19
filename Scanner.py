import serial
import time

PORT = 'COM3'
# The most common speeds for CubeSpace and aerospace hardware
BAUD_RATES = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

def run_scanner():
    # The KISS-wrapped Identification command (0x80)
    packet = bytearray([0xC0, 0x00, 0x80, 0xC0])

    print(f"--- Starting ADCS Baud Rate Scanner on {PORT} ---")
    
    for baud in BAUD_RATES:
        print(f"\n[TESTING] {baud} baud...", end=" ", flush=True)
        try:
            # Open port with a short timeout to keep the scan moving
            ser = serial.Serial(PORT, baud, timeout=0.3)
            ser.setDTR(True)
            ser.setRTS(True)
            
            # Send a burst of 10 packets to give the ADCS a chance to "hear" it
            for _ in range(10):
                ser.write(packet)
                time.sleep(0.02)
                
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting)
                    print(f"\n\n>>> SUCCESS AT {baud} BAUD! <<<")
                    print(f"RESPONSE (HEX): {response.hex().upper()}")
                    ser.close()
                    return
            
            print("No response.")
            ser.close()
            
        except Exception as e:
            print(f"Error: {e}")

    print("\n--- Scan Complete. No baud rate matched. ---")
    print("Possibilities: Missing shared Ground, wrong Port, or ADCS is in I2C mode.")

if __name__ == "__main__":
    run_scanner()
