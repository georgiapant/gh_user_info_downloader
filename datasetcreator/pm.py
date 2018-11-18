import datetime
import json
import sys
from properties import (GitHubAuthToken, dataFolderPath, packageFolderPath)
sys.path.insert(0, packageFolderPath) 
from dateutil.relativedelta import relativedelta
from datamanager.filemanager import FileManager
from datasetcreator.communication import Communication
from downloader.githubdownloader import GithubDownloader
from datasetcreator.list_of_repos_urls import List_of_repos_urls

'''
Class that includes functions that are related to project management skills
'''

class Project_management(FileManager):
    
    
    def keywords_db(self):
        project_words = ["plan","timeline","project", "sprint", "risk", "resources", "agile" , "progress", "cost", "planning", "budget", "analysis", \
        "business model" , "value", "communication", "task", "task manager", "complete", "constraint", "stakeholders", "customer", "critical success factor", \
        "KPI", "effort", "impact", "XP", "goal setting", "goal" , "HR"]
        bug_words = ["bug", "error","defect","debug", "faulty", "problem", "trial", "try", "tried","solve", "solution", "fix", "fixed", "issue", \
        "wrong", "mistake", "issues"]
        test_words = ["test", "defect", "test case", "testing", "debugging", "expected result", "fat", "fault injection", "maintenance"\
        "quality", "QA", "quality assurance", "re-testing", "risk", "scenario", "tpi"]

        return project_words, bug_words, test_words

    def bug_assigned(self, dataFolderPath, user_name):
        issues_authored = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")

        count_issues = 0
        issue_id_list = []
        for issue_id in issues_authored.keys():
            if bool(issues_authored[issue_id]["assignee"]): #False if dict is empty
                if any(word in issues_authored[issue_id]["body"] for word in self.keywords_db()[1]):               
                    count_issues = count_issues + 1
                    issue_id_list.append(issue_id)
                else:
                    for item in range(len(issues_authored[issue_id]["labels"])):
                        if any(word in issues_authored[issue_id]["labels"][item]["name"] for word in self.keywords_db()[1]):
                            count_issues = count_issues + 1
                            issue_id_list.append(issue_id)
                
        return count_issues, issue_id_list

    def resolved_time(self, dataFolderPath, user_name):
        issues_authored = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")
        issues_dict = {}
        time_diff = []
        not_closed_bugs = 0
        for issue_id in issues_authored.keys():
            if issue_id in self.bug_assigned(dataFolderPath,user_name)[1]:
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

    def assigned_label(self, dataFolderPath, user_name):
        issues_authored = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")
        count_labels = 0
        total_issues_authored = len(issues_authored.keys())
        
        for issue_id in issues_authored.keys():
            if bool(issues_authored[issue_id]["labels"]): #False if dict is empty
                count_labels = count_labels + 1

        return count_labels, total_issues_authored

    def assign_milestone(self, dataFolderPath, user_name):
        issues_authored = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")
        total_milestones = 0
        milestones_authored_by_user = 0
        total_issues_authored = len(issues_authored.keys())
        
        for issue_id in issues_authored.keys():
            if bool(issues_authored[issue_id]["milestone"]) and issues_authored[issue_id]["milestone"]["creator"]["login"]==user_name:
                milestones_authored_by_user = milestones_authored_by_user + 1
            elif bool(issues_authored[issue_id]["milestone"]):
                total_milestones = total_milestones +1
                
        return total_milestones, milestones_authored_by_user, total_issues_authored

    def project_comments(self, dataFolderPath, user_name):
        cm = Communication()
        comments = cm.user_comments(dataFolderPath,user_name)[1]
        comments_project = 0
        total_comments = 0
        for issue_id in comments["comments_on_issues"].keys():
            for comment_id in comments["comments_on_issues"][issue_id].keys():
                body = comments["comments_on_issues"][issue_id][comment_id]["body"]
                total_comments = total_comments + 1
                if any(word in body for word in self.keywords_db()[0]):
                    comments_project = comments_project + 1


        for issue_id in comments["commnents_on_committs"].keys():
            for comment_id in comments["commnents_on_committs"][issue_id].keys():
                body = comments["commnents_on_committs"][issue_id][comment_id]["body"]
                total_comments = total_comments + 1
                if any(word in body for word in self.keywords_db()[0]):
                    comments_project = comments_project + 1


        return comments_project, total_comments
'''
Method that aims to count the amount of merges done by the user

def amount_of_merges(dataFolderPath, user_name):
    ghd = GithubDownloader(GitHubAuthToken)
    ls = List_of_repos_urls()
    list_url = ls.get_list_of_repos_urls(dataFolderPath,user_name)
    headers = {}
    pull_merged = 0
    headers["Accept"]="application/vnd.github.symmetra-preview+json"
    headers['Authorization'] = 'token ' + GitHubAuthToken
    parameters = "?state=all"

    for item in list_url:
        url = "https://api.github.com/repos" +"/"+ '/'.join(item.split('/')[-2:])+"/merges"
        r = requests.get(url+parameters, headers=headers)
        ghd.set_request_number(r.headers['x-ratelimit-remaining'], r.headers['x-ratelimit-reset'])
        r_dict = json.loads(r.text)
        
        if bool(r_dict):
            break
    return r_dict

import requests
user_name = 'nbriz'

fm = FileManager()

test = amount_of_merges(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/amount_of_merges.json", test) 
#print(test) 
'''