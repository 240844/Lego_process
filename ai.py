
from keras import Sequential
from keras.src.layers import Flatten, Conv2D, Dense, Dropout, MaxPool2D
from keras.src.preprocessing.image import ImageDataGenerator

# Define parameters
input_shape = (56, 56, 3)
a = input_shape[:2]
print(a)
batch_size = 32
epochs = 10
# Create data generators for training and validation

train_generator = ImageDataGenerator().flow_from_directory('data_processed', target_size=input_shape[:2], batch_size=batch_size, class_mode='categorical')
#validation_generator = ImageDataGenerator().flow_from_directory('data_processed', target_size=input_shape[:2], batch_size=batch_size, class_mode='categorical')
validation_generator = None #TODO

# Create the model
model = Sequential()
model.add(Conv2D(32,3,padding="same", activation="relu", input_shape=input_shape))
model.add(MaxPool2D())
model.add(Conv2D(32, 3, padding="same", activation="relu"))
model.add(MaxPool2D())
model.add(Conv2D(64, 3, padding="same", activation="relu"))
model.add(MaxPool2D())
model.add(Dropout(0.4))

model.add(Flatten())
model.add(Dense(128,activation="relu"))
model.add(Dense(6, activation="softmax"))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_generator, epochs=epochs, validation_data=validation_generator)

# Save the model
model.save(f'models/lego_classifier_model_[e={epochs},bs={batch_size}].h5')
