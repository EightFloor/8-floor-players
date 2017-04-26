#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 10:17:53 2017

@author: zzzzzui
"""

import os
import pandas as pd
from pandas import DataFrame, Series
from sklearn import preprocessing

path = os.getcwd() + '/dataSets/afterPre'
to_path = os.getcwd() + '/dataSets/afterScale'
#pattern = '.csv'
#trainOriginal = [a for a in os.listdir(path) if re.search(pattern, a)]
'''
trajectories = pd.read_csv(path + '/' + 'trajectories(table 5)_training.csv', dtype='str')
volume = pd.read_csv(path + '/' + 'volume(table 6)_training.csv', dtype='str')
routes = pd.read_csv(path + '/' + 'routes (table 4).csv', dtype='str')
links = pd.read_csv(path + '/' + 'links (table 3).csv', dtype='str')
weather = pd.read_csv(path + '/' + 'weather (table 7)_training.csv', dtype='str')
'''

for filename in os.listdir(path):
    file = pd.read_csv(path+'/'+filename)
    file = file.dropna()
    file['precipitation'] = preprocessing.scale(file['precipitation'])
    file['pressure'] = preprocessing.scale(file['pressure'])
    file['rel_humidity'] = preprocessing.scale(file['rel_humidity'])
    file['sea_pressure'] = preprocessing.scale(file['sea_pressure'])
    file['temperature'] = preprocessing.scale(file['temperature'])
    file['wind_direction'] = preprocessing.scale(file['wind_direction'])
    file['wind_speed'] = preprocessing.scale(file['wind_speed'])
    file.to_csv(to_path+'/'+filename, index=False)