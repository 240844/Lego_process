import os
import time

import keras
import numpy as np
from keras import Sequential
from keras.src.layers import Flatten, Conv2D, Dense, Dropout, MaxPool2D

from app.classifier.brick_enum import LegoBrick
from app.image_processing.image_processing import change_color_by_vector
from app.utils.utils import load_image, view_image


class LegoBrickModel:
    def __init__(self, model_filename=None):
        self.model = None
        self.load_model(model_filename)

    def load_model(self, model_filename):
        model_path = os.path.join('models', model_filename)
        self.model = keras.saving.load_model(model_path)


    # image musi być w formacie RGB. inaczej wypisze bzdury
    def predict_brick(self, imageRGB):
        start = time.time()
        if imageRGB.shape != (56, 56, 3):
            raise Exception(f"Image shape is {imageRGB.shape}, but should be (56, 56, 3)")
        imageRGB = np.expand_dims(imageRGB, axis=0)

        predictions = self.model.predict(imageRGB)
        #print(f"Predictions: {predictions}")
        result = []
        for i in range(len(LegoBrick)):
            result.append((LegoBrick(i), predictions[0][i]))

        print(f"Classification took: {time.time() - start:.3f}s")

        result.sort(key=lambda x: x[1], reverse=True)
        return result


def create_model(input_shape, optimizer='adam'):
    model = Sequential()
    model.add(Conv2D(3, 3, padding="same", activation="relu", input_shape=input_shape))
    model.add(MaxPool2D())
    model.add(Dropout(0.4))
    model.add(Flatten())
    for i in range(0, 5):
        model.add(Dense(128, activation="relu"))
        #model.add(Dropout(0.4))
    model.add(Dense(6, activation="softmax"))

    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    return model


# Example predict usage:
def example(test_brick = LegoBrick.CHERRY, image_index = 36):
    image_path = f'data_processed/{test_brick.name}/{test_brick.name}_{image_index}.png'
    print(f"Image path: {image_path}")
    imageRGB = load_image(image_path)  # image musi być w formacie RGB
    view_image(imageRGB)

    model = LegoBrickModel('lego_classifier_adam_[e=5,bs=600].keras')
    result = model.predict_brick(imageRGB)

    for brick, confidence in result:
        print(f"Predicted class: {brick.name}, confidence: {confidence * 100:.1f}%")


def test_junk():
    model = LegoBrickModel('lego_classifier_adam_[e=5,bs=600].keras')

    for filename in os.listdir(os.path.join('junk_items')):
        print(filename)
        image_path = f'junk_items/{filename}'
        imageRGB = load_image(image_path)  # image musi być w formacie RGB
        view_image(imageRGB)


        result = model.predict_brick(imageRGB)

        for brick, confidence in result:
            print(f"Predicted class: {brick.name}, confidence: {confidence * 100:.1f}%")


def view_confusion_matrix(model_filename):
    model = LegoBrickModel(model_filename)
    matrix = np.zeros((6, 6))
    for brick in LegoBrick:
        for i in range(0, 100):
            image_path = f'data_processed/{brick.name}/{brick.name}_{i}.png'
            imageRGB = load_image(image_path)  # image musi być w formacie RGB
            random_vector = np.random.randint(-20, 20, 3)
            imageRGB = change_color_by_vector(imageRGB, random_vector)
            result = model.predict_brick(imageRGB)
            matrix[brick.value][result[0][0].value] += 1
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    im = ax.imshow(matrix)
    ax.set_xticks(np.arange(6))
    ax.set_yticks(np.arange(6))
    ax.set_xticklabels([brick.name for brick in LegoBrick])
    ax.set_yticklabels([brick.name for brick in LegoBrick])
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    for i in range(6):
        for j in range(6):
            text = ax.text(j, i, matrix[i, j], ha="center", va="center", color="w")

    accuracy = np.trace(matrix) / np.sum(matrix)
    ax.set_title(f"Confusion matrix, accuracy: {accuracy*100:.2f}%")
    fig.tight_layout()
    plt.show()



if __name__ == '__main__':
    print("testing model")
    #example()
    #test_junk()
    view_confusion_matrix('lego_classifier_adam_[e=5,bs=600].keras')
