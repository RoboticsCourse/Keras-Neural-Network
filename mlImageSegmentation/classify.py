#!/usr/bin/python3
# https://www.tensorflow.org/tutorials/keras/basic_classification
# https://machinelearningmastery.com/index-slice-reshape-numpy-arrays-machine-learning-python/
# https://www.datacamp.com/community/tutorials/tensorflow-tutorial

from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

# fashion_mnist = keras.datasets.fashion_mnist

# (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

xdim,ydim=11,11
lineardim=xdim*ydim*3

class_names = ['floor', 'other']
def convertClass(x):
    if x== b'floor': return 0
    if x== b'other':return 1
    return 2

converter = { lineardim : convertClass }

raw = np.loadtxt("features.txt", delimiter=',', converters = converter)

print(raw[3])

X = data = raw[:,:-1]/255.0
y = labels = raw[:,-1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

model = keras.Sequential([
    keras.layers.Dense(lineardim, activation=tf.nn.relu),
    keras.layers.Dense(lineardim, activation=tf.nn.relu),
    keras.layers.Dense(lineardim, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train, epochs=5)
test_loss, test_acc = model.evaluate(X_test, y_test)

print((test_loss, test_acc))

# https://www.tensorflow.org/tutorials/keras/save_and_restore_models
model.save_weights('./checkpoints/my_checkpoint')
