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
  <img src="https://github.com/fastovetsilya/Automatic_NN_Swiper/blob/master/examples/bumble_logo.jpg"><br><br>
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

