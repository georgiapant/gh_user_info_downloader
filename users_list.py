
import json
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose, packageFolderPath
from downloader.githubdownloader import GithubDownloader
from datamanager.filemanager import FileManager

'''
Here I download the profile links of the users that have more than ten public repos and more than 20 followers. 
These users will be used to do the benchmarking
'''

ghd = GithubDownloader(GitHubAuthToken)
users = "https://api.github.com/search/users?q=repos:10+followers:20"
logins = []

for user in ghd.download_paginated_object(users):
    logins.append(user["html_url"])

p = "\n".join(logins)

new_file=open(packageFolderPath +"/USERS_LIST.txt",mode="w",encoding="utf-8")
new_file.write(p)
new_file.close()
