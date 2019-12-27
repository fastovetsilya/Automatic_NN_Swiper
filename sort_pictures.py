import os
import matplotlib.pyplot as plt
from skimage.io import imread
from shutil import move

# Handle folder
handle_folder = 'Yes'

# List files in screenshot directory
screenshot_files = os.listdir(os.getcwd() + '/saved_screenshots/' + handle_folder + '/')

# Wait for input
for file in screenshot_files:

    im = imread(os.getcwd() + '/saved_screenshots/' + handle_folder + '/' + file)
    plt.imshow(im)
    plt.show()
    
    print('Copy file to Yes(y), No(n), or skip(s)?')
    decision = input()
    
    if decision == 'y':
        move(os.getcwd() + '/saved_screenshots/' + file, os.getcwd() + '/Yes/')
        print('Moved to Yes')
    
    elif decision == 'n':
        move(os.getcwd() + '/saved_screenshots/' + file, os.getcwd() + '/No/')
        print('Moved to No')
        
    elif decision == 's':
        print('Skip')
        continue
    
    else:
        print('Not understood, continue')
        continue
    

