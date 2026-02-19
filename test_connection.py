import serial
import time
import struct

# CONFIGURATION
PORT = 'COM3'         # Update this to match your Device Manager
BAUD = 115200         # CubeSpace UART often defaults to 115200
TIMEOUT = 1

# KISS PROTOCOL FLAGS
FEND = 0xC0  # Frame End (used as start and stop)
FESC = 0xDB  # Frame Escape
TFEND = 0xDC # Transposed Frame End
TFESC = 0xDD # Transposed Frame Escape

def kiss_encode(data):
    """
    Wraps data in KISS protocol flags. 
    Escapes special characters found within the data.
    """
    encoded = bytearray([FEND])
    for byte in data:
        if byte == FEND:
            encoded.extend([FESC, TFEND])
        elif byte == FESC:
            encoded.extend([FESC, TFESC])
        else:
            encoded.append(byte)
    encoded.append(FEND)
    return encoded

def send_adcs_command(ser, cmd_id):
    """
    Sends a command wrapped in a KISS frame.
    Most CubeSpace UART implementations expect an 'Address' or 'Port' 
    byte first, often 0x00 for the main controller.
    """
    # Packet: [Address/Port] [Command ID]
    payload = bytearray([0x00, cmd_id])
    packet = kiss_encode(payload)
    
    print(f"\n[INFO] Sending CMD 0x{cmd_id:02X}")
    print(f"[RAW] {packet.hex().upper()}")
    ser.write(packet)

def listen_for_response(ser):
    """
    Reads the buffer and attempts to find a KISS-wrapped response.
    """
    print("[INFO] Waiting for response...")
    time.sleep(0.5)
    raw_data = ser.read(ser.in_waiting or 10)
    
    if raw_data:
        print(f"[SUCCESS] Received: {raw_data.hex().upper()}")
        # Check if response is KISS wrapped (starts and ends with C0)
        if raw_data.startswith(b'\xc0') and raw_data.endswith(b'\xc0'):
            print(">>> Valid KISS frame detected!")
        return raw_data
    else:
        print("[FAIL] No response. Try swapping TX/RX or checking Baud.")
        return None

def run_test():
    try:
        # Initializing with 8N1 (Standard)
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
        print(f"[SYSTEM] Connected to {PORT} at {BAUD} baud.")
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    # TEST 1: Identification (0x80)
    send_adcs_command(ser, 0x80)
    listen_for_response(ser)

    time.sleep(1)

    # TEST 2: Current State (0x84)
    send_adcs_command(ser, 0x84)
    listen_for_response(ser)

    ser.close()
    print("\n[SYSTEM] Test complete.")

if __name__ == "__main__":
    run_test()
