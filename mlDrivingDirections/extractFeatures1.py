#!/usr/bin/python3
# https://pillow.readthedocs.io/en/stable/
import PIL
from PIL import Image
import json
import numpy as np
import math
import cv2
import pickle
import time
from datetime import datetime
from matplotlib import pyplot as plt
from shutil import copyfile


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
    
try:
    with open ("images/data.json", "r") as myfile:
        data = ''.join(myfile.readlines())
        data = json.loads(data)
except:
    data = []


arr = []
group = []
#groupF = []
prev = 0
lbls = []
for f in data:
    # Getting the image, equalizing it and then resizing.
    filename = f["Filename"]
    #filename = filename.replace("_",":")
    im = Image.open("images/"+ filename + ".jpg")
    im = im.convert("L")
    im = im.resize((50,50),PIL.Image.NEAREST)
    im = np.asarray(im)
    image = cv2.equalizeHist(im)

    #Getting the flipped version of the image
    imageFlipped = np.flip(image,1).reshape(2500,-1)

    #Getting lbls
    forward = int(f["Forward"])
    speed= int(f["Speed"])
    label = getBucket(forward,speed)

    #Allows us to flip the bin 
    flipLabel = [2,1,0,3,4,5,8,7,6]

    # Getting milliseconds of when image is take
    #imgDate = int(datetime.strptime(f["Image Time"], '%d:%m:%y:%H:%M:%S:%f').strftime("%S")) 
    imgDate = time.mktime(datetime.strptime(f["Image Time"], '%d:%m:%y:%H:%M:%S:%f').timetuple())
    #print(f["Image Time"])
    #print(imgDate)
    #print((imgDate,prev))
    if prev == 0 or abs(imgDate - prev) <= 2:
        #Image corresponds to current group and so appending it their
        group.append([image.flatten().tolist(),label])
        #print(imgDate)
        #groupF.append([imageFlipped.flatten().tolist(),flipLabel[label]])
    else:
        #Image does not correspond to current group and so making a new group
        print(prev)
        print(imgDate)
        print("------------------------------")
        arr.append(group)
        #arr.append(groupF)
        group = [[image.flatten().tolist(),label]]
        #group = []
        #groupF = []
    prev = imgDate
    
arr.append(group)
#arr.append(groupF)
print(len(arr))
print(lbls)

with open('features.txt', 'wb') as fp:
    pickle.dump(arr, fp)
