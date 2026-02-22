import serial
import time

# Configuration
PORT = 'COM3'
BAUD = 115200
TIMEOUT = 0.5

def encode_csp_header(priority, source, dest, destination_port):
    """
    Encodes a standard 32-bit CSP v1 Header.
    """
    header = 0
    header |= (priority & 0x03) << 30
    header |= (source & 0x1F) << 25
    header |= (dest & 0x1F) << 20
    header |= (destination_port & 0x3F) << 14
    # Remaining bits are flags/reserved (usually 0)
    
    # Return as 4 bytes (Big Endian)
    return header.to_bytes(4, byteorder='big')

def send_cubespace_cmd(ser, cmd_byte, dest_node=1, source_node=10):
    # FEND marker
    FEND = b'\xC0'
    
    # Generate Header: Priority 2, Source 10, Dest 1, Port 0
    header = encode_csp_header(2, source_node, dest_node, 0)
    
    # The payload (The Identification command)
    payload = bytes([cmd_byte])
    
    # Construct the full KISS Frame
    # [FEND] [CSP_HEADER] [DATA] [FEND]
    packet = FEND + header + payload + FEND
    
    print(f"Sending Command {hex(cmd_byte)} to Node {dest_node}: {packet.hex().upper()}")
    ser.write(packet)

def main():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
        ser.setDTR(True)
        ser.setRTS(True)
        
        # CubeSupport often sends a few '0xC0' to clear the bus first
        ser.write(b'\xC0\xC0\xC0')
        time.sleep(0.1)
        
        # Test common Node IDs (1 is most common for ADCS, 2 for OBC)
        for target in [1, 2]:
            send_cubespace_cmd(ser, 0x80, dest_node=target)
            time.sleep(0.2)
            
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                print(f"!!! RESPONSE FROM NODE {target}: {data.hex().upper()}")
                return
                
        print("No response. Re-check if CubeSupport is fully closed on the other PC.")
        ser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
