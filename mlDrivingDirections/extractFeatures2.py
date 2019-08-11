#!/usr/bin/python3
# https://pillow.readthedocs.io/en/stable/
from PIL import Image
import json

def mapFS(fw,sp):
    if int(fw) == 0 or int(sp) == 0:
        return 0
    elif int(fw) > 0 and int(sp) > 0:
        return 1
    elif int(fw) < 0 and int(sp) > 0:
        return 2
    elif int(fw) > 0 and int(sp) < 0:
        return 3
    else:
        return 4

def loadImage(f):
    fileName = f["FileName"]

    im = Image.open("images/"+fileName) 
    im = im.convert("L") # comment out for rgb
    newSize = (50,50) # CHANGE DIMENSION OF IMAGE HERE
    im = im.resize(newSize)
    #im.show()
    pix = im.load()
    (dx,dy)=im.size  

    s = []
    for x in range(dx):
        for y in range(dy):
            # s.extend(pix[x,y]) # for rgb
            s.append(pix[x,y]) # for greyscale

    forward = int(f["Forward"])
    speed= int(f["Speed"])
    label = mapFS(int(forward),int(speed))

    s.append(label)
    s=map(str, s)
    #print(s)
    print(",".join(s))

    # l = len(s)
    # print(str(l)+" "+str(forward)+" "+str(label))
    
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
