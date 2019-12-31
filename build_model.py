# Load the modules
from keras.models import Sequential
from keras.layers import Activation, BatchNormalization, AlphaDropout
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
import keras.backend as K
# from keras.regularizers import l2


def simple_convolutional_model():
    
    '''
    This function builds a convolutional part of the model to train it on the 
    data from scratch. 

    '''
    # Convolutional layers
    model = Sequential()
    
    model.add(BatchNormalization())
    model.add(Conv2D(32, (3, 3), input_shape=(
        224, 224, 3), data_format='channels_last', kernel_initializer='lecun_normal'))
    model.add(Activation('selu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_last'))
    
    model.add(BatchNormalization())
    model.add(Conv2D(32, (3, 3), data_format='channels_last', kernel_initializer='lecun_normal'))
    model.add(Activation('selu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_last'))
    
    # Dense layers
    model.add(Flatten())
    model.add(Dense(1024, activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(AlphaDropout(0.5))
    model.add(Dense(256, activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(Dense(1, activation='sigmoid'))

    return(model)

def VGG_16(weights_path='/media/saltair/Library/ASS/vgg16_weights.h5'):
    '''
    This function builds a pre-trained VGG-16 part of the NN and loads 
    weights from the weights path specified in the input of the function.
    '''

    model = Sequential()
    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1), input_shape=(
        224, 224, 3), data_format='channels_last'))
    model.add(BatchNormalization())
    model.add(Conv2D(64, kernel_size=(3, 3), strides=1, activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(64, kernel_size=(3, 3), strides=1, activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2), strides=(
        2, 2), data_format='channels_last'))

    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(128, kernel_size=(3, 3), activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(128, kernel_size=(3, 3), activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2), strides=(
        2, 2), data_format='channels_last'))

    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(256, kernel_size=(3, 3), activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(256, kernel_size=(3, 3), activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(256, kernel_size=(3, 3), activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2), strides=(
        2, 2), data_format='channels_last'))
    
    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3), activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3), activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2), strides=(
        2, 2), data_format='channels_last'))

    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3), activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3), activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(ZeroPadding2D((1, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3), activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2), strides=(
        2, 2), data_format='channels_last'))


    # model.load_weights(weights_path, by_name=True)

    # # set trainable to false in all layers
    # for layer in model.layers:
    #     if hasattr(layer, 'trainable'):
    #         layer.trainable = False
            
    model.add(Flatten())
    model.add(BatchNormalization())
    model.add(Dense(4096, activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    # model.add(AlphaDropout(0.5))
    model.add(Dense(1024, activation='selu', kernel_initializer='lecun_normal'))
    model.add(BatchNormalization())
    # model.add(AlphaDropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    return model

def matthews_correlation(y_true, y_pred):
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