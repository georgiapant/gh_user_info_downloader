from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose
from datamanager.filemanager import FileManager
from logger.downloadlogger import Logger
from downloader.gitdownloader import GitDownloader

from datasetcreator.productivity import Productivity
from datasetcreator.activeness import time_active
from datasetcreator.communication import Communication
from datasetcreator.languages import Languages
from datasetcreator.pm import Project_management
from datasetcreator.project_preferences import Project_preferences
#from datasetcreator.response_time import response_time_to_comments_mentioned
from datasetcreator.testing import add_test_case,test_comments,closed_issues
from datasetcreator.commits import files_in_commits, commit_changes, empty_commit_message, bug_fixing_contribution
from datasetcreator.operational import documentation_comments, documentation_commit



#user_address = "https://github.com/nbriz"
#user_api_address = "https://api.github.com/users/" + '/'.join(user_address.split('/')[-1:])
user_name='nbriz'
dataFolderPath = '/Users/georgia/Desktop'
'''
This is a file to run to gather a first example of all possible raw data that can be dowloaded
'''

productivity = Productivity(dataFolderPath, user_name)
fm = FileManager()
cm = Communication()
lan = Languages()
pm = Project_management(dataFolderPath,user_name)
pp = Project_preferences()
lg = Logger(verbose)
gd = GitDownloader(gitExecutablePath, lg)

lg.start_action("Retrieving user data ...", 29)


contribution_days = productivity.contribution_days(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/contribution_days.json", contribution_days) 
print("contribution_days done")
lg.step_action()

activities_frequency = productivity.activities_frequency(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/activities_frequency.json", activities_frequency) 
print("activities freq done")
lg.step_action()

create_close_issue_diff = productivity.create_close_issue_diff(user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/create_close_issue_diff.json", create_close_issue_diff)
print("create close issue diff done") 
lg.step_action()

assign_close_issue_diff = productivity.assign_close_issue_diff(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/assign_close_issue_diff.json", assign_close_issue_diff) 
print("assigne close issue diff done") 
lg.step_action()

commit_time_diff = productivity.commit_time_diff(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/commit_time_diff.json", commit_time_diff) 
print("committ time diff done") 
lg.step_action()

pull_merge_diff = productivity.pull_merge_diff(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/pull_merge_diff.json", pull_merge_diff) 
print("pull merge diff done") 
lg.step_action()

projects_per_day = productivity.projects_per_day(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/projects_per_day.json", projects_per_day)
print("projects per day done") 
lg.step_action()

time_active = time_active(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/time_active.json", time_active)
print("time_active done") 
lg.step_action()

user_comments = cm.user_comments(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/user_comments.json", user_comments)
print("user comments done") 
lg.step_action()

comment_length = cm.comment_length(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/comment_length.json", comment_length)
print("comment_length done") 
lg.step_action()

number_of_comment_answers = cm.number_of_comment_answers(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/number_of_comment_answers.json", number_of_comment_answers)
print("number of comment answers done") 
lg.step_action()

comment_reactions = cm.comment_reactions(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/comment_reactions.json", comment_reactions)
print("comment reactions done") 
lg.step_action()

count_languages = lan.count_languages(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/count_languages.json", count_languages)
print("count languages done") 
lg.step_action()

bugs_assigned = pm.bug_assigned(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/bugs_assigned.json", bugs_assigned)
print(" bugs assigned done") 
lg.step_action()

resolved_time = pm.resolved_time(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/resolved_time.json", resolved_time)
print("resolved time done") 
lg.step_action()

assigned_label = pm.assigned_label(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/assigned_label.json", assigned_label)
print("assigned label done") 
lg.step_action()

assigned_milestone = pm.assign_milestone(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/assigned_milestone.json", assigned_milestone)
print("assigned milestone done")
lg.step_action() 

project_comments = pm.project_comments(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/project_comments.json", project_comments)
print("project comments done") 
lg.step_action()

project_popularity_stats = pp.project_popularity_stats(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/project_popularity_stats.json", project_popularity_stats)
print("project popularity done") 
lg.step_action()

project_scale_stats = pp.project_scale_stats(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/project_scale_stats.json", project_scale_stats)
print("project scale stats done") 
lg.step_action()

#############

closed_issues = closed_issues(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/closed_issues.json", closed_issues)
print("closed_issues done") 
lg.step_action()

test_comments = test_comments(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/test_comments.json", test_comments)
print("test_comments done") 
lg.step_action()

add_test_case = add_test_case(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/add_test_case.json", add_test_case)
print("add_test_case done") 
lg.step_action()

files_in_commits = files_in_commits(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/files_in_commits.json", files_in_commits)
print("files_in_commits done") 
lg.step_action()

commit_changes = commit_changes(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/commit_changes.json", commit_changes)
print("commit_changes done") 
lg.step_action()

empty_commit_message = empty_commit_message(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/empty_commit_message.json", empty_commit_message)
print("empty_commit_message done") 
lg.step_action()

bug_fixing_contribution = bug_fixing_contribution(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/bug_fixing_contribution.json", bug_fixing_contribution)
print("bug_fixing_contribution done") 
lg.step_action()

documentation_commit = documentation_commit(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/documentation_commit.json", documentation_commit)
print("documentation_commit done") 
lg.step_action()

documentation_comments = documentation_comments(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/documentation_comments.json", documentation_comments)
print("documentation_comments done") 
lg.end_action()


'''
response_time_to_comments_mentioned = response_time_to_comments_mentioned(dataFolderPath,user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/all_data/response_time_to_comments_mentioned.json", response_time_to_comments_mentioned)
print("response time to comments mentioned done") 
lg.end_action()
'''



