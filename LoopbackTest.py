import serial
import time

PORT = 'COM3'
BAUD = 115200 

def run_diagnostic():
    try:
        # Initializing with the settings you provided
        ser = serial.Serial(
            port=PORT,
            baudrate=BAUD,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            rtscts=False,  # Flow control: most ADCS don't use this
            dsrdtr=False,
            timeout=1
        )
        
        print(f"--- Diagnostic Started on {PORT} ---")
        
        # 1. Hardware Pin Check: Toggle DTR/RTS
        # Sometimes this "wakes up" the converter
        ser.dtr = True
        ser.rts = True
        time.sleep(0.1)
        
        # 2. Loopback Test
        test_val = b'\x80' # Sending the ADCS Identification ID
        print(f"[STEP 1] Sending Test Byte: {test_val.hex().upper()}")
        ser.write(test_val)
        
        time.sleep(0.1)
        
        # 3. Read Results
        if ser.in_waiting > 0:
            echo = ser.read(ser.in_waiting)
            print(f"[STEP 2] Received Echo: {echo.hex().upper()}")
            if echo == test_val:
                print("\n>>> SUCCESS: Loopback confirmed. Python and Converter are working.")
            else:
                print("\n>>> WARNING: Data corruption. Received different bytes.")
        else:
            print("\n>>> FAIL: No data received. Is the jumper wire connecting TX to RX?")

    except serial.SerialException as e:
        print(f"\n[PORT ERROR] {e}")
        print("Check if another program (Cube Support) is open.")
    except Exception as e:
        print(f"\n[GENERAL ERROR] {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("--- Port Closed ---")

if __name__ == "__main__":
    run_diagnostic()
