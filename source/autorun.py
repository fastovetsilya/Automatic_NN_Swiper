#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 14:43:04 2020

@author: Ilya Fastovets
"""
from clicker import Clicker
import model
import time
import tkinter as tk
from shutil import move
import sys
import os

class Commander():
    
    def __init__(self):
        self.build_model_window = None
        self.sort_images_window = None
        self.sort_images_filename = None
    
    
    @staticmethod
    def check_directories():
        if os.path.isdir('./images_train/No') == False:
            os.makedirs('./images_train/No')
            print('New directory created')
            
        if os.path.isdir('./images_train/Yes') == False:
            os.makedirs('./images_train/Yes')
            print('New directory created')
            
        if os.path.isdir('./saved_screenshots/No') == False:
            os.makedirs('./saved_screenshots/No')
            print('New directory created')
            
        if os.path.isdir('./saved_screenshots/Yes') == False:
           os.makedirs('./saved_screenshots/Yes')
           print('New directory created')
            

    @staticmethod
    def no_command():
        pass
    
    
    @staticmethod
    def swipe_right():
        # Close the dialog window
        main_window.destroy()
        
        # Initialize clicker
        clicker = Clicker()
        clicker.decision = 1
        
        while True:
            clicker.positions()
            clicker.click_button()
            clicker.resize_screenshot()
            clicker.save_screenshot()
            time.sleep(1)
    
    
    @staticmethod
    def swipe_smart():
        # Close the dialog window
        main_window.destroy()
        
        # Initialize clicker
        clicker = Clicker(decision_threshold = 0.5)
        
        # Initialize model
        clicker.initialize_model()
        
        # Swiping loop
        while True:
            clicker.positions()
            clicker.make_decision()
            clicker.save_screenshot()
            clicker.click_button()
            clicker.clean_tmp_vars()
            time.sleep(1)
            
            
    @classmethod   
    def train_model_with_validation(cls):
        # Close the dialog window
        cls.build_model_window.destroy()
        # Train model
        model.train_model(validation_mode=True)
            
        
    @classmethod
    def train_model_without_validation(cls):
        # Close the dialog window
        cls.build_model_window.destroy()
        # Train model
        model.train_model(validation_mode=False)
            
        
    @classmethod
    def build_model(cls):
        # Close the dialog window
        main_window.destroy()
        cls.build_model_window = tk.Tk()
        cls.build_model_window.title('Building model')
        cls.build_model_window.minsize(300, 150)
        tk.Label(cls.build_model_window, text = 'Please choose validation preference',  
          font =('Verdana', 15)).pack(pady = 10) 
        tk.Button(cls.build_model_window, text = 'Use validation', width = 15, command = Commander.train_model_with_validation).pack()
        tk.Button(cls.build_model_window, text = 'No validation', width = 15, command = Commander.train_model_without_validation).pack()
        cls.build_model_window.mainloop()
        
        
    @classmethod
    def sort_image_yes(cls, *args):
        cls.sort_images_window.destroy()
        move(cls.sort_images_filename, './images_train/Yes')
        
    
    
    @classmethod
    def sort_image_no(cls, *args):
        cls.sort_images_window.destroy()
        move(cls.sort_images_filename, './images_train/No')
    
    
    @classmethod
    def sort_image_delete(cls, *args):
        cls.sort_images_window.destroy()
        os.remove(cls.sort_images_filename)
    
    
    @classmethod
    def sort_image_quit(cls, *args):
        cls.sort_images_window.destroy()
        sys.exit()
        
        
    @classmethod
    def sort_images(cls):
        # Close the dialog window
        main_window.destroy()
        
        for image_file in os.listdir('./saved_screenshots/Yes/'):
            cls.sort_images_filename = './saved_screenshots/Yes/' + image_file
            cls.sort_images_window = tk.Tk()
            cls.sort_images_window.minsize(400, 300)
            cls.sort_images_window.title('Sorting saved screenshots (Yes folder)')
            sample_photo = tk.PhotoImage(file=cls.sort_images_filename)
            tk.Label(cls.sort_images_window, image=sample_photo).pack()
            cls.sort_images_window.bind('<Right>', cls.sort_image_yes)
            cls.sort_images_window.bind('<Left>', cls.sort_image_no)
            cls.sort_images_window.bind('<Delete>', cls.sort_image_delete)
            cls.sort_images_window.bind('<q>', cls.sort_image_quit)
            tk.Button(cls.sort_images_window, text='Yes (Right button)', width=30, command=Commander.sort_image_yes).pack()
            tk.Button(cls.sort_images_window, text='No (Left button)', width=30, command=Commander.sort_image_no).pack()
            tk.Button(cls.sort_images_window, text='Delete image (Del button)', width=30, command=Commander.sort_image_delete).pack()
            tk.Button(cls.sort_images_window, text='Quit (q button)', width=30, command=Commander.sort_image_quit).pack()
    
            cls.sort_images_window.mainloop()
        
        for image_file in os.listdir('./saved_screenshots/No/'):
            cls.sort_images_filename = './saved_screenshots/No/' + image_file
            cls.sort_images_window = tk.Tk()
            cls.sort_images_window.minsize(400, 300)
            cls.sort_images_window.title('Sorting saved screenshots (No folder)')
            sample_photo = tk.PhotoImage(file=cls.sort_images_filename)
            tk.Label(cls.sort_images_window, image=sample_photo).pack()
            cls.sort_images_window.bind('<Right>', cls.sort_image_yes)
            cls.sort_images_window.bind('<Left>', cls.sort_image_no)
            cls.sort_images_window.bind('<Delete>', cls.sort_image_delete)
            cls.sort_images_window.bind('<q>', cls.sort_image_quit)
            tk.Button(cls.sort_images_window, text='Yes (Right button)', width=30, command=Commander.sort_image_yes).pack()
            tk.Button(cls.sort_images_window, text='No (Left button)', width=30, command=Commander.sort_image_no).pack()
            tk.Button(cls.sort_images_window, text='Delete image (Del button)', width=30, command=Commander.sort_image_delete).pack()
            tk.Button(cls.sort_images_window, text='Quit (q button)', width=30, command=Commander.sort_image_quit).pack()
    
            cls.sort_images_window.mainloop()


# Check that the directories exist. If they do not exist, create them
Commander.check_directories()

# Create main tkinter window
main_window = tk.Tk()
main_window.title('Automatic dating swiper')
main_window.minsize(300, 150)
tk.Label(main_window, text = 'Please choose what to do',  
      font =('Verdana', 15)).pack(pady = 10) 
tk.Button(main_window, text = 'Swipe right', width = 15, command = Commander.swipe_right).pack()
tk.Button(main_window, text = 'Run smart swiper', width = 15, command = Commander.swipe_smart).pack()
tk.Button(main_window, text = 'Build model', width = 15, command = Commander.build_model).pack()
tk.Button(main_window, text = 'Sort images', width = 15, command = Commander.sort_images).pack()
main_window.mainloop()