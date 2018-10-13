import os
import sys
import traceback
from logger.downloadlogger import Logger
from datamanager.dbmanager import DBManager
from downloader.gitdownloader import GitDownloader
from downloader.githubdownloader import GithubDownloader
from helpers import get_number_of, print_usage, read_file_in_lines, get_total_count
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose, \
download_commits_authored 

db = DBManager()
lg = Logger(verbose)
ghd = GithubDownloader(GitHubAuthToken)
gd = GitDownloader(gitExecutablePath, lg)
#headers={'Accept':'application/vnd.github.cloak-preview'}

def download_information(user_address):

	user_api_address = "https://api.github.com/users/" + '/'.join(user_address.split('/')[-1:])
	user_name = '_'.join(user_address.split('/')[-1:])

	db.initialize_write_to_disk(user_name)

	project = db.read_project_from_disk(user_name)

	try:
		lg.log_action("Downloading user information " + user_name)

		# Download the json file with the info of the user
		'''
		if project.user_info_exists():
			lg.log_action("User already exists! Updating...")
		user_info = ghd.download_object(user_api_address)
		project.add_user_info(user_info)
		db.write_project_user_info_to_disk(user_name, project["user_info"])
	
		'''
		lg.start_action("Retrieving user statistics ...", 7)
		user_stats = {}
		user_stats["commits_authored"] = get_total_count(ghd, user_name, 'commits?q=author:')
		lg.step_action()
		project.add_user_stats(user_stats)
		lg.end_action()
		db.write_project_user_stats_to_disk(user_name, project["user_stats"])
		print(user_stats["commits_authored"])



		if download_commits_authored:
			lg.start_action("Retrieving committs authored by user...", user_stats["commits_authored"])
			committs_authored_by_user_address = "https://api.github.com/search/commits?q=author:" + user_name

			for commit_authored in ghd.download_paginated_object(committs_authored_by_user_address):
				if not project.commit_authored_exists(commit_authored):
					project.add_commit_authored(commit_authored)
					db.write_project_commit_authored_to_disk(user_name, commit_authored)
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
		download_information(sys.argv[1])
	elif(os.path.exists(sys.argv[1])):	#here it goes if we have as input a txt with URLs
		users = read_file_in_lines(sys.argv[1])
		for user in users:
			download_information(user)
	else:
		print_usage()
