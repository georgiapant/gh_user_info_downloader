import datetime
import json
import sys
from properties import (GitHubAuthToken, dataFolderPath, packageFolderPath)
sys.path.insert(0, packageFolderPath) 
from dateutil.relativedelta import relativedelta

from datasetcreator.communication import Communication
from datasetcreator.dbs import Databases

'''
Class that includes functions that are related to project management skills
'''

class Project_management():
    
    def bug_assigned(self, issues_authored):
        '''
        returns the amount of issues that are assigned to any user and are bugs (bugs are considered issues that either include
        a bug related word in their body or in their label)
        '''
        dbs = Databases()
        count_bugs_assigned = 0
        issue_id_list = []
        total_issues_with_assginee = 0
        for issue_id in issues_authored.keys():
            if bool(issues_authored[issue_id]["assignee"]): #False if dict is empty
                total_issues_with_assginee += 1
                if bool(issues_authored[issue_id]["body"]) and any(word in issues_authored[issue_id]["body"] for word in dbs.keywords_db()[1]):               
                    count_bugs_assigned = count_bugs_assigned + 1
                    issue_id_list.append(issue_id)
                else:
                    for item in range(len(issues_authored[issue_id]["labels"])):
                        if any(word in issues_authored[issue_id]["labels"][item]["name"] for word in dbs.keywords_db()[1]):
                            count_bugs_assigned = count_bugs_assigned + 1
                            issue_id_list.append(issue_id)
                
        return count_bugs_assigned, total_issues_with_assginee, issue_id_list

    def resolved_time(self, issues_authored):
        '''
        Returns the time difference between the assignment of a bug and its closure
        '''
        issues_dict = {}
        time_diff = []
        not_closed_bugs = 0
        for issue_id in issues_authored.keys():
            if issue_id in self.bug_assigned(issues_authored)[2]:
                if bool(issues_authored[issue_id]["closed_at"]):
                    issues_dict[issue_id] = {}
                    issues_dict[issue_id]["created_at"] = issues_authored[issue_id]["created_at"]
                    issues_dict[issue_id]["closed_at"] = issues_authored[issue_id]["closed_at"]

                    open_time = datetime.datetime.strptime(issues_authored[issue_id]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                    close_time = datetime.datetime.strptime(issues_authored[issue_id]["closed_at"],'%Y-%m-%dT%H:%M:%SZ')
                    a = relativedelta( close_time,open_time).months, relativedelta(close_time,open_time).days, \
                    relativedelta(close_time,open_time).minutes, relativedelta(close_time,open_time).seconds
                    issues_dict[issue_id]["time_diff"] = a
                    time_diff.append(a)
                else:
                    not_closed_bugs = not_closed_bugs + 1
                                    

        return issues_dict, time_diff, not_closed_bugs

    def assigned_label(self, issues_authored):
        '''
        Returns the amount of labels assigned to issues authored by the user. This is assumed to be the same number of labels assigned 
        by the user since there is no "created_by" in labels
        '''
        count_labels = 0
        
        for issue_id in issues_authored.keys():
            if bool(issues_authored[issue_id]["labels"]): #False if dict is empty
                count_labels = count_labels + 1

        return count_labels

    def assign_milestone(self, user_name, issues_authored):
        '''
        Returns the total amount of milestones that all issues authored by the user have and how many were assigned by the user
        '''
        total_milestones = 0
        milestones_authored_by_user = 0
       
        for issue_id in issues_authored.keys():
            if bool(issues_authored[issue_id]["milestone"]):
                if issues_authored[issue_id]["milestone"]["creator"]["login"]==user_name:
                    milestones_authored_by_user = milestones_authored_by_user + 1
                total_milestones = total_milestones +1
                
        return total_milestones, milestones_authored_by_user

    def project_comments(self, user_name, issue_comments, commit_authored_comments):
        '''
        Returns the amount of comments made by the user that include a project management keyword in them
        '''
        
        dbs = Databases()
        cm = Communication()
        comments = cm.user_comments(user_name, issue_comments, commit_authored_comments)[1]
        comments_project = 0
        total_comments = 0
        for issue_id in comments["comments_on_issues"].keys():
            for comment_id in comments["comments_on_issues"][issue_id].keys():
                body = comments["comments_on_issues"][issue_id][comment_id]["body"]
                total_comments = total_comments + 1
                if any(word in body for word in dbs.keywords_db()[0]):
                    comments_project = comments_project + 1


        for issue_id in comments["commnents_on_committs"].keys():
            for comment_id in comments["commnents_on_committs"][issue_id].keys():
                body = comments["commnents_on_committs"][issue_id][comment_id]["body"]
                total_comments = total_comments + 1
                if any(word in body for word in dbs.keywords_db()[0]):
                    comments_project = comments_project + 1


        return comments_project, total_comments
