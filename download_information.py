import os
import sys
import traceback
from logger.downloadlogger import Logger
from datamanager.dbmanager import DBManager
from downloader.gitdownloader import GitDownloader
from downloader.githubdownloader import GithubDownloader
from helpers import get_number_of, print_usage, read_file_in_lines, get_total_count
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose, \
download_commits_authored, download_commits_committed, download_issues_assigned, \
download_issues_authored, download_issues_mentions, download_issues_commented, \
download_issues_owened, download_repositories_owned 

db = DBManager()
lg = Logger(verbose)
ghd = GithubDownloader(GitHubAuthToken)
gd = GitDownloader(gitExecutablePath, lg)

def download_information(user_address):

	user_api_address = "https://api.github.com/users/" + '/'.join(user_address.split('/')[-1:])
	user_name = '_'.join(user_address.split('/')[-1:])

	db.initialize_write_to_disk(user_name)

	project = db.read_project_from_disk(user_name)

	try:
		lg.log_action("Downloading user information " + user_name)

		# Download the json file with the info of the user
		
		if project.user_info_exists():
			lg.log_action("User already exists! Updating...")
		user_info = ghd.download_object(user_api_address)
		project.add_user_info(user_info)
		db.write_project_user_info_to_disk(user_name, project["user_info"])
		
		
		lg.start_action("Retrieving user statistics ...", 15)
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
		
		user_stats["commit_authored"] = get_total_count(ghd, user_name, 'commits?q=author:', "state=all")
		lg.step_action()
		user_stats["commit_committed"] = get_total_count(ghd, user_name, 'commits?q=committer:', "state=all")
		lg.step_action()
		user_stats["issues_assigned"] = get_total_count(ghd, user_name, 'issues?q=assignee:', "state=all")
		lg.step_action()
		user_stats["issues_authored"] = get_total_count(ghd, user_name, 'issues?q=author:', "state=all")
		lg.step_action()
		user_stats["issues_mentions"] = get_total_count(ghd, user_name, 'issues?q=mentions:', "state=all")
		lg.step_action()
		user_stats["issues_commented"] = get_total_count(ghd, user_name, 'issues?q=commenter:', "state=all")
		lg.step_action()
		user_stats["issues_owned"] = get_total_count(ghd, user_name, 'issues?q=user:', "state=all")
		lg.step_action()
		user_stats["repositories_owned"] = get_total_count(ghd, user_name, 'repositories?q=user:', "state=all")
		lg.step_action()
		project.add_user_stats(user_stats)
		lg.end_action()
		db.write_project_user_stats_to_disk(user_name, project["user_stats"])


		if download_commits_authored:
			lg.start_action("Retrieving committs authored by user...", user_stats["commit_authored"])
			committs_authored_by_user_address = "https://api.github.com/search/commits?q=author:" + user_name

			for commit_authored in ghd.download_paginated_object(committs_authored_by_user_address):
				if not project.commit_authored_exists(commit_authored):
					project.add_commit_authored(commit_authored)
					db.write_project_commit_authored_to_disk(user_name, commit_authored)
				lg.step_action()
			lg.end_action()

		if download_commits_committed:
			lg.start_action("Retrieving committs committed by user...", user_stats["commit_committed"])
			committs_committed_by_user_address = "https://api.github.com/search/commits?q=committer:" + user_name

			for commit_committed in ghd.download_paginated_object(committs_committed_by_user_address):
				if not project.commit_committed_exists(commit_committed):
					project.add_commit_committed(commit_committed)
					db.write_project_commit_committed_to_disk(user_name, commit_committed)
				lg.step_action()
			lg.end_action()

		if download_issues_assigned:
			lg.start_action("Retrieving issues assigned to user...", user_stats["issues_assigned"])
			issues_assigned_to_user_address = "https://api.github.com/search/issues?q=assignee:" + user_name

			for issue_assigned in ghd.download_paginated_object(issues_assigned_to_user_address):
				if not project.issue_assigned_exists(issue_assigned):
					project.add_issue_assigned(issue_assigned)
					db.write_project_issue_assigned_to_disk(user_name, issue_assigned)
				lg.step_action()
			lg.end_action()

		if download_issues_authored:
			lg.start_action("Retrieving issues authored by user...", user_stats["issues_authored"])
			issues_authored_from_user_address = "https://api.github.com/search/issues?q=author:" + user_name

			for issue_authored in ghd.download_paginated_object(issues_authored_from_user_address):
				if not project.issue_authored_exists(issue_authored):
					project.add_issue_authored(issue_authored)
					db.write_project_issue_authored_to_disk(user_name, issue_authored)
				lg.step_action()
			lg.end_action()	

		if download_issues_mentions:
			lg.start_action("Retrieving issues that mention the user...", user_stats["issues_mentions"])
			issues_mentions_user_address = "https://api.github.com/search/issues?q=mentions:" + user_name

			for issue_mentions in ghd.download_paginated_object(issues_mentions_user_address):
				if not project.issue_mentions_exists(issue_mentions):
					project.add_issue_mentions(issue_mentions)
					db.write_project_issue_mentions_to_disk(user_name, issue_mentions)
				lg.step_action()
			lg.end_action()	

		if download_issues_commented:
			lg.start_action("Retrieving issues commented by the user...", user_stats["issues_commented"])
			issues_commented_by_user_address = "https://api.github.com/search/issues?q=commenter:" + user_name

			for issues_commented in ghd.download_paginated_object(issues_commented_by_user_address):
				if not project.issue_commented_exists(issues_commented):
					project.add_issue_commented(issues_commented)
					db.write_project_issue_commented_to_disk(user_name, issues_commented)
				lg.step_action()
			lg.end_action()	

		if download_issues_owened:
			lg.start_action("Retrieving issues owned by the user...", user_stats["issues_owned"])
			issues_owned_by_user_address = "https://api.github.com/search/issues?q=user:" + user_name

			for issues_owned in ghd.download_paginated_object(issues_owned_by_user_address):
				if not project.issue_owned_exists(issues_owned):
					project.add_issue_owned(issues_owned)
					db.write_project_issue_owned_to_disk(user_name, issues_owned)
				lg.step_action()
			lg.end_action()	

		if download_repositories_owned:
			lg.start_action("Retrieving repositories owned by the user...", user_stats["repositories_owned"])
			repositories_owned_by_user_address = "https://api.github.com/search/repositories?q=user:" + user_name

			for repos_owned in ghd.download_paginated_object(repositories_owned_by_user_address):
				if not project.repositories_owned_exists(repos_owned):
					project.add_repositories_owned(repos_owned)
					db.write_project_repos_owned_to_disk(user_name, repos_owned)
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
