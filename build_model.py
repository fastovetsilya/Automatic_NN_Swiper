# Load the modules
from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
import keras.backend as K


def VGG_16(weights_path='./vgg16_weights.h5'):
    '''
    This function builds a pre-trained VGG-16 Neural Network and loads 
    weights from the weights path specified in the input of the function.
    After loading weights to the convolutional layers dense layers are 
    added at the top of the model (the layers that are trained).
    
    '''

    # Original VGG_16 with pre-trained weights
    model = Sequential()
    
    model.add(ZeroPadding2D((1, 1), input_shape=(
        224, 224, 3), data_format='channels_last'))
    model.add(Conv2D(64, kernel_size=(3, 3), strides=1, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(64, kernel_size=(3, 3), strides=1, activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(
        2, 2), data_format='channels_last'))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(
        2, 2), data_format='channels_last'))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(
        2, 2), data_format='channels_last'))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(
        2, 2), data_format='channels_last'))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(
        2, 2), data_format='channels_last'))

    # model.add(Flatten())
    # model.add(Dense(4096, activation='relu'))
    # model.add(Dropout(0.5))
    # model.add(Dense(4096, activation='relu'))
    # model.add(Dropout(0.5))
    # model.add(Dense(1000, activation='softmax'))

    model.load_weights(weights_path, by_name=True)

    # set trainable to false in all layers
    for layer in model.layers:
        if hasattr(layer, 'trainable'):
            layer.trainable = False
            
    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
        
    return model


def matthews_correlation(y_true, y_pred):
    '''
    This function defines the Matthews correlation coefficient to use as a 
    validation metric for training the Neural Network. 
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
