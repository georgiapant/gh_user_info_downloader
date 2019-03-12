from datamanager.filemanager import FileManager
from analysis import histogram_creation
import pandas as pd
import numpy as np

'''
Which histograms do I want to create?
- percentage amount of testing files
- percentage amount of files committed per language
- percentage of repos contributed
- percentage bug word in commit message
- percentage comments with test keyword
- percentage comments with documentation keyword
- percentage comments with issue number
- percentage comments with project mgmt keyword
- percentage of bugs assigned by the user
- percentage of labels assigned by the user
- percentage of issues with milestone/total issues
- percentage of issues with milestone assigned by the user/total issues
- percentage of issues with milestone assigned by the user/issues with milestones
- percentage of open issues created by the user/total issues
- percentage of issues created by the user and closed by the user/ total issues
- percentage of issues assigned to the user that are still open
- percentage of issues assigned to the user that were closed by other user
- percentage of bugs closed by the user/ total amount of bugs
- percentage of pull requests done by the user that were merged
- percentage of pull requests done by the user that were closed but not merged
- percentage of pull requests done by the user that are still open
- percentage of activities per day of the week

- projects per week - per day
- bugs resolved per week - per day
- issues per week
- commits per week
- comments per week
- activities per week

- amount of files changed in a commit (mean)
- comment length (mean)
- number of comment answers (mean)


- project popularity stats - forks (mean)
- project popularity stats - stars (mean)
- project popularity stats - watchers (mean)

- project scale stats - commits (mean)
- project scale stats - contributors (mean)
- project scale stats - releases (mean)



- issue_assigned_to_user_and_closed_by_user_time_diff - check seconds (mean)
- issue_created_by_user_closed_by_user_time_diff - check seconds (mean)
- time_diff_between_consequtive_commiits_committed_by_user - check seconds (mean)
- pull merge time diff
'''

dataFolderPath = '/Users/georgia/Desktop/Thesis/DataUser/datasets'
fm = FileManager()
stats = fm.read_stats_jsons_from_folder(dataFolderPath)


#percentage histograms
df_percentage = pd.DataFrame.from_dict({(i): stats[i]["normalised"] for i in stats.keys()}, orient='index')

for column in df_percentage:
    break
    
    x = np.nanpercentile(df_percentage[column],98)
    range_x = (df_percentage[column].min(),x)
    histogram_creation(df_percentage[column], 20,range_x, column,"#users", column, dataFolderPath+"/histograms")
    # print(column)
    

print("normalised done")
#mean values histograms    

df_mean = pd.DataFrame.from_dict({(j,i): stats[i]["described"][j] for i in stats.keys() for j in stats[i]["described"].keys() }, orient='columns')

for column in df_mean:
    break
    data = df_mean[column[0]].transpose()["mean"]
    x = np.nanpercentile(data,98)
    range_x = (data.min(),x)
    histogram_creation(data, 20, range_x, column[0],"#users", column[0], dataFolderPath+"/histograms")
    

print("described done")

#to do histograms for project popularity and scale stats
df_project = pd.DataFrame.from_dict({(k,j,i): stats[i]["project_preference_info"][k][j] for i in stats.keys() for k in stats[i]["project_preference_info"].keys() for j in stats[i]["project_preference_info"][k].keys()}, orient='index')

for i in df_project.index.levels[0]:
    break
    for j in df_project.index.levels[1]:
        try:
            
            data = df_project.transpose()[i][j].transpose()
            # print(data)
            x = np.nanpercentile(data["mean"],98)
            range_x = (data["mean"].min(),x)
            histogram_creation(data["mean"], 20, range_x, j,"#users", i, dataFolderPath+"/histograms")

        except:
            continue
print("project preferences done") 

#histograms for time differences
df_time_diff = pd.DataFrame.from_dict({(k,i): stats[i]["time_diff"][k]["Seconds"] for i in stats.keys() for k in stats[i]["time_diff"].keys()}, orient='index')

for i in df_time_diff.index.levels[0]:
    break
    try:
        
        data = df_time_diff.transpose()[i].transpose()
        x = np.nanpercentile(data["mean"],95)
        range_x = (data["mean"].min(),x)
        #histogram_creation(data["mean"], 20, range_x, "mean_seconds","#users", i, dataFolderPath+"/histograms")
        histogram_creation(data["mean"], 20, range_x, i,"#users", i, dataFolderPath+"/histograms")

    except:
        continue
print("time diff done")
# fm.write_json_to_file(dataFolderPath + "/STATS.json", stats) 