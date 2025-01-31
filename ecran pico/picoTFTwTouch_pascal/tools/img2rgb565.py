# -*- coding: utf-8 -*-
"""Utility to convert images to raw RGB565 format.

Usage:
    python img2rgb565.py <your_image>
    <your_image> is the full path to the image file you want to convert.
"""

from PIL import Image
from struct import pack
from os import path
import sys


def error(msg):
    """Display error and exit."""
    print (msg)
    sys.exit(-1)


def write_bin(f, pixel_list, invert=False):
    """Save image in RGB565 format."""
    for pix in pixel_list:
        r = (pix[0] >> 3) & 0x1F
        g = (pix[1] >> 2) & 0x3F
        b = (pix[2] >> 3) & 0x1F
        if invert:
            r=(~r) & 0x1F
            g=(~g) & 0x3F
            b=(~b) & 0x1F
        f.write(pack('>H', (r << 11) + (g << 5) + b))


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        error('Please specify input file: ./img2rgb565.py test.png')
    in_path = args[1]
    invert = False # PG : ajouté pour inverser les bit de l'image (car sur mon écran TFT c'est comme ça)
    if not path.exists(in_path):
        error('File Not Found: ' + in_path)

    filename, ext = path.splitext(in_path)
    out_path = filename + '.raw'
    img = Image.open(in_path).convert('RGB')
    pixels = list(img.getdata())
    with open(out_path, 'wb') as f:
        write_bin(f, pixels, invert=invert)
    print('Saved: ' + out_path)
