import sys
from properties import (GitHubAuthToken, dataFolderPath,  packageFolderPath)
sys.path.insert(0, packageFolderPath) 
from datamanager.filemanager import FileManager
from downloader.githubdownloader import GithubDownloader
import json
import datetime
import calendar
import requests
from dateutil.relativedelta import relativedelta
from collections import Counter
from datasetcreator.communication import Communication
from datasetcreator.list_of_repos_urls import List_of_repos_urls

'''
This class contains functions that return:
-> when they mostly work (days of the week) 
-> frequency of activities (committs/day - issues/day)
-> Time between creation and closure of an issue by the user (both) 
-> time between the assignment of an issue to the user and the closure of the issue 
-> time between two committs of the same developer
-> time between pull request and merge 
-> deploy rate 
-> # projects per day 
-> Duration a repository is active
'''
class Productivity(FileManager,GithubDownloader):
    
    def contribution_days(self,dataFolderPath, user_name):
        '''
        This function takes the days the user made an action. These actions can be: 
        - a committ committed
        - a committ authored 
        - an issue create by the user
        - an issue closed by the user
        - a comment made by the user
        and returns the amount of activities per day of the week
        '''
        cm = Communication()
        weekday = []
        days_contribution = {} 
        commit_committed = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_committed","sha")
        commit_authored=self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
        issues_authored= self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")
        comments_by_user = cm.user_comments(dataFolderPath,user_name)[1]

        for element_id in commit_committed.keys():
            date_str = commit_committed[element_id]["commit"]["committer"]["date"]
            date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ') 
            weekday.append(calendar.day_name[date.weekday()])
            #print(weekday)
        
        for element_id in commit_authored.keys():
            date_str = commit_authored[element_id]["commit"]["author"]["date"]
            date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ') 
            weekday.append(calendar.day_name[date.weekday()])
        
        
        for element_id in issues_authored.keys():
            date_str = issues_authored[element_id]["created_at"]
            date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            weekday.append(calendar.day_name[date.weekday()])
            
            if bool(issues_authored[element_id]["closed_at"]):
                if issues_authored[element_id]["closed_by"]["login"] == user_name:
                    date_str = issues_authored[element_id]["closed_at"]
                    date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                    weekday.append(calendar.day_name[date.weekday()])
            
        for issue_id in comments_by_user["comments_on_issues"].keys():
                for comment_id in comments_by_user["comments_on_issues"][issue_id].keys():
                    date_str= comments_by_user["comments_on_issues"][issue_id][comment_id]["created_at"]
                    date = datetime.datetime.strptime(date_str,'%Y-%m-%dT%H:%M:%SZ')
                    weekday.append(calendar.day_name[date.weekday()])


        for issue_id in comments_by_user["commnents_on_committs"].keys():
                for comment_id in comments_by_user["commnents_on_committs"][issue_id].keys():
                    date_str= comments_by_user["commnents_on_committs"][issue_id][comment_id]["created_at"]
                    date = datetime.datetime.strptime(date_str,'%Y-%m-%dT%H:%M:%SZ')
                    weekday.append(calendar.day_name[date.weekday()])
        
        days_contribution["total_days_worked"] = len(weekday)
        weekday = Counter(weekday)

        for item in weekday.keys():
            days_contribution[item] = weekday[item]
        
        return days_contribution

    def activities_frequency(self, dataFolderPath, user_name): #committs per day, issues per day
        '''
        This function shows the frequency of commits authored and issues authored by the user per day
        '''
        commit_authored=self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
        issues_authored= self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")
        
        committs_per_day = {}
        issues_per_day = {}
        activities_freq = {}

        for element_id in commit_authored.keys():
            date_str = commit_authored[element_id]["commit"]["author"]["date"]
            date = date_str.split('T')
            try:
                committs_per_day[date[0]] = committs_per_day[date[0]] + 1
            except:
                committs_per_day[date[0]] = 1
        
        for element_id in issues_authored.keys():
            date_str = issues_authored[element_id]["created_at"]
            date = date_str.split('T')
            try:
                issues_per_day[date[0]] = issues_per_day[date[0]] + 1
            except:
                issues_per_day[date[0]] = 1
        
        activities_freq["issues_per_day"] = issues_per_day
        activities_freq["committs_per_day"] = committs_per_day
        
        return activities_freq

    def create_close_issue_diff(self,dataFolderPath,user_name):
        issues_authored = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")
        created_closed_diff = []
        create_close = {}
        closed_by_user = 0
        closed_by_other = 0
        still_open = 0

        for element_id in issues_authored.keys():
            if bool(issues_authored[element_id]["closed_at"]):
                if issues_authored[element_id]["closed_by"]["login"]== user_name:
                    date_created = datetime.datetime.strptime(issues_authored[element_id]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                    date_closed = datetime.datetime.strptime(issues_authored[element_id]["closed_at"],'%Y-%m-%dT%H:%M:%SZ') 
                    a = relativedelta( date_closed,date_created).months, relativedelta(date_closed, date_created).hours, relativedelta(date_closed, date_created).days, \
                    relativedelta(date_closed, date_created).minutes, relativedelta(date_closed, date_created).seconds
                    created_closed_diff.append(a)
                    closed_by_user = closed_by_user + 1
                else:
                    closed_by_other = closed_by_other + 1
            else:
                still_open = still_open + 1
        create_close["still_open_issues"] = still_open
        create_close["closed_by_other"] = closed_by_other
        create_close["closed_by_user"] = closed_by_user
        create_close["create_close_diff"] = created_closed_diff

        return create_close

    def assign_close_issue_diff(self, dataFolderPath, user_name):
        issues_assigned = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_assigned", "id")
        assigned_closed_diff = []
        closed_issue = 0
        still_open = 0
        closed_by_user = 0
        assign_close = {}
        for element_id in issues_assigned.keys():
            if bool(issues_assigned[element_id]["closed_at"]):
                date_created = datetime.datetime.strptime(issues_assigned[element_id]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                date_closed = datetime.datetime.strptime(issues_assigned[element_id]["closed_at"],'%Y-%m-%dT%H:%M:%SZ') 
                a = relativedelta( date_closed,date_created).months, relativedelta(date_closed, date_created).days, \
                relativedelta(date_closed, date_created).minutes, relativedelta(date_closed, date_created).seconds
                assigned_closed_diff.append(a)
                closed_issue = closed_issue + 1
                if issues_assigned[element_id]["closed_by"]["login"]== user_name:
                    closed_by_user = closed_by_user + 1
            else:
                still_open = still_open + 1
        assign_close["still_open_issues"] = still_open
        assign_close["closed_issue"] = closed_issue
        assign_close["closed_by_user"] = closed_by_user
        assign_close["create_close_diff"] = assigned_closed_diff

        return assign_close

    def commit_time_diff(self, dataFolderPath,user_name):
        '''
        This function takes the committs committed by a user and returns the difference between two consecutive committs
        '''
        commit_committed = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_committed","sha")
        dates_list = []

        for element_id in commit_committed.keys():
            date_str =  commit_committed[element_id]["commit"]["committer"]["date"]
            date_committed = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            dates_list.append(date_committed)
        
        dates_list.sort()
        dates = [(relativedelta(commit_2,commit_1).years, relativedelta(commit_2,commit_1).months, \
        relativedelta(commit_2, commit_1).days, relativedelta(commit_2, commit_1).hours, relativedelta(commit_2, commit_1).minutes,\
        relativedelta(commit_2, commit_1).seconds) for commit_1, commit_2 in zip(dates_list[:-1], dates_list[1:])]
        return dates


    def pull_merge_diff(self, dataFolderPath, user_name):
        '''
        This function checks all pulls made by the user in all repositories the user has contributed and keeps the time bettween 
        the pull request and its merge
        '''
        ls = List_of_repos_urls()
        list_url = ls.get_list_of_repos_urls(dataFolderPath,user_name)
        diff_list = []
        headers = {}
        pull_merged = 0
        pull_closed_not_merged = 0
        pull_open = 0
        pulls_total = 0
        pulls = {}
        headers["Accept"]="application/vnd.github.symmetra-preview+json"
        headers['Authorization'] = 'token ' + GitHubAuthToken
        parameters = "?state=all"
        for item in list_url:
            url = "https://api.github.com/repos" +"/"+ '/'.join(item.split('/')[-2:])+"/pulls"
            r = requests.get(url+parameters, headers=headers)
            self.set_request_number(r.headers['x-ratelimit-remaining'], r.headers['x-ratelimit-reset'])
            r_dict = json.loads(r.text)
            
            for item in range(len(r_dict)):
                if r_dict[item]["user"]["login"] == user_name:
                    if bool(r_dict[item]["merged_at"]):
                        date_created_str =  r_dict[item]["created_at"]
                        date_created = datetime.datetime.strptime(date_created_str, '%Y-%m-%dT%H:%M:%SZ')
                        date_merged_str =  r_dict[item]["merged_at"]
                        date_merged= datetime.datetime.strptime(date_merged_str, '%Y-%m-%dT%H:%M:%SZ')
                        diff= (relativedelta(date_merged,date_created).years, relativedelta(date_merged,date_created).months, \
                        relativedelta(date_merged, date_created).days, relativedelta(date_merged, date_created).hours, \
                        relativedelta(date_merged, date_created).minutes, relativedelta(date_merged, date_created).seconds)
                        diff_list.append(diff)                    
                        pull_merged = pull_merged + 1
                    elif bool(r_dict[item]["closed_at"]):
                        pull_closed_not_merged = pull_closed_not_merged + 1
                    else:
                        pull_open = pull_open +1
                    pulls_total = pulls_total + 1

        pulls["pull_merged"] = pull_merged
        pulls["pull_closed_not_merged"] = pull_closed_not_merged
        pulls["pull_open"] = pull_open
        pulls["pulls_total"] = pulls_total
        pulls["pull_merge_diff"] = diff_list  

        return pulls

    def deploy_rate(self, dataFolderPath, user_name):
        '''
        This function checks all the repos the user contributes and saves the difference between deploys, if there are any
        and when the repo was created, when it was last updated and the difference between those dates.
        This can be used for deploy rate.
        '''
        ls = List_of_repos_urls()
        url_list = ls.get_list_of_repos_urls(dataFolderPath,user_name)
        headers = {}
        deploy_dates = {}
        headers["Accept"]="application/vnd.github.ant-man-preview+json"
        headers['Authorization'] = 'token ' + GitHubAuthToken

        for item in url_list:
            dates_list = []
            
            url = "https://api.github.com/repos" +"/"+ '/'.join(item.split('/')[-2:])+"/deployments"
            r = requests.get(url, headers=headers)
            self.set_request_number(r.headers['x-ratelimit-remaining'], r.headers['x-ratelimit-reset'])
            r_dict = json.loads(r.text)
            if bool(r_dict):
                deploy_dates[url] = {}
                for i in range(len(r_dict)):
                    
                    date_str =  r_dict[i]["created_at"]
                    date_created = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                    dates_list.append(date_created)
                    
                dates_list.sort()
                dates = [(relativedelta(deploy_2,deploy_1).years, relativedelta(deploy_2,deploy_1).months, \
                relativedelta(deploy_2, deploy_1).days, relativedelta(deploy_2, deploy_1).hours, relativedelta(deploy_2, deploy_1).minutes,\
                relativedelta(deploy_2, deploy_1).seconds) for deploy_1, deploy_2 in zip(dates_list[:-1], dates_list[1:])]
                deploy_dates[url]["dates_diff"]=dates

                #to get how long this repo is active

                active_dur = self.repo_active_dur(item)
                deploy_dates[url]["repo_created_at"]=active_dur[0]
                deploy_dates[url]["repo_last_updated_at"]=active_dur[1]
                deploy_dates[url]["repo_active_dur"]=active_dur[2]
                    
        return deploy_dates

    def repo_active_dur(self, repo_url):
        '''
        This function returns how long the repository is active. Meaning the difference between its creation and its last update
        '''

        headers = {}
        headers["Accept"]="application/vnd.github.ant-man-preview+json"
        headers['Authorization'] = 'token ' + GitHubAuthToken
        
        url = "https://api.github.com/repos" +"/"+ '/'.join(repo_url.split('/')[-2:])
        r = requests.get(url, headers=headers)
        self.set_request_number(r.headers['x-ratelimit-remaining'], r.headers['x-ratelimit-reset'])
        r_dict = json.loads(r.text)
        repo_created_at = r_dict["created_at"]
        repo_last_updated_at = r_dict["updated_at"]
        date_created = datetime.datetime.strptime(repo_created_at, '%Y-%m-%dT%H:%M:%SZ')
        date_last_updated= datetime.datetime.strptime(repo_last_updated_at, '%Y-%m-%dT%H:%M:%SZ')

        diff= (relativedelta(date_last_updated,date_created).years, relativedelta(date_last_updated,date_created).months, \
        relativedelta(date_last_updated, date_created).days, relativedelta(date_last_updated, date_created).hours, \
        relativedelta(date_last_updated, date_created).minutes, relativedelta(date_last_updated, date_created).seconds)

        repo_active_dur = diff  
        return repo_created_at, repo_last_updated_at, repo_active_dur


    def projects_per_day(self,dataFolderPath, user_name):
        commit_authored=self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
        issues_authored= self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")
        
        projects_per_day = {}
            
        for element_id in commit_authored.keys():
            
            date_str = commit_authored[element_id]["commit"]["author"]["date"]
            date = date_str.split('T')
            project = '/'.join(commit_authored[element_id]["url"].split('/')[:-2])
            try:
                if project not in projects_per_day[date[0]]["project_list"]:
                    projects_per_day[date[0]]["count"] = projects_per_day[date[0]]["count"] + 1
                    
                    projects_per_day[date[0]]["project_list"].append(project)
            except:
                projects_per_day[date[0]] = {}
                projects_per_day[date[0]]["count"] = 1
                projects_per_day[date[0]]["project_list"] = []
                projects_per_day[date[0]]["project_list"].append(project)
        
        for element_id in issues_authored.keys():
            date_str = issues_authored[element_id]["created_at"]
            date = date_str.split('T')
            project = '/'.join(issues_authored[element_id]["url"].split('/')[:-2])
            try:
                if date[0] in projects_per_day.keys():
                    if project not in projects_per_day[date[0]]["project_list"]:
                        projects_per_day[date[0]]["count"] = projects_per_day[date[0]]["count"] + 1
                        projects_per_day[date[0]]["project_list"].append(project)
            except:              
                projects_per_day[date[0]] = {}
                projects_per_day[date[0]]["count"] = 1
                projects_per_day[date[0]]["project_list"] = []
                projects_per_day[date[0]]["project_list"].append(project)
        return  projects_per_day


#test = pr.projects_per_day(dataFolderPath,user_name)

#fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/projects_per_day_new.json", test) 
#test1 = pull_merge_diff(dataFolderPath,user_name)[1]
#fm.write_json_to_file(dataFolderPath + "/" + user_name +"/pull_requests.json", test1) 
#print(test) 

