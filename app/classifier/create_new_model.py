import os

from keras.src.preprocessing.image import ImageDataGenerator

from app.classifier.lego_model import create_model
from utils import get_root_dir


def create_new_lego_model(filename="lego_classifier_model", epochs=3, batch_size=1, optimizer="adam"):

    input_shape = (56, 56, 3) #wielkość obrazka z palca

    data_dir = os.path.join('data_processed')
    data2_dir = os.path.join('data')
    save_dir = os.path.join('models')

    if optimizer is not "none":
        model = create_model(input_shape, optimizer)
    else:
        model = create_model(input_shape)
    train_data = ImageDataGenerator().flow_from_directory(data_dir, target_size=input_shape[:2], batch_size=batch_size, class_mode='categorical')
    validation_data = ImageDataGenerator().flow_from_directory(data2_dir, target_size=input_shape[:2], batch_size=batch_size, class_mode='categorical')
    print(train_data.class_indices)

    model.fit(train_data, epochs=epochs, validation_data=validation_data)
    model.save(f'{save_dir}/{filename}_{optimizer}_[e={epochs},bs={batch_size}].keras')

if __name__ == '__main__':
    create_new_lego_model("lego_classifier_model", epochs=1, batch_size=600, optimizer='adam')

