# Load the modules
from keras.models import Sequential
from keras.layers import Flatten, Dense, BatchNormalization, Activation, AlphaDropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
import keras.backend as K

def convolutional_model():
    '''
    This function builds a simple convolutional neural network with Keras
    '''
    
    # Simple model
    model = Sequential()
    
    model.add(BatchNormalization(input_shape=(224, 224, 3)))
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
