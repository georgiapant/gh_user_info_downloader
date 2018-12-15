# import sys
# from properties import (dataFolderPath,  packageFolderPath)
# sys.path.insert(0, packageFolderPath) 
# # import json
# from datamanager.filemanager import FileManager
from downloader.githubdownloader import GithubDownloader
from helpers import get_number_of
from list_of_repos_urls import List_of_repos_urls
# from properties import (GitHubAuthToken, dataFolderPath, gitExecutablePath,verbose)


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

