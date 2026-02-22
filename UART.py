import serial
import time

ser = serial.Serial('COM3', 115200, timeout=0.2)
ser.setDTR(True)
ser.setRTS(True)

def test_node_ids():
    # 1. Send Wake-up pulse
    print("Sending Wake-up sync...")
    ser.write(b'\x55' * 20)
    time.sleep(0.1)

    # 2. Try Node IDs 1 through 5 (Most common for ADCS)
    for node in range(1, 6):
        print(f"Testing Destination Node: {node}")
        # CSP Packet: [FEND] [Priority/Source/Dest/Port] [CMD 0x80] [FEND]
        # We vary the Destination Node byte here
        header_byte = (node & 0x1F) << 3 # Simplified CSP-style destination shift
        packet = bytearray([0xC0, 0x02, header_byte, 0x00, 0x00, 0x80, 0xC0])
        
        ser.write(packet)
        time.sleep(0.2)
        
        if ser.in_waiting > 0:
            print(f"!!! SUCCESS ON NODE {node}: {ser.read(ser.in_waiting).hex().upper()}")
            return
    
    print("No nodes responded.")

if __name__ == "__main__":
    test_node_ids()
    ser.close()
