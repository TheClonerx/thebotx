import base64
import os
import random

if not args:
    room.message("missing argument")
else:
    mask_len = random.randint(1, min(10, len(args)))
    mask = os.urandom(mask_len)
    text = args.encode()
    encoded = bytes(x ^ mask[i % mask_len] for i, x in enumerate(text))
    encoded = bytes([mask_len]) + mask + text[::-1]
    encoded = base64.b85encode(encoded)
    room.message(encoded.decode())
