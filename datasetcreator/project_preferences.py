# import sys
# from properties import (dataFolderPath,  packageFolderPath)
# sys.path.insert(0, packageFolderPath) 
# # import json
from datamanager.filemanager import FileManager
from downloader.githubdownloader import GithubDownloader
from helpers import get_number_of
from list_of_repos_urls import List_of_repos_urls
from collections import Counter
from properties import GitHubAuthToken
import requests
import json


'''
Take the list of repos he has contributed
make a request for each repo and take wathers, subscribers and forks of each project
make additional requests for amount of contributors, realeases and commits
'''

class Project_preferences(List_of_repos_urls):
    
    def project_popularity_stats(self, dataFolderPath, user_name):
        '''
        This function returns a dictionary with keys the amount of subscripitons, amount of the people that started the repo 
        and as items a list of the amounts per repository.
        '''
        
        repos = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/repositories_owned","id")
        stats = {}
        watchers = []
        stargazers = []
        forks = []
        
        for repo_id in repos.keys():
            watchers.append(repos[repo_id]["watchers_count"])
            stargazers.append(repos[repo_id]["stargazers_count"])
            forks.append(repos[repo_id]["forks_count"])
        
        stats["watchers_count"]= watchers
        stats["stargazers_count"]=stargazers
        stats["forks_count"]= forks
        
        return stats

    def project_scale_stats(self, dataFolderPath,user_name, GitHubAuthToken):
        '''
        This function returns a dictionary with keys the name of each repository and as values another dictionary with items the 
        amount of commits, amount of contributors and the amount of releases.
        '''

        list_url = self.read_json_from_file(dataFolderPath + "/" + user_name +"/list_of_repos.json")
        ghd = GithubDownloader(GitHubAuthToken)
        stats = {}
        commits = []
        contributors = []
        realeases = []
        for item in list_url:
            url = "https://api.github.com/repos" +"/"+ '/'.join(item.split('/')[-2:])
            commits.append(get_number_of(ghd, url, "commits"))
            contributors.append(get_number_of(ghd, url, "contributors"))
            realeases.append(get_number_of(ghd, url, "releases")) 
            
        stats["amount_of_commits"]=commits
        stats["amount_of_contributors"] = contributors
        stats["amount_of_releases"] = realeases
        return stats


    

    def mostly_contributed_projects(self,GitHubAuthToken, commit_authored, issues_authored):
        ghd = GithubDownloader(GitHubAuthToken)
        project_list = []
        mostly_contributed_projects = {}
        
        for element_id in commit_authored.keys():
            project = '/'.join(commit_authored[element_id]["url"].split('/')[:-2])
            
            project_list.append(project)

        for element_id in issues_authored.keys():
            project = '/'.join(issues_authored[element_id]["url"].split('/')[:-2])
           
            project_list.append(project)
        
        project_occurance = Counter(project_list).most_common(3)
        list_url = []
        for item in project_occurance:
            list_url.append(item[0])
      
        for url in list_url:
            

            r = requests.get(url)
            content = json.loads(r.text or r.content)
            
            
            try:
                mostly_contributed_projects[url] = {}
                mostly_contributed_projects[url]["popularity_stats"] = {}
                mostly_contributed_projects[url]["scale_stats"] = {}
                
                mostly_contributed_projects[url]["popularity_stats"]["watchers_count"] = content["watchers_count"]
                mostly_contributed_projects[url]["popularity_stats"]["stargazers_count"] = content["stargazers_count"]
                mostly_contributed_projects[url]["popularity_stats"]["forks_count"] = content["forks_count"]

                mostly_contributed_projects[url]["scale_stats"]["amount_of_commits"] = get_number_of(ghd, url, "commits")
                mostly_contributed_projects[url]["scale_stats"]["amount_of_contributors"] = get_number_of(ghd, url, "contributors")
                mostly_contributed_projects[url]["scale_stats"]["amount_of_releases"] = get_number_of(ghd, url, "releases")
            except KeyError:
                continue
            
        return mostly_contributed_projects



'''
dataFolderPath  = "/Users/georgia/Desktop"
user_name = "nbriz"
pp = Project_preferences()
fm = FileManager()
commit_authored = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name +"/commit_authored", "sha")
issues_authored = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name +"/issues_authored", "id")

print(pp.mostly_contributed_projects(GitHubAuthToken, commit_authored, issues_authored))
'''