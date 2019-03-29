from datamanager.filemanager import FileManager
from properties import dataFolderPath
import pandas as pd
import numpy as np
import os

# dataFolderPath = '/Users/georgia/Desktop/Thesis/DataUser/datasets'
fm = FileManager()

def set_ascending(data):
    '''
    Function that sets an ascending profile to the metric
    Ascending profile means the higher the value the better
    '''
    score = []
    for item in ["Good", "Medium", "Bad"]:
        profile = {}
        if item== "Bad":
            low_thres = data.min()
            high_thres = np.nanpercentile(data,33)
        elif item =="Medium":
            low_thres = np.nanpercentile(data,33)
            high_thres = np.nanpercentile(data,66)
        else:
            low_thres = np.nanpercentile(data,66)
            high_thres = np.nanpercentile(data,98)
    
        profile["Name"] = item
        profile["Lower_threshold"] = low_thres
        profile["Higher_threshold"] = high_thres
        score.append(profile)
    return score

def set_descending(data):
    '''
    Function that sets an descending profile to the metric
    Ascending profile means the lowner the value the better
    '''
    score = []
    for item in ["Good", "Medium", "Bad"]:
        profile = {}
        if item== "Good":
            low_thres = data.min()
            high_thres = np.nanpercentile(data,33)
        elif item =="Medium":
            low_thres = np.nanpercentile(data,33)
            high_thres = np.nanpercentile(data,66)
        else:
            low_thres = np.nanpercentile(data,66)
            high_thres = np.nanpercentile(data,98)
    
        profile["Name"] = item
        profile["Lower_threshold"] = low_thres
        profile["Higher_threshold"] = high_thres
        score.append(profile)
    return score

def set_middle(data):
    '''
    Function that sets an middle peak profile to the metric
    Ascending profile means the more medium the value the better
    '''
    score = []
    for item in ["good", "bad_low", "bad_high"]:
        profile = {}
        if item== "bad_low":
            low_thres = data.min()
            high_thres = np.nanpercentile(data,33)
        elif item =="good":
            low_thres = np.nanpercentile(data,33)
            high_thres = np.nanpercentile(data,66)
        else:
            low_thres = np.nanpercentile(data,66)
            high_thres = np.nanpercentile(data,98)
    
        profile["Name"] = item
        profile["Lower_threshold"] = low_thres
        profile["Higher_threshold"] = high_thres
        score.append(profile)
    return score

def set_ascending_normalised(data):
    '''
    Function that sets an ascending profile to the metric
    Ascending profile means the higher the value the better
    '''
    score = []
    for item in ["Good", "Medium", "Bad"]:
        profile = {}
        if item== "Bad":
            low_thres = (data.min()/(np.nanpercentile(data,98)-data.min()))*100
            high_thres = (np.nanpercentile(data,33)/(np.nanpercentile(data,98)-data.min()))*100
        elif item =="Medium":
            low_thres = (np.nanpercentile(data,33)/(np.nanpercentile(data,98)-data.min()))*100
            high_thres = (np.nanpercentile(data,66)/(np.nanpercentile(data,98)-data.min()))*100
        else:
            low_thres = (np.nanpercentile(data,66)/(np.nanpercentile(data,98)-data.min()))*100
            high_thres = (np.nanpercentile(data,98)/(np.nanpercentile(data,98)-data.min()))*100
    
        profile["Name"] = item
        profile["Lower_threshold"] = low_thres
        profile["Higher_threshold"] = high_thres
        score.append(profile)
    return score

def set_descending_normalised(data):
    '''
    Function that sets an descending profile to the metric
    Ascending profile means the lowner the value the better
    '''
    score = []
    for item in ["Good", "Medium", "Bad"]:
        profile = {}
        if item== "Good":
            low_thres = (data.min()/(np.nanpercentile(data,98)-data.min()))*100
            high_thres = (np.nanpercentile(data,33)/(np.nanpercentile(data,98)-data.min()))*100
        elif item =="Medium":
            low_thres = (np.nanpercentile(data,33)/(np.nanpercentile(data,98)-data.min()))*100
            high_thres = (np.nanpercentile(data,66)/(np.nanpercentile(data,98)-data.min()))*100
        else:
            low_thres = (np.nanpercentile(data,66)/(np.nanpercentile(data,98)-data.min()))*100
            high_thres = (np.nanpercentile(data,98)/(np.nanpercentile(data,98)-data.min()))*100
    
        profile["Name"] = item
        profile["Lower_threshold"] = low_thres
        profile["Higher_threshold"] = high_thres
        score.append(profile)
    return score

