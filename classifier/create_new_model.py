import os

from keras.src.preprocessing.image import ImageDataGenerator

from classifier.lego_model import create_model
from utils import get_root_dir


def create_new_lego_model(filename="lego_classifier_model", epochs=3, batch_size=1):

    input_shape = (56, 56, 3) #wielkość obrazka z palca

    data_dir = os.path.join(get_root_dir(), 'data_processed')
    save_dir = os.path.join(get_root_dir(), 'models')

    model = create_model(input_shape)
    train_data = ImageDataGenerator().flow_from_directory(data_dir, target_size=input_shape[:2], batch_size=batch_size, class_mode='categorical')
    print(train_data.class_indices)
    validation_data = None  # TODO

    model.fit(train_data, epochs=epochs, validation_data=validation_data)
    model.save(f'{save_dir}/{filename}_[e={epochs},bs={batch_size}].keras')

if __name__ == '__main__':
    create_new_lego_model("lego_classifier_model", epochs=10, batch_size=32)

