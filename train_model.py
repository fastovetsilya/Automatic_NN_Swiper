# Load the modules
from build_model import simple_convolutional_model, VGG_16
from build_model import matthews_correlation
from keras.preprocessing.image import ImageDataGenerator
from keras_applications import resnet50
import data_preparation as prepare
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
import gc
gc.disable()

# Process raw data
# Load the images    
yes_filenames = os.listdir(os.getcwd() + '/Yes')
no_filenames = os.listdir(os.getcwd() + '/No')
yes_images = prepare.create_image_data(yes_filenames, classtype = 'Yes')
no_images = prepare.create_image_data(no_filenames, classtype = 'No')

# Or load the .pickle file with the fetched images
# file = open('images_Yes.pickle', 'rb')
# yes_images = pickle.load(file)
# file.close()
# file = open('images_No.pickle', 'rb')
# no_images = pickle.load(file)
# file.close()

# Create image dataset
# dataset = prepare.generate_dataset(yes_images, no_images)

# Load the data
file = open('data.pickle', 'rb')
data = pickle.load(file)
file.close()

# Shuffle data
data = prepare.shuffle_dataset(data)

# Make train and test splits
train_data, test_data = prepare.make_validation_split(data, val_split=0.2)

# Flip the images to increase dataset size
train_data = prepare.flip_images(train_data)
test_data = prepare.flip_images(test_data)

# Rotate images to increase dataset size
train_data = prepare.random_rotation(train_data)
test_data = prepare.random_rotation(test_data)

# Save prepared sets
file = open('prepared_sets.pickle', 'wb')
pickle.dump([train_data, test_data], file)
file.close()

# Load prepared sets
file = open('prepared_sets.pickle', 'rb')
prepared_data = pickle.load(file)
file.close()
train_data = prepared_data[0]
test_data = prepared_data[1]

# Define Train_X and Train_y
Train_X = train_data[0]
Train_y = train_data[1]
Test_X = test_data[0]
Test_y = test_data[1]

# Make the model
model = VGG_16()
model.compile(optimizer='nadam', loss='binary_crossentropy', metrics=['binary_accuracy', matthews_correlation])

# Train the model
history = model.fit(Train_X, Train_y, batch_size=10, 
          epochs=50, validation_data = [Test_X, Test_y])
plt.plot(history.history['val_loss'])
plt.plot(history.history['loss'])
plt.plot(history.history['val_binary_accuracy'])

# Or use automatic image generator to train the model
# datagen = ImageDataGenerator(
#     featurewise_center=True,
#     featurewise_std_normalization=True,
#     rotation_range=20,
#     width_shift_range=0.2,
#     height_shift_range=0.2,
#     horizontal_flip=True)

# datagen.fit(Train_X)

# model.fit_generator(datagen.flow(Train_X, Train_y, batch_size=10), 
#           epochs=30, validation_data = [Test_X, Test_y])

# Save the model
model.save('trained_model.h5')



