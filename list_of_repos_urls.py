
from datamanager.filemanager import FileManager
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose
import json
 
#commit_committed
class List_of_repos_urls(FileManager):
    '''
    This class returns a list with the repositories that the user has contributed into
    '''

    def list_of_repos_urls_from_committs(self, dataFolderPath, user_name):
        
        commit_authored=self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
        commit_committed = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_committed","sha")

        list_url = []
        
        for element_id in commit_authored.keys():
            url = commit_authored[element_id]["repository"]["html_url"]
            if url not in list_url:
                list_url.append(url)
        
        for element_id in commit_committed.keys():
            url = commit_committed[element_id]["repository"]["html_url"]
            if url not in list_url:
                list_url.append(url)
        
        return list_url

    def list_of_repos_urls_from_issues(self, dataFolderPath, user_name):
        issues_assigned = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_assigned", "id")
        issues_authored = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_authored", "id")
        issues_commented = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_commented", "id")
        issues_mentions = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_mentions", "id")
        issues_owned = self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/issues_owned", "id")

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

        for element_id, in repos_owned_wforked.keys():
                url = repos_owned_wforked[element_id]["html_url"]
                if url not in list_url:
                    list_url.append(url)
        return list_url

    def get_list_of_repos_urls(self, dataFolderPath, user_name):
        list1 = self.list_of_repos_urls_from_committs(dataFolderPath,user_name) +self.list_of_repos_urls_from_issues(dataFolderPath,user_name) + self.list_of_repos_urls_from_repos_owned(dataFolderPath, user_name)
        final_list = []
        
        for element in list1:
            if element not in final_list:
                final_list.append(element)

        return final_list