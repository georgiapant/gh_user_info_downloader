import pandas as pd
from datetime import datetime, timedelta, date
import time

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
        y =("%d:%d:%d:%d" %((datetime(1,1,1) + timedelta(seconds=seconds)).day-1, (datetime(1,1,1) + timedelta(seconds=seconds)).hour, (datetime(1,1,1) + timedelta(seconds=seconds)).minute, (datetime(1,1,1) + timedelta(seconds=seconds)).second))
    except:
        y = 'NaN'
    return y


def activities_per_week(data):
    '''
    Data should be a dictionary of date,activity - key, value pairs
    '''
    per_week = {}
    for key in data.keys():
        date_str= datetime.strptime(key, '%Y-%m-%d')        
        year,week= datetime.date(date_str).isocalendar()[:2]
        year_week = str(year) + "_" + str(week)
        if year_week in per_week.keys():   
            per_week[year_week] = per_week[year_week] + data[key]        
        else:
            per_week[year_week] = data[key]
    return per_week


#TESTING
'''
from datasetcreator.productivity import Productivity
from datamanager.filemanager import FileManager
from properties import GitHubAuthToken
import calendar
from collections import Counter

pr = Productivity(GitHubAuthToken)
fm = FileManager()
dataFolderPath = '/Users/georgia/Desktop'
user_name = 'nbriz'

commit_committed = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_committed","sha")
commit_authored=fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
issues_authored= fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")
issues_assigned = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_assigned", "id")
issue_comments = fm.read_comment_jsons_from_folder(dataFolderPath+ "/" + user_name + "/issue_comments")
commit_authored_comments = fm.read_comment_jsons_from_folder(dataFolderPath+ "/" + user_name + "/commit_comments")


data1, data2, data3, data4= pr.issue_commits_activities_freq(user_name, commit_committed, commit_authored, issues_authored, issue_comments, commit_authored_comments)[1]
activities_per_day = pr.issue_commits_activities_freq(user_name, commit_committed, commit_authored, issues_authored, issue_comments, commit_authored_comments)[2]
total_list = []
total_list.extend((data1,data2,data2, data4))
names = ["issues", "commits","comments", "total_activities"]

days_contrib = pr.contribution_days(dataFolderPath, user_name, commit_committed, commit_authored, issues_authored, issues_assigned, issue_comments, commit_authored_comments)
x = list_stats(total_list, names)
# print(x)
days_contriburion = {}
weekday = []
for key in activities_per_day.keys():
    date = datetime.strptime(key,'%Y-%m-%d')
    weekday.append(calendar.day_name[date.weekday()])

days_contriburion["total_days_worked"] = len(weekday)
weekday = Counter(weekday)

for item in weekday.keys():
    days_contriburion[item] = weekday[item]



user_dataset = {}

user_dataset["commits_frequency"] = x['commits'].to_dict()
user_dataset["issues_frequency"] = x['issues'].to_dict()
user_dataset["comments"] = x['comments'].to_dict()
user_dataset["activities_frequency"] = x['total_activities'].to_dict()

user_dataset["days_contrib_old"] = days_contrib
user_dataset["days_contribution"] = days_contriburion

fm.write_json_to_file(dataFolderPath + "/" + user_name +"/TESTTTTTTT.json", user_dataset) 
'''