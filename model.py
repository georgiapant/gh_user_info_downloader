from datamanager.filemanager import FileManager
from properties import dataFolderPath
import pandas as pd
import numpy as np
import os
import re

# dataFolderPath = '/Users/georgia/Desktop/Thesis/DataUser/datasets'
fm = FileManager()

def remove_outliers(data, percentile):
    new_data = []
    limit = np.nanpercentile(data,percentile)

    for item in data:
        if item <= limit:
            new_data.append(item)
    
    return new_data

def normalise_data(data):
    data_normalised = []
    new_data_df = pd.DataFrame(data)   
  
    for item in data:
        x = ((item - new_data_df.min())/(new_data_df.max()-new_data_df.min()))*100
        data_normalised.append(x[0])
    return data_normalised



def set_ascending(data):
    '''
    Function that sets an ascending profile to the metric
    Ascending profile means the higher the value the better
    '''
    score = []

    try:
        categories = pd.qcut(data, 3, duplicates='drop')
        
        # print(len(categories.categories))
        if len(categories.categories)==3:
            for item in ["Good", "Medium", "Bad"]:
                
                profile = {}
                
                if item== "Bad":
                    thresholds = categories.categories[0]
                elif item =="Medium":
                    thresholds = categories.categories[1]
                else:
                    thresholds = categories.categories[2]
                
                left, right = str(thresholds).split(',')[::1]
                low_thres= re.findall(r"[-+]?\d*\.\d+|\d+", left)
                high_thres = re.findall(r"[-+]?\d*\.\d+|\d+", right)
                
                profile["Name"] = item
                profile["Lower_threshold"] = float(low_thres[0])
                profile["Higher_threshold"] = float(high_thres[0])
                score.append(profile)
            
        elif len(categories.categories)==2:
            for item in ["Good", "Bad"]:
                
                profile = {}
                
                if item== "Bad":
                    thresholds = categories.categories[0]    
                elif item =="Good":
                    thresholds = categories.categories[1]
                
            
                left, right = str(thresholds).split(',')[::1]
                low_thres= re.findall(r"[-+]?\d*\.\d+|\d+", left)
                high_thres = re.findall(r"[-+]?\d*\.\d+|\d+", right)
                
                profile["Name"] = item
                profile["Lower_threshold"] = float(low_thres[0])
                profile["Higher_threshold"] = float(high_thres[0])
                score.append(profile)
        else:
            profile["Name"] = "No categories"
            profile["Lower_threshold"] = float('nan')
            profile["Higher_threshold"] = float('nan')
    except:
        profile = {}
        profile["Name"] = "No categories"
        profile["Lower_threshold"] = float('nan')
        profile["Higher_threshold"] = float('nan')
    
        score.append(profile)    
    
    return score

def set_descending(data):
    '''
    Function that sets an descending profile to the metric
    Ascending profile means the lowner the value the better
    '''
    score = []
    try:
        categories = pd.qcut(data, 3, duplicates='drop')
        

        if len(categories.categories)==3:
            for item in ["Good", "Medium", "Bad"]:
                
                profile = {}
                
                if item== "Good":
                    thresholds = categories.categories[0]    
                elif item =="Medium":
                    thresholds = categories.categories[1]
                else:
                    thresholds = categories.categories[2]
            
                left, right = str(thresholds).split(',')[::1]
                low_thres= re.findall(r"[-+]?\d*\.\d+|\d+", left)
                high_thres = re.findall(r"[-+]?\d*\.\d+|\d+", right)
                
                profile["Name"] = item
                profile["Lower_threshold"] = float(low_thres[0])
                profile["Higher_threshold"] = float(high_thres[0])
                score.append(profile)
            
        elif len(categories.categories)==2:
            for item in ["Good", "Bad"]:
                
                profile = {}
                
                if item== "Good":
                    thresholds = categories.categories[0]    
                elif item =="Bad":
                    thresholds = categories.categories[1]
                
            
                left, right = str(thresholds).split(',')[::1]
                low_thres= re.findall(r"[-+]?\d*\.\d+|\d+", left)
                high_thres = re.findall(r"[-+]?\d*\.\d+|\d+", right)
                
                profile["Name"] = item
                profile["Lower_threshold"] = float(low_thres[0])
                profile["Higher_threshold"] = float(high_thres[0])
                score.append(profile)
        else:
            profile["Name"] = "No categories"
            profile["Lower_threshold"] = float('nan')
            profile["Higher_threshold"] = float('nan')
    except:

        profile = {}
       
        profile["Name"] = "No categories"
        profile["Lower_threshold"] = float('nan')
        profile["Higher_threshold"] = float('nan')
    
        score.append(profile)

    # score.append(profile)    
    
    return score

