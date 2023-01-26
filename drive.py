import os

import numpy as np
from numpy import asarray
from PIL import Image
import blosc

img = Image.open("static/images/20220919_170234.jpg")
image_array = asarray(img)
compressed_bytes = blosc.pack_array(image_array)


decompressed_array = blosc.unpack_array(compressed_bytes)
im = Image.fromarray(decompressed_array)
im.show()