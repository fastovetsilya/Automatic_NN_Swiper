# Load the modules
from build_model import convolutional_model, matthews_correlation
from keras.preprocessing.image import ImageDataGenerator

# Define the image directories
images_train_dir = './images_train'   

# Initialize and compile the model
model = convolutional_model()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['binary_accuracy', matthews_correlation])

# Build image data generator
# Initialize the generator
train_image_generator = ImageDataGenerator(
    rescale = 1. / 255,
    validation_split=0.2,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    data_format='channels_last') 

# Define the data flow from train directory
train_image_generator_dirflow = train_image_generator.flow_from_directory(
    images_train_dir,
    target_size=(224, 224),
    color_mode='rgb',
    batch_size=20,
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
    epochs=20)

# Save the model
model.save('trained_model.h5')