#!/usr/bin/python3
# https://pillow.readthedocs.io/en/stable/
import PIL
from PIL import Image
import json
import numpy as np
import math
import matplotlib.pyplot as plt
import cv2

def getBucket(fw,sp):
    radius = 15
    if (math.pow(fw,2) + math.pow(sp,2) <= math.pow(radius,2)):
        return 4

    bin1Size = int((255*2+1)/3)
    bin1Num = int((fw+254)/bin1Size)

    bin2Size = int((150*2+1)/3)
    bin2Num = int((sp+149)/bin2Size)

    binNum = bin1Num + 3*bin2Num # 0,...,binNum

    if binNum == 3:
        if sp > 0:
            return 6
        return 0
    elif binNum == 4:
        if sp > 0:
            return 3
        return 5
    elif binNum == 5:
        if sp > 0:
            return 8
        return 2
    else:
        return binNum

def equalize(histogram):
    lut = []
    for pixel in range(0, len(histogram), 256):
        step = sum(histogram[pixel:pixel+256]) / 255

        n = 0
        for i in range(256):
            lut.append(n / step)
            n += histogram[i+pixel]
    return lut

def loadImage(f):
    filename = f["Filename"]
    #filename = filename.replace("_",":")
    img = cv2.imread("images/"+ filename + ".jpg",0)
    equ = cv2.equalizeHist(img)
    resized = cv2.resize(equ, dsize=(50, 50), interpolation=cv2.INTER_NEAREST)
    
    img_str = ' '.join(map(str,resized.flatten()))
    #print(img_str)

    forward = int(f["Forward"])
    speed= int(f["Speed"])
    label = getBucket(forward,speed)

    img_str += " " + str(label) + "\n"
    return img_str
    
def loadData():
    try:
        with open ("images/data.json", "r") as myfile:
            data = ''.join(myfile.readlines())
            data = json.loads(data)
    except:
        data = []

    index = 0
    file = open("features.txt", "w")
    for f in data:
        file.write(loadImage(f))
        index += 1

    file.close()

loadData()
