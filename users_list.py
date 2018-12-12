
import json
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose, packageFolderPath
from downloader.githubdownloader import GithubDownloader
from datamanager.filemanager import FileManager

'''
Here I download the profile links of the users that have more than ten public repos and more than 20 followers. 
These users will be used to do the benchmarking
'''

ghd = GithubDownloader(GitHubAuthToken)
fm = FileManager()
users = "https://api.github.com/search/users?q=repos:10+followers:20"
logins = []
final_list = []

for user in ghd.download_paginated_object(users):
    logins.append(user["html_url"])



for item in logins:
	name = '_'.join(item.split('/')[-1:])
	try:
		stats = fm.read_json_from_file(dataFolderPath + "/" + name + "/user_stats.json")
		if stats["commit_authored"]>100:
			final_list.append(item)
	except:
		continue

p = "\n".join(final_list)

new_file=open(packageFolderPath +"/USERS_LIST_more_than_100_commits.txt",mode="w",encoding="utf-8")
new_file.write(p)
new_file.close()