def set_middle_normalised(data):
    '''
    Function that sets an middle peak profile to the metric
    Ascending profile means the more medium the value the better
    '''
    score = []
    for item in ["good", "bad_low", "bad_high"]:
        profile = {}
        if item== "bad_low":
            low_thres = (data.min()/(np.nanpercentile(data,98)-data.min()))*100
            high_thres = (np.nanpercentile(data,33)/(np.nanpercentile(data,98)-data.min()))*100
        elif item =="good":
            low_thres = (np.nanpercentile(data,33)/(np.nanpercentile(data,98)-data.min()))*100
            high_thres = (np.nanpercentile(data,66)/(np.nanpercentile(data,98)-data.min()))*100
        else:
            low_thres = (np.nanpercentile(data,66)/(np.nanpercentile(data,98)-data.min()))*100
            high_thres = (np.nanpercentile(data,98)/(np.nanpercentile(data,98)-data.min()))*100
    
        profile["Name"] = item
        profile["Lower_threshold"] = low_thres
        profile["Higher_threshold"] = high_thres
        score.append(profile)
    return score

def create_model(dataFolderPath):
    stats = fm.read_stats_jsons_from_folder(os.path.join(dataFolderPath,"datasets"))
    model = fm.read_json_from_file(os.path.join(dataFolderPath,"datasets","model","model_profiles.json"))
    
    #model creation for normalised statistics
    df_percentage = pd.DataFrame.from_dict({(i): stats[i]["normalised"] for i in stats.keys()}, orient='index')
    for column in df_percentage:
        
        for i in model:
            if i["Name"] == column:
                if i["Profile"]== "Ascending":
                    score = set_ascending(df_percentage[column])
                    score_normalised = set_ascending_normalised(df_percentage[column])
                elif i["Profile"] =="Descending":
                    score = set_descending(df_percentage[column])
                    score_normalised = set_descending_normalised(df_percentage[column])
                elif i["Profile"]  == "Middle":
                    score = set_middle(df_percentage[column])
                    score_normalised = set_middle_normalised(df_percentage[column])
                else:
                    continue
                i["Score_instructions"] = score
                i["Score_instructions_normalised"] = score_normalised
                i["Score_min"] = df_percentage[column].min()
                i["Score_max"] = np.nanpercentile(df_percentage[column],98) 
                break
     
    #profiles for described metrics   
    df_mean = pd.DataFrame.from_dict({(j,i): stats[i]["described"][j] for i in stats.keys() for j in stats[i]["described"].keys() }, orient='columns')
    for column in df_mean:    
        data = df_mean[column[0]].transpose()["mean"]
        # print(data)
        for i in model:
            if i["Name"] == column[0]:
                # print("yoo")
                if i["Profile"]== "Ascending":
                    score = set_ascending(data)
                    score_normalised = set_ascending_normalised(data)
                elif i["Profile"] =="Descending":
                    score = set_descending(data)
                    score_normalised = set_descending_normalised(data)
                elif i["Profile"]  == "Middle":
                    score = set_middle(data)
                    score_normalised = set_middle_normalised(data)
                else:
                    continue
                i["Score_instructions"] = score
                i["Score_instructions_normalised"] = score_normalised
                i["Score_min"] = data.min()
                i["Score_max"] = np.nanpercentile(data,98) 
                break
        
    
    '''
    df_project = pd.DataFrame.from_dict({(k,j,i): stats[i]["project_preference_info"][k][j] for i in stats.keys() for k in stats[i]["project_preference_info"].keys() for j in stats[i]["project_preference_info"][k].keys()}, orient='index')
    
    for i in df_project.index.levels[0]:
        for j in df_project.index.levels[1]:
            try:    
                data = df_project.transpose()[i][j].transpose()
                
                for item in model:
                    if item["Name"] == "project_preferences_" +j:
                        if item["Profile"]== "Ascending":
                            score = set_ascending(data["mean"])
                        elif item["Profile"] =="Descending":
                            score = set_descending(data["mean"])
                        elif i["Profile"]  == "Middle":
                            score = set_middle(data["mean"])
                        else:
                            continue
                        item["Score_instructions"] = score
                        item["Score_min"] = data["mean"].min()
                        item["Score_max"] = np.nanpercentile(data["mean"],98) 
                        break
            except:
                continue
    '''    
        
    df_time_diff = pd.DataFrame.from_dict({(k,i): stats[i]["time_diff"][k]["Seconds"] for i in stats.keys() for k in stats[i]["time_diff"].keys()}, orient='index')
    for i in df_time_diff.index.levels[0]:
        # print(i)
        try:
            data = df_time_diff.transpose()[i].transpose()
            for item in model:
                if item["Name"] == i:
                    if item["Profile"]== "Ascending":
                        score = set_ascending(data["mean"])
                        score_normalised = set_ascending_normalised(data["mean"])
                    elif item["Profile"] =="Descending":
                        score = set_descending(data["mean"])
                        score_normalised = set_descending_normalised(data["mean"])
                    elif i["Profile"]  == "Middle":
                        score = set_middle(data["mean"])
                        score_normalised = set_middle_normalised(data["mean"])
                    else:
                        continue
                    item["Score_instructions"] = score
                    item["Score_instructions_normalised"] = score_normalised
                    item["Score_min"] = data["mean"].min()
                    item["Score_max"] = np.nanpercentile(data["mean"],98)
                    break
        except:
            continue
    
    return model

model = create_model(dataFolderPath)
fm.write_json_to_file(os.path.join(dataFolderPath,"datasets","model","model_normalised.json"), model)

