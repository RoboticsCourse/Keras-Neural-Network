#!/usr/bin/python3
from __future__ import absolute_import, division, print_function


# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

# image libarary
from tkinter import *
from PIL import Image, ImageTk
from sys import argv
import json


print(tf.__version__)

xdim,ydim=11,11
lineardim=xdim*ydim*3

class_names = ['floor', 'other']
model = keras.Sequential([
    keras.layers.Dense(lineardim, activation=tf.nn.relu),
    keras.layers.Dense(lineardim, activation=tf.nn.relu),
    keras.layers.Dense(lineardim, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.load_weights('./checkpoints/first_cp')

class ScrolledCanvas(Frame):
    def __init__(self, filename, parent=None):
        Frame.__init__(self, parent)
        self.master.title("Spectrogram Viewer")
        self.pack(expand=YES, fill=BOTH)
        canv = Canvas(self, relief=SUNKEN)
        canv.config(width=400, height=200)
        #canv.config(scrollregion=(0,0,1000, 1000))
        #canv.configure(scrollregion=canv.bbox('all'))
        canv.config(highlightthickness=0)

        sbarV = Scrollbar(self, orient=VERTICAL)
        sbarH = Scrollbar(self, orient=HORIZONTAL)

        sbarV.config(command=canv.yview)
        sbarH.config(command=canv.xview)

        canv.config(yscrollcommand=sbarV.set)
        canv.config(xscrollcommand=sbarH.set)

        sbarV.pack(side=RIGHT, fill=Y)
        sbarH.pack(side=BOTTOM, fill=X)

        canv.pack(side=LEFT, expand=YES, fill=BOTH)
        self.im=Image.open(filename)

        # fraction=.25
        # width = int(self.im.size[0]*fraction)
        # height = int(self.im.size[1]*fraction)
        # self.im = self.im.resize((width, height), Image.ANTIALIAS)

        self.pix = self.im.load()

        width,height=self.im.size
        canv.config(scrollregion=(0,0,width,height))

        canv.bind("<Button-1>", callbackclick)
        # canv.bind("<B1-Motion>", callbackdrag)
        # canv.bind("<ButtonRelease-1>", callbackrelease)

        self.im2=ImageTk.PhotoImage(self.im)
        self.imgtag=canv.create_image(0,0,anchor="nw",image=self.im2)

def buildImage():
    m = [(255,0,0), (0,255,0), (0,0,255)]
    im = sc.im.copy()
    fraction=.10
    width = int(im.size[0]*fraction)
    height = int(im.size[1]*fraction)
    im = im.resize((width, height), Image.ANTIALIAS)

    pix = im.load()
    for x in range(1,im.size[0]-1):
        for y in range(1,im.size[1]-1):
            x0,y0=int(x/fraction), int(y/fraction)
            c = classify(x0,y0)
            pix[x,y]=m[c]
    im.show()

def classify(x,y):
    xdim, ydim = 11,11
    xd2,yd2 = int(xdim/2),int(ydim/2)
    global model, sc
    s = []
    for dx in range(-xd2,xd2+1):
        for dy in range(-yd2,yd2+1):
            # s.append("{}".format(pix[x+dx,y+dy]))
            s.extend(sc.pix[x+dx,y+dy])
            # print(",".join(s))
    data = np.array([s])
    data = data/255.0

    predictions = model.predict(data)
    return np.argmax(predictions[0])
    # print(predictions)
    # print(np.argmax(predictions[0]))

def callbackclick(event):
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    # print canvas.find_closest(x, y)
    # print "clicked at: ", event.x, event.y
    # print "clicked at: ", x, y
    print(classify(x,y))

if len(argv)==2:
    sc=ScrolledCanvas(argv[1])
    #buildImage()
    #sc.mainloop()
else:
    print("usage: testClassifier [FILE_NAME]")
