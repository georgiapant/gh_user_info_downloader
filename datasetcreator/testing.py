import datetime
import json
import sys
import re
from properties import (GitHubAuthToken, dataFolderPath, packageFolderPath)
sys.path.insert(0, packageFolderPath) 
from dateutil.relativedelta import relativedelta
from datamanager.filemanager import FileManager
from datasetcreator.communication import Communication
#from downloader.githubdownloader import GithubDownloader
from datasetcreator.pm import Project_management

'''
- close issues labeled with keywords like bug, faulty etc - done
- committed comments that include an issue num - done
- add comments that incude keywords like test, defect, test case etc - done
- number of issues he closed by the user - done
- amount of test cases added (file committed with test relevant words in their name)
'''
user_name = 'nbriz'
fm = FileManager()
pm = Project_management()
cm = Communication()

def closed_issues(dataFolderPath, user_name):
    '''
    User closes issues labeled with keyword related to bug
    '''
    issues_authored = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")
    issues_assigned = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_assigned", "id")
    issues_commented = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_commented", "id")
    issues_mentions = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_mentions", "id")
    issues_owned = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_owned", "id")

    issue_ids = []
    closed_issues_count = 0 #total amount of issues closed by the user
    closed_bugs_count = 0 #total amount of issues identified as bugs closed by the user

    for issue_id in issues_authored.keys():
        if bool(issues_authored[issue_id]["closed_at"]) and issues_authored[issue_id]["closed_by"]["login"]== user_name:
            issue_ids.append(issue_id)
            closed_issues_count += 1
            if bool(issues_authored[issue_id]["labels"]):                 
                for item in range(len(issues_authored[issue_id]["labels"])):
                    if any(word in issues_authored[issue_id]["labels"][item]["name"] for word in pm.keywords_db()[1]):                    
                        closed_bugs_count += 1
    
    for issue_id in issues_assigned.keys():
        if issue_id not in issue_ids:
            if bool(issues_assigned[issue_id]["closed_at"]) and issues_assigned[issue_id]["closed_by"]["login"]== user_name:
                issue_ids.append(issue_id)
                closed_issues_count += 1
                if bool(issues_assigned[issue_id]["labels"]): 
                    for item in range(len(issues_assigned[issue_id]["labels"])):
                        if any(word in issues_assigned[issue_id]["labels"][item]["name"] for word in pm.keywords_db()[1]): 
                            closed_bugs_count += 1

    for issue_id in issues_commented.keys():
        if issue_id not in issue_ids:
            if bool(issues_commented[issue_id]["closed_at"]) and issues_commented[issue_id]["closed_by"]["login"]== user_name:
                issue_ids.append(issue_id)
                closed_issues_count += 1
                if bool(issues_commented[issue_id]["labels"]):                     
                    for item in range(len(issues_commented[issue_id]["labels"])): 
                        if any(word in issues_commented[issue_id]["labels"][item]["name"] for word in pm.keywords_db()[1]): 
                            closed_bugs_count += 1

    for issue_id in issues_mentions.keys():
        if issue_id not in issue_ids:
            if bool(issues_mentions[issue_id]["closed_at"]) and issues_mentions[issue_id]["closed_by"]["login"]== user_name:
                issue_ids.append(issue_id)
                closed_issues_count += 1
                if bool(issues_mentions[issue_id]["labels"]):
                    for item in range(len(issues_mentions[issue_id]["labels"])):
                        if any(word in issues_mentions[issue_id]["labels"][item]["name"] for word in pm.keywords_db()[1]): 
                            closed_bugs_count += 1

    for issue_id in issues_owned.keys():
        if issue_id not in issue_ids:
            if bool(issues_owned[issue_id]["closed_at"]) and issues_owned[issue_id]["closed_by"]["login"]== user_name:
                issue_ids.append(issue_id)
                closed_issues_count += 1
                if bool(issues_owned[issue_id]["labels"]): 
                    for item in range(len(issues_owned[issue_id]["labels"])):                        
                        if any(word in issues_owned[issue_id]["labels"][item]["name"] for word in pm.keywords_db()[1]): 
                            closed_bugs_count += 1

    return closed_bugs_count, closed_issues_count

def test_comments(dataFolderPath, user_name):
    '''
    This function returns 
    - the amount of comments written by the user
    - the amount of those that include wordscrelated to testing and quality
    - the amount of comments that contain an issue number reference
    '''
    user_comments = cm.user_comments(dataFolderPath, user_name)[1]
    issue_comments = user_comments["comments_on_issues"]
    committ_comments = user_comments["commnents_on_committs"]
    test_comments_count = 0
    total_comment_count = 0
    contains_issue_num = 0
    reg = re.compile('#[0-9]+')

    for issue_id in issue_comments.keys():
        for sub_id in issue_comments[issue_id].keys():
            total_comment_count += 1
            if any(word in issue_comments[issue_id][sub_id]["body"] for word in pm.keywords_db()[2]):
                test_comments_count += 1
            if bool(re.findall(reg, issue_comments[issue_id][sub_id]["body"])): #can get even the issue numbers if needed by removing the bool
                contains_issue_num += 1
            
    
    for committ_sha in committ_comments.keys():
        for sub_id in committ_comments[committ_sha].keys():
            total_comment_count += 1
            if any(word in committ_comments[committ_sha][sub_id]["body"] for word in pm.keywords_db()[2]):
                test_comments_count += 1
            if bool(re.findall(reg, issue_comments[issue_id][sub_id]["body"])): #can get even the issue numbers if needed by removing the bool
                contains_issue_num += 1
            
    
    return test_comments_count, contains_issue_num, total_comment_count



x = test_comments(dataFolderPath,user_name)
print(x)


