#!/usr/bin/python3
# https://pillow.readthedocs.io/en/stable/
from PIL import Image
import json

def mapForward(val,bins):
    # val is in range -255,255
    # bins is the number of bins, actually the number of positive bins
    binSize = int(255/bins)
    binNum = int(val/binSize)
    # return binNum*binSize
    return bins+binNum # -binNum,...,binNum to 0,...,2*binNum

def loadImage(f):
    fileName = f["FileName"]
    forward = int(f["Forward"])
    label = mapForward(forward,5)

    im = Image.open("images/"+fileName) 
    newSize = (40,40)
    im = im.resize(newSize)
    pix = im.load()
    (dx,dy)=im.size  

    s = []
    for x in range(dx):
        for y in range(dy):
            s.extend(pix[x,y])
    s.append(label)
    s=map(str, s)
    print(",".join(s))
    # print(str(forward)+" "+str(mapForward(forward,5)))
    
def loadData():
    try:
        with open ("data.json", "r") as myfile:
            data = ''.join(myfile.readlines())
            data = json.loads(data)
    except:
        data = []

    for f in data:
        loadImage(f)

loadData()
