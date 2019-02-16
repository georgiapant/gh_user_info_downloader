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


'''
This class contains functions that return:
-> when they mostly work (days of the week) 
-> frequency of activities (committs/day - issues/day - comments/day - total_activities/day)
-> Time between creation and closure of an issue by the user (both) 
-> time between the assignment of an issue to the user and the closure of the issue 
-> time between two committs of the same developer
-> time between pull request and merge 
-> deploy rate 
-> # projects per day 
-> Duration a repository is active
'''
class Productivity(FileManager,GithubDownloader):
    
    
    def issue_commits_activities_freq(self,  user_name, commit_committed, commit_authored, issues_authored, issue_comments, commit_authored_comments): #committs per day, issues per day
        '''
        This function shows the frequency of commits authored, issues authored and comments made by the user per day
        Also, it merges the commits,issues and comments to activities per day

        It returns 
        - a dictionary that includes in detail (date: amount of activity) the commits per day, issues per day and comments per day,
        - a dictionary that includes the activities per day in detail
        - also tuple that includes 4 lists with the counts of each activity
        '''
        cm = Communication()
        committs_per_day = {}
        issues_per_day = {}
        comments_per_day = {}
        activities_per_day = {}
        issue_commits_comments_freq = {}

        count_issues = []
        count_commits = []
        count_comments = []
        count_activities_per_day = []
        commit_ids = []
        
        comments_by_user = cm.user_comments(user_name, issue_comments, commit_authored_comments)[1]

        for element_id in commit_authored.keys():
            commit_ids.append(element_id)
            date_str = commit_authored[element_id]["commit"]["author"]["date"]
            date = date_str.split('T')
            try:
                committs_per_day[date[0]] = committs_per_day[date[0]] + 1
            except:
                committs_per_day[date[0]] = 1


        for element_id in commit_committed.keys():
            if element_id not in commit_ids:
                date_str = commit_committed[element_id]["commit"]["author"]["date"]
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
            
            if bool(issues_authored[element_id]["closed_at"]):
                if bool(issues_authored[element_id]["closed_by"]) and issues_authored[element_id]["closed_by"]["login"] == user_name:
                    date_str =issues_authored[element_id]["closed_at"]
                    date = date_str.split('T')
                    try:
                        issues_per_day[date[0]] = issues_per_day[date[0]] + 1
                    except:
                        issues_per_day[date[0]] = 1
       
        
        for issue_id in comments_by_user["comments_on_issues"].keys():
            for comment_id in comments_by_user["comments_on_issues"][issue_id].keys():
                try:
                    date_str= comments_by_user["comments_on_issues"][issue_id][comment_id]["created_at"]
                    date = date_str.split('T')
                    try:
                        comments_per_day[date[0]] = comments_per_day[date[0]] + 1
                    except:
                        comments_per_day[date[0]] = 1

                except KeyError:
                    continue


        for issue_id in comments_by_user["commnents_on_committs"].keys():
            for comment_id in comments_by_user["commnents_on_committs"][issue_id].keys():
                try:
                    date_str= comments_by_user["commnents_on_committs"][issue_id][comment_id]["created_at"]
                    date = date_str.split('T')
                    try:
                        comments_per_day[date[0]] = comments_per_day[date[0]] + 1
                    except:
                        comments_per_day[date[0]] = 1

                except KeyError:
                    continue
                
       
        issue_commits_comments_freq["issues_per_day"] = issues_per_day
        issue_commits_comments_freq["committs_per_day"] = committs_per_day
        issue_commits_comments_freq["comments_per_day"] = comments_per_day

        #make lists out of the dictionaries for processing

        for key in issue_commits_comments_freq["issues_per_day"].keys():
        	count_issues.append(issue_commits_comments_freq["issues_per_day"][key])

        for key in issue_commits_comments_freq["committs_per_day"].keys():
        	count_commits.append(issue_commits_comments_freq["committs_per_day"][key])
        
        for key in issue_commits_comments_freq["comments_per_day"].keys():
        	count_comments.append(issue_commits_comments_freq["comments_per_day"][key])
        
        #Merging commits per day, issues per day and comments per day to make activities per day
        
        activities_per_day = committs_per_day

        for key in issues_per_day.keys():
            if key in activities_per_day.keys():
                activities_per_day[key] = activities_per_day[key]+issues_per_day[key]
            else:
                activities_per_day[key] = issues_per_day[key]

        for key in comments_per_day.keys():
            if key in activities_per_day.keys():
                activities_per_day[key] = activities_per_day[key]+comments_per_day[key]
            else:
                activities_per_day[key] = comments_per_day[key]
        
        # make the list of activities per day
         
        for key in activities_per_day.keys():
            count_activities_per_day.append(activities_per_day[key])


        issues_commits_activities_list = (count_issues, count_commits, count_comments, count_activities_per_day)
        return  issues_commits_activities_list, activities_per_day, issue_commits_comments_freq
    
    def contribution_days(self, activities_per_day):
        activities = activities_per_day
        days_contriburion = {}
        weekday = []
        for key in activities.keys():
            date = datetime.datetime.strptime(key,'%Y-%m-%d')
            weekday.append(calendar.day_name[date.weekday()])

        days_contriburion["total_days_worked"] = len(weekday)
        weekday = Counter(weekday)

        for item in weekday.keys():
            days_contriburion[item] = weekday[item]
        
        return days_contriburion

    def create_close_issue_diff(self,user_name, issues_authored):
        '''
        Time difference between the creation of an issue by the user and its closure. 
        This function also returns the amount of still open issues and the amount of issues closed by another user
        '''
        
        created_closed_diff = []
        create_close = {}
        closed_by_user = 0
        closed_by_other = 0
        still_open = 0

        for element_id in issues_authored.keys():
            if bool(issues_authored[element_id]["closed_at"]):
                if bool(issues_authored[element_id]["closed_by"]) and issues_authored[element_id]["closed_by"]["login"]== user_name:
                    date_created = datetime.datetime.strptime(issues_authored[element_id]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                    date_closed = datetime.datetime.strptime(issues_authored[element_id]["closed_at"],'%Y-%m-%dT%H:%M:%SZ')
                    
                    a = (date_closed-date_created).total_seconds()

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

        create_close_tuple = (still_open, closed_by_user, closed_by_other)

        return create_close, create_close_tuple

    def assign_close_issue_diff(self,  user_name, issues_assigned):
        
        assigned_closed_diff = []
        closed_issue = 0
        still_open = 0
        closed_by_user = 0
        assign_close = {}
        for element_id in issues_assigned.keys():
            if bool(issues_assigned[element_id]["closed_at"]):
                date_created = datetime.datetime.strptime(issues_assigned[element_id]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                date_closed = datetime.datetime.strptime(issues_assigned[element_id]["closed_at"],'%Y-%m-%dT%H:%M:%SZ') 
                a = (date_closed-date_created).total_seconds()
                assigned_closed_diff.append(a)
                closed_issue = closed_issue + 1
                if bool(issues_assigned[element_id]["closed_by"]) and issues_assigned[element_id]["closed_by"]["login"]== user_name:
                    closed_by_user = closed_by_user + 1
            else:
                still_open = still_open + 1
        closed_by_other = closed_issue - closed_by_user
        assign_close["still_open_issues"] = still_open
        assign_close["closed_issue"] = closed_issue
        assign_close["closed_by_other"] = closed_by_other
        assign_close["closed_by_user"] = closed_by_user
        assign_close["create_close_diff"] = assigned_closed_diff

        assign_close_tuple = (still_open, closed_by_user, closed_by_other, closed_issue)
        return assign_close, assign_close_tuple

    def commit_time_diff(self, commit_committed):
        '''
        This function takes the committs committed by a user and returns the difference between two consecutive committs
        '''
        
        dates_list = []

        for element_id in commit_committed.keys():
            date_str =  commit_committed[element_id]["commit"]["committer"]["date"]
            date_committed = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            dates_list.append(date_committed)
        
        dates_list.sort()
        dates = [(commit_2-commit_1).total_seconds() for commit_1, commit_2 in zip(dates_list[:-1], dates_list[1:])]
       
        return dates


    def pull_merge_diff(self, dataFolderPath, user_name):
        '''
        This function checks all pulls made by the user in all repositories the user has contributed and keeps the time bettween 
        the pull request and its merge
        '''
        
        list_url = self.read_json_from_file(dataFolderPath + "/" + user_name +"/list_of_repos.json")
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
                try:
                    if bool(r_dict[item]["user"]["login"]) and r_dict[item]["user"]["login"] == user_name:
                        if bool(r_dict[item]["merged_at"]):
                            date_created_str =  r_dict[item]["created_at"]
                            date_created = datetime.datetime.strptime(date_created_str, '%Y-%m-%dT%H:%M:%SZ')
                            date_merged_str =  r_dict[item]["merged_at"]
                            date_merged= datetime.datetime.strptime(date_merged_str, '%Y-%m-%dT%H:%M:%SZ')
                            diff = (date_merged-date_created).total_seconds()     
                            diff_list.append(diff)               
                            pull_merged = pull_merged + 1
                        elif bool(r_dict[item]["closed_at"]):
                            pull_closed_not_merged = pull_closed_not_merged + 1
                        else:
                            pull_open = pull_open +1
                        pulls_total = pulls_total + 1
                except:
                    continue
        pulls["pull_merged"] = pull_merged
        pulls["pull_closed_not_merged"] = pull_closed_not_merged
        pulls["pull_open"] = pull_open
        pulls["pulls_total"] = pulls_total
        pulls["pull_merge_diff"] = diff_list 
        
        pulls_tuple = (pulls_total, pull_merged, pull_closed_not_merged, pull_open )
        return pulls, pulls_tuple

    def deploy_rate(self, dataFolderPath, user_name):
        '''
        This function checks all the repos the user contributes and saves the difference between deploys, if there are any
        and when the repo was created, when it was last updated and the difference between those dates.
        This can be used for deploy rate.
        '''
        
        url_list = self.read_json_from_file(dataFolderPath + "/" + user_name +"/list_of_repos.json")
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
                dates = [(deploy_2-deploy_1).total_seconds() for deploy_1, deploy_2 in zip(dates_list[:-1], dates_list[1:])]
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


    def projects_per_day(self,commit_authored, issues_authored):
        
        projects_per_day = {}
        count = []
            
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

        for key in projects_per_day.keys():
        	count.append(projects_per_day[key]["count"])
        
        projects_per_day_short = {}
        for key in projects_per_day.keys():
            projects_per_day_short[key] = projects_per_day[key]["count"]

        return  projects_per_day, count, projects_per_day_short