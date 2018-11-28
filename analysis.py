import pandas as pd
from datetime import datetime
#import statistics 
from datasetcreator.commits import commit_changes
from datasetcreator.operational import documentation_commit
from datasetcreator.productivity import Productivity
from datamanager.filemanager import FileManager


user_name = 'nbriz'
dataFolderPath = '/Users/georgia/Desktop'


##################
#df = pd.DataFrame(data)
# example 
# CSS = df['CSS']
#additions = CSS['additions']
#deletions = CSS['deletions']
#df2 = pd.Series( (v for v in additions) )
#df3 = pd.Series( (v for v in deletions) )
#col_names = ['CSS additions', 'CSS deletions', 'nada']
#x = df2.describe()
#y = df3.describe()
#z = df3.describe()
#data_tuples = list(zip(x,y,z))
#new = pd.DataFrame(data_tuples, columns=col , index=list(x.index))
####################

#data = commit_changes(dataFolderPath, user_name)
#data1 = documentation_commit(dataFolderPath,user_name)[0]
#print(data)

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
    y =("%d:%d:%d:%d" %((datetime(1,1,1) + datetime.timedelta(seconds=seconds)).day-1, (datetime(1,1,1) + datetime.timedelta(seconds=seconds)).hour, (datetime(1,1,1) + datetime.timedelta(seconds=seconds)).minute, (datetime(1,1,1) + datetime.timedelta(seconds=seconds)).second))
    return y
    

pr = Productivity(dataFolderPath, user_name)
fm = FileManager()
x = pr.create_close_issue_diff(user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/new_create_close_issue_diff!!!!.json", x) 
#x = additions_deletions_stats(data)
#y = additions_deletions_stats(data1)
#z = x.join(y)
#print(list(x.columns))
#print(z)
#final_df.to_json() #transforms the dataframe to json. final_df.to_dict() does the same to dictionary


