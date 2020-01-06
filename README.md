# Automatic_NN_Swiper

## Description
Automatic swiping tool for dating sites. It takes a screenshot, feeds it to a convolutional neural network (CNN) and 
makes a descision where to swipe. After decision is made, automatic clicker ckicks on the corresponding putton, and 
the cycle repeats. 

Testing and README creation in progress

## Usage
1. Collect sample images to Yes/No folders

2. Train the model on the images

3. Setup image and button location. Run clicker

4. While autoswiping, screenshots are saved. After the session, classify correctly and train classifier again

5. When the satisfactory accuracy is achieved, enjoy automatic partner search

## Features
Simple and VGG-16 CNN architectures with selu activations and batch normalization, images preparation(data augmentation), 
easy-to-use after-session manual classifier of saved screenshots. Does not require API. 




