# import matplotlib.pyplot as plt
from skimage.io import imread, imsave
# from skimage.transform import resize
from keras.models import load_model
# import numpy as np
import os
import pyautogui
from screenshot import take_screenshot
import datetime

# Set decision threshold
threshold = 0.5

# Load model
model = load_model('trained_model.h5')

# Find the position of yes/no buttons on the screen
# yes_click_position = pyautogui.locateOnScreen(os.getcwd() + '/icons/' + 'yes.png')
# no_click_position = pyautogui.locateOnScreen(os.getcwd() + '/icons/' + 'no.png')
pyautogui.moveTo(950, 680)
no_click_position = [750, 680]
yes_click_position = [950, 680]

# Iterate through girls
n_trials = 300
for i in range(n_trials):
    # Take screenshot
    screenshot = take_screenshot()
    screenshot = screenshot.reshape(1, 224, 224, 3)
    
    # Make prediction and decide
    prob_predicted = model.predict(screenshot)[0][0]
    if prob_predicted >= threshold:
        decision = 'yes'
        # Save screenshot
        screenshot = screenshot[0]
        time_now = str(datetime.datetime.now())
        savedir = os.getcwd() + '/saved_screenshots/Yes' +  time_now +'.jpg'
        imsave(savedir, screenshot)
        
    if prob_predicted < threshold:
        decision = 'no'
        # Save screenshot
        screenshot = screenshot[0]
        time_now = str(datetime.datetime.now())
        savedir = os.getcwd() + '/saved_screenshots/No' +  time_now +'.jpg'
        imsave(savedir, screenshot)
    
    # Make a click
    # Yes_click
    if decision == 'yes':
        pyautogui.click(x=yes_click_position[0],y=yes_click_position[1],
                                    clicks=1, pause=1, button="left")
    
    # No_click
    if decision == 'no':
        pyautogui.click(x=no_click_position[0], y=no_click_position[1],
                                    clicks=1, pause=1, button="left")
