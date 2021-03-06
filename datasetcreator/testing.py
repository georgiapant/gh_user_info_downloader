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
from datasetcreator.dbs import Databases

'''
- close issues labeled with keywords like bug, faulty etc - done
- committed comments that include an issue num - done
- add comments that incude keywords like test, defect, test case etc - done
- number of issues he closed by the user - done
- amount of test cases added (file committed with test relevant words in their name)
'''

class Test(Databases):

    def closed_issues( self, user_name, issues_authored, issues_assigned, issues_commented, issues_mentions, issues_owned):
        '''
        User closes issues labeled with keyword related to bug
        '''
        issue_ids = []
        closed_issues_count = 0 #total amount of issues closed by the user
        closed_bugs_count = 0 #total amount of issues identified as bugs closed by the user
        bugs_per_day = {}
        list_bugs_per_day = []

        for issue_id in issues_authored.keys():
            if bool(issues_authored[issue_id]["closed_at"]) and bool(issues_authored[issue_id]["closed_by"]) and issues_authored[issue_id]["closed_by"]["login"]== user_name:
                issue_ids.append(issue_id)
                closed_issues_count += 1
                if bool(issues_authored[issue_id]["labels"]):                 
                    for item in range(len(issues_authored[issue_id]["labels"])):
                        if any(word in issues_authored[issue_id]["labels"][item]["name"] for word in self.keywords_db()[1]):                    
                            closed_bugs_count += 1
                            date_str = issues_authored[issue_id]["closed_at"]
                            date = date_str.split('T')
                            try:
                                bugs_per_day[date[0]] = bugs_per_day[date[0]] + 1
                            except:
                                bugs_per_day[date[0]] = 1
                            
        
        for issue_id in issues_assigned.keys():
            if issue_id not in issue_ids:
                if bool(issues_assigned[issue_id]["closed_at"]) and bool(issues_assigned[issue_id]["closed_by"]) and issues_assigned[issue_id]["closed_by"]["login"]== user_name:
                    issue_ids.append(issue_id)
                    closed_issues_count += 1
                    if bool(issues_assigned[issue_id]["labels"]): 
                        for item in range(len(issues_assigned[issue_id]["labels"])):
                            if any(word in issues_assigned[issue_id]["labels"][item]["name"] for word in self.keywords_db()[1]): 
                                closed_bugs_count += 1
                                date_str = issues_assigned[issue_id]["closed_at"]
                                date = date_str.split('T')
                                try:
                                    bugs_per_day[date[0]] = bugs_per_day[date[0]] + 1
                                except:
                                    bugs_per_day[date[0]] = 1
       
        for issue_id in issues_commented.keys():
            if issue_id not in issue_ids:
                # print(issue_id)
                if (bool(issues_commented[issue_id]["closed_at"]) and bool(issues_commented[issue_id]["closed_by"]) and issues_commented[issue_id]["closed_by"]["login"]== user_name):
                    issue_ids.append(issue_id)
                    closed_issues_count += 1
                    if bool(issues_commented[issue_id]["labels"]):                     
                        for item in range(len(issues_commented[issue_id]["labels"])): 
                            if any(word in issues_commented[issue_id]["labels"][item]["name"] for word in self.keywords_db()[1]): 
                                closed_bugs_count += 1
                                # print(issues_commented[issue_id])
                                date_str = issues_commented[issue_id]["closed_at"]
                                date = date_str.split('T')
                                try:
                                    bugs_per_day[date[0]] = bugs_per_day[date[0]] + 1
                                except:
                                    bugs_per_day[date[0]] = 1
            
        for issue_id in issues_mentions.keys():
            if issue_id not in issue_ids:
                if bool(issues_mentions[issue_id]["closed_at"]) and bool(issues_mentions[issue_id]["closed_by"]) and issues_mentions[issue_id]["closed_by"]["login"]== user_name:
                    issue_ids.append(issue_id)
                    closed_issues_count += 1
                    if bool(issues_mentions[issue_id]["labels"]):
                        for item in range(len(issues_mentions[issue_id]["labels"])):
                            if any(word in issues_mentions[issue_id]["labels"][item]["name"] for word in self.keywords_db()[1]): 
                                closed_bugs_count += 1
                                date_str = issues_mentions[issue_id]["closed_at"]
                                date = date_str.split('T')
                                try:
                                    bugs_per_day[date[0]] = bugs_per_day[date[0]] + 1
                                except:
                                    bugs_per_day[date[0]] = 1
        
        for issue_id in issues_owned.keys():
            if issue_id not in issue_ids:
                
                if bool(issues_owned[issue_id]["closed_at"]) and bool(issues_owned[issue_id]["closed_by"]) and issues_owned[issue_id]["closed_by"]["login"]== user_name:
                    issue_ids.append(issue_id)
                    closed_issues_count += 1
                    if bool(issues_owned[issue_id]["labels"]): 
                        for item in range(len(issues_owned[issue_id]["labels"])):                        
                            if any(word in issues_owned[issue_id]["labels"][item]["name"] for word in self.keywords_db()[1]): 
                                closed_bugs_count += 1
                                date_str = issues_owned[issue_id]["closed_at"]
                                date = date_str.split('T')
                                try:
                                    bugs_per_day[date[0]] = bugs_per_day[date[0]] + 1
                                except:
                                    bugs_per_day[date[0]] = 1
        
        for key in bugs_per_day.keys():
            list_bugs_per_day.append(bugs_per_day[key])
        

        return closed_bugs_count, closed_issues_count, list_bugs_per_day, bugs_per_day

    def opened_bugs(self, user_name, issues_authored):
        opened_bugs_count = 0
        bugs_opened_per_day = {}
        list_bugs_opened_per_day = []

        for issue_id in issues_authored.keys():
            if bool(issues_authored[issue_id]["labels"]):                 
                for item in range(len(issues_authored[issue_id]["labels"])):
                    if any(word in issues_authored[issue_id]["labels"][item]["name"] for word in self.keywords_db()[1]):                    
                        opened_bugs_count += 1
                        date_str = issues_authored[issue_id]["created_at"]
                        date = date_str.split('T')
                        try:
                            bugs_opened_per_day[date[0]] = bugs_opened_per_day[date[0]] + 1
                        except:
                            bugs_opened_per_day[date[0]] = 1

        for key in bugs_opened_per_day.keys():
            list_bugs_opened_per_day.append(bugs_opened_per_day[key])
        
        return opened_bugs_count, list_bugs_opened_per_day, bugs_opened_per_day



    def test_comments(self, user_name, issue_comments, commit_authored_comments):
        '''
        This function returns 
        - the amount of comments written by the user
        - the amount of those that include wordscrelated to testing and quality
        - the amount of comments that contain an issue number reference
        '''
        cm = Communication()
        user_comments = cm.user_comments(user_name, issue_comments, commit_authored_comments)[1]
        issue_comments = user_comments["comments_on_issues"]
        committ_comments = user_comments["commnents_on_committs"]
        test_comments_count = 0
        total_comment_count = 0
        contains_issue_num = 0
        reg = re.compile('#[0-9]+')

        for issue_id in issue_comments.keys():
            for sub_id in issue_comments[issue_id].keys():
                total_comment_count += 1
                if any(word in issue_comments[issue_id][sub_id]["body"] for word in self.keywords_db()[2]):
                    test_comments_count += 1
                if bool(re.findall(reg, issue_comments[issue_id][sub_id]["body"])): #can get even the issue numbers if needed by removing the bool
                    contains_issue_num += 1
                
        
        for committ_sha in committ_comments.keys():
            for sub_id in committ_comments[committ_sha].keys():
                total_comment_count += 1
                if any(word in committ_comments[committ_sha][sub_id]["body"] for word in self.keywords_db()[2]):
                    test_comments_count += 1
                
                try:
                    if bool(re.findall(reg, committ_comments[committ_sha][sub_id]["body"])): #can get even the issue numbers if needed by removing the bool
                        contains_issue_num += 1
                except KeyError:
                    continue
                
        test_comments_out = (test_comments_count, contains_issue_num)
        return test_comments_out, total_comment_count

    def add_test_case(self, commit_authored):
        '''
        This function returns the amount of added files include the string /test/ or /tests/ in their name. 
        It is assumed that those files are part of test cases made by the user
        '''
       
        list_of_filenames = []
        test_cases = 0

        for element_id in commit_authored.keys():
            files = commit_authored[element_id]["files"]
            for item in range(len(files)):
                file_name = files[item]["filename"]
                list_of_filenames.append(file_name)
        
        for item in range(len(list_of_filenames)):
            if any(word in list_of_filenames[item] for word in self.keywords_db()[3]):
                test_cases +=1

        return test_cases
