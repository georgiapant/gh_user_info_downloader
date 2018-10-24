import sys
from properties import (dataFolderPath,  packageFolderPath)
sys.path.insert(0, packageFolderPath) 
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
        This function returns a dictionary with keys the amount of subscripitons, amount of the people that started the repo 
        and as items a list of the amounts per repository.
        '''
        
        ghd = GithubDownloader(GitHubAuthToken)
        list_url = self.get_list_of_repos_urls(dataFolderPath,user_name)
        stats = {}
        subscribers = []
        stargazers = []
        forks = []
        for item in list_url:
            url = "https://api.github.com/repos" +"/"+ '/'.join(item.split('/')[-2:])
            r = ghd.download_request(url)
            r_dict = json.loads(r.text)
            subscribers.append(r_dict["subscribers_count"])
            stargazers.append(r_dict["stargazers_count"])
            forks.append(r_dict["forks_count"])

        stats["subscribers_count"]= subscribers
        stats["stargazers_count"]=stargazers
        stats["forks_count"]= forks
        return stats

    '''
    def get_avg_popularity_preference(self, stats):
        """
        HERE CAN BE DONE THE PROCESSING OF THE POPULARITY --> MAYBE WITH CLUSTERING?

        This function gets as input the statistics of a repository as they are formated from the project_popularity_stats()
        and return the average of each statistic. This average includes possible extremes and maybe the output isn't completly representable
        of the popularity of the project the user prefers.

        TRY GETTING THE MEDIAN
        """
        average_preference = {}
        subscribers = []
        forks = []
        stars = []

        for key in stats.keys():
            subscribers = (stats[key]["subscribers_count"] + subscribers)/2
            forks = (stats[key]["forks_count"] + forks)/2
            stars = (stats[key]["stargazers_count"] + stars)/2

        average_preference["avg_subscribers_count"] = subscribers
        average_preference["avg_forks_count"] = forks
        average_preference["avg_stargazers_count"] = stars
        return average_preference
    '''
    def project_scale_stats(self, dataFolderPath,user_name):
        '''
        This function returns a dictionary with keys the name of each repository and as values another dictionary with items the 
        amount of commits, amount of contributors and the amount of releases.
        '''
        list_url = self.get_list_of_repos_urls(dataFolderPath,user_name)
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

    '''
    def get_avg_scale_preference(self, stats):
        """
        HERE CAN BE DONE THE PROCESSING OF THE SCALE --> MAYBE WITH CLUSTERING?

        This function gets as input the statistics of a repository as they are formated from the project_scale_stats()
        and return the average of each statistic. This average includes possible extremes and maybe the output 
        isn't completly representable of the scale of the project the user prefers.
        """
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
    '''


user_name='nbriz'
pp= Project_preferences() 
stats = pp.project_scale_stats(dataFolderPath, user_name)
#avg_pref = get_avg_scale_preference(stats)
fm = FileManager()
#fm.write_json_to_file(dataFolderPath + "/" + user_name +"/project_preferences_commits_avg.json", avg_pref)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/project_preferences_scale.json", stats)

