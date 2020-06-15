# import matplotlib.pyplot as plt
from model import matthews_correlation
# from skimage.transform import resize
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import os
import pyautogui
# import matplotlib.pyplot as plt
import datetime


class Clicker():

    
    def __init__(self, decision_threshold = 0.5):
        self.decision_threshold = decision_threshold
        self.model = None
        self.yes_position = None
        self.no_position = None
        self.screenshot = None
        self.screenshot_resized = None
        self.prob_predicted = None
        self.decision = None
        
       
    def clean_tmp_vars(self):
        self.yes_position = None
        self.no_position = None
        self.screenshot = None
        self.screenshot_resized = None
        self.prob_predicted = None
        self.decision = None
        
        
    def positions(self):  
        while True:
            # Print message
            print('Looking for Bumble icons on the screen')
            # Find the position of yes/no buttons on the screen
            yes_position = pyautogui.locateOnScreen(os.getcwd() + '/icons/' + 'yes.png')
            no_position = pyautogui.locateOnScreen(os.getcwd() + '/icons/' + 'no.png')
            
            if yes_position == None or no_position == None:
                continue
            
            else:
                # Print message
                print('Bumble images captured')
                # Compute the position of the photo
                yes_no_length = yes_position[0] - no_position[0]
                photo_bottomright_postion = [int(round(no_position[0] + yes_no_length / 2)), 
                                             int(round(min(yes_position[1], no_position[1])))]
                
                photo_position = {
                    'left': photo_bottomright_postion[0] - yes_no_length * 2.8,
                    'upper': photo_bottomright_postion[1] - yes_no_length * 3.8,
                    'right': photo_bottomright_postion[0],
                    'lower': photo_bottomright_postion[1]}
                
                # Take a screenshot
                screenshot = pyautogui.screenshot()
                screenshot = screenshot.crop(tuple(photo_position.values()))
  
                self.yes_position = yes_position
                self.no_position = no_position
                self.screenshot = screenshot
                
                break
                
                
    def initialize_model(self):
        model = load_model('trained_model.h5',
                           custom_objects={'matthews_correlation': matthews_correlation})
        self.model = model


    def make_decision(self):
        
        decision_threshold = self.decision_threshold
        model = self.model
        
        if model == None:
            raise Exception('Model not loaded. Please load model first')
        
        else: 
            self.resize_screenshot()
            screenshot = self.screenshot_resized
            screenshot_arr = img_to_array(screenshot)
            screenshot_arr = np.array([screenshot_arr])
            prob_predicted = model.predict(screenshot_arr)[0][0]
            self.prob_predicted = prob_predicted
            
            if prob_predicted > decision_threshold:
                decision = 1
                
            else:
                decision = 0
             
            self.decision = decision
    
    
    def resize_screenshot(self):
        screenshot = self.screenshot
        screenshot = screenshot.resize(size=(224, 300))
        self.screenshot_resized = screenshot
        
    
    def save_screenshot(self):
        screenshot = self.screenshot_resized
        decision = self.decision
            
        if decision == 1:
            time_now = str(datetime.datetime.now())
            savedir = './saved_screenshots/Yes/' +  time_now + '.png'
            screenshot.save(savedir)
        
        else:
            time_now = str(datetime.datetime.now())
            savedir = './saved_screenshots/No/' +  time_now + '.png'
            screenshot.save(savedir)
                
    
    def click_button(self):
        decision = self.decision
        yes_position = self.yes_position
        no_position = self.no_position
        
        
        if decision == 1: 
            pyautogui.moveTo(yes_position)
            pyautogui.click(x=yes_position[0],y=yes_position[1],
                                    clicks=1, button='left')
        
        else:
            pyautogui.moveTo(no_position)
            pyautogui.click(x=no_position[0],y=no_position[1],
                                    clicks=1, button="left")
        
        pyautogui.moveTo(100, 100)