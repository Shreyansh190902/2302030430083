"""Cut a person out of a photo (transparent PNG) with rembg.

Usage: python3 cut.py <input image> <output.png> [model]
Needs: pip install "rembg[cpu]"  (default model: birefnet-portrait, ~1 GB download)
"""
import sys
import time

from PIL import Image
from rembg import new_session, remove

model = sys.argv[3] if len(sys.argv) > 3 else "birefnet-portrait"
t = time.time()
session = new_session(model)
remove(Image.open(sys.argv[1]).convert("RGB"), session=session).save(sys.argv[2])
print(sys.argv[1], round(time.time() - t), "s")
