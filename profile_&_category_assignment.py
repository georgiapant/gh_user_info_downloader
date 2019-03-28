from datamanager.filemanager import FileManager
from properties import dataFolderPath
import pandas as pd
import numpy as np
import json
import os

# dataFolderPath = '/Users/georgia/Desktop/Thesis/DataUser/datasets'
fm = FileManager()
stats = fm.read_stats_jsons_from_folder(os.path.join(dataFolderPath,"datasets"))

profile_choices = {"A": "Ascending", "D":"Descending", "M":"Middle", "U":"Unclassified", "E":"Not Included"}
category_choices = {"A":"Main_Page", "B":"Productivity", "C":"Dev_Productivity", "D":"Ops_Productivity","E":"Project_Management", "F":"Quality&Testing"}
'''
Ascending profile: The higher the better
Descending profile: The lower the better
Middle profile: Either extreme is bad
Unclassified: It is included in the final json but doesnt have a profile
Not Included: It is not included in the final json
'''
model = []

#profiles for normalised metrics
df_percentage = pd.DataFrame.from_dict({(i): stats[i]["normalised"] for i in stats.keys()}, orient='index')

for column in df_percentage:
    
    profile_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(column) + ".\n\033[1;0;40mThe choices are: "+ str(profile_choices)+"\n")
    p_ch = profile_choice.upper()
    if p_ch == "E":
        continue
    else: 
        metric = {}
        metric["Name"] = column

        
        metric["Profile"] = profile_choices[p_ch]

        category_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(column) + ".\n\033[1;0;40mThe choices are: "+ str(category_choices)+"\n")
        c_ch = category_choice.upper()
        metric["Category"] = category_choices[c_ch]

        if p_ch == "U":
            model.append(metric)
            continue
        else:
            metric["Score_instructions"] = []
            model.append(metric)
    
print("\nProfiles of normalised metrics: DONE\n")

#profiles for described metrics   
df_mean = pd.DataFrame.from_dict({(j,i): stats[i]["described"][j] for i in stats.keys() for j in stats[i]["described"].keys() }, orient='columns')
names_of_metrics = set()

for column in df_mean.columns.values:
    names_of_metrics.add(column[0])

for item in names_of_metrics:
    profile_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(item) + ".\n\033[1;0;40mThe choices are: "+ str(profile_choices)+"\n")
    p_ch = profile_choice.upper()
    
    if p_ch == "E":
        continue
    else:  
        metric = {}
        metric["Name"] = item
        metric["Profile"] = profile_choices[p_ch]

        category_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(item) + ".\n\033[1;0;40mThe choices are: "+ str(category_choices)+"\n")
        c_ch = category_choice.upper()
        metric["Category"] = category_choices[c_ch]

        if p_ch == "U":
            model.append(metric)
            continue
        else:
            metric["Score_instructions"] = []
            model.append(metric)
        
    
print("\nProfiles of described metrics: DONE\n")

#profiles for metrics about project preferences
'''



df_project = pd.DataFrame.from_dict({(k,j,i): stats[i]["project_preference_info"][k][j] for i in stats.keys() for k in stats[i]["project_preference_info"].keys() for j in stats[i]["project_preference_info"][k].keys()}, orient='index')

for j in df_project.index.levels[1]:
    try:
        profile_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(j) + ".\n\033[1;0;40mThe choices are: "+ str(profile_choices)+"\n")
        p_ch = profile_choice.upper()

        if p_ch == "E":
            continue
        else:    
            metric = {}
            metric["Name"] = "project_preferences_" +j

            
            metric["Profile"] = profile_choices[p_ch]

            category_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(j) + ".\n\033[1;0;40mThe choices are: "+ str(category_choices)+"\n")
            c_ch = category_choice.upper()
            metric["Category"] = category_choices[c_ch]

            if p_ch == "U":
                model.append(metric)
                continue
            else:
                metric["Score_instructions"] = []
                model.append(metric)
    except:
        continue
print("\nProfiles of project preferences metrics: DONE\n") 
'''

#profiles for metrics about time differences
df_time_diff = pd.DataFrame.from_dict({(k,i): stats[i]["time_diff"][k]["Seconds"] for i in stats.keys() for k in stats[i]["time_diff"].keys()}, orient='index')
for i in df_time_diff.index.levels[0]:
    try: 
        profile_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(i) + ".\n\033[1;0;40mThe choices are: "+ str(profile_choices)+"\n")
        p_ch = profile_choice.upper()   

        if p_ch == "E":
            continue
        else:    
            metric = {}
            metric["Name"] = i
            metric["Profile"] = profile_choices[p_ch]

            category_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(i) + ".\n\033[1;0;40mThe choices are: "+ str(category_choices)+"\n")
            c_ch = category_choice.upper()
            metric["Category"] = category_choices[c_ch]

            if p_ch == "U":
                model.append(metric)
                continue
            else:
                metric["Score_instructions"] = []
                model.append(metric)

    except:
        continue
print("\nProfiles of time differences metrics: DONE\n")

df_raw_data = pd.DataFrame.from_dict({(i): stats[i]["raw_data"] for i in stats.keys()}, orient='index')
for column in df_raw_data:

    profile_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(column) + ".\n\033[1;0;40mThe choices are: "+ str(profile_choices)+"\n")   
    p_ch = profile_choice.upper()
    
    if p_ch == "E":
        continue
    else:
        metric = {}
        metric["Name"] = column
        metric["Profile"] = profile_choices[p_ch]
        
        category_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(column) + ".\n\033[1;0;40mThe choices are: "+ str(category_choices)+"\n")
        c_ch = category_choice.upper()
        metric["Category"] = category_choices[c_ch]

        if p_ch == "U":
            model.append(metric)
            continue
        else:
            metric["Score_instructions"] = []
            model.append(metric)

print("\nProfiles of raw data: DONE\n")

df_basic_stats = pd.DataFrame.from_dict({(i): stats[i] for i in stats.keys()}, orient='index')

for column in df_basic_stats:
    
    profile_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(column) + ".\n\033[1;0;40mThe choices are: "+ str(profile_choices)+"\n")   
    p_ch = profile_choice.upper()
    
    if p_ch == "E":
        continue
    else:
        metric = {}
        metric["Name"] = column
        metric["Profile"] = profile_choices[p_ch]
        
        category_choice = input("\nChose profile of "+ "\033[1;32;40m"+ str(column) + ".\n\033[1;0;40mThe choices are: "+ str(category_choices)+"\n")
        c_ch = category_choice.upper()
        metric["Category"] = category_choices[c_ch]
        if p_ch == "U":
            model.append(metric)
            continue
        else:
            metric["Score_instructions"] = []
            model.append(metric)

print("\nProfiles of basic stats: DONE\n")    

fm.write_json_to_file(os.path.join(dataFolderPath,"datasets","model","model_profiles.json"), model)