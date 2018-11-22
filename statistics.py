from datamanager.dbmanager import DBManager
from datamanager.filemanager import FileManager
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose, packageFolderPath
from helpers import get_number_of, get_total_count
from logger.downloadlogger import Logger
from downloader.gitdownloader import GitDownloader
from downloader.githubdownloader import GithubDownloader

from datasetcreator.languages import Languages
from datasetcreator.pm import Project_management
from datasetcreator.project_preferences import Project_preferences
from datasetcreator.productivity import Productivity
from datasetcreator.activeness import time_active
from datasetcreator.communication import Communication

import os
import json
import codecs
import sys
import traceback
'''
The final code that will be executable to gather the final statistics to create the dataset
'''

ghd = GithubDownloader(GitHubAuthToken)
lg = Logger(verbose)
gd = GitDownloader(gitExecutablePath, lg)
db= DBManager()


def create_dataset(user_address):

	user_api_address = "https://api.github.com/users/" + '/'.join(user_address.split('/')[-1:])
	user_name = '_'.join(user_address.split('/')[-1:])

	
	project = db.read_project_from_disk(user_name)

	productivity = Productivity(GitHubAuthToken, user_name)
	cm = Communication()
	lan = Languages()
	pm = Project_management(dataFolderPath,user_name)
	pp = Project_preferences()

	try:
		lg.start_action("Retrieving user statistics ...", 31)

		user_stats = {}

		user_stats["repos"] = get_number_of(ghd, user_api_address, "repos") #including the forked ones
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
		user_stats["commit_authored"] = get_total_count(ghd, user_name, 'commits?q=author:')
		lg.step_action()
		user_stats["commit_committed"] = get_total_count(ghd, user_name, 'commits?q=committer:')
		lg.step_action()
		user_stats["issues_assigned"] = get_total_count(ghd, user_name, 'issues?q=assignee:')
		lg.step_action()
		user_stats["issues_authored"] = get_total_count(ghd, user_name, 'issues?q=author:')
		lg.step_action()
		user_stats["issues_mentions"] = get_total_count(ghd, user_name, 'issues?q=mentions:')
		lg.step_action()
		user_stats["issues_commented"] = get_total_count(ghd, user_name, 'issues?q=commenter:')
		lg.step_action()
		user_stats["issues_owned"] = get_total_count(ghd, user_name, 'issues?q=user:')
		lg.step_action()
		user_stats["repositories_owned"] = get_total_count(ghd, user_name, 'repositories?q=user:') #doesn't include the forked ones
		lg.step_action()
		user_stats["contribution_days"] = productivity.contribution_days(dataFolderPath,user_name) 
		lg.step_action()
		user_stats["activities_frequency"] = productivity.activities_frequency(dataFolderPath,user_name)
		lg.step_action()
		user_stats["create_close_issue_diff"] = productivity.create_close_issue_diff(dataFolderPath,user_name)
		lg.step_action()
		user_stats["assign_close_issue_diff"] = productivity.assign_close_issue_diff(dataFolderPath,user_name)
		lg.step_action()
		user_stats["commit_time_diff"] = productivity.commit_time_diff(dataFolderPath,user_name)
		lg.step_action()
		user_stats["pull_merge_diff"] = productivity.pull_merge_diff(dataFolderPath,user_name)
		lg.step_action()
		user_stats["projects_per_day"] = productivity.projects_per_day(dataFolderPath,user_name)
		lg.step_action()
		user_stats["time_active"] = time_active(dataFolderPath,user_name)
		lg.step_action()
		user_stats["comment_length"] = cm.comment_length(dataFolderPath,user_name)
		lg.step_action()
		user_stats["number_of_comment_answers"] = cm.number_of_comment_answers(dataFolderPath,user_name)
		lg.step_action()
		user_stats["count_languages"] = lan.count_languages(dataFolderPath,user_name)
		lg.step_action()
		user_stats["amount_of_bugs_assigned"] = pm.bug_assigned(dataFolderPath,user_name)[0]
		lg.step_action()
		user_stats["amount_assigned_labels_by_user_&_total_labels_assigned"] = pm.assigned_label(dataFolderPath,user_name)
		lg.step_action()
		user_stats["comments_with_project_mgmt_reference_&_total_amount_of_comments_by_user"] = pm.project_comments(dataFolderPath,user_name)
		lg.step_action()
		user_stats["project_popularity_stats"] = pp.project_popularity_stats(dataFolderPath,user_name)
		lg.step_action()
		user_stats["project_scale_stats"] = pp.project_scale_stats(dataFolderPath,user_name)
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


