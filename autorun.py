#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 14:43:04 2020

@author: saltair
"""
from clicker import Clicker
import time

clicker = Clicker(decision_threshold = 0.5)

clicker.initialize_model()

while True:
    clicker.positions()
    clicker.make_decision()
    clicker.save_screenshot()
    clicker.click_button()
    clicker.clean_tmp_vars()
    time.sleep(1)
