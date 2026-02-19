import serial
import time

ser = serial.Serial('COM3', 115200, timeout=0.5)

# CSP v1 Header: Priority 2, Source 10, Dest 1, Port 0
# Packet = [FEND] [CSP HEADER (4 bytes)] [CMD 0x80] [FEND]
csp_id_packet = bytearray([0xC0, 0x02, 0x8A, 0x00, 0x00, 0x80, 0xC0])

print("Sending CSP-formatted ID command...")
try:
    for _ in range(20):
        ser.write(csp_id_packet)
        time.sleep(0.1)
        if ser.in_waiting > 0:
            print(f"RESPONSE: {ser.read(ser.in_waiting).hex().upper()}")
            break
    else:
        print("Still silent. ADCS may require a specific CSP Destination Node ID.")
finally:
    ser.close()
