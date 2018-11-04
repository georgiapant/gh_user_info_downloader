import sys
from properties import (GitHubAuthToken, dataFolderPath, gitExecutablePath,verbose,  packageFolderPath)
sys.path.insert(0, packageFolderPath) 
from datamanager.filemanager import FileManager

import json
import datetime
from dateutil.relativedelta import relativedelta

user_address = "https://github.com/nbriz"
user_api_address = "https://api.github.com/users/" + '/'.join(user_address.split('/')[-1:])
user_name='nbriz'

fm = FileManager()
def time_active(dataFolderPath, user_name):
    '''
    This funtion returns the years, months and days between the first commit committed and the last by the user in the form of a tuple
    It needs to have downloaded the full version of the committs_committed 
    '''
   
    commit_committed = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_committed","sha")

    first_commit = datetime.datetime.combine(datetime.datetime.now().date(), datetime.datetime.now().time())
    last_commit = datetime.datetime.combine(datetime.date.min,  datetime.time.min)

    for element_id in commit_committed.keys():
        date_str = commit_committed[element_id]["commit"]["committer"]["date"]
        date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ') 

        if date<first_commit:
            first_commit = date 
        elif date>last_commit:
            last_commit = date
        else:
            continue

    return relativedelta(last_commit, first_commit).years, relativedelta(last_commit, first_commit).months, relativedelta(last_commit, first_commit).days


