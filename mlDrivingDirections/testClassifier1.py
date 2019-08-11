import tensorflow as tf
from tensorflow import keras
import sys
import glob
import numpy as np
import cv2
import PIL
from PIL import Image

def mapImgLabel(Xarr, array):
    array = np.asarray(array).T
    array = array.tolist()
    for i in range (len(array[0]) - 9):
        Xarr.append(array[0][i:i+10])

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = keras.models.model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")
 
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

path = str(sys.argv[1])
images = [file for file in glob.glob(path + "*.jpg")]
images.sort()

array = []
group = []
name = []
for img_path in images:
        im = Image.open(img_path)
        name.append(img_path[11:])
        im = im.convert("L")
        im = im.resize((50,50),PIL.Image.NEAREST)
        im = np.asarray(im)
        im = im - 2
        group.append([im.flatten().tolist(),0])
array.append(group)

Xarr = []
for arr in array:
    mapImgLabel(Xarr,arr)

#Xarr = np.stack(Xarr, axis=0)

#newX = np.zeros((Xarr.shape[0],50,50,10),dtype=int)

"""for group_index in range(Xarr.shape[0]):
        for image_index in range(Xarr.shape[1]):
                for row in range(50):
                        for col in range(50):
                                newX[group_index][row][col][image_index] = Xarr[group_index][image_index][50*row+col]"""



newX = np.stack(Xarr, axis=0)
newX = np.transpose(newX, (0, 2, 1)).reshape(newX.shape[0],50,50,10)
bucket = model.predict_classes(newX) 


space = [4,3,2,1]
string = ','.join(name[:10]) + "\n"
for x in newX[0]:
        for y in x:
                for z in y:
                        z = str(z)
                        string += z + ","
                string += "\n"

with open("output.txt", "a") as myfile:
        myfile.write(string)


bucket = model.predict_classes(newX) 
for buc in bucket:
        print(buc)

print("DONE!!!!")
