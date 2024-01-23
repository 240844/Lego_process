import os

import keras
import numpy as np
from keras import Sequential
from keras.src.layers import Flatten, Conv2D, Dense, Dropout, MaxPool2D

from app.classifier.brick_enum import LegoBrick
from utils import load_image, get_root_dir, view_image


class LegoBrickModel:
    def __init__(self, model_filename=None):
        self.model = None
        self.load_model(model_filename)

    def load_model(self, model_filename):
        model_path = os.path.join(get_root_dir()+'/../', 'models', model_filename)
        self.model = keras.src.saving.saving_api.load_model(model_path)


    # image musi być w formacie RGB. inaczej wypisze bzdury
    def predict_brick(self, imageRGB):
        if imageRGB.shape != (56, 56, 3):
            raise Exception(f"Image shape is {imageRGB.shape}, but should be (56, 56, 3)")
        imageRGB = np.expand_dims(imageRGB, axis=0)

        predictions = self.model.predict(imageRGB)
        #print(f"Predictions: {predictions}")
        result = []
        for i in range(len(LegoBrick)):
            result.append((LegoBrick(i), predictions[0][i]))

        result.sort(key=lambda x: x[1], reverse=True)
        return result


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
def example(test_brick = LegoBrick.CHERRY, image_index = 36):
    image_path = f'data_processed/{test_brick.name}/{test_brick.name}_{image_index}.png'
    print(f"Image path: {image_path}")
    imageRGB = load_image(image_path)  # image musi być w formacie RGB
    view_image(imageRGB)

    model = LegoBrickModel('lego_classifier_model_[e=10,bs=32].keras')
    result = model.predict_brick(imageRGB)

    for brick, confidence in result:
        print(f"Predicted class: {brick.name}, confidence: {confidence * 100:.1f}%")


def test_junk():
    model = LegoBrickModel('lego_classifier_model_[e=1,bs=50].keras')

    for filename in os.listdir(os.path.join(get_root_dir(), 'junk_items')):
        print(filename)
        image_path = f'junk_items/{filename}'
        imageRGB = load_image(image_path)  # image musi być w formacie RGB
        view_image(imageRGB)


        result = model.predict_brick(imageRGB)

        for brick, confidence in result:
            print(f"Predicted class: {brick.name}, confidence: {confidence * 100:.1f}%")


if __name__ == '__main__':
    print("testing model")
    #example()
    test_junk()