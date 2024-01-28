import os

import numpy as np
from keras.src.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

from app.classifier.lego_model import create_model


def create_new_lego_model(filename="lego_classifier_model", epochs=3, batch_size=1, optimizer=None):

    input_shape = (56, 56, 3) #wielkość obrazka z palca

    data_dir = os.path.join('data_processed')
    data2_dir = os.path.join('data')
    save_dir = os.path.join('models')

    if optimizer is None:
        model = create_model(input_shape)
    else:
        model = create_model(input_shape, optimizer)

    image_generator = ImageDataGenerator(validation_split=0.2)

    train_dataset = image_generator.flow_from_directory(data_dir,
                                                        target_size=input_shape[:2],
                                                        subset="training",
                                                        class_mode='categorical',
                                                        shuffle=True)

    validation_dataset = image_generator.flow_from_directory(data_dir,
                                                        target_size=input_shape[:2],
                                                        subset="validation",
                                                        class_mode='categorical',
                                                        shuffle=True)
    #print number of classes
    print(train_dataset.num_classes)

    model.fit(train_dataset, epochs=epochs, validation_data=validation_dataset)
    model.save(f'{save_dir}/{filename}_{optimizer}_[e={epochs},bs={batch_size}].keras')

if __name__ == '__main__':
    create_new_lego_model("lego_classifier", epochs=5, batch_size=600, optimizer='adam')

