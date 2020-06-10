# Load the modules
from build_model import VGG_16
from build_model import matthews_correlation
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# Define the image directories
images_train_dir = './images_train'   

# Build the model
model = VGG_16()
model.compile(optimizer='nadam', loss='binary_crossentropy', metrics=['binary_accuracy', matthews_correlation])

# Build image data generator
# Initialize the generator
train_image_generator = ImageDataGenerator(
    rescale = 1 / 255,
    validation_split=0.2,
    # rotation_range=20,
    # width_shift_range=0.2,
    # height_shift_range=0.2,
    # shear_range=0.2,
    # zoom_range=0.2,
    horizontal_flip=True,
    data_format='channels_last') 

# Define the data flow from train directory
train_image_generator_dirflow = train_image_generator.flow_from_directory(
    images_train_dir,
    target_size=(224, 224),
    color_mode='rgb',
    batch_size=10,
    class_mode='binary', 
    subset='training')

validation_image_generator_dirflow = train_image_generator.flow_from_directory(
    images_train_dir,
    target_size=(224, 224),
    color_mode='rgb',
    batch_size=20,
    class_mode='binary', 
    subset='validation')

# Train the model
model_history = model.fit_generator(
    train_image_generator_dirflow, 
    validation_data=validation_image_generator_dirflow,
    epochs=10)

plt.plot(model_history.history['val_loss'])
plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_binary_accuracy'])


# Save the model
model.save('trained_model.h5')
