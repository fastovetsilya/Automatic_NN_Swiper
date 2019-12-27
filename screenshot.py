import pyautogui
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imsave
from skimage.transform import resize
from skimage.util import img_as_ubyte
import os
import datetime

def take_screenshot():
    # Take a screenshot
    im = pyautogui.screenshot(region=(450,150, 420, 550))
    plt.imshow(im)
    plt.show()
    im = np.array(im)
    im = resize(im, (224, 224))
    im = img_as_ubyte(im)    
    return(im)
