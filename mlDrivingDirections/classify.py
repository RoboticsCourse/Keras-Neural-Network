#!/usr/bin/python3
# https://www.tensorflow.org/tutorials/keras/basic_classification
# https://machinelearningmastery.com/index-slice-reshape-numpy-arrays-machine-learning-python/
# https://www.datacamp.com/community/tutorials/tensorflow-tutorial

from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tensorflow.contrib import lite
from keras import backend as K
from keras import layers
from keras.models import Sequential
from keras.models import Model

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

raw = np.loadtxt("features.txt", delimiter=',')
X = data = raw[:,:-1]/255.0
lineardim = X.shape[1]
#y = labels = raw[:,-1]
y = labels = raw[:,-1]
#bins = np.array([0,1,2,3,4])
bins = np.array([0,1,2,3,4,5,6,7,8])
numBins = bins.size

print(X.shape)
X = X.reshape(2540,50,50,1)

arr = []
multi = [8,60,9,8,30,19,1,1,1]
size = X.shape[0]
for i in range(size):
    num = int(y[i])
    arr.append(multi[num])

newX = np.repeat(X, arr, axis=0)
newY = np.repeat(y, arr, axis=0)

X_train, X_test, y_train, y_test = train_test_split(newX, newY, test_size=0.33, random_state=42)

X_train = X_train.astype(int)
X_test = X_test.astype(int)

print("Type of X is "+str(type(X_train)))
print("Type of y is "+str(type(y_train)))
print(len(X))
print(X[0].shape)
print(X.shape)
print(y[0])

model = Sequential()
model.add(layers.Conv2D(9, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(50,50,1)))
model.add(layers.Conv2D(9, (3, 3), activation='relu', name='my_layer'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Dropout(0.25))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(numBins, activation='softmax'))
"""
model = keras.Sequential();
model.add(keras.layers.Dense(1000, activation=tf.nn.relu, input_shape=(2500,)));
second_layer = keras.layers.Dropout(0.25);
model.add(second_layer);
model.add(keras.layers.Dense(250, activation=tf.nn.relu));
model.add(keras.layers.Dropout(0.25));
model.add(keras.layers.Dense(50, activation=tf.nn.relu));
model.add(keras.layers.Dropout(0.25));
model.add(keras.layers.Dense(25, activation=tf.nn.relu));
model.add(keras.layers.Dense(numBins, activation=tf.nn.softmax)); # must match number of bins in extractFeatures.py
"""

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=1, batch_size=70)
test_loss, test_acc = model.evaluate(X_test, y_test)

layer_name = 'my_layer'
intermediate_layer_model = Model(inputs=model.input,
                                 outputs=model.get_layer(layer_name).output)
intermediate_output = intermediate_layer_model.predict(X_test)
print(intermediate_output)

print((test_loss, test_acc))

keras_file = "model.h5"
tf.keras.models.save_model(model, keras_file)

converter = lite.TFLiteConverter.from_keras_model_file(keras_file)
tflite_model = converter.convert()
open("model.tflite", "wb").write(tflite_model)


