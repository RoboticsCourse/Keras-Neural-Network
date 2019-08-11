#!/usr/bin/python3
# https://pillow.readthedocs.io/en/stable/
from PIL import Image
import json


def loadImage(fileName, label, x0,y0,x1,y1):
    im = Image.open(fileName) # Can be many different formats.
    pix = im.load()
    (dx,dy)=im.size  # Get the width and hight of the image for iterating over
    '''
    for x in range(x0,x1):
        for y in range(y0,y1):
            print("({},{}),{}".format(x,y,pix[x,y]))  # Get the RGBA Value of the a pixel of an image
    '''
    xdim,ydim = 11,11
    xd2,yd2 = int(xdim/2),int(ydim/2)

    for x in range(x0+xd2,x1-xd2,5):
        for y in range(y0+yd2,y1-yd2,5):
            s = []
            for dx in range(-xd2,xd2+1):
                for dy in range(-yd2,yd2+1):
                    # s.append("{}".format(pix[x+dx,y+dy]))
                    s.extend(pix[x+dx,y+dy])
            s.append(label)
            s=map(str, s)
            print(",".join(s))
    
    # pix[x,y] = value  # Set the RGBA Value of the image (tuple)
    # im.save('alive_parrot.png')  # Save the modified pixels as .png

def loadData():
    try:
        with open ("data.txt", "r") as myfile:
            data = ''.join(myfile.readlines())
            data = json.loads(data)
    except:
        data = []

    for f in data:
            fileName = f["fileName"]
            x0 = f["x0"]
            y0 = f["y0"]
            x1 = f["x1"]
            y1 = f["y1"]
            label = f["label"]
            loadImage(fileName, label, x0,y0,x1,y1)

loadData()
