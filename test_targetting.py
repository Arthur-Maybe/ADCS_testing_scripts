import serial
import time
import struct

PORT = '/dev/ttyUSB0'
BAUD = 9600

# Command ID for 'SetTrackingControllerTargetReference' (Check ICD/Header!)
CMD_SET_TARGET = 0x37

def send_target(lat_deg, lon_deg, alt_km):
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    print(f"[INFO] Targeting: Lat {lat_deg} | Lon {lon_deg} | Alt {alt_km} km")

    # --- SCALING ---
    # CubeSpace typically expects Lat/Lon as integers scaled by 10,000,000 (1e7)
    # Altitude is often in meters or scaled km.
    lat_int = int(lat_deg * 10_000_000)
    lon_int = int(lon_deg * 10_000_000)
    alt_int = int(alt_km * 1000)

    # --- PACKING ---
    # '<' = Little Endian
    # 'i' = Signed 32-bit Integer (4 bytes) - negative Latitude!
    # 'I' = Unsigned 32-bit Integer (4 bytes) - positive
    payload = struct.pack('<iiI', lon_int, lat_int, alt_int)

    # Construct Packet: [ID] [Payload]
    packet = struct.pack('B', CMD_SET_TARGET) + payload
    
    ser.write(packet)
    time.sleep(0.2)
    
    # Ideally, read an ACK here. For now, we assume it sent.
    print(f"[SENT] {packet.hex().upper()}")
    print("Check ADCS telemetry to verify it is tracking this coordinate.")

    ser.close()

if __name__ == "__main__":
    # Test pointing at Athens, Greece (Approx 37.98, 23.72)
    send_target(37.9838, 23.7275, 500)
