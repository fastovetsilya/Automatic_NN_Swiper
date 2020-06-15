# Load the modules
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Flatten, Dense, BatchNormalization, Activation, AlphaDropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
import keras.backend as K
from sklearn.utils import class_weight
import numpy as np


def convolutional_model():
    '''
    This function builds a simple convolutional neural network with Keras. 
    The returned object is a Keras model.

    The model architecture is a simple convolutional model with elu activations
    and Batch Normalization and Alpha Dropout added for regularization.
    '''

    # Simple model
    model = Sequential()

    model.add(BatchNormalization(input_shape=(300, 224, 3)))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('elu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(BatchNormalization())
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('elu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(BatchNormalization())
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('elu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(BatchNormalization())
    model.add(Dense(1024, activation='elu'))
    model.add(BatchNormalization())
    model.add(AlphaDropout(0.5))
    model.add(Dense(1024, activation='elu'))
    model.add(BatchNormalization())
    model.add(AlphaDropout(0.3))
    model.add(Dense(1, activation='sigmoid'))

    return model


def matthews_correlation(y_true, y_pred):
    '''
    This function defines the Matthews correlation coefficient to use as a 
    validation metric for training the CNN. 
    '''

    y_pred_pos = K.round(K.clip(y_pred, 0, 1))
    y_pred_neg = 1 - y_pred_pos

    y_pos = K.round(K.clip(y_true, 0, 1))
    y_neg = 1 - y_pos

    tp = K.sum(y_pos * y_pred_pos)
    tn = K.sum(y_neg * y_pred_neg)

    fp = K.sum(y_neg * y_pred_pos)
    fn = K.sum(y_pos * y_pred_neg)

    numerator = (tp * tn - fp * fn)
    denominator = K.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))

    return numerator / (denominator + K.epsilon())


def train_model(validation_mode=True, epochs=20,
                images_train_dir='./images_train'):
    '''
    This procedure initializes, trains and save the CNN model. 

    Parameters
    ----------
    validation_mode: boolian, optional
        If True (default), a 20% portion of the data is used for validation of 
        the model, and the validation metrics are displayed during the progress. 
        If False, no validation is used

    epochs: int, optional
        The number of epochs to use to train the model. The default is 20.

    images_train_dir: str, optional
        The directory with classified images (training data)

    Returns 
    ----------
    None
    '''

    # Initialize and compile the model
    model = convolutional_model()
    model.compile(optimizer='adam', loss='binary_crossentropy',
                  metrics=['binary_accuracy', matthews_correlation])
    
    if validation_mode == True:
        # Build image data generator
        # Initialize the generator
        train_image_generator = ImageDataGenerator(
            validation_split=0.2,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            data_format='channels_last')
        
        # Initialize the train data flow from train directory
        train_image_generator_dirflow = train_image_generator.flow_from_directory(
            images_train_dir,
            target_size=(300, 224),
            color_mode='rgb',
            batch_size=20,
            class_mode='binary',
            subset='training')
        
        # Compute class weights for unbalanced data
        class_weights = class_weight.compute_class_weight(
            'balanced',
            np.unique(train_image_generator_dirflow.classes), 
            train_image_generator_dirflow.classes)
        
        # Initialize the validation data from from val split from train directory
        validation_image_generator_dirflow = train_image_generator.flow_from_directory(
            images_train_dir,
            target_size=(300, 224),
            color_mode='rgb',
            batch_size=20,
            class_mode='binary',
            subset='validation')
    
        # Train the model
        model.fit_generator(
            train_image_generator_dirflow,
            validation_data=validation_image_generator_dirflow,
            epochs=epochs, 
            class_weight=class_weights)
        
    elif validation_mode == False:
        # Build image data generator
        # Initialize the generator
        train_image_generator = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            data_format='channels_last')
        
        # Initialize the train data flow from train directory
        train_image_generator_dirflow = train_image_generator.flow_from_directory(
            images_train_dir,
            target_size=(300, 224),
            color_mode='rgb',
            batch_size=20,
            class_mode='binary')
        
        # Compute class weights for unbalanced data
        class_weights = class_weight.compute_class_weight(
            'balanced',
            np.unique(train_image_generator_dirflow.classes), 
            train_image_generator_dirflow.classes)
        
        # Train the model
        model.fit_generator(
            train_image_generator_dirflow,
            epochs=epochs, 
            class_weight=class_weights)
    
    else: 
        raise Exception('The value "validation mode" should be boolean')
        
    # Save the model
    model.save('trained_model.h5')


