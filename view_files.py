from properties import dataFolderPath
from datamanager.filemanager import FileManager
import json
import os
from analysis import to_day_hour_min_sec
import time
import calendar
import operator
from collections import OrderedDict


'''
Create the view files for the UI
'''

fm = FileManager()
datasets = fm.read_stats_jsons_from_folder(os.path.join(dataFolderPath,"datasets", "final_datasets"))
model = fm.read_json_from_file(os.path.join(dataFolderPath,"datasets","model","model.json"))
# datasets = fm.read_stats_jsons_from_folder(os.path.join(dataFolderPath,"datasets", "final_datasets"))

for user in datasets:
    view = {}
    
    
    #initialising
    view["scores"] = []
    view["stats"]= {}
    view["timeactive"]={}
    view["projects"]= {}
    view["projects"]["labels"]= ["Owner", "Contributor"]
    
    view["languages"]=[]

    view["contributions"] = {}
    view["contributions"]["headers"]= ["Name","Commits","Contributors","Releases","Followers","Stargazers","Forks"]
    view["contributions"]["data"] = []
   
    # view["projectmgmtvalues"] = {}
    # view["qualitytestingvalues"] = {}
    view["issuevalues"] = {}
    view["bugvaluesopen"] = {}
    view["bugvaluesclose"] ={}
    view["projectsvalues"] = {}
    view["workperday"]={}
    view["workperday"]["labels"] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    view["workperday"]["values"] = [0] * 7
    view["activitiespermonth"] = {}
    view["activitiespermonth"]["comments"] = {}
    view["activitiespermonth"]["issues"] = {}
    view["activitiespermonth"]["commits"] = {}

    view["pullrequests"] = {}
    view["pullrequests"]["labels"] = ["Open", "Merged", "Closed"]
    view["response time"] = {}
    view["languageslong"] = {}

    #initialising month labels
    now = time.localtime()
    latest_months = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(8)]
    labels = []
    for item in latest_months[::-1]:
        labels.append(calendar.month_abbr[item[1]])

    view["issuevalues"]["labels"] = labels
    view["bugvaluesopen"]["labels"] = labels 
    view["bugvaluesclose"]["labels"] = labels 
    view["projectsvalues"]["labels"] = labels 
    view["activitiespermonth"]["comments"]["labels"] = labels 
    view["activitiespermonth"]["issues"]["labels"] = labels 
    view["activitiespermonth"]["commits"]["labels"] = labels

    #user name
    view["user_name"] = datasets[user]["name"]

    #performance scores
    pr_mgmt = {}
    pr_mgmt["Project management"]= round(datasets[user]["performance_scores"]["Project_Management"], 2)
    view["scores"].append(pr_mgmt)

    qual_testing = {}
    qual_testing ["Project Quality & Testing"]= round(datasets[user]["performance_scores"]["Quality&Testing"], 2)
    view["scores"].append( qual_testing )

    dev_prod = {}
    dev_prod["Dev Productivity"]= round(datasets[user]["performance_scores"]["Dev_Productivity"], 2)
    view["scores"].append(dev_prod)

    ops_prod = {}
    ops_prod["Ops Productivity"]= round(datasets[user]["performance_scores"]["Ops_Productivity"], 2)
    view["scores"].append(ops_prod)

    languages_long_dict = {}
    for item in datasets[user]["metrics_unclassified"]:
        
        if item["Name"] == "followers":
            view["stats"]["Followers"] = item["Value"]

        if item["Name"]=="commit_authored":
            view["stats"]["Commits authored"] = item["Value"]
        
        if item["Name"]=="issues_authored":
            view["stats"]["Issues authored"] = item["Value"]
            
        if item["Name"]=="issues_assigned":
            view["stats"]["Issues assigned"] = item["Value"]
            
        if item["Name"]=="total_pull_request_done_by_the_user":    
            view["stats"]["Pull requests"] = item["Value"]
            
        if item["Name"]=="total_comments_made_by_user":
            view["stats"]["Comments authored"] = item["Value"]
            
        if item["Name"]=="issues_mentions":  
            view["stats"]["Number of Mentions"] = item["Value"]
        
        if item["Name"]=="total_files_committed":
            view["stats"]["Files commited"] = item["Value"]

        if item["Name"]=="time_active - (y,m,d)":
            view["timeactive"]["years"]=item["Value"][0]
            view["timeactive"]["months"]=item["Value"][1]
            view["timeactive"]["days"]=item["Value"][2]

        if item["Name"] == "repos":
            view["projects"]["total"] = item["Value"]
        
        if item["Name"] == "repositories_owned":
            view["projects"]["values"]=[item["Value"],view["projects"]["total"]-item["Value"]]
        
        if item["Name"] == "percentage_of_activities_per_Monday":
            view["workperday"]["values"][0] = round(item["Value"],2)

        if item["Name"] == "percentage_of_activities_per_Tuesday":
            view["workperday"]["values"][1] = round(item["Value"],2)

        if item["Name"] == "percentage_of_activities_per_Wednesday":
            view["workperday"]["values"][2] = round(item["Value"],2)

        if item["Name"] == "percentage_of_activities_per_Thursday":
            view["workperday"]["values"][3] = round(item["Value"],2)

        if item["Name"] == "percentage_of_activities_per_Friday":
            view["workperday"]["values"][4] = round(item["Value"],2)

        if item["Name"] == "percentage_of_activities_per_Saturday":
            view["workperday"]["values"][5] = round(item["Value"],2)

        if item["Name"] == "percentage_of_activities_per_Sunday":
            view["workperday"]["values"][6] = round(item["Value"],2)


        if item["Name"] == "mostly_contributed_projects":
            for project in item["Value"]:
                project_name = '_'.join(project.split('/')[-1:])
                pr = [project_name, str(item["Value"][project]["scale_stats"]["amount_of_commits"]),str(item["Value"][project]["scale_stats"]["amount_of_contributors"]),\
                    str(item["Value"][project]["scale_stats"]["amount_of_releases"]),str(item["Value"][project]["popularity_stats"]["watchers_count"]),\
                        str(item["Value"][project]["popularity_stats"]["stargazers_count"]),str(item["Value"][project]["popularity_stats"]["forks_count"])]
                view["contributions"]["data"].append(pr)
        
        values = [0] * 8
        if item["Name"] == "projects_per_month_long":
            i = 0
            for monthyear in latest_months[::-1]:
                year_month = str(monthyear[0]) +"_"+str(monthyear[1])
                try:
                    if item["Value"][year_month]:
                        values[i]= item["Value"][year_month]
                except KeyError:
                    continue
                i +=  1

            view["projectsvalues"]["values"] = values

        
        if item["Name"] == "bugs_opened_per_month_long":
            i = 0
            for monthyear in latest_months[::-1]:
                year_month = str(monthyear[0]) +"_"+str(monthyear[1])
                try:
                    if item["Value"][year_month]:
                        values[i]= item["Value"][year_month]
                except KeyError:
                    continue
                i +=  1

            view["bugvaluesopen"]["values"] = values

        if item["Name"] == "bugs_closed_per_month_long":
            i = 0
            for monthyear in latest_months[::-1]:
                year_month = str(monthyear[0]) +"_"+str(monthyear[1])
                try:
                    if item["Value"][year_month]:
                        values[i]= item["Value"][year_month]
                except KeyError:
                    continue
                i +=  1

            view["bugvaluesclose"]["values"] = values

        if item["Name"] == "comments_per_month_long":
            i = 0
            for monthyear in latest_months[::-1]:
                year_month = str(monthyear[0]) +"_"+str(monthyear[1])
                try:
                    if item["Value"][year_month]:
                        values[i]= item["Value"][year_month]
                except KeyError:
                    continue
                i +=  1

            view["activitiespermonth"]["comments"]["values"] = values

        if item["Name"] == "issues_per_month_long":
            i = 0
            for monthyear in latest_months[::-1]:
                year_month = str(monthyear[0]) +"_"+str(monthyear[1])
                try:
                    if item["Value"][year_month]:
                        values[i]= item["Value"][year_month]
                except KeyError:
                    continue
                i +=  1

            view["activitiespermonth"]["issues"]["values"] = values

        if item["Name"] == "commits_per_month_long":
            i = 0
            for monthyear in latest_months[::-1]:
                year_month = str(monthyear[0]) +"_"+str(monthyear[1])
                try:
                    if item["Value"][year_month]:
                        values[i]= item["Value"][year_month]
                except KeyError:
                    continue
                i +=  1

            view["activitiespermonth"]["commits"]["values"] = values
                
        if "percentage_of_files_committed_in" in item["Name"]:
            # print(item["Name"])
            name = item["Name"].split('_')[-1]
            languages_long_dict[name] = item["Value"]

    sorted_languages = sorted(languages_long_dict.items(), key=lambda kv: kv[1])
    lang_labels = []
    lang_values = []
    for item in sorted_languages[::-1]:
        lang_labels.append(item[0])
        lang_values.append(item[1])

    view["languageslong"]["labels"] = lang_labels
    view["languageslong"]["values"] = lang_values


    #initialising for classified metrics

    project_mgm_list = [0]*7
    qualitytestinglist = [0]*6
    dev_prod_list = [0] * 2
    ops_prod_list  = [0] * 4
    view["pullrequests"]["values"] = [0] * 3
    view["timebetweenvalues"] = [0] * 4


    for item in datasets[user]["metrics_classified"]:
        
        if item["Name"]=="percentage_of_comments_with_documentation_keyword":
            view["stats"]["Comments with documentation keywords (%)"] = [round(item["Value_normalised"],2), item["Score"]]

        empty_dict = {}
        # if item["Name"]== "percentage_of_issues_created_by_the_user_that_are_still_open":
        #     empty_dict["(%) issues authored by the user are closed"] = [100- round(item["Value_normalised"],2),item["Score"]]
        #     project_mgm_list.append(empty_dict)
        
        if item["Name"]== "percentage_of_issues_created_by_the_user_closed_by_user":
            empty_dict["(%) issues authored and closed by the user"] = [round(item["Value_normalised"],2),item["Score"]]
            project_mgm_list[0] = empty_dict
        
        if item["Name"]== "percentage_of_issues_with_assigned_label":
            empty_dict["(%) issues labeled by the user"] = [round(item["Value_normalised"],2),item["Score"]]
            project_mgm_list[1] = empty_dict
        
        if item["Name"]== "percentage_of_issues_created_by_the_user_with_assigned_milestone":
            empty_dict["(%) issues with milestone"] = [round(item["Value_normalised"],2),item["Score"]]
            project_mgm_list[2] = empty_dict

        if item["Name"]== "percentage_of_issues_created_by_the_user_with_assigned_milestone_by_the_user":
            empty_dict["(%) milestones assigned by the user"] = [round(item["Value_normalised"],2),item["Score"]]
            project_mgm_list[3] = empty_dict

        if item["Name"]== "percentage_of_issues_opened_by_the_user_with_bug_keyword":
            empty_dict["(%) issues related to bugs"] = [round(item["Value_normalised"],2),item["Score"]]
            project_mgm_list[4] = empty_dict

        if item["Name"]== "percentage_of_issues_with_bug_keyword_assigned_by_the_user":
            empty_dict["(%) bugs assigned to someone by the user"] = [round(item["Value_normalised"],2),item["Score"]]
            project_mgm_list[5] = empty_dict

        if item["Name"]== "percentage_of_comments_with_project_management_keyword":
            empty_dict["(%) of comments related to project management"] = [round(item["Value_normalised"],2),item["Score"]]
            project_mgm_list[6] = empty_dict
        
        view["projectmgmtvalues"] = project_mgm_list

        if item["Name"]== "percentage_of_comments_with_test_keyword":
            empty_dict["(%) comments related to testing"] = [round(item["Value_normalised"],2),item["Score"]]
            qualitytestinglist[0] = empty_dict

        if item["Name"]== "percentage_of_comments_with_issue_number":
            empty_dict["(%) comments referring to an issue "] = [round(item["Value_normalised"],2),item["Score"]]
            qualitytestinglist[1] = empty_dict

        if item["Name"]== "bugs_opened_per_month":
            empty_dict["(%) bugs opened per month"] = [round(item["Value_normalised"],2),item["Score"]]
            qualitytestinglist[2] = empty_dict

        if item["Name"]== "percentage_of_issues_closed_by_the_user_with_bug_keyword":
            empty_dict["(%) issues assigned to user that are bugs"] = [round(item["Value_normalised"],2),item["Score"]]
            qualitytestinglist[3] = empty_dict

        if item["Name"]== "percentage_of_testing_related_files_committed_by_the_user":
            empty_dict["(%) files commited related to testing"] = [round(item["Value_normalised"],2),item["Score"]]
            qualitytestinglist[4] = empty_dict

        if item["Name"]== "bugs_resolved_per_month":
            empty_dict["(%) bugs resolved per month"] = [round(item["Value_normalised"],2),item["Score"]]
            qualitytestinglist[5] = empty_dict

        view["qualitytestingvalues"] = qualitytestinglist
    
        if item["Name"]== "percentage_of_issues_assigned_to_the_user_closed_by_user":
            empty_dict["(%) Issues assigned to user are closed"] = [round(item["Value_normalised"],2),item["Score"]]
            dev_prod_list[0] = empty_dict

        if item["Name"]== "amount_of_files_changed_in_a_commit":
            empty_dict["(%) Number of files changes in a commit"] = [round(item["Value_normalised"],2),item["Score"]]
            dev_prod_list[1] = empty_dict

        view["devproductivityvalues"] = dev_prod_list

        if item["Name"]== "comment_length":
            empty_dict["Score - Comments length"] = [round(item["Value_normalised"],2),item["Score"]]
            ops_prod_list[0] = empty_dict

        if item["Name"]== "number_of_comment_answers":
            empty_dict["Score - Number of comment answers"] = [round(item["Value_normalised"],2),item["Score"]]
            ops_prod_list[1] = empty_dict

        if item["Name"]== "comments_frequency_per_month":
            empty_dict["Score - Comments per month"] = [round(item["Value_normalised"],2),item["Score"]]
            ops_prod_list[2] = empty_dict

        if item["Name"]== "percentage_of_comments_with_documentation_keyword":
            empty_dict["Score - Comments related to documentation"] = [round(item["Value_normalised"],2),item["Score"]]
            ops_prod_list[3] = empty_dict

        view["opsproductivityvalues"] = ops_prod_list
    
        if item["Name"]== "percentage_of_pull_requests_made_by_the_user_that_are_still_open":
            view["pullrequests"]["values"] [0] = round(item["Value"],2)
            
        if item["Name"]== "percentage_of_pull_requests_made_by_the_user_that_were_merged":
            view["pullrequests"]["values"] [1] = round(item["Value"],2)

        if item["Name"]== "percentage_of_pull_requests_made_by_the_user_that_were_closed_not_merged":
            view["pullrequests"]["values"] [2] = round(item["Value"],2)

        if item["Name"] == "time_diff_between_consequtive_commiits_committed_by_user":
            empty_dict["Consecutive commits"] ={}
            value = to_day_hour_min_sec(item["Value"]).split(':')[0]
            empty_dict["Consecutive commits"]["value"] = int(value)
            view["timebetweenvalues"][0] = empty_dict

        if item["Name"] == "pull_merge_diff":
            empty_dict["Pull Request-Merge"] ={}
            value = to_day_hour_min_sec(item["Value"]).split(':')[0]
            empty_dict["Pull Request-Merge"]["value"] = int(value)
            view["timebetweenvalues"][1] = empty_dict

        if item["Name"] == "issue_created_by_user_closed_by_user_time_diff":
            empty_dict["Issues Created-Closed"] ={}
            value = to_day_hour_min_sec(item["Value"]).split(':')[0]
            empty_dict["Issues Created-Closed"]["value"] = int(value)
            view["timebetweenvalues"][2] = empty_dict

        if item["Name"] == "issue_assigned_to_user_and_closed_by_user_time_diff":
            empty_dict["Issues Assigned-Closed"] ={}
            value = to_day_hour_min_sec(item["Value"]).split(':')[0]
            empty_dict["Issues Assigned-Closed"]["value"] = int(value)
            view["timebetweenvalues"][3] = empty_dict

        if item["Name"] == "response_time_to_comments_mentioned":
            value = to_day_hour_min_sec(item["Value"]).split(':')[0]
            view["response time"]["value"] = int(value)
            


    #finish time_diff    
    for item in model:
        if item["Name"] == "time_diff_between_consequtive_commiits_committed_by_user":
            view["timebetweenvalues"][0]["Consecutive commits"]["min"] = int(to_day_hour_min_sec(item["Score_min"]).split(':')[0])
            view["timebetweenvalues"][0]["Consecutive commits"]["max"] = int(to_day_hour_min_sec(item["Score_max"]).split(':')[0])
            view["timebetweenvalues"][0]["Consecutive commits"]["low"] = int(to_day_hour_min_sec(item["Score_instructions"][1]["Lower_threshold"]).split(':')[0])
            view["timebetweenvalues"][0]["Consecutive commits"]["high"] = int(to_day_hour_min_sec(item["Score_instructions"][1]["Higher_threshold"]).split(':')[0])
            
        if item["Name"] == "pull_merge_diff":
            view["timebetweenvalues"][1]["Pull Request-Merge"]["min"] = int(to_day_hour_min_sec(item["Score_min"]).split(':')[0])
            view["timebetweenvalues"][1]["Pull Request-Merge"]["max"] = int(to_day_hour_min_sec(item["Score_max"]).split(':')[0])
            view["timebetweenvalues"][1]["Pull Request-Merge"]["low"] = int(to_day_hour_min_sec(item["Score_instructions"][1]["Lower_threshold"]).split(':')[0])
            view["timebetweenvalues"][1]["Pull Request-Merge"]["high"] = int(to_day_hour_min_sec(item["Score_instructions"][1]["Higher_threshold"]).split(':')[0])
         
        if item["Name"] == "issue_created_by_user_closed_by_user_time_diff":
            view["timebetweenvalues"][2]["Issues Created-Closed"]["min"] = int(to_day_hour_min_sec(item["Score_min"]).split(':')[0])
            view["timebetweenvalues"][2]["Issues Created-Closed"]["max"] = int(to_day_hour_min_sec(item["Score_max"]).split(':')[0])
            view["timebetweenvalues"][2]["Issues Created-Closed"]["low"] = int(to_day_hour_min_sec(item["Score_instructions"][1]["Lower_threshold"]).split(':')[0])
            view["timebetweenvalues"][2]["Issues Created-Closed"]["high"] = int(to_day_hour_min_sec(item["Score_instructions"][1]["Higher_threshold"]).split(':')[0])
         
        if item["Name"] == "issue_assigned_to_user_and_closed_by_user_time_diff":
            view["timebetweenvalues"][3]["Issues Assigned-Closed"]["min"] = int(to_day_hour_min_sec(item["Score_min"]).split(':')[0])
            view["timebetweenvalues"][3]["Issues Assigned-Closed"]["max"] = int(to_day_hour_min_sec(item["Score_max"]).split(':')[0])
            view["timebetweenvalues"][3]["Issues Assigned-Closed"]["low"] = int(to_day_hour_min_sec(item["Score_instructions"][1]["Lower_threshold"]).split(':')[0])
            view["timebetweenvalues"][3]["Issues Assigned-Closed"]["high"] = int(to_day_hour_min_sec(item["Score_instructions"][1]["Higher_threshold"]).split(':')[0])
         
        if item["Name"] == "response_time_to_comments_mentioned":
            view["response time"]["min"] = int(to_day_hour_min_sec(item["Score_min"]).split(':')[0])
            view["response time"]["max"] = int(to_day_hour_min_sec(item["Score_max"]).split(':')[0])
            view["response time"]["low"] = int(to_day_hour_min_sec(item["Score_instructions"][1]["Lower_threshold"]).split(':')[0])
            view["response time"]["high"] = int(to_day_hour_min_sec(item["Score_instructions"][1]["Higher_threshold"]).split(':')[0])
         


    #two mostly used languages
    first_lang = max(languages_long_dict.items(), key=operator.itemgetter(1))[0]
    del languages_long_dict[first_lang]
    second_lang = max(languages_long_dict.items(), key=operator.itemgetter(1))[0]

    view["languages"].append(first_lang)
    view["languages"].append(second_lang)

    # print(view)
    # fm.write_json_to_file(os.path.join(dataFolderPath,"datasets","view_files", "vieweg.json"), view)    

    # break
    fm.write_json_to_file(os.path.join(dataFolderPath,"datasets","view_files", str(user)+ ".json"), datasets)

# print(datasets)
# fm.write_json_to_file(os.path.join(dataFolderPath,"datasets","view_files", "group.json"), datasets)
# fm.write_json_to_file(os.path.join(dataFolderPath,"datasets","view_files", str(user)+ ".json"), datasets)