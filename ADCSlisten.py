import serial

PORT = 'COM3'
BAUD = 115200 # Try 9600 if this fails

def sniff_traffic():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=0.1)
        print(f"--- Sniffing on {PORT} at {BAUD} baud ---")
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                print(f"HEX: {data.hex().upper()}")
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        ser.close()

if __name__ == "__main__":
    sniff_traffic()
