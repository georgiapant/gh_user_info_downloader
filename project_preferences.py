import json
from datamanager.filemanager import FileManager
from downloader.githubdownloader import GithubDownloader
from helpers import get_number_of
from list_of_repos_urls import List_of_repos_urls
from properties import (GitHubAuthToken, dataFolderPath, gitExecutablePath,verbose)


'''
Take the list of repos he has contributed
make a request for each repo and take wathers, subscribers and forks of each project
make additional requests for amount of contributors, realeases and commits
'''

class Project_preferences(List_of_repos_urls):
    
    def project_popularity_stats(self, dataFolderPath,user_name):
        '''
        This function returns a dictionary with keys the name of each repository and as values another dictionary with items the 
        amount of subscripitons, amount of the people that started the repo and the amount of the forks done.
        '''
        ghd = GithubDownloader(GitHubAuthToken)
        list_url = self.get_list_of_repos_urls(dataFolderPath,user_name)
        stats = {}
        for item in list_url:
            url = "https://api.github.com/repos" +"/"+ '/'.join(item.split('/')[-2:])
            r = ghd.download_request(url)
            r_dict = json.loads(r.text)
            stats[item]= {}
            stats[item]["subscribers_count"]= r_dict["subscribers_count"]
            stats[item]["stargazers_count"]=r_dict["stargazers_count"]
            stats[item]["forks_count"]= r_dict["forks_count"]
        return stats


    def get_avg_popularity_preference(self, stats):
        '''
        This function gets as input the statistics of a repository as they are formated from the project_popularity_stats()
        and return the average of each statistic. This average includes possible extremes and maybe the output isn't completly representable
        of the popularity of the project the user prefers.
        '''
        average_preference = {}
        subscribers = 0
        forks = 0
        stars = 0

        for key in stats.keys():
            subscribers = (stats[key]["subscribers_count"] + subscribers)/2
            forks = (stats[key]["forks_count"] + forks)/2
            stars = (stats[key]["stargazers_count"] + stars)/2

        average_preference["avg_subscribers_count"] = subscribers
        average_preference["avg_forks_count"] = forks
        average_preference["avg_stargazers_count"] = stars
        return average_preference

    def project_scale_stats(self, dataFolderPath,user_name):
        '''
        This function returns a dictionary with keys the name of each repository and as values another dictionary with items the 
        amount of commits, amount of contributors and the amount of releases.
        '''
        list_url = self.get_list_of_repos_urls(dataFolderPath,user_name)
        ghd = GithubDownloader(GitHubAuthToken)
        stats = {}
        for item in list_url:
            url = "https://api.github.com/repos" +"/"+ '/'.join(item.split('/')[-2:])
            commits = get_number_of(ghd, url, "commits")
            contributors = get_number_of(ghd, url, "contributors")
            realeases = get_number_of(ghd, url, "releases") 
            stats[item]= {}
            stats[item]["amount_of_commits"]=commits
            stats[item]["amount_of_contributors"] = contributors
            stats[item]["amount_of_releases"] = realeases
        return stats

    def get_avg_scale_preference(self, stats):
        '''
        This function gets as input the statistics of a repository as they are formated from the project_scale_stats()
        and return the average of each statistic. This average includes possible extremes and maybe the output 
        isn't completly representable of the scale of the project the user prefers.
        '''
        average_preference = {}
        commits = 0
        contributors = 0
        releases = 0

        for key in stats.keys():
            commits = (stats[key]["amount_of_commits"] + commits)/2
            contributors = (stats[key]["amount_of_contributors"] + contributors)/2
            releases = (stats[key]["amount_of_releases"] + releases)/2

        average_preference["avg_amount_of_commits"] = commits
        average_preference["avg_amount_of_contributors"] = contributors
        average_preference["avg_amount_of_releases"] = releases
        
        return average_preference
