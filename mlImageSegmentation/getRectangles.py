#!/usr/bin/python3
from Tkinter import *
from PIL import Image, ImageTk
from sys import argv
import json

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
        width,height=self.im.size
        canv.config(scrollregion=(0,0,width,height))

        canv.bind("<Button-1>", callbackclick)
        canv.bind("<B1-Motion>", callbackdrag)
        canv.bind("<ButtonRelease-1>", callbackrelease)

        self.im2=ImageTk.PhotoImage(self.im)
        self.imgtag=canv.create_image(0,0,anchor="nw",image=self.im2)

x0,y0,x1,y1=0,0,0,0

def callbackclick(event):
    global x0,y0,x1,y1
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    # print canvas.find_closest(x, y)
    # print "clicked at: ", event.x, event.y
    print "clicked at: ", x, y
    x0,y0=x,y

def callbackdrag(event):
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    # print canvas.find_closest(x, y)
    # print "clicked at: ", event.x, event.y
    # print "dragged at: ", x, y

def callbackrelease(event):
    global x0,y0,x1,y1
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    # print canvas.find_closest(x, y)
    # print "clicked at: ", event.x, event.y
    # print "released at: ", x, y
    x1,y1=x,y
    canvas.create_rectangle(x0,y0,x1,y1,outline='green')
    saveData()

def saveData():
    global argv, x0,y0,x1,y1
    try:
        with open ("data.txt", "r") as myfile:
            data = ''.join(myfile.readlines())
            data = json.loads(data)
    except:
        print("Exception")
        data = []

    x0,x1 = int(min(x0,x1)),int(max(x0,x1))
    y0,y1 = int(min(y0,y1)),int(max(y0,y1))

    data.append({ 'fileName': argv[1], 'x0':x0, 'y0': y0, 'x1':x1,'y1': y1, 'label':argv[2]})
    data = json.dumps(data, indent=4)
    with open ("data.txt", "w") as myfile:
        myfile.write(data)

if len(argv)==3:
    ScrolledCanvas(argv[1]).mainloop()
else:
    print("usage: getRectangles [FILE_NAME] [LABEL]")
