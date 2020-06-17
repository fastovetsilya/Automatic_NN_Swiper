#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 14:43:04 2020

@author: Ilya Fastovets
"""
from clicker import Clicker
from model import Model
import time
import tkinter as tk
from shutil import move
import sys
import os


class Commander():

    def __init__(self):
        self.main_window = None
        self.build_model_window = None
        self.sort_images_window = None
        self.sort_images_filename = None

    def create_main_window(self):
        # Create main tkinter window
        self.main_window = tk.Tk()
        self.main_window.title('Automatic dating swiper')
        self.main_window.minsize(300, 150)
        tk.Label(self.main_window, text='Please choose what to do',
                 font=('Verdana', 15)).pack(pady=10)
        tk.Button(self.main_window, text='Swipe right',
                  width=15, command=self.swipe_right).pack()
        tk.Button(self.main_window, text='Run smart swiper',
                  width=15, command=self.swipe_smart).pack()
        tk.Button(self.main_window, text='Build model',
                  width=15, command=self.build_model).pack()
        tk.Button(self.main_window, text='Sort images',
                  width=15, command=self.sort_images).pack()
        self.main_window.mainloop()

    def check_directories(self):
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

    def swipe_right(self):
        # Close the dialog window
        self.main_window.destroy()

        # Initialize clicker
        clicker = Clicker()
        clicker.decision = 1

        while True:
            clicker.positions()
            clicker.click_button()
            clicker.resize_screenshot()
            clicker.save_screenshot()
            time.sleep(1)

    def swipe_smart(self):
        # Close the dialog window
        self.main_window.destroy()

        # Initialize clicker
        clicker = Clicker(decision_threshold=0.5)

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

    def train_model_with_validation(self):
        # Close the dialog window
        self.build_model_window.destroy()
        # Train model
        model = Model()
        model.train_model(validation_mode=True)

    def train_model_without_validation(self):
        # Close the dialog window
        self.build_model_window.destroy()
        # Train model
        model = Model()
        model.train_model(validation_mode=False)

    def build_model(self):
        # Close the dialog window
        self.main_window.destroy()
        self.build_model_window = tk.Tk()
        self.build_model_window.title('Building model')
        self.build_model_window.minsize(300, 150)
        tk.Label(self.build_model_window, text='Please choose validation preference',
                 font=('Verdana', 15)).pack(pady=10)
        tk.Button(self.build_model_window, text='Use validation',
                  width=15, command=self.train_model_with_validation).pack()
        tk.Button(self.build_model_window, text='No validation', width=15,
                  command=self.train_model_without_validation).pack()
        self.build_model_window.mainloop()

    def sort_image_yes(self, *args):
        self.sort_images_window.destroy()
        move(self.sort_images_filename, './images_train/Yes')

    def sort_image_no(self, *args):
        self.sort_images_window.destroy()
        move(self.sort_images_filename, './images_train/No')

    def sort_image_delete(self, *args):
        self.sort_images_window.destroy()
        os.remove(self.sort_images_filename)

    def sort_image_quit(self, *args):
        self.sort_images_window.destroy()
        sys.exit()

    def sort_images(self):
        # Close the dialog window
        self.main_window.destroy()

        for image_file in os.listdir('./saved_screenshots/Yes/'):
            self.sort_images_filename = './saved_screenshots/Yes/' + image_file
            self.sort_images_window = tk.Tk()
            self.sort_images_window.minsize(400, 300)
            self.sort_images_window.title(
                'Sorting saved screenshots (Yes folder)')
            sample_photo = tk.PhotoImage(file=self.sort_images_filename)
            tk.Label(self.sort_images_window, image=sample_photo).pack()
            self.sort_images_window.bind('<Right>', self.sort_image_yes)
            self.sort_images_window.bind('<Left>', self.sort_image_no)
            self.sort_images_window.bind('<Delete>', self.sort_image_delete)
            self.sort_images_window.bind('<q>', self.sort_image_quit)
            tk.Button(self.sort_images_window, text='Yes (Right button)',
                      width=30, command=self.sort_image_yes).pack()
            tk.Button(self.sort_images_window, text='No (Left button)',
                      width=30, command=self.sort_image_no).pack()
            tk.Button(self.sort_images_window, text='Delete image (Del button)',
                      width=30, command=self.sort_image_delete).pack()
            tk.Button(self.sort_images_window, text='Quit (q button)',
                      width=30, command=self.sort_image_quit).pack()

            self.sort_images_window.mainloop()

        for image_file in os.listdir('./saved_screenshots/No/'):
            self.sort_images_filename = './saved_screenshots/No/' + image_file
            self.sort_images_window = tk.Tk()
            self.sort_images_window.minsize(400, 300)
            self.sort_images_window.title(
                'Sorting saved screenshots (No folder)')
            sample_photo = tk.PhotoImage(file=self.sort_images_filename)
            tk.Label(self.sort_images_window, image=sample_photo).pack()
            self.sort_images_window.bind('<Right>', self.sort_image_yes)
            self.sort_images_window.bind('<Left>', self.sort_image_no)
            self.sort_images_window.bind('<Delete>', self.sort_image_delete)
            self.sort_images_window.bind('<q>', self.sort_image_quit)
            tk.Button(self.sort_images_window, text='Yes (Right button)',
                      width=30, command=self.sort_image_yes).pack()
            tk.Button(self.sort_images_window, text='No (Left button)',
                      width=30, command=self.sort_image_no).pack()
            tk.Button(self.sort_images_window, text='Delete image (Del button)',
                      width=30, command=self.sort_image_delete).pack()
            tk.Button(self.sort_images_window, text='Quit (q button)',
                      width=30, command=self.sort_image_quit).pack()

            self.sort_images_window.mainloop()
