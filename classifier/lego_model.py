import os

import cv2
import keras
import numpy as np
from keras import Sequential
from keras.src.layers import Flatten, Conv2D, Dense, Dropout, MaxPool2D

from classifier.brick_enum import LegoBrick
from utils import load_image, get_root_dir


class LegoBrickModel:
    def __init__(self, model_filename=None):
        self.model = None
        self.load_model(model_filename)

    def load_model(self, model_filename):
        model_path = os.path.join(get_root_dir(), 'models', model_filename)
        self.model = keras.src.saving.saving_api.load_model(model_path)


    # image musi być w formacie RGB. inaczej wypisze bzdury
    def predict_brick(self, imageRGB, input_shape=(56, 56)):
        imageRGB = cv2.resize(imageRGB, input_shape)
        imageRGB = imageRGB / 255.0  # Normalize pixel values to be between 0 and 1
        imageRGB = np.expand_dims(imageRGB, axis=0)  # Add batch dimension

        predictions = self.model.predict(imageRGB)

        predicted_brick = LegoBrick(np.argmax(predictions))
        confidence = np.max(predictions)
        print(f"Predictions: {predictions}")
        #print(f"Predicted class: {predicted_brick.name}, confidence: {confidence * 100:.1f}%")
        return predicted_brick, confidence


def create_model(input_shape):
    model = Sequential()
    model.add(Conv2D(32, 3, padding="same", activation="relu", input_shape=input_shape))
    model.add(MaxPool2D())
    model.add(Dropout(0.4))
    model.add(Flatten())
    model.add(Dense(128, activation="relu"))
    model.add(Dense(6, activation="softmax"))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model



# Example predict usage:
if __name__ == '__main__':
    test_brick = LegoBrick.CHERRY
    image_path = f'{test_brick.name}/{test_brick.name}_{36}.png'
    imageRGB = load_image(image_path)  # image musi być w formacie RGB

    model = LegoBrickModel('lego_classifier_model_[e=10,bs=32].keras')
    predicted_brick, confidence = model.predict_brick(imageRGB)
    print(f"prediction: {predicted_brick.name}, index: {predicted_brick.value}, confidence: {confidence * 100:.1f}%")

