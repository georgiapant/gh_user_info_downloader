from datamanager.dbmanager import DBManager
from datamanager.filemanager import FileManager
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose, packageFolderPath
from helpers import get_number_of, print_usage, read_file_in_lines, get_total_count
from logger.downloadlogger import Logger
from downloader.gitdownloader import GitDownloader
from downloader.githubdownloader import GithubDownloader

from datasetcreator.languages import Languages
from datasetcreator.pm import Project_management
from datasetcreator.project_preferences import Project_preferences
from datasetcreator.productivity import Productivity
from datasetcreator.activeness import time_active
from datasetcreator.communication import Communication
from datasetcreator.testing import Test
from datasetcreator.commits import Commits
from datasetcreator.operational import Operational
from analysis import list_stats, additions_deletions_stats, time_diff, activities_per_week, percentage_creation
from list_of_repos_urls import List_of_repos_urls
import pandas
import time

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
fm = FileManager()
productivity = Productivity(GitHubAuthToken)
cm = Communication()
lan = Languages()
pm = Project_management()
pp = Project_preferences()
commits = Commits()
testing = Test()
operational = Operational()
ls = List_of_repos_urls()



def create_dataset(user_address):
	start_time = time.time()

	#user_api_address = "https://api.github.com/users/" + '/'.join(user_address.split('/')[-1:])
	user_name = '_'.join(user_address.split('/')[-1:])
	
	db.initialize_write_to_disk(user_name)
	project = db.read_project_from_disk(user_name)

	
	#initialising all needed variables
	
	user_stats_initial = project["user_stats"]
	commit_committed = project["commit_committed"]
	commit_authored = project["commit_authored"]
	issues_authored = project["issues_authored"]
	issues_assigned = project["issues_assigned"]
	issues_commented = project["issues_commented"]
	issues_mentions = project["issues_mentions"]
	issues_owned = project["issues_owned"]
	issue_comments = project["issue_comments"]
	commit_authored_comments = project["commit_comments"]
	# print('here!')
	
	list_of_repos = ls.get_list_of_repos_urls(dataFolderPath, user_name, issues_assigned, issues_authored, issues_commented, issues_mentions, issues_owned, commit_authored, commit_committed)
	fm.write_json_to_file(dataFolderPath + "/" + user_name +"/list_of_repos.json", list_of_repos)
	
	try:
		lg.log_action("Creating dataset of " + user_name)
		lg.start_action("Retrieving user statistics ...", 30)

		user_dataset = {}
		user_dataset["described"] = {}
		user_dataset["normalised"] = {}
		user_dataset["time_diff"] = {}
		user_dataset["project_preference_info"] = {}
		user_dataset["commit_changes"] = {}
		user_dataset["raw_data"] = {}
		total_list = []

		for key in user_stats_initial.keys():
			user_dataset[key] = user_stats_initial[key]
		
		closed_bugs_count, closed_issues_count, list_bugs_per_day, bugs_per_day_long = testing.closed_issues(user_name, issues_authored, issues_assigned, issues_commented, issues_mentions, issues_owned)
		bugs_per_week = activities_per_week(bugs_per_day_long)[1]

		user_dataset["raw_data"]["amount_of_issues_closed_by_user_with_bug_keyword"] = closed_bugs_count
		user_dataset["raw_data"]["total_amount_of_issues_closed_by_user"] = closed_issues_count
	
	
		open_bugs_count, list_bugs_opened_per_day, bugs_opened_per_day = testing.opened_bugs(user_name,issues_authored)
		bugs_opened_per_week = activities_per_week(bugs_opened_per_day)[1]

		user_dataset["raw_data"]["amount_of_issues_created_by_the_user_with_bug_keyword"] = open_bugs_count
		

		activities_freq, issue_commits_comments_freq  = productivity.issue_commits_activities_freq(user_name, commit_committed, commit_authored, issues_authored, issue_comments, commit_authored_comments)[1:3]
		lg.step_action()
		
		list_count_commits_freq = activities_per_week(issue_commits_comments_freq["committs_per_day"])[1]
		list_count_issues_freq = activities_per_week(issue_commits_comments_freq["issues_per_day"])[1]
		list_count_comments_freq = activities_per_week(issue_commits_comments_freq["comments_per_day"])[1]
		list_count_activities_freq = activities_per_week(activities_freq)[1]

		projects_per_day, projects_per_day_long = productivity.projects_per_day(commit_authored, issues_authored)[1:3]
		lg.step_action()
		projects_per_week = activities_per_week(projects_per_day_long)[1]

		comment_length = cm.comment_length(user_name, issue_comments, commit_authored_comments)
		lg.step_action()
		number_of_comment_answers = cm.number_of_comment_answers(user_name, issue_comments)
		lg.step_action()
		amount_of_files_changed_in_a_commit = commits.files_in_commits(commit_authored)
		lg.step_action()

		total_list.extend((list_count_commits_freq,list_count_issues_freq, list_count_comments_freq, list_count_activities_freq, projects_per_day, projects_per_week, comment_length, number_of_comment_answers, amount_of_files_changed_in_a_commit, list_bugs_per_day, bugs_per_week, list_bugs_opened_per_day, bugs_opened_per_week))
		names = ['commits_frequency_per_week', 'issues_frequency_per_week','comments_frequency_per_week', 'activities_frequency_per_week' ,'projects_per_day', "projects_per_week",'comment_length', 'number_of_comment_answers','amount_of_files_changed_in_a_commit', 'bugs_resolved_per_day', 'bugs_resolved_per_week', 'bugs_opened_per_day', 'bugs_opened_per_week']
		out = list_stats(total_list, names)

		user_dataset["described"]["commits_frequency_per_week"] = out['commits_frequency_per_week'].to_dict()
		user_dataset["described"]["issues_frequency_per_week"] = out['issues_frequency_per_week'].to_dict()
		user_dataset["described"]["comments_frequency_per_week"] = out['comments_frequency_per_week'].to_dict()
		user_dataset["described"]["activities_frequency_per_week"] = out['activities_frequency_per_week'].to_dict()
		user_dataset["described"]["projects_per_day"] = out['projects_per_day'].to_dict()
		user_dataset["described"]["projects_per_week"] = out['projects_per_week'].to_dict()
		user_dataset["described"]["comment_length"] = out['comment_length'].to_dict()
		user_dataset["described"]["number_of_comment_answers"] = out['number_of_comment_answers'].to_dict()
		user_dataset["described"]["amount_of_files_changed_in_a_commit"] = out['amount_of_files_changed_in_a_commit'].to_dict()
		user_dataset["described"]["bugs_resolved_per_day"] = out["bugs_resolved_per_day"].to_dict()
		user_dataset["described"]['bugs_resolved_per_week'] = out['bugs_resolved_per_week'].to_dict()
		user_dataset["described"]["bugs_opened_per_day"] = out["bugs_opened_per_day"].to_dict()
		user_dataset["described"]['bugs_opened_per_week'] = out['bugs_opened_per_week'].to_dict()

		user_dataset["raw_data"]["amount_of_activities_done_per_day_of_the_week"] = productivity.contribution_days(activities_freq)
		lg.step_action()

		user_dataset["time_diff"]["issue_created_by_user_closed_by_user_time_diff"] = time_diff(productivity.create_close_issue_diff(user_name, issues_authored)[0]['create_close_diff']).to_dict()
		lg.step_action()
		user_dataset["raw_data"]["amount_of_issues_created_by_the_user_still_open"], user_dataset["raw_data"]["amount_of_issues_created_by_the_user_closed_by_user"], \
		user_dataset["raw_data"]["amount_of_issues_created_by_the_user_closed_by_other_user"] = productivity.create_close_issue_diff(user_name, issues_authored)[1]
		lg.step_action()		
		user_dataset["time_diff"]["issue_assigned_to_user_and_closed_by_user_time_diff"] = time_diff(productivity.assign_close_issue_diff(user_name, issues_assigned)[0]["create_close_diff"]).to_dict()
		lg.step_action()
		user_dataset["raw_data"]["amount_of_issues_assigned_to_the_user_still_open"],user_dataset["raw_data"]["amount_of_issues_assigned_to_the_user_closed_by_the_user"],\
		user_dataset["raw_data"]["amount_of_issues_assigned_to_the_user_closed_by_other_user"], user_dataset["raw_data"]["amount_of_issues_assigned_to_the_user_that_are_closed"] \
		= productivity.assign_close_issue_diff(user_name, issues_assigned)[1]
		lg.step_action()
		user_dataset["time_diff"]["time_diff_between_consequtive_commiits_committed_by_user"] = time_diff(productivity.commit_time_diff(commit_committed)).to_dict()
		lg.step_action()
		user_dataset["time_diff"]["pull_merge_diff"] = time_diff(productivity.pull_merge_diff(dataFolderPath,user_name)[0]["pull_merge_diff"]).to_dict()
		lg.step_action()
		user_dataset["raw_data"]["total_pull_request_done_by_the_user"],user_dataset["raw_data"]["amount_of_pull_request_done_by_the_user_were_merged"],\
		user_dataset["raw_data"]["amount_of_pull_request_done_by_the_user_were_closed_not_merged"], user_dataset["raw_data"]["amount_of_pull_request_done_by_the_user_still_open"]\
		= productivity.pull_merge_diff(dataFolderPath,user_name)[1]
		lg.step_action()
		user_dataset["raw_data"]["time_active - (y,m,d)"] = time_active(commit_committed)
		lg.step_action()
		user_dataset["raw_data"]["amount_of_files_committed_per_language"],user_dataset["raw_data"]["total_files_committed"]= lan.count_languages(commit_authored)
		lg.step_action()
		user_dataset["raw_data"]["total_issues_with_bug_keyword_assigned_to_someone_by_the_user"], user_dataset["raw_data"]["total_issues_assigned_to_someone_by_the_user"] = pm.bug_assigned(issues_authored)[0:2]
		lg.step_action()
		user_dataset["raw_data"]["total_issues_with_label_assigned_by_the_user"] = pm.assigned_label(issues_authored)
		lg.step_action()		
		user_dataset["raw_data"]["total_issues_created_by_user_with_milestone_assigned"], user_dataset["raw_data"]["total_issues_with_milestone_assigned_by_the_user"] = pm.assign_milestone(user_name, issues_authored)
		lg.step_action()
		user_dataset["raw_data"]["number_of_comments_with_project_mgmt_keywords"],user_dataset["raw_data"]["total_comments_made_by_user"]  = pm.project_comments(user_name, issue_comments, commit_authored_comments)
		lg.step_action()				
		user_dataset["commit_changes"]["commit_changes_per_language"] = additions_deletions_stats(commits.commit_changes(commit_authored)).to_dict()
		lg.step_action()
		user_dataset["commit_changes"]["documentation_commit_changes"] = additions_deletions_stats(operational.documentation_commit(commit_authored)[0]).to_dict()
		lg.step_action()
		user_dataset["raw_data"]["amount_of_files_related_to_testing_committed_by_user"]  = testing.add_test_case(commit_authored)
		lg.step_action()
		user_dataset["raw_data"]["bug_word_in_commit_message/bug_fixing_contribution"] = commits.bug_fixing_contribution(commit_authored)
		lg.step_action()
		user_dataset["raw_data"]["amount_of_comments_made_by_the_user_with_test_keyword"], user_dataset["raw_data"]["amount_of_comments_made_by_the_user_with_issue_number_reference"] = testing.test_comments(user_name, issue_comments, commit_authored_comments)[0]
		lg.step_action()		
		user_dataset["raw_data"]["number_of_comments_with_documentation_keywords"] = operational.documentation_comments( user_name, issue_comments, commit_authored_comments)
		lg.step_action()
		
		user_dataset["raw_data"]["count_of_empty_commit_messages"] = commits.empty_commit_message(commit_committed)
		lg.step_action()

		#THIS TAKES A LOT OF TIME - because it does requests to the API
		user_dataset["project_preference_info"]["project_popularity_stats"] = {"forks": list_stats([pp.project_popularity_stats(dataFolderPath,user_name)["forks_count"]],["forks"])["forks"].to_dict(),\
		"stargazers":list_stats([pp.project_popularity_stats(dataFolderPath,user_name)["stargazers_count"]],["stargazers"])["stargazers"].to_dict(),\
		"watchers":list_stats([pp.project_popularity_stats(dataFolderPath,user_name)["watchers_count"]],["watchers"])["watchers"].to_dict()}
		lg.step_action()
		
		user_dataset["project_preference_info"]["project_scale_stats"] = {"commits": list_stats([pp.project_scale_stats(dataFolderPath,user_name, GitHubAuthToken)["amount_of_commits"]],["commits"])["commits"].to_dict(),\
		"contributors":list_stats([pp.project_scale_stats(dataFolderPath,user_name, GitHubAuthToken)["amount_of_contributors"]],["contributors"])["contributors"].to_dict(),\
		"releases":list_stats([pp.project_scale_stats(dataFolderPath,user_name, GitHubAuthToken)["amount_of_releases"]],["releases"])["releases"].to_dict()}
		lg.step_action()
		#UNTIL HERE		

		#percentages creation
	
		user_dataset["normalised"]["percentage_of_testing_related_files_committed_by_the_user"] = percentage_creation(user_dataset["raw_data"]["amount_of_files_related_to_testing_committed_by_user"],user_dataset["commit_committed"])
		

		for key in user_dataset["raw_data"]["amount_of_files_committed_per_language"].keys():
			user_dataset["normalised"]["percentage_of_files_committed_in_" +key] = percentage_creation(user_dataset["raw_data"]["amount_of_files_committed_per_language"][key],user_dataset["raw_data"]["total_files_committed"])
		
		user_dataset["normalised"]["percentage_of_repos_the_user_contributed_that_he_owes"] = percentage_creation(user_dataset["repositories_owned"],user_dataset["repos"])
		user_dataset["normalised"]["percentage_of_empty_commit_messages"] = percentage_creation(user_dataset["raw_data"]["count_of_empty_commit_messages"],user_dataset["commit_committed"])
		user_dataset["normalised"]["percentage_of_commit_messages_with_bug_keyword"] = percentage_creation(user_dataset["raw_data"]["bug_word_in_commit_message/bug_fixing_contribution"],user_dataset["commit_committed"])
		user_dataset["normalised"]["percentage_of_comments_with_test_keyword"] = percentage_creation(user_dataset["raw_data"]["amount_of_comments_made_by_the_user_with_test_keyword"],user_dataset["raw_data"]["total_comments_made_by_user"])
		user_dataset["normalised"]["percentage_of_comments_with_documentation_keyword"] = percentage_creation(user_dataset["raw_data"]["number_of_comments_with_documentation_keywords"],user_dataset["raw_data"]["total_comments_made_by_user"])
		user_dataset["normalised"]["percentage_of_comments_with_project_management_keyword"] = percentage_creation(user_dataset["raw_data"]["number_of_comments_with_project_mgmt_keywords"],user_dataset["raw_data"]["total_comments_made_by_user"])
		user_dataset["normalised"]["percentage_of_comments_with_issue_number"] = percentage_creation(user_dataset["raw_data"]["amount_of_comments_made_by_the_user_with_issue_number_reference"],user_dataset["raw_data"]["total_comments_made_by_user"])
		user_dataset["normalised"]["percentage_of_issues_with_bug_keyword_assigned_by_the_user"] = percentage_creation(user_dataset["raw_data"]["total_issues_with_bug_keyword_assigned_to_someone_by_the_user"],user_dataset["raw_data"]["total_issues_assigned_to_someone_by_the_user"])
		user_dataset["normalised"]["percentage_of_issues_with_assigned_label"] = percentage_creation(user_dataset["raw_data"]["total_issues_with_label_assigned_by_the_user"],user_dataset["issues_authored"])
		user_dataset["normalised"]["percentage_of_issues_created_by_the_user_with_assigned_milestone"] = percentage_creation(user_dataset["raw_data"]["total_issues_created_by_user_with_milestone_assigned"],user_dataset["issues_authored"])
		user_dataset["normalised"]["percentage_of_issues_created_by_the_user_with_assigned_milestone_by_the_user"] = percentage_creation(user_dataset["raw_data"]["total_issues_with_milestone_assigned_by_the_user"],user_dataset["issues_authored"])
		user_dataset["normalised"]["percentage_of_issues_with_milestone_where_that_milestone_was_assigned_by_the_user"] = percentage_creation(user_dataset["raw_data"]["total_issues_with_milestone_assigned_by_the_user"],user_dataset["raw_data"]["total_issues_created_by_user_with_milestone_assigned"])
		user_dataset["normalised"]["percentage_of_issues_created_by_the_user_that_are_still_open"] = percentage_creation(user_dataset["raw_data"]["amount_of_issues_created_by_the_user_still_open"],user_dataset["issues_authored"])
		user_dataset["normalised"]["percentage_of_issues_created_by_the_user_closed_by_user"] = percentage_creation(user_dataset["raw_data"]["amount_of_issues_created_by_the_user_closed_by_user"],user_dataset["issues_authored"])
		user_dataset["normalised"]["percentage_of_issues_assigned_to_the_user_closed_by_user"] = percentage_creation(user_dataset["raw_data"]["amount_of_issues_assigned_to_the_user_closed_by_the_user"],user_dataset["issues_assigned"])
		user_dataset["normalised"]["percentage_of_issues_assigned_to_the_user_still_open"] = percentage_creation(user_dataset["raw_data"]["amount_of_issues_assigned_to_the_user_still_open"],user_dataset["issues_assigned"])
		user_dataset["normalised"]["percentage_of_issues_closed_by_the_user_with_bug_keyword"] = percentage_creation(user_dataset["raw_data"]["amount_of_issues_closed_by_user_with_bug_keyword"],user_dataset["raw_data"]["total_amount_of_issues_closed_by_user"])
		user_dataset["normalised"]["percentage_of_pull_requests_made_by_the_user_that_were_merged"] = percentage_creation(user_dataset["raw_data"]["amount_of_pull_request_done_by_the_user_were_merged"],user_dataset["raw_data"]["total_pull_request_done_by_the_user"])
		user_dataset["normalised"]["percentage_of_pull_requests_made_by_the_user_that_were_closed_not_merged"] = percentage_creation(user_dataset["raw_data"]["amount_of_pull_request_done_by_the_user_were_closed_not_merged"],user_dataset["raw_data"]["total_pull_request_done_by_the_user"])
		user_dataset["normalised"]["percentage_of_pull_requests_made_by_the_user_that_are_still_open"] = percentage_creation(user_dataset["raw_data"]["amount_of_pull_request_done_by_the_user_still_open"],user_dataset["raw_data"]["total_pull_request_done_by_the_user"])


		for key in user_dataset["raw_data"]["amount_of_activities_done_per_day_of_the_week"].keys():
			user_dataset["normalised"]["percentage_of_activities_per_"+ key] = percentage_creation(user_dataset["raw_data"]["amount_of_activities_done_per_day_of_the_week"][key],user_dataset["raw_data"]["amount_of_activities_done_per_day_of_the_week"]["total_days_worked"])


		project.add_user_dataset(user_dataset)
		lg.end_action()
		db.write_project_user_dataset_to_disk(user_name, project["user_dataset"])
		
	except Exception:
		# Catch any exception and print it before exiting
		sys.exit(traceback.format_exc())
	finally:
		# This line of code is always executed even if an exception occurs
		db.finalize_write_to_disk(user_name, project)
		print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
	if ((not sys.argv) or len(sys.argv) <= 1):
		print_usage()
	elif(sys.argv[1].startswith("https://github.com")): #here it goes if we use just one URL
		create_dataset(sys.argv[1])
	elif(os.path.exists(sys.argv[1])):	#here it goes if we have as input a txt with URLs
		users = read_file_in_lines(sys.argv[1])
		for user in users:
			create_dataset(user)
	else:
		print_usage()


#create_dataset('https://github.com/nbriz')