import sys
from properties import (GitHubAuthToken,dataFolderPath,  packageFolderPath)
sys.path.insert(0, packageFolderPath) 
from datamanager.filemanager import FileManager

from downloader.githubdownloader import GithubDownloader
import json
import datetime
import requests
from dateutil.relativedelta import relativedelta


fm = FileManager()
#ghd = GithubDownloader(GitHubAuthToken)
# user_name = 'nbriz'
# dataFolderPath = '/Users/georgia/Desktop'

# issues_mentions = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_mentions", "id")
# issue_comments = fm.read_comment_jsons_from_folder(dataFolderPath+ "/" + user_name + "/issue_comments")

def response_time_to_comments_mentioned(user_name, issues_mentions, issue_comments):
    mention = "@"+user_name
    issue_mentions_ids = []
    response_times = []

    for key in issues_mentions.keys():
        issue_mentions_ids.append(key)
    
    for key in issue_comments.keys():
        if int(key) in issue_mentions_ids:
            counter = len(issue_comments[key])            
            for item in issue_comments[key]:
                if mention in item["body"]:
                    mention_time = datetime.datetime.strptime(item["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                    for comment_item in range(counter):
                        if issue_comments[key][comment_item]["user"]["login"]==user_name:                            
                            response_time = datetime.datetime.strptime(issue_comments[key][comment_item]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                            if mention_time < response_time:
                                a = (response_time-mention_time).total_seconds()
                                response_times.append(a)
                                break

    return  response_times

'''
x= response_time_to_comments_mentioned(user_name, issues_mentions, issue_comments)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/response_time_to_comments_mentioned.json", x) 
'''



