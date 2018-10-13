#user info downloader that uses all modified gddownloader code

import os
import sys
import traceback
from logger.downloadlogger import Logger
from datamanager.dbmanager import DBManager
from downloader.gitdownloader import GitDownloader
from downloader.githubdownloader import GithubDownloader
from helpers import get_number_of, print_usage, read_file_in_lines
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose, \
	download_user_repos

# Initialize all required objects
db = DBManager()
lg = Logger(verbose)
ghd = GithubDownloader(GitHubAuthToken)
gd = GitDownloader(gitExecutablePath, lg)

def download_user(user_address):
	"""
	Downloads all the data of a user given its GitHub URL.

	:param user_address: the URL of the user of which the data are downloaded.
	"""
	user_api_address = "https://api.github.com/users/" + '/'.join(user_address.split('/')[-1:])
	user_name = '_'.join(user_address.split('/')[-1:])

	db.initialize_write_to_disk(user_name)

	project = db.read_project_from_disk(user_name)

	try:
		lg.log_action("Downloading user " + user_name)

		# Download the json file with the info of the user
		
		if project.user_info_exists():
			lg.log_action("User already exists! Updating...")
		user_info = ghd.download_object(user_api_address)
		project.add_user_info(user_info)
		db.write_project_user_info_to_disk(user_name, project["user_info"])
	
		#download statistics about the user (outside of the ones existing in the user info)

		lg.start_action("Retrieving user statistics ...", 7)
		user_stats = {}
		user_stats["repos"] = get_number_of(ghd, user_api_address, "repos", "state=all")
		lg.step_action()
		user_stats["followers"] = get_number_of(ghd, user_api_address, "followers")
		lg.step_action()
		user_stats["following"] = get_number_of(ghd, user_api_address, "following")
		lg.step_action()
		user_stats["starred"] = get_number_of(ghd, user_api_address, "starred")
		lg.step_action()
		user_stats["organisations"] = get_number_of(ghd, user_api_address, "orgs")
		lg.step_action()
		user_stats["events"] = get_number_of(ghd, user_api_address, "events")
		lg.step_action()
		user_stats["received_event"] = get_number_of(ghd, user_api_address, "received_event")
		lg.step_action()
		project.add_user_stats(user_stats)
		lg.end_action()
		db.write_project_user_stats_to_disk(user_name, project["user_stats"])
	
		if download_user_repos:
			lg.start_action("Retrieving user repositories...", user_stats["repos"])
			user_repos_address = user_api_address + "/repos"
			
			#for repo in ghd.download_paginated_object(user_repos_address, ["state=all"]):

			for user_repo in ghd.download_paginated_object(user_repos_address):
				if not project.user_repo_exists(user_repo):
					project.add_user_repo(user_repo)
					db.write_project_user_repo_to_disk(user_name, user_repo)
				lg.step_action()
			lg.end_action()

	except Exception:
		# Catch any exception and print it before exiting
		sys.exit(traceback.format_exc())
	finally:
		# This line of code is always executed even if an exception occurs
		db.finalize_write_to_disk(user_name, project)

if __name__ == "__main__":
	if ((not sys.argv) or len(sys.argv) <= 1):
		print_usage()
	elif(sys.argv[1].startswith("https://github.com")): #here it goes if we use just one URL
		download_user(sys.argv[1])
	elif(os.path.exists(sys.argv[1])):	#here it goes if we have as input a txt with URLs
		users = read_file_in_lines(sys.argv[1])
		for user in users:
			download_user(user)
	else:
		print_usage()

