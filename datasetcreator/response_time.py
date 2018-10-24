import sys
from properties import (GitHubAuthToken, dataFolderPath, packageFolderPath)
sys.path.insert(0, packageFolderPath) 
from datamanager.filemanager import FileManager

from downloader.githubdownloader import GithubDownloader
import json
import datetime
import requests
from dateutil.relativedelta import relativedelta


fm = FileManager()
ghd = GithubDownloader(GitHubAuthToken)

def response_time_to_comments_mentioned(dataFolderPath, user_name):
    '''
    FIX THIS xD
    '''
    issues_mentions = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_mentions", "id")
    mention = "@"+user_name
    mention_comments = {}
    reply_comments = {}

    for element_id in issues_mentions.keys():
        comments_url = issues_mentions[element_id]["comments_url"]
        mention_comments[element_id]={}
        reply_comments[element_id]={}

        if mention in issues_mentions[element_id]["body"]:
            created_time = datetime.datetime.strptime(issues_mentions[element_id]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
            comment_id, time, body = element_id, created_time, issues_mentions[element_id]["body"]
            #body_created_list.append((str(time),body))
            
            mention_comments[element_id]["comment_id"]= comment_id
            mention_comments[element_id]["body"]= body
            mention_comments[element_id]["created_at"]=str(time)
    
        r = ghd.download_request(comments_url)
        r_dict = json.loads(r.text)
        for item in range(len(r_dict)):
            try:
                if mention in r_dict[item]["body"]:
                    created_time = datetime.datetime.strptime(r_dict[item]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                    updated_time = datetime.datetime.strptime(r_dict[item]["updated_at"],'%Y-%m-%dT%H:%M:%SZ')
                                        
                    if created_time==updated_time:
                        mention_time = created_time
                    else:
                        mention_time = updated_time
                    
                    comment_id, time, body = r_dict[item]["id"], mention_time, r_dict[item]["body"]
                                
                    mention_comments[element_id][item]={}
                    mention_comments[element_id][item]["comment_id"]= comment_id
                    mention_comments[element_id][item]["body"]= body
                    mention_comments[element_id][item]["created_at"]=str(time)
                    
                if r_dict[item]["user"]["login"]==user_name:
                    created_time = datetime.datetime.strptime(r_dict[item]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                    updated_time = datetime.datetime.strptime(r_dict[item]["updated_at"],'%Y-%m-%dT%H:%M:%SZ')
                    
                    if created_time==updated_time:
                        reply_time = created_time
                    else:
                        reply_time = updated_time
                    
                    comment_id, time, body = r_dict[item]["id"], reply_time, r_dict[item]["body"]
                                        
                    reply_comments[element_id][item]={}
                    reply_comments[element_id][item]["comment_id"]= comment_id
                    reply_comments[element_id][item]["body"]= body
                    reply_comments[element_id][item]["created_at"]=str(time)   
            
            except IndexError:
                    continue 

        # Until here i have created to dictionaries, one with the comments with mentions+times and one with all replies to issues
    
    response_times_dict = {}
    mention_times_dict = {}
    issue_ids = []
    dict_time = {}
    for element_id in mention_comments.keys():
        
        if bool(reply_comments[element_id]):   #False if dictionary is empty
            issue_ids.append(element_id) #keep only isuse ids with possible replies from the user


    for issue_id in issue_ids:
        mention_times_dict[issue_id] = {}
        response_times_dict[issue_id] = {}
        
        for item in mention_comments[issue_id].keys():
            try:
                
                mention_time =  datetime.datetime.strptime(mention_comments[issue_id][item]["created_at"],'%Y-%m-%d %H:%M:%S')
                mention_times_dict[issue_id][mention_comments[issue_id][item]["comment_id"]] = str(mention_time)
            except:
                mention_time =  datetime.datetime.strptime(mention_comments[issue_id]["created_at"],'%Y-%m-%d %H:%M:%S')
                mention_times_dict[issue_id][mention_comments[issue_id]["comment_id"]] = str(mention_time)    
            
        for item in reply_comments[issue_id].keys():
            response_time = datetime.datetime.strptime(reply_comments[issue_id][item]["created_at"],'%Y-%m-%d %H:%M:%S')
            response_times_dict[issue_id][reply_comments[issue_id][item]["comment_id"]] = str(response_time)
    
#so far I have created two dictionaries one with main keys the issue ids and kep the dates of the mention 
# and another with the resposne times 

    for issue_id in mention_times_dict.keys(): #in the mention dict check all items
        dict_time[issue_id] = {}
        
        for comment_id in mention_times_dict[issue_id].keys(): #for each item 
            mention_time = datetime.datetime.strptime(mention_times_dict[issue_id][comment_id],'%Y-%m-%d %H:%M:%S')
            dict_time[issue_id][comment_id] = {}
        
            for response_comment_id in response_times_dict[issue_id].keys():
                response_time = datetime.datetime.strptime(response_times_dict[issue_id][response_comment_id],'%Y-%m-%d %H:%M:%S')
        
                if response_time > mention_time:
        
                    if not bool(dict_time[issue_id][comment_id]): 
        
                        for item in dict_time[issue_id].keys():
        
                            try:
        
                                if response_time == datetime.datetime.strptime(dict_time[issue_id][item]["response_time"],'%Y-%m-%d %H:%M:%S'):
                                    break
                                else:
                                    a = relativedelta( response_time,mention_time).months, relativedelta(response_time, mention_time).days, \
                                    relativedelta(response_time, mention_time).minutes, relativedelta(response_time, mention_time).seconds
                                    dict_time[issue_id][comment_id]["mention_time"] = str(mention_time)
                                    dict_time[issue_id][comment_id]["response_time"] = str(response_time)
                                    dict_time[issue_id][comment_id]["final_response_time"] = a
                                   
        
                            except:
                                a = relativedelta( response_time,mention_time).months, relativedelta(response_time, mention_time).days, \
                                relativedelta(response_time, mention_time).minutes, relativedelta(response_time, mention_time).seconds
                                
                                dict_time[issue_id][comment_id]["mention_time"] = str(mention_time)
                                dict_time[issue_id][comment_id]["response_time"] = str(response_time)
                                dict_time[issue_id][comment_id]["final_response_time"] = a                          
    
    return dict_time