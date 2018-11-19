import os
import sys
import traceback
import requests
import json
from logger.downloadlogger import Logger
from datamanager.dbmanager import DBManager
from datamanager.filemanager import FileManager
from downloader.gitdownloader import GitDownloader
from downloader.githubdownloader import GithubDownloader
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose

fm = FileManager()
db = DBManager()
lg = Logger(verbose)
ghd = GithubDownloader(GitHubAuthToken)
gd = GitDownloader(gitExecutablePath, lg)

'''
Haven't implemented checking if comments exist already nor step_action.
This e
'''

#user_api_address = "https://api.github.com/users/" + '/'.join(user_address.split('/')[-1:])
#user_name = '_'.join(user_address.split('/')[-1:])
user_name = "nbriz"

db.initialize_write_to_disk(user_name)
project = db.read_project_from_disk(user_name)


download_issue_comments = True
download_commit_comments = True

if download_issue_comments:
    
    issues_commented = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_commented", "id")
    for element_id in issues_commented.keys():
        fm.create_folder_if_it_does_not_exist(dataFolderPath + "/" + user_name + "/issue_comments" + "/" + str(element_id))
        all_comments_url = issues_commented[element_id]["comments_url"]        
        for comment in ghd.download_paginated_object2(all_comments_url):            
            db.write_project_issue_comments_to_disk(user_name, comment, element_id)

if download_commit_comments:
    commit_authored=fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
    commit_committed = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_committed","sha")
    commit_sha_list = []

    for commit_sha in commit_authored.keys():
        commit_sha_list.append(commit_sha)
        if commit_authored[commit_sha]["commit"]["comment_count"]>0:
            fm.create_folder_if_it_does_not_exist(dataFolderPath + "/" + user_name + "/commit_comments" + "/" + str(commit_sha))
            all_comments_url = commit_authored[commit_sha]["comments_url"]       
            for comment in ghd.download_paginated_object2(all_comments_url):            
                db.write_project_commit_comments_to_disk(user_name, comment, commit_sha)

    for commit_sha in commit_committed.keys():
        if commit_sha not in commit_sha_list and commit_committed[commit_sha]["commit"]["comment_count"]>0:
            fm.create_folder_if_it_does_not_exist(dataFolderPath + "/" + user_name + "/commit_comments" + "/" + str(commit_sha))
            all_comments_url = commit_authored[commit_sha]["comments_url"]       
            for comment in ghd.download_paginated_object2(all_comments_url):            
                db.write_project_commit_comments_to_disk(user_name, comment, commit_sha)            

