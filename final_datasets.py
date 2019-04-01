from properties import dataFolderPath
from datamanager.filemanager import FileManager
import pandas as pd
import numpy as np
import math
import json
import os


def set_score(score_instructions, value):
    highest_threshold = -1
    lowest_threshold = float('inf')
    
    for item in score_instructions:
        
        if item["Name"]=='No categories':
            score = "Undefined"
            break
        else:
            if math.isnan(value):
                score = "Undefined"
                break
            
            elif value <= item["Higher_threshold"] and value > item["Lower_threshold"]:
                score = item["Name"]
                break
            else:
                #To cover the posibility of the value being higher than the highest threshold or lower than the lowest
                if item["Higher_threshold"]> highest_threshold:
                    highest_threshold = item["Higher_threshold"]                    
                    if value > highest_threshold:
                        score = item["Name"]

                if item["Lower_threshold"]< lowest_threshold:
                    lowest_threshold = item["Lower_threshold"]
                    if value < lowest_threshold:
                        score = item["Name"]
                        
            continue              
 
    return score

def create_final_datasets(dataFolderPath):
    '''
    This function creates the final dataset of a user. 
    This dataset includes all metrics divited in two clasters. The classified, which are the ones that have limits based on 
    benchmarking and the unclassified, which are the ones that haven't been benchmarked.
    
    The dataset also includes the final performance grade per category. In order for the grade to be between 0 and 100 all 
    benchmarked values were additionally normalised with a simple rule. Normalised value equals the initial value 
    divided by the difference between maximum and minimum value of all the users [normalised = initial_value/(max-min)] and 
    then it is multiplied by 100. 

    Finally if the value is larger than the maximum value of all users, the normalised value is set as 100 which is the maximum.
    '''


    fm = FileManager()
    stats = fm.read_stats_jsons_from_folder(os.path.join(dataFolderPath,"datasets"))
    model = fm.read_json_from_file(os.path.join(dataFolderPath,"datasets","model","model.json"))

    
    for user in stats.keys():
        user_dataset = {}
        user_dataset["name"] = user.split('_')[::-1][1]
        user_dataset["metrics_classified"]=[]
        user_dataset["metrics_unclassified"] = []
        user_dataset["performance_scores"] = {}


        for key in stats[user]:
            for item in model:
                if item["Name"] == key:
                    metric = {}
                    metric["Name"]= key
                    metric["Category"] = item["Category"]
                    metric["Value"]= stats[user][key]
                    
                    if item["Profile"] == "Unclassified":
                        user_dataset["metrics_unclassified"].append(metric)
                    else:
                        if metric["Value"]>item["Score_max"]:
                            metric["Value_normalised"] = 100 #to include the possibility of the current value being outside of the upper limit of the initial benchamarking dataset
                        else:
                            metric["Value_normalised"]= ((stats[user][key]-item["Score_min"])/(item["Score_max"]-item["Score_min"]))*100
                        metric["Score"] = set_score(item["Score_instructions"],metric["Value"])
                        metric["Profile"] = item["Profile"]
                        user_dataset["metrics_classified"].append(metric)
        
        for key in stats[user]["normalised"]:
            for item in model:
                if item["Name"] == key:
                    metric = {}
                    metric["Name"]= key
                    metric["Category"] = item["Category"]
                    metric["Value"]= stats[user]["normalised"][key]
                    
                    if item["Profile"] == "Unclassified":
                        user_dataset["metrics_unclassified"].append(metric)
                    else:
                        if metric["Value"]>item["Score_max"]:
                            metric["Value_normalised"] = 100 #to include the possibility of the current value being outside of the upper limit of the initial benchamarking dataset
                        else:
                            try:
                                metric["Value_normalised"] = ((stats[user]["normalised"][key]-item["Score_min"])/(item["Score_max"]-item["Score_min"]))*100
                            except:
                                metric["Value_normalised"] =  float('nan')
                        metric["Score"] = set_score(item["Score_instructions"],metric["Value"])
                        metric["Profile"] = item["Profile"]
                        user_dataset["metrics_classified"].append(metric)

        for key in stats[user]["described"]:
            for item in model:
                if item["Name"] == key:
                    metric = {}
                    metric["Name"]= key
                    metric["Category"] = item["Category"]
                    metric["Value"]= stats[user]["described"][key]["mean"]
                    if item["Profile"] == "Unclassified":
                        user_dataset["metrics_unclassified"].append(metric)
                    else:
                        if metric["Value"]>item["Score_max"]: #to include the possibility of the current value being outside of the upper limit of the initial benchamarking dataset 
                            metric["Value_normalised"] = 100
                        else:
                            metric["Value_normalised"]= ((stats[user]["described"][key]["mean"]-item["Score_min"])/(item["Score_max"]-item["Score_min"]))*100
                        metric["Score"] = set_score(item["Score_instructions"],metric["Value"])
                        metric["Profile"] = item["Profile"]
                        user_dataset["metrics_classified"].append(metric)

        for key in stats[user]["time_diff"]:
            for item in model:
                if item["Name"] == key:
                    metric = {}
                    metric["Name"]= key
                    metric["Category"] = item["Category"]        
                    try:
                        metric["Value"]= stats[user]["time_diff"][key]["Seconds"]["mean"]
                        if metric["Value"]>item["Score_max"]:
                            metric["Value_normalised"] = 100 #to include the possibility of the current value being outside of the upper limit of the initial benchamarking dataset
                        else:
                            metric["Value_normalised"]= ((stats[user]["time_diff"][key]["Seconds"]["mean"]-item["Score_min"])/(item["Score_max"]-item["Score_min"]))*100
                    except:
                        metric["Value"] = float('nan')

                    if item["Profile"] == "Unclassified":
                        user_dataset["metrics_unclassified"].append(metric)
                    else:
                        metric["Score"] = set_score(item["Score_instructions"],metric["Value"])
                        metric["Profile"] = item["Profile"]
                        user_dataset["metrics_classified"].append(metric)
        
        for key in stats[user]["raw_data"]:
            for item in model:
                if item["Name"] == key:
                    metric = {}
                    metric["Name"]= key
                    metric["Category"] = item["Category"]
                    metric["Value"]= stats[user]["raw_data"][key]
                    if item["Profile"] == "Unclassified":
                        user_dataset["metrics_unclassified"].append(metric)
                    else:
                        if metric["Value"]>item["Score_max"]:
                            metric["Value_normalised"] = 100 #to include the possibility of the current value being outside of the upper limit of the initial benchamarking dataset
                        else:
                            metric["Value_normalised"]= ((stats[user]["raw_data"][key]-item["Score_min"])/(item["Score_max"]-item["Score_min"]))*100
                        metric["Score"] = set_score(item["Score_instructions"],metric["Value"])
                        metric["Profile"] = item["Profile"]
                        user_dataset["metrics_classified"].append(metric)

        #from here i include the performance scores
        
        for item in user_dataset["metrics_classified"]:            
            for metric in model:
                if item["Name"]==metric["Name"]:

                    if item["Score"]== "Undefined": #to count nan as 0 for the general score
                        score_initial = 0
                    else:
                        if item["Profile"] == "Ascending":
                            score_initial =  item["Value_normalised"]
                            
                        elif item["Profile"] == "Descending":
                            score_initial =  100 - item["Value_normalised"]
                            
                        elif item["Profile"] == "Middle":
                            score_initial = 100 - 2* abs(50 - item["Value_normalised"])
                        
                    try:
                        user_dataset["performance_scores"][item["Category"]] = (user_dataset["performance_scores"][item["Category"]]+ score_initial)/2
                    except:    #initialise the category 
                        user_dataset["performance_scores"][item["Category"]] = score_initial
        
        
        fm.write_json_to_file(os.path.join(dataFolderPath,"datasets","final_datasets", str(user)+ "_final_dataset.json"), user_dataset)
        

create_final_datasets(dataFolderPath)             
