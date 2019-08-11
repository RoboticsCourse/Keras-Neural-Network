#!/usr/bin/python
# https://pillow.readthedocs.io/en/stable/
from PIL import Image
im = Image.open('images/1104.JPG') # Can be many different formats.
pix = im.load()
(dx,dy)=im.size  # Get the width and hight of the image for iterating over
for x in range(dx):
    for y in range(dy):
        print("({},{}),{}".format(x,y,pix[x,y]))  # Get the RGBA Value of the a pixel of an image

# pix[x,y] = value  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .png
