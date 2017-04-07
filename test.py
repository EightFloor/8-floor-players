#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 10:17:53 2017

@author: zzzzzui
"""

import os
import re
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt

path = os.getcwd() + '/dataSets/training'
#pattern = '.csv'
#trainOriginal = [a for a in os.listdir(path) if re.search(pattern, a)]
'''
trajectories = pd.read_csv(path + '/' + 'trajectories(table 5)_training.csv', dtype='str')
volume = pd.read_csv(path + '/' + 'volume(table 6)_training.csv', dtype='str')
routes = pd.read_csv(path + '/' + 'routes (table 4).csv', dtype='str')
links = pd.read_csv(path + '/' + 'links (table 3).csv', dtype='str')
weather = pd.read_csv(path + '/' + 'weather (table 7)_training.csv', dtype='str')
'''

X = weather.index
Y = list(weather.rel_humidity)
plt.plot(X, Y)