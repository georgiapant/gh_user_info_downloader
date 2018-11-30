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
from analysis import list_stats, additions_deletions_stats, time_diff
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

start_time = time.time()

def create_dataset(user_address):

	#user_api_address = "https://api.github.com/users/" + '/'.join(user_address.split('/')[-1:])
	user_name = '_'.join(user_address.split('/')[-1:])

	project = db.read_project_from_disk(user_name)

	db.initialize_write_to_disk(user_name)
	#initialising all needed variables
	'''
	commit_committed = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_committed","sha")
	commit_authored = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
	issues_authored = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")
	issues_assigned = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_assigned", "id")
	issues_commented = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_commented", "id")
	issues_mentions = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_mentions", "id")
	issues_owned = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_owned", "id")
	issue_comments = fm.read_comment_jsons_from_folder(dataFolderPath+"/"+ user_name + "/issue_comments")
	commit_authored_comments=fm.read_comment_jsons_from_folder(dataFolderPath+"/"+ user_name + "/commit_comments")
	commit_committed_comments = fm.read_comment_jsons_from_folder(dataFolderPath+"/"+ user_name + "/commit_comments")
	'''
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
	print('here!')
	
	try:
		lg.start_action("Retrieving user statistics ...", 30)

		user_dataset = {}
		total_list = []

		for key in user_stats_initial.keys():
			user_dataset[key] = user_stats_initial[key]
		'''
		user_dataset["repos_contributed"] = get_number_of(ghd, user_api_address, "repos") #including the forked ones
		lg.step_action()
		user_dataset["followers"] = get_number_of(ghd, user_api_address, "followers")
		lg.step_action()
		user_dataset["following"] = get_number_of(ghd, user_api_address, "following")
		lg.step_action()
		user_dataset["starred"] = get_number_of(ghd, user_api_address, "starred")
		lg.step_action()
		user_dataset["organisations"] = get_number_of(ghd, user_api_address, "orgs")
		lg.step_action()
		user_dataset["events"] = get_number_of(ghd, user_api_address, "events")
		lg.step_action()
		user_dataset["received_event"] = get_number_of(ghd, user_api_address, "received_event")
		lg.step_action()
		user_dataset["total_commits_authored"] = get_total_count(ghd, user_name, 'commits?q=author:')
		lg.step_action()
		user_dataset["total_commits_committed"] = get_total_count(ghd, user_name, 'commits?q=committer:')
		lg.step_action()
		user_dataset["total_issues_assigned_to_the_user"] = get_total_count(ghd, user_name, 'issues?q=assignee:')
		lg.step_action()
		user_dataset["total_issues_created/authored_by_the_user"] = get_total_count(ghd, user_name, 'issues?q=author:')
		lg.step_action()
		user_dataset["total_issues_mentions user"] = get_total_count(ghd, user_name, 'issues?q=mentions:')
		lg.step_action()
		user_dataset["total_issues_commented by user"] = get_total_count(ghd, user_name, 'issues?q=commenter:')
		lg.step_action()
		user_dataset["total_issues_owned by user"] = get_total_count(ghd, user_name, 'issues?q=user:')
		lg.step_action()
		user_dataset["repositories_owned"] = get_total_count(ghd, user_name, 'repositories?q=user:') #doesn't include the forked ones
		lg.step_action()
		'''

		user_dataset["amount_of_activities_done_per_day_of_the_week"] = productivity.contribution_days(dataFolderPath,user_name, commit_committed, commit_authored, issues_authored, issues_assigned, issue_comments, commit_authored_comments) 
		lg.step_action()

		#user_dataset["activities_frequency"] = list_stats(productivity.activities_frequency(dataFolderPath,user_name),['activities_frequency'])
		#lg.step_action()
	
		list_count_issues_freq, list_count_commits_freq  = productivity.activities_frequency(commit_authored, issues_authored)[1]
		lg.step_action()
		projects_per_day = productivity.projects_per_day(commit_authored, issues_authored)[1]
		lg.step_action()
		comment_length = cm.comment_length(user_name, issue_comments, commit_authored_comments)
		lg.step_action()
		number_of_comment_answers = cm.number_of_comment_answers(user_name, issue_comments)
		lg.step_action()
		amount_of_files_changed_in_a_commit = commits.files_in_commits(commit_authored)
		lg.step_action()

		total_list.extend((list_count_commits_freq,list_count_issues_freq, projects_per_day, comment_length, number_of_comment_answers, amount_of_files_changed_in_a_commit))
		names = ['commits_frequency', 'issues_frequency', 'projects_per_day','comment_length', 'number_of_comment_answers','amount_of_files_changed_in_a_commit']
		out = list_stats(total_list, names)

		user_dataset["commits_frequency"] = out['commits_frequency'].to_dict()
		user_dataset["issues_frequency"] = out['issues_frequency'].to_dict()
		user_dataset["projects_per_day"] = out['projects_per_day'].to_dict()
		user_dataset["comment_length"] = out['comment_length'].to_dict()
		user_dataset["number_of_comment_answers"] = out['number_of_comment_answers'].to_dict()
		user_dataset["amount_of_files_changed_in_a_commit"] = out['amount_of_files_changed_in_a_commit'].to_dict()
		
		user_dataset["issue_created_by_user_closed_by_user_time_diff"] = time_diff(productivity.create_close_issue_diff(user_name, issues_authored)[0]['create_close_diff']).to_dict()
		lg.step_action()
		user_dataset["amount_of_issues_created_by_the_user_still_open"], user_dataset["amount_of_issues_created_by_the_user_closed_by_user"], \
		user_dataset["amount_of_issues_created_by_the_user_closed_by_other_user"] = productivity.create_close_issue_diff(user_name, issues_authored)[1]
		lg.step_action()		
		user_dataset["issue_assigned_to_user_and_closed_by_user_time_diff"] = time_diff(productivity.assign_close_issue_diff(user_name, issues_assigned)[0]["create_close_diff"]).to_dict()
		lg.step_action()
		user_dataset["amount_of_issues_assigned_to_the_user_still_open"],user_dataset["amount_of_issues_assigned_to_the_user_closed_by_the_user"],\
		user_dataset["amount_of_issues_assigned_to_the_user_closed_by_other_user"], user_dataset["amount_of_issues_assigned_to_the_user_that_are_closed"] \
		= productivity.assign_close_issue_diff(user_name, issues_assigned)[1]
		lg.step_action()
		user_dataset["time_diff_between_consequtive_commiits_committed_by_user"] = time_diff(productivity.commit_time_diff(commit_committed)).to_dict()
		lg.step_action()
		user_dataset["pull_merge_diff"] = time_diff(productivity.pull_merge_diff(dataFolderPath,user_name)[0]["pull_merge_diff"]).to_dict()
		lg.step_action()
		user_dataset["total_pull_request_done_by_the_user"],user_dataset["amount_of_pull_request_done_by_the_user_were_merged"],\
		user_dataset["amount_of_pull_request_done_by_the_user_were_closed_not_merged"], user_dataset["amount_of_pull_request_done_by_the_user_still_open"]\
		= productivity.pull_merge_diff(dataFolderPath,user_name)[1]
		lg.step_action()
		user_dataset["time_active - (y,m,d)"] = time_active(commit_committed)
		lg.step_action()
		user_dataset["amount_of_files_committed_per_language"] = lan.count_languages(commit_authored)
		lg.step_action()
		user_dataset["total_issues_with_bug_keyword_assigned_to_someone_by_the_user"] = pm.bug_assigned(issues_authored)[0]
		lg.step_action()
		user_dataset["total_issues_with_label_assigned_by_the_user"] = pm.assigned_label(issues_authored)
		lg.step_action()		
		user_dataset["total_issues_created_by_user_with_milestone_assigned"], user_dataset["total_issues_with_milestone_assigned_by_the_user"] = pm.assign_milestone(user_name, issues_authored)
		lg.step_action()
		user_dataset["number_of_comments_with_project_mgmt_keywords"],user_dataset["total_comments_made_by_user"]  = pm.project_comments(user_name, issue_comments, commit_authored_comments)
		lg.step_action()				
		user_dataset["commit_changes_per_language"] = additions_deletions_stats(commits.commit_changes(commit_authored)).to_dict()
		lg.step_action()
		user_dataset["documentation_commit_changes"] = additions_deletions_stats(operational.documentation_commit(commit_authored)[0]).to_dict()
		lg.step_action()
		user_dataset["amount_of_files_related_to_testing_committed_by_user"] = testing.add_test_case(commit_authored)
		lg.step_action()
		user_dataset["bug_word_in_commit_message/bug_fixing_contribution"] = commits.bug_fixing_contribution(commit_authored)
		lg.step_action()
		user_dataset["amount_of_comments_made_by_the_user_with_test_keyword"], user_dataset["amount_of_comments_made_by_the_user_with_issue_number_reference"] = testing.test_comments(user_name, issue_comments, commit_authored_comments)[0]
		lg.step_action()		
		user_dataset["number_of_comments_with_documentation_keywords"] = operational.documentation_comments( user_name, issue_comments, commit_authored_comments)
		lg.step_action()
		user_dataset["amount_of_issues_closed_by_user_with_bug_keyword"], user_dataset["total_amount_of_issues_closed_by_user"] = testing.closed_issues(user_name, issues_authored, issues_assigned, issues_commented, issues_mentions, issues_owned)
		lg.step_action()
		user_dataset["count_of_empty_commit_messages"] = commits.empty_commit_message(commit_committed)
		lg.step_action()

		#user_dataset["deploy_days_time_diff"] = productivity.deploy_rate(dataFolderPath,user_name)
		#lg.step_action()

		user_dataset["project_popularity_stats"] = {"forks": list_stats([pp.project_popularity_stats(dataFolderPath,user_name)["forks_count"]],["forks"])["forks"].to_dict(),\
		"stargazers":list_stats([pp.project_popularity_stats(dataFolderPath,user_name)["stargazers_count"]],["stargazers"])["stargazers"].to_dict(),\
		"watchers":list_stats([pp.project_popularity_stats(dataFolderPath,user_name)["watchers_count"]],["watchers"])["watchers"].to_dict()}
		lg.step_action()
		
		user_dataset["project_scale_stats"] = {"commits": list_stats([pp.project_scale_stats(dataFolderPath,user_name)["amount_of_commits"]],["commits"])["commits"].to_dict(),\
		"contributors":list_stats([pp.project_scale_stats(dataFolderPath,user_name)["amount_of_contributors"]],["contributors"])["contributors"].to_dict(),\
		"releases":list_stats([pp.project_scale_stats(dataFolderPath,user_name)["amount_of_releases"]],["releases"])["releases"].to_dict()}
		lg.step_action()

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