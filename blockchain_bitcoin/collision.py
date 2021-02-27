import zlib


bit = zlib.crc32(b"Thomas")
bit2 = zlib.crc32(b"Thomas2077614111")


print(bit, hex(bit))

print(bit2, hex(bit2))

if bit == bit2:
    print("true")
else:
    print("false")
