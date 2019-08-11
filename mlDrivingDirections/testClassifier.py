import tensorflow as tf
from tensorflow import keras
import sys
import glob
import numpy as np
import cv2
import PIL
from PIL import Image

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

lines = "-" * 50

for img_path in images:
        im = Image.open(img_path)
        im = im.convert("L")
        im = im.resize((50,50),PIL.Image.NEAREST)
        pix = im.load()
        (dx,dy)=im.size 

        string = lines + "\n"
        pixels = ""
        space = [4,3,2,1]
        for x in range(dx):
                for y in range(dy):
                        pixel = str(pix[x,y])
                        string += pixel + "," + (" " * space[len(pixel)])
                        pixels += pixel + ","
                string += "\n"
        string += lines + "\n"

        image = np.fromstring(pixels, dtype=int, sep=',')
        image = image.reshape(1,50,50,1)
        image = image/255.0
        print(image)

        bucket = model.predict_classes(image) 
        with open("output.txt", "a") as myfile:
                myfile.write(str(img_path.split("/")[-1].replace(":","_")) + " " + str(bucket[0]) + "\n")
        with open("pixel.txt", "a") as myfile:
                myfile.write(string)

print("DONE!!!!")
