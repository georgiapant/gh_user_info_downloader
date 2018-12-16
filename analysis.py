import pandas as pd
from datetime import datetime, timedelta, date
import time
import numpy as np
import matplotlib.pyplot as plt

'''
This file contains 
- a function that returns stats for additions/deletions 
- Stats of lists 
- processing the time differences from seconds to d:h:m:s
- transformation of per_day to per_week
- percentage creation
- histogram creation and save
'''

def additions_deletions_stats(data):
    '''
    this function takes any file that has additions, deletions by language/type and returns a dataframe with all basic statistics
    count, mean, std, min, 25%, 50%, 75%, max
    It works with docummentation_commit() and commit_changes()
    '''
    
    initial_df = pd.DataFrame(data)
    lis= []
    col = []

    for item in list(initial_df.columns):
        name = str(item)
        item = initial_df[item]
        for index in list(initial_df.index):
            name_new = name  +'_'+ str(index)
            new = item[index]
            if str(new) == 'nan':
                continue
            elif bool(new):               
                lis.append(new)
                col.append(name_new)
    #leanedList = [x for x in lis if str(x) != 'nan']
    #print(lis)
  
    df_support = pd.DataFrame(lis)
    transposed_df = df_support.transpose()
    df= pd.DataFrame(transposed_df.values, columns=col)
    if df.empty:
        final_df = df
    else:
        final_df=df.describe()
    return final_df

def list_stats(data, data_name):
    '''
    Input
    data: list of lists with the data to be analysed. eg. data = [[1,2,3],[4,5,6]]
    data_name: a list of names for the data to be analysed. eg. data_name = ['random1','random2']
    both lists should have the same length

    Output
    stats: a dataframe with column names the data_name and index the count, mean, std, min, 25%, 50%, 75%, max of each of the 
    data lists
    '''
    series_list = []
    for item in range(len(data)):
        # print(item)
        # print(data[item])
        series = pd.Series(data[item], name=data_name[item])
        series_list.append(series)
    x = pd.concat(series_list, axis = 1)
    stats = x.describe()

    return stats

def time_diff(data):
    '''
    Takes the data in seconds and returns a dataframe with the mean, std, min, max, 25%, 50% and 75% of the time differences
    both in seconds and in Days:hours:minutes:seconds (for easier reading) 
    '''
    s = pd.DataFrame(data, columns=['Seconds'])
    describe = s.describe()
    to_series = pd.Series(describe['Seconds'])
    transform = to_series.apply(lambda x: to_day_hour_min_sec(x))
    describe['Days:Hours:Minutes:Seconds'] = pd.Series(transform, index=describe.index)
    describe = describe.drop(['count'])
    return describe

def to_day_hour_min_sec(seconds):
    '''
    Takes seconds and transdorms them to Days:hours:minutes:seconds
    '''
    try:
        y =("%d:%d:%d:%d" %(timedelta(seconds=seconds).days, (datetime(1,1,1) + timedelta(seconds=seconds)).hour, (datetime(1,1,1) + timedelta(seconds=seconds)).minute, (datetime(1,1,1) + timedelta(seconds=seconds)).second))
    except:
        y = 'NaN'
    return y


def activities_per_week(data):
    '''
    Data should be a dictionary of date,activity - key, value pairs
    '''
    per_week = {}
    list_per_week = []
    for key in data.keys():
        date_str= datetime.strptime(key, '%Y-%m-%d')        
        year,week= datetime.date(date_str).isocalendar()[:2]
        year_week = str(year) + "_" + str(week)
        if year_week in per_week.keys():   
            per_week[year_week] = per_week[year_week] + data[key]        
        else:
            per_week[year_week] = data[key]
    
    for key in per_week.keys():
        list_per_week.append(per_week[key])

    return per_week, list_per_week

def percentage_creation(data, divided_by):
    try:
        percentage = (data/divided_by)*100
    except ZeroDivisionError:
        percentage = 'NaN'
    return percentage

def histogram_creation(data, bins, xlabel, ylabel, title, datafolderpath):
    plt.hist(data, bins, facecolor='#274e13', rwidth=0.9)
    plt.grid(axis='y', alpha=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(datafolderpath +"/"+ title+".png")

