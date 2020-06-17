# Automatic_NN_Swiper


## Description
Automatic swiping tool for dating apps. The current version is available for Bumble only. 
The tool is a computer vision machine learning algorithm based on convolutional neural 
network (CNN). 

The neural network is trained on the screenshots after initial swiping for the specific 
preferences of the user. A separate classification tool of the saved screenshots is available 
which is similar to the interface of the dating apps. 

The tool does not require API and interacts with the browser only by taking screenshots and 
initiating mouse clicks. 

<div align="center">
  <img src="https://github.com/fastovetsilya/Automatic_NN_Swiper/blob/master/examples/bumble_logo.png"><br><br>
</div>


## Installation 
On Unix-like systems run:
```console
$ git clone https://github.com/fastovetsilya/Automatic_NN_Swiper
$ cd Automatic_NN_Swiper/ 
$ pip install .
```

The dependencies should be installed automatically. Then run the program:
```console
$ python autoswipe
```

On Windows the installation process is similar. However, some dependencies have to be installed separately. 


## Usage
Open the browser with a dating app and then run the tool. The picture of a person and the navigation buttons should not 
be covered by other windows.

### The main window
The main window offers a variety of options. 

<div align="center">
  <img src="https://github.com/fastovetsilya/Automatic_NN_Swiper/blob/master/examples/main_window.png"><br><br>
</div>

**Swipe right** Swipe only right. Run this option at the beginning of usage to get the necessary number of screenshots to train the model. 
The required number of images to train should be big (ideally, thousands of images). 

**Run smart swiper** Smart swiping using the pre-trained model. Before running it, you should first build the model on the saved 
screenshots. 

**Build model** Builds the model using the sorted screenshots.

**Sort images** An app to sort saved screenshots in a way similar to dating apps. 

### Build model window

<div align="center">
  <img src="https://github.com/fastovetsilya/Automatic_NN_Swiper/blob/master/examples/build_model_window.png"><br><br>
</div>

The neural network is trained using pre-configured parameters for convenience. In theory, it weights the classes to account for the unbalanced samples. However, it is better to keep the number of images in Yes/No folders close to the same. 

For simplicity, all the training parameters are not changed in this window. They can be adjusted, however, in the model.py file. 

The two available options for training the model are: 

**Use validation** Train the model with a 20% validation set. This allows to display the validation metrics in the terminal (validation accuracy and validation Matthews correlation), but some of the data is lost.

**No validation** Train the model without a validation set. This saves samples, but makes it impossible to see the validation metrics. 

One of the ways to train the model is to train it with validation first, and if the results are good, train with no validation. 

### Sort images window

<div align="center">
  <img src="https://github.com/fastovetsilya/Automatic_NN_Swiper/blob/master/examples/sort_images_window.png"><br><br>
</div>

An app to sort saved sreenshots into Yes/No directories to train the model. The interface is similar to the interface of the dating apps. 
Press Right for 'Yes' and Left for 'No'. 















