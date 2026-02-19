import serial
import time

PORT = 'COM3'
BAUD = 115200 
TIMEOUT = 0.5

def run_burst_test():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
        # Force the handshake pins high like in the loopback script
        ser.setDTR(True)
        ser.setRTS(True)
        
        print(f"--- Burst ID Test on {PORT} ---")
        print("Sending 100 identification pulses (Watch for flicker)...")

        # KISS Packet for ID: [FEND, Port, CMD, FEND]
        packet = bytearray([0xC0, 0x00, 0x80, 0xC0])

        for i in range(100):
            ser.write(packet)
            time.sleep(0.01) # 10ms delay between tries
            
            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting)
                print(f"\n[!!!] SUCCESS! Received: {response.hex().upper()}")
                ser.close()
                return

        print("\n[FAIL] Sent 100 packets. TX should have flickered, but ADCS stayed silent.")
        ser.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_burst_test()