def set_middle(data):
    '''
    Function that sets an middle peak profile to the metric
    Ascending profile means the more medium the value the better
    '''
    score = []

    try:
        categories = pd.qcut(data, 3, duplicates='drop')
        
        if len(categories.categories)==3:
            for item in ["good", "bad_low", "bad_high"]:
                
                profile = {}
                
                if item== "bad_low":
                    thresholds = categories.categories[0]    
                elif item =="good":
                    thresholds = categories.categories[1]
                else:
                    thresholds = categories.categories[2]
                    
            
                left, right = str(thresholds).split(',')[::1]
                low_thres= re.findall(r"[-+]?\d*\.\d+|\d+", left)
                high_thres = re.findall(r"[-+]?\d*\.\d+|\d+", right)
                
                profile["Name"] = item
                profile["Lower_threshold"] = float(low_thres[0])
                profile["Higher_threshold"] = float(high_thres[0])
                score.append(profile)
            
        elif len(categories.categories)==2:
            for item in ["Goodish", "Badish"]:
                
                profile = {}
                
                if item== "Goodish":
                    thresholds = categories.categories[0]    
                elif item =="Badish":
                    thresholds = categories.categories[1]
                
                left, right = str(thresholds).split(',')[::1]
                low_thres= re.findall(r"[-+]?\d*\.\d+|\d+", left)
                high_thres = re.findall(r"[-+]?\d*\.\d+|\d+", right)
                
                profile["Name"] = item
                profile["Lower_threshold"] = float(low_thres[0])
                profile["Higher_threshold"] = float(high_thres[0])
                score.append(profile)
        else:
            profile["Name"] = "No categories"
            profile["Lower_threshold"] = float('nan')
            profile["Higher_threshold"] = float('nan')
    except:
        profile = {}
        profile["Name"] = "No categories"
        profile["Lower_threshold"] = float('nan')
        profile["Higher_threshold"] = float('nan')
    

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

                data = remove_outliers(df_percentage[column],98)
                data_normalised = normalise_data(data)

                if i["Profile"]== "Ascending":
                    score = set_ascending(data)
                    score_normalised = set_ascending(data_normalised)
                elif i["Profile"] =="Descending":
                    score = set_descending(data)
                    score_normalised = set_descending(data_normalised)
                elif i["Profile"]  == "Middle":
                    score = set_middle(data)
                    score_normalised = set_middle(data_normalised)
                else:
                    continue
                i["Score_instructions"] = score
                i["Score_instructions_normalised"] = score_normalised

                new_data_df = pd.DataFrame(data)
                i["Score_min"] = float(new_data_df.min())
                i["Score_max"] = float(new_data_df.max())

                break
     
    #profiles for described metrics   
    df_mean = pd.DataFrame.from_dict({(j,i): stats[i]["described"][j] for i in stats.keys() for j in stats[i]["described"].keys() }, orient='columns')
    for column in df_mean:    
        data_init = df_mean[column[0]].transpose()["mean"]
        
        for i in model:
            if i["Name"] == column[0]:
                
                data = remove_outliers(data_init,98)
                data_normalised = normalise_data(data)

                if i["Profile"]== "Ascending":
                    score = set_ascending(data)
                    score_normalised = set_ascending(data_normalised)
                elif i["Profile"] =="Descending":
                    score = set_descending(data)
                    score_normalised = set_descending(data_normalised)
                elif i["Profile"]  == "Middle":
                    score = set_middle(data)
                    score_normalised = set_middle(data_normalised)
                else:
                    continue
                i["Score_instructions"] = score
                i["Score_instructions_normalised"] = score_normalised

                new_data_df = pd.DataFrame(data)
                i["Score_min"] = float(new_data_df.min())
                i["Score_max"] = float(new_data_df.max())

                break
    
        
    df_time_diff = pd.DataFrame.from_dict({(k,i): stats[i]["time_diff"][k]["Seconds"] for i in stats.keys() for k in stats[i]["time_diff"].keys()}, orient='index')
    for i in df_time_diff.index.levels[0]:

        try:
            data_init = list(df_time_diff.transpose()[i].transpose()["mean"])
            
            for item in model:
                if item["Name"] == i:
                    data = remove_outliers(data_init,98)
                    
                    data_normalised = normalise_data(data)
                    
                    if item["Profile"]== "Ascending":
                        score = set_ascending(data)
                        score_normalised = set_ascending(data_normalised)
                    elif item["Profile"] =="Descending":
                        score = set_descending(data)
                        score_normalised = set_descending(data_normalised)
                    elif item["Profile"]  == "Middle":
                        score = set_middle(data)
                        score_normalised = set_middle(data_normalised)
                    else:
                        continue
                    item["Score_instructions"] = score
                    item["Score_instructions_normalised"] = score_normalised

                    new_data_df = pd.DataFrame(data)
                    item["Score_min"] = float(new_data_df.min())
                    item["Score_max"] = float(new_data_df.max())
                    
                    break
        except:
            continue
    
    return model

model = create_model(dataFolderPath)
fm.write_json_to_file(os.path.join(dataFolderPath,"datasets","model","model.json"), model)

