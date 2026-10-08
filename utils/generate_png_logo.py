"""
Pure Python script to generate a PNG image file for assets/logo.png without third-party dependencies.
"""

import os
import zlib
import struct

def create_png_logo():
    width = 120
    height = 120
    
    # We will draw a stylish rounded square with indigo gradient and an 'M' letter
    raw_data = bytearray()
    
    for y in range(height):
        raw_data.append(0)  # filter type 0 (None)
        for x in range(width):
            # Check if within rounded rectangle (radius 24)
            # Center of corner circles: (24, 24), (width-25, 24), etc.
            dx = max(0, max(24 - x, x - (width - 25)))
            dy = max(0, max(24 - y, y - (height - 25)))
            dist_sq = dx * dx + dy * dy
            
            if dist_sq > 24 * 24:
                # Transparent outside rounded rect
                raw_data.extend([0, 0, 0, 0])
                continue
            
            # Indigo-to-violet gradient
            t = (x + y) / (width + height)
            r = int(79 + t * (124 - 79))
            g = int(70 + t * (58 - 70))
            b = int(229 + t * (237 - 229))
            
            # Simple stylized 'M' glyph in center
            # X ranges: 35..85, Y ranges: 35..85
            is_m = False
            if 36 <= y <= 84:
                # Left bar
                if 36 <= x <= 45:
                    is_m = True
                # Right bar
                elif 75 <= x <= 84:
                    is_m = True
                # Diagonal left
                elif 45 <= x <= 60 and abs((y - 36) - (x - 45) * 2) <= 5:
                    is_m = True
                # Diagonal right
                elif 60 <= x <= 75 and abs((y - 36) - (75 - x) * 2) <= 5:
                    is_m = True
            
            if is_m:
                raw_data.extend([255, 255, 255, 255])
            else:
                raw_data.extend([r, g, b, 255])

    def chunk(tag, data):
        return struct.pack("!I", len(data)) + tag + data + struct.pack("!I", zlib.crc32(tag + data) & 0xffffffff)

    png_header = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack("!IIBBBBB", width, height, 8, 6, 0, 0, 0)
    ihdr = chunk(b"IHDR", ihdr_data)
    idat = chunk(b"IDAT", zlib.compress(bytes(raw_data)))
    iend = chunk(b"IEND", b"")

    png_bytes = png_header + ihdr + idat + iend

    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    out_path = os.path.join(assets_dir, "logo.png")
    with open(out_path, "wb") as f:
        f.write(png_bytes)
    print(f"Created {out_path} ({len(png_bytes)} bytes)")

if __name__ == "__main__":
    create_png_logo()
