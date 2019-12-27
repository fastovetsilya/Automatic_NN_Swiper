import pickle
from skimage.io import imread
from skimage.transform import resize, rotate
import matplotlib.pyplot as plt
import numpy as np
from numpy import fliplr
import os

yes_filenames = os.listdir(os.getcwd() + '/Yes')
no_filenames = os.listdir(os.getcwd() + '/No')

def create_image_data(filenames_list, classtype = 'No'):
    image_data = []
    for filename in filenames_list:
        print('Loading ', filename)
        
        # Try to load images
        try:
            img = imread(os.getcwd() + '/' + classtype + '/' + filename)
            img = resize(img, (224, 224))
            img = img[:, :, :3]
            img = img * 255
            img = img.astype(np.uint8)
            img = np.reshape(img, [1, 224, 224, 3])

            if image_data == []:
                image_data = img
        
            else:
                image_data = np.concatenate([image_data, img], axis=0)
        
            # Display downloaded images
            # plt.imshow(img[0, :, :, :])
            # plt.show()
            # plt.close()
        except:
            print('Could not fetch the image')
    
    # Try saving files. If failed, at least just return
    file = open(os.getcwd() + '/images_' + classtype + '.pickle', 'wb')
    pickle.dump(image_data, file)
    file.close()
    
    return(image_data)
    
# Concatenate image tensors and create target
def generate_dataset(yes_images, no_images):
    yes_target = np.repeat(1, yes_images.shape[0])
    no_target = np.repeat(0, no_images.shape[0])
    images_data = np.concatenate((yes_images, no_images))
    target = np.concatenate((yes_target, no_target))
    dataset = [images_data, target]
    
    file = open('data.pickle', 'wb')
    pickle.dump(dataset, file)
    file.close()
    
    return(dataset)

def flip_images(data):
    # ? Make additional transformations to increase train set size ?
    # Create dataset of flipped images
    images = data[0]
    y = data[1]
    images_flipped = [] 
    for entry in range(0, images.shape[0]):
        image = images[entry]
        image_flipped = fliplr(image)
        image_flipped = image_flipped.astype(np.uint8)
        image_flipped = image_flipped.reshape(1, 224, 224, 3)
        
        if images_flipped == []:
            images_flipped = image_flipped
            images_flipped = images_flipped.reshape(1, 224, 224, 3)
        else:
            images_flipped = np.concatenate((images_flipped, image_flipped))
    
    # Make data look like original
    images = np.concatenate((images, images_flipped))
    y = np.concatenate((y, y))
    
    return([images, y])

def shuffle_dataset(data):
    # Shuffle data
    shuf_index = np.arange(data[1].shape[0])
    np.random.shuffle(shuf_index)
    data = [data[0][shuf_index], data[1][shuf_index]]
    
    return(data)

def random_rotation(data):
    # pick a random degree of rotation between 25% on the left and 25% on the right
    random_degree = np.random.uniform(-25, 25)
    images = data[0]
    y = data[1]
    images_rotated = [] 
    for entry in range(0, images.shape[0]):
        image = images[entry]
        image_rotated = rotate(image, random_degree)
        image_rotated = image_rotated * 255
        image_rotated = image_rotated.astype(np.uint8)
        image_rotated = image_rotated.reshape(1, 224, 224, 3)
        
        if images_rotated == []:
            images_rotated = image_rotated
            images_rotated = images_rotated.reshape(1, 224, 224, 3)
        else:
            images_rotated = np.concatenate((images_rotated, image_rotated))
    
    # Make data look like original
    images = np.concatenate((images, images_rotated))
    y = np.concatenate((y, y))
    
    return([images, y])

def make_validation_split(data, val_split=0.2, raw_data_filepath='raw_data_filtered.csv'):
    Train_X = data[0]
    Train_y = data[1]
    train_test_index = np.zeros(Train_y.shape)
    train_test_index = np.array([bool(np.random.choice(np.arange(0, 2), p=[val_split, 1-val_split])) for i in range(Train_y.shape[0])])
    Test_X = Train_X[train_test_index == False]
    Test_y = Train_y[train_test_index == False]
    Train_X = Train_X[train_test_index]
    Train_y = Train_y[train_test_index]

    return([Train_X, Train_y], [Test_X, Test_y])

