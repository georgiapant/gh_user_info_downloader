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
from datasetcreator.testing import add_test_case,test_comments,closed_issues
from datasetcreator.commits import files_in_commits, commit_changes, empty_commit_message, bug_fixing_contribution
from datasetcreator.operational import documentation_comments, documentation_commit
from analysis import list_stats, additions_deletions_stats, time_diff
import pandas

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

	productivity = Productivity(dataFolderPath, user_name)
	cm = Communication()
	lan = Languages()
	pm = Project_management(dataFolderPath,user_name)
	pp = Project_preferences()
	
	try:
		lg.start_action("Retrieving user statistics ...", 53)

		user_stats = {}

		user_stats["repos_contributed"] = get_number_of(ghd, user_api_address, "repos") #including the forked ones
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

		user_stats["total_commits_authored"] = get_total_count(ghd, user_name, 'commits?q=author:')
		lg.step_action()
		user_stats["total_commits_committed"] = get_total_count(ghd, user_name, 'commits?q=committer:')
		lg.step_action()
		user_stats["total_issues_assigned_to_the_user"] = get_total_count(ghd, user_name, 'issues?q=assignee:')
		lg.step_action()
		user_stats["total_issues_created/authored_by_the_user"] = get_total_count(ghd, user_name, 'issues?q=author:')
		lg.step_action()
		user_stats["total_issues_mentions user"] = get_total_count(ghd, user_name, 'issues?q=mentions:')
		lg.step_action()
		user_stats["total_issues_commented by user"] = get_total_count(ghd, user_name, 'issues?q=commenter:')
		lg.step_action()
		user_stats["total_issues_owned by user"] = get_total_count(ghd, user_name, 'issues?q=user:')
		lg.step_action()
		user_stats["repositories_owned"] = get_total_count(ghd, user_name, 'repositories?q=user:') #doesn't include the forked ones
		lg.step_action()

		user_stats["amount_of_activities_done_per_day_of_the_week"] = productivity.contribution_days(dataFolderPath,user_name) 
		lg.step_action()

		#user_stats["activities_frequency"] = list_stats(productivity.activities_frequency(dataFolderPath,user_name),['activities_frequency'])
		#lg.step_action()
		user_stats["commits_frequency"] = list_stats([productivity.activities_frequency(dataFolderPath,user_name)[2]],['commits_frequency'])['commits_frequency'].to_dict()
		lg.step_action()
		user_stats["issues_frequency"] = list_stats([productivity.activities_frequency(dataFolderPath,user_name)[1]], ['issues_frequency'])['issues_frequency'].to_dict()
		lg.step_action()


		user_stats["issue_created_by_user_closed_by_user_time_diff"] = time_diff(productivity.create_close_issue_diff(user_name)['create_close_diff']).to_dict()
		lg.step_action()
		user_stats["amount_of_issues_created_by_the_user_still_open"] = productivity.create_close_issue_diff(user_name)['still_open_issues']
		lg.step_action()
		user_stats["amount_of_issues_created_by_the_user_closed_by_user"] = productivity.create_close_issue_diff(user_name)['closed_by_user']
		lg.step_action()
		user_stats["amount_of_issues_created_by_the_user_closed_by_other_user"] = productivity.create_close_issue_diff(user_name)['closed_by_other']
		lg.step_action()

		user_stats["issue_assigned_to_user_and_closed_by_user_time_diff"] = time_diff(productivity.assign_close_issue_diff(dataFolderPath,user_name)["create_close_diff"]).to_dict()
		lg.step_action()
		user_stats["amount_of_issues_assigned_to_the_user_still_open"] = productivity.assign_close_issue_diff(dataFolderPath,user_name)["still_open_issues"]
		lg.step_action()
		user_stats["amount_of_issues_assigned_to_the_user_closed_by_the_user"] = productivity.assign_close_issue_diff(dataFolderPath,user_name)["closed_by_user"]
		lg.step_action()
		user_stats["amount_of_issues_assigned_to_the_user_closed_by_other_user"] = productivity.assign_close_issue_diff(dataFolderPath,user_name)["closed_by_other"]
		lg.step_action()
		user_stats["amount_of_issues_assigned_to_the_user_that_are_closed"] = productivity.assign_close_issue_diff(dataFolderPath,user_name)["closed_issue"]
		lg.step_action()


		user_stats["time_diff_between_consequtive_commiits_committed_by_user"] = time_diff(productivity.commit_time_diff(dataFolderPath,user_name)).to_dict()
		lg.step_action()

		user_stats["pull_merge_diff"] = time_diff(productivity.pull_merge_diff(dataFolderPath,user_name)["pull_merge_diff"]).to_dict()
		lg.step_action()
		user_stats["total_pull_request_done_by_the_user"] = productivity.pull_merge_diff(dataFolderPath,user_name)["pulls_total"]
		lg.step_action()
		user_stats["amount_of_pull_request_done_by_the_user_were_merged"] = productivity.pull_merge_diff(dataFolderPath,user_name)["pull_merged"]
		lg.step_action()
		user_stats["amount_of_pull_request_done_by_the_user_were_closed_not_merged"] = productivity.pull_merge_diff(dataFolderPath,user_name)["pull_closed_not_merged"]
		lg.step_action()
		user_stats["amount_of_pull_request_done_by_the_user_still_open"] = productivity.pull_merge_diff(dataFolderPath,user_name)["pull_open"]
		lg.step_action()
		

		user_stats["projects_per_day"] = list_stats([productivity.projects_per_day(dataFolderPath,user_name)[1]], ['projects_per_day'])['projects_per_day'].to_dict()
		lg.step_action()

		user_stats["time_active - (y,m,d)"] = time_active(dataFolderPath,user_name)
		lg.step_action()

		user_stats["comment_length"] = list_stats([cm.comment_length(dataFolderPath,user_name)], ['comment_length'])['comment_length'].to_dict()
		lg.step_action()
		user_stats["number_of_comment_answers"] = list_stats([cm.number_of_comment_answers(dataFolderPath,user_name)],['number_of_comment_answers'])['number_of_comment_answers'].to_dict()
		lg.step_action()

		user_stats["amount_of_files_committed_per_language"] = lan.count_languages(dataFolderPath,user_name)
		lg.step_action()

		user_stats["total_issues_with_bug_keyword_assigned_to_someone_by_the_user"] = pm.bug_assigned(dataFolderPath,user_name)[0]
		lg.step_action()
		user_stats["total_issues_with_label_assigned_by_the_user"] = pm.assigned_label(dataFolderPath,user_name)[0]
		lg.step_action()
		user_stats["total_issues_with_milestone_assigned_by_the_user"] = pm.assign_milestone(dataFolderPath,user_name)[1]
		lg.step_action()
		user_stats["total_issues_created_by_user_with_milestone_assigned"] = pm.assign_milestone(dataFolderPath,user_name)[0]
		lg.step_action()

		user_stats["number_of_comments_with_project_mgmt_keywords"],user_stats["total_comments_made_by_user"]  = pm.project_comments(dataFolderPath,user_name)
		lg.step_action()
				
		user_stats["commit_changes_per_language"] = additions_deletions_stats(commit_changes(dataFolderPath,user_name)).to_dict()
		lg.step_action()
		user_stats["documentation_commit_changes"] = additions_deletions_stats(documentation_commit(dataFolderPath,user_name)[0]).to_dict()
		lg.step_action()

		user_stats["amount_of_files_changed_in_a_commit"] = list_stats([files_in_commits(dataFolderPath,user_name)],['files_in_commits'])['files_in_commits'].to_dict()
		lg.step_action()
		
		user_stats["amount_of_files_related_to_testing_committed_by_user"] = add_test_case(dataFolderPath,user_name)
		lg.step_action()
		
		user_stats["bug_word_in_commit_message/bug_fixing_contribution"] = bug_fixing_contribution(dataFolderPath,user_name)
		lg.step_action()
		
		user_stats["amount_of_comments_made_by_the_user_with_test_keyword"] = test_comments(dataFolderPath,user_name)[0]
		lg.step_action()
		user_stats["amount_of_comments_made_by_the_user_with_issue_number_reference"] = test_comments(dataFolderPath,user_name)[1]
		lg.step_action()
		user_stats["number_of_comments_with_documentation_keywords"] = documentation_comments(dataFolderPath,user_name)
		lg.step_action()

		user_stats["amount_of_issues_closed_by_user_with_bug_keyword"], user_stats["total_amount_of_issues_closed_by_user"] = closed_issues(dataFolderPath,user_name)
		lg.step_action()

		#user_stats["deploy_days_time_diff"] = productivity.deploy_rate(dataFolderPath,user_name)
		#lg.step_action()

		user_stats["project_popularity_stats"] = {"forks": list_stats([pp.project_popularity_stats(dataFolderPath,user_name)["forks_count"]],["forks"])["forks"].to_dict(),\
		"stargazers":list_stats([pp.project_popularity_stats(dataFolderPath,user_name)["stargazers_count"]],["stargazers"])["stargazers"].to_dict(),\
		"watchers":list_stats([pp.project_popularity_stats(dataFolderPath,user_name)["watchers_count"]],["watchers"])["watchers"].to_dict()}
		lg.step_action()
		
		user_stats["project_scale_stats"] = {"commits": list_stats([pp.project_scale_stats(dataFolderPath,user_name)["amount_of_commits"]],["commits"])["commits"].to_dict(),\
		"contributors":list_stats([pp.project_scale_stats(dataFolderPath,user_name)["amount_of_contributors"]],["contributors"])["contributors"].to_dict(),\
		"releases":list_stats([pp.project_scale_stats(dataFolderPath,user_name)["amount_of_releases"]],["releases"])["releases"].to_dict()}
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

create_dataset('https://github.com/nbriz')