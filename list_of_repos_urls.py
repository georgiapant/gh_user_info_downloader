
import sys
from properties import (dataFolderPath,  packageFolderPath)
sys.path.insert(0, packageFolderPath) 
from datamanager.filemanager import FileManager
import json
 

class List_of_repos_urls(FileManager):
    '''
    This class returns a list with the repositories that the user has contributed into
    In order to be able to get a result you need to have downloaded commits_authored and commits_committed full
    
    '''
    def list_of_repos_urls_from_committs(self, commit_authored, commit_committed):
        
        list_url = []
        
        for element_id in commit_authored.keys():
            url = '/'.join(commit_authored[element_id]["html_url"].split('/')[:-2])
            if url not in list_url:
                list_url.append(url)
        
        for element_id in commit_committed.keys():
            url = '/'.join(commit_committed[element_id]["html_url"].split('/')[:-2])
            if url not in list_url:
                list_url.append(url)
        
        return list_url

    def list_of_repos_urls_from_issues(self, issues_assigned, issues_authored, issues_commented,  issues_mentions, issues_owned):
        list_url = []

        for element_id in issues_assigned.keys():
            
            api_url = issues_assigned[element_id]["repository_url"]
            url = "https://github.com/" + '/'.join(api_url.split('/')[-2:])
            if url not in list_url:
                list_url.append(url)

        for element_id in issues_authored.keys():
            api_url = issues_authored[element_id]["repository_url"]
            url = "https://github.com/" + '/'.join(api_url.split('/')[-2:])
            if url not in list_url:
                list_url.append(url)

        for element_id in issues_commented.keys():
            api_url = issues_commented[element_id]["repository_url"]
            url = "https://github.com/" + '/'.join(api_url.split('/')[-2:])
            if url not in list_url:
                list_url.append(url)

        for element_id in issues_mentions.keys():
            api_url = issues_mentions[element_id]["repository_url"]
            url = "https://github.com/" + '/'.join(api_url.split('/')[-2:])
            if url not in list_url:
                list_url.append(url)

        for element_id in issues_owned.keys():
            api_url = issues_owned[element_id]["repository_url"]
            url = "https://github.com/" + '/'.join(api_url.split('/')[-2:])
            if url not in list_url:
                list_url.append(url)

        return list_url

    def list_of_repos_urls_from_repos_owned(self, dataFolderPath, user_name):
        repos_owned = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/repositories_owned", "id")
        repos_owned_wforked = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/user_repo", "id")

        list_url = []
        for element_id in repos_owned.keys():
            url = repos_owned[element_id]["html_url"]
            if url not in list_url:
                list_url.append(url)

        for element_id in repos_owned_wforked.keys():
            url = repos_owned_wforked[element_id]["html_url"]
            if url not in list_url:
                list_url.append(url)
        return list_url

    def get_list_of_repos_urls(self, dataFolderPath, user_name, issues_assigned, issues_authored,  issues_commented, issues_mentions, issues_owned, commit_authored, commit_committed):
        list1 = self.list_of_repos_urls_from_committs(commit_authored, commit_committed) \
        +self.list_of_repos_urls_from_issues(issues_assigned, issues_authored, issues_commented,  issues_mentions, issues_owned) \
        + self.list_of_repos_urls_from_repos_owned(dataFolderPath, user_name)
        
        final_list = []
        
        for element in list1:
            if element not in final_list:
                final_list.append(element)

        return final_list