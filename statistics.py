from datamanager.dbmanager import DBManager
from datamanager.filemanager import FileManager
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose, packageFolderPath
from helpers import get_number_of
from logger.downloadlogger import Logger
from downloader.gitdownloader import GitDownloader
from downloader.githubdownloader import GithubDownloader
from datasetcreator.list_of_repos_urls import List_of_repos_urls
from datasetcreator.languages import Languages
from datasetcreator.pm import Project_management
from datasetcreator.project_preferences import Project_preferences
from datasetcreator.productivity import Productivity

import os
import json
import codecs
import sys
import traceback
'''
The final code that will be executable to create the dataset
'''

ghd = GithubDownloader(GitHubAuthToken)
lg = Logger(verbose)
gd = GitDownloader(gitExecutablePath, lg)
db= DBManager()


def create_dataset(user_address):

    user_api_address = "https://api.github.com/users/" + '/'.join(user_address.split('/')[-1:])
    user_name = '_'.join(user_address.split('/')[-1:])

	
    project = db.read_project_from_disk(user_name)
    lr_url = List_of_repos_urls()
    productivity = Productivity(GitHubAuthToken)
    
    try:
        lg.start_action("Retrieving user statistics ...", 3)

        user_stats = {}
        user_stats["repos"] = get_number_of(ghd, user_api_address, "repos") #including the forked ones
        lg.step_action()
        user_stats["followers"] = get_number_of(ghd, user_api_address, "followers")
        lg.step_action()
        user_stats["repo_urls"] = lr_url.get_list_of_repos_urls(dataFolderPath, user_name)
        lg.step_action()
        
        



        project.add_user_stats(user_stats)
        lg.end_action()
        db.write_project_user_stats_to_disk(user_name, project["user_stats"])
    
    except Exception:
		# Catch any exception and print it before exiting
	    sys.exit(traceback.format_exc())
    finally:
		# This line of code is always executed even if an exception occurs
	    db.finalize_write_to_disk(user_name, project)