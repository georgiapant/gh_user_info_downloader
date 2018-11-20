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
#from list_of_repos_urls import List_of_repos_urls
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


download_issue_comments = False
download_commit_comments = False

if download_issue_comments:
   
    issues_commented = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_commented", "id")
    lg.start_action("Retrieving issue comments ", len(issues_commented.keys()))
       
    for element_id in issues_commented.keys():
        all_comments_url = issues_commented[element_id]["comments_url"]
        r = ghd.download_request(all_comments_url)
        r_dict = json.loads(r.text)
        comment = {}
        comment[element_id]= r_dict  
        if not project.issue_comment_exists(comment):
            project.add_issue_comment(comment)
            db.write_project_issue_comments_to_disk(user_name, comment)
    
        lg.step_action() 
    lg.end_action()


if download_commit_comments:
    commit_authored=fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
    commit_committed = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_committed","sha")
    length = len(commit_authored.keys()) + len(commit_committed.keys())
    lg.start_action("Retrieving commit comments ", length)
    
    for commit_sha in commit_authored.keys():
        
        if commit_authored[commit_sha]["commit"]["comment_count"]>0:
            all_comments_url = commit_authored[commit_sha]["comments_url"]  
            r = ghd.download_request(all_comments_url)
            r_dict = json.loads(r.text)
            comment = {}
            comment[commit_sha]= r_dict  
            print("its here!")
            if not project.commit_comment_exists(comment):
                project.add_commit_comment(comment)
                db.write_project_commit_comments_to_disk(user_name, comment) 
        lg.step_action() 

    for commit_sha in commit_committed.keys():
        if commit_committed[commit_sha]["commit"]["comment_count"]>0:
            all_comments_url = commit_committed[commit_sha]["comments_url"] 
            r = ghd.download_request(all_comments_url)
            r_dict = json.loads(r.text)
            comment = {}
            comment[commit_sha]= r_dict  
            print("its here too!")
            if not project.commit_comment_exists(comment):
                project.add_commit_comment(comment)
                db.write_project_commit_comments_to_disk(user_name, comment)     
        
        lg.step_action() 
    lg.end_action()

