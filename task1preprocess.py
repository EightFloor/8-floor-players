#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:06:44 2017

@author: zzzzzui
"""

import pandas as pd
from pandas import DataFrame
from datetime import datetime
import math
#import requests

path = '/home/zzzzzui/Tianchi/8-floor-players/dataSets/training'
out_path = '/home/zzzzzui/Tianchi/8-floor-players/dataSets/afterPre'

fileName = 'trajectories(table 5)_training.csv'
links_fileName = 'links (table 3).csv'
weather_fileName = 'weather(table 7)_training.csv'
holiday_fileName = 'holidays_dummies.csv'
                           
links_info = pd.read_csv(path + '/' + links_fileName, dtype=str)
weather_info = pd.read_csv(path + '/' + weather_fileName, dtype=str)
trajectories = pd.read_csv(path + '/' + fileName, dtype=str)
holidays = holidays=pd.read_csv(path+'/'+'holidays_dummies.csv',
                                header=None, names=['date', 'working_day', 
                                'day_before_holiday', 'weekends', 'holidays', 'day_after_holiday'],
                                dtype=str)

'''
url = 'http://www.easybots.cn/api/holiday.php?m='
months = ['00', '01', '02', '03', '04', '05', '06', 
          '07', '08', '09', '10', '11', '12']
years = ['2016', '2017']
for year in years:
    for month in months:
        url += (year+month+',')
url = url[:-1]
post = requests.post(url)
holidays = post.json()
'''

def timewindow_process(aStr):
    starting_time = datetime.strptime(aStr, "%Y-%m-%d %H:%M:%S")
    timewindow_minutes = math.floor(starting_time.minute / 20) * 20
    timewindow = datetime(starting_time.year, starting_time.month,starting_time.day,
                           starting_time.hour, timewindow_minutes, 0)
    return timewindow



link_dict = {}

#travel time
for line in trajectories['travel_seq']:
    seq = line.split(';')
    for link in seq:
        link_info = link.split('#')
        
        if link_info[0] not in link_dict:
            link_dict[link_info[0]] = {}
            
        timewindow = timewindow_process(link_info[1]) 
        if timewindow not in link_dict[link_info[0]]:
            link_dict[link_info[0]][timewindow] = [float(link_info[2])]
        else:
            link_dict[link_info[0]][timewindow].append(float(link_info[2]))
         
#links_info
links_info = links_info.fillna('')
links_info['in_top'] = links_info['in_top'].apply(lambda x: math.floor(len(x)/3))
links_info['out_top'] = links_info['out_top'].apply(lambda x: math.floor(len(x)/3))            

for link_No in link_dict:
    
    #weather
    for timewindow in link_dict[link_No]:
        link_dict[link_No][timewindow] = sum(link_dict[link_No][timewindow])/len(link_dict[link_No][timewindow])
    
    aDF = DataFrame(link_dict[link_No], index=[0]).T

    aDF.columns = ['avg_travel_time']
    #aDF = pd.concat([aDF, DataFrame(columns=weather_info.columns[:2])])
    aDF = pd.concat([aDF, DataFrame(columns=['date', 'hour', 'timewindow'])])
    aDF['date'] = aDF.index
    aDF['hour'] = aDF.index
    aDF['timewindow'] = aDF.index
    aDF['date'] = aDF['date'].apply(lambda x: str(x.year) + '-' + ('%02d' % x.month) + '-' + ('%02d' % x.day))
    aDF['hour'] = aDF['hour'].apply(lambda x: str(math.floor(x.hour / 3) * 3))
    
    #test = pd.merge(aDF, weather_info, how='left', left_on=['date', 'hour'], right_on=['date', 'hour'], sort=False)

    aDF = pd.merge(aDF, weather_info, on=['date', 'hour'], how='left', sort=False)#.fillna('-1')
    
    
    #link_fundamental_info
    aDF = pd.concat([aDF, DataFrame(columns=['link_id'])])
    aDF.loc[:, ['link_id']] = link_No
    
    
    aDF = pd.merge(aDF, links_info, on=['link_id'], how='left', sort=False)
    
    #holidays
    aDF = pd.merge(aDF, holidays, on=['date'], how='left', sort=False)
    
    aDF.index = aDF['timewindow']
    del aDF['date']
    del aDF['hour']
    del aDF['timewindow']
    
    aDF.to_csv(out_path+'/'+link_No+'_info.csv')
       


