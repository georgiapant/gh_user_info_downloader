import sys
from properties import (GitHubAuthToken, dataFolderPath,  packageFolderPath)
sys.path.insert(0, packageFolderPath) #should be something universal, add to properties
from datamanager.filemanager import FileManager
from downloader.githubdownloader import GithubDownloader
import json
import datetime
import requests


'''
Left to do two functions and retest the comment_reactions()
'''

#user_address = "https://github.com/nbriz"
#user_api_address = "https://api.github.com/users/" + '/'.join(user_address.split('/')[-1:])
#user_name='nbriz'

class Communication (FileManager):    

    def comments_on_issues(self, dataFolderPath, user_name):
        '''
        This function returns all comment URLs of comments on issues and the comments themselves
        '''
        issue_comments = self.read_comment_jsons_from_folder(dataFolderPath+"/"+ user_name + "/issue_comments")
        list_url = []
        comments = {}

        for element_id in issue_comments.keys():
            r_list = issue_comments[element_id]
            comments[element_id] = {}
            
            for item in range(len(r_list)):
                try:
                    if r_list[item]["user"]["login"]== user_name:
                        
                        comments[element_id][r_list[item]["id"]] ={}
                        url = r_list[item]["url"]
                        created_at = r_list[item]["created_at"]
                        updated_at = r_list[item]["updated_at"]
                        body = r_list[item]["body"]
                        issue_url = r_list[item]["issue_url"]
                        list_url.append(url)
                        comments[element_id][r_list[item]["id"]]["created_at"]=created_at
                        comments[element_id][r_list[item]["id"]]["updated_at"]=updated_at
                        comments[element_id][r_list[item]["id"]]["body"]=body
                        comments[element_id][r_list[item]["id"]]["issues_url"]=issue_url 
                                   
                except IndexError:
                    continue           
            
        return list_url, comments




    def comments_on_committs(self, dataFolderPath, user_name):
        '''
        This function returns all comment URLs of comments on committs and the comments themselves
        '''

        commit_authored_comments=self.read_comment_jsons_from_folder(dataFolderPath+"/"+ user_name + "/commit_comments")
        commit_committed_comments = self.read_comment_jsons_from_folder(dataFolderPath+"/"+ user_name + "/commit_comments")
         
        comments = {}
        list_url = []

        for element_id in commit_authored_comments.keys():
            
            r_dict = commit_authored_comments[element_id]
            comments[element_id] = {}
            for item in range(len(r_dict)):
                try:
                    if r_dict[item]["user"]["login"]== user_name:
                        
                        comments[element_id][r_dict[item]["id"]] ={}
                        url = r_dict[item]["url"]
                        created_at = r_dict[item]["created_at"]
                        updated_at = r_dict[item]["updated_at"]
                        body = r_dict[item]["body"] 
                
                        comments[element_id]["created_at"]=created_at
                        comments[element_id]["updated_at"]=updated_at
                        comments[element_id]["body"]=body  
                        if url not in list_url:
                            list_url.append(url)          
                except IndexError:
                    continue 

        for element_id in commit_committed_comments.keys():
            
            r_dict = commit_committed_comments[element_id]
            comments[element_id] ={}
            for item in range(len(r_dict)):
                try:
                    if r_dict[item]["user"]["login"]== user_name:
                        
                        comments[element_id][r_dict[item]["id"]] ={}
                        url = r_dict[item]["url"]
                        created_at = r_dict[item]["created_at"]
                        updated_at = r_dict[item]["updated_at"]
                        body = r_dict[item]["body"] 
                
                        comments[element_id]["created_at"]=created_at
                        comments[element_id]["updated_at"]=updated_at
                        comments[element_id]["body"]=body
                        if url not in list_url:
                            list_url.append(url)          
                except IndexError:
                    continue 
        return list_url, comments

    def user_comments(self, dataFolderPath,user_name):
        '''
        This function returns a list of URLs of the comments the user had made (can be used ot get reactions)
        and a dictionary with all those comments (can be used to evaluate his comments)
        '''
        issues_comments_urls, issues_comments=self.comments_on_issues(dataFolderPath,user_name)
        committs_comments_urls, committs_comments = self.comments_on_committs(dataFolderPath, user_name)
        
        list1 = issues_comments_urls + committs_comments_urls
        final_url_list = []

        for element in list1:
            if element not in final_url_list:
                final_url_list.append(element)
        
        final_comments={}
        final_comments["comments_on_issues"]= issues_comments
        final_comments["commnents_on_committs"] = committs_comments

        return final_url_list, final_comments



    def comment_length(self, dataFolderPath,user_name):
        '''
        This function returns a list with the length of all comments the user has writtern
        '''
        comments= self.user_comments(dataFolderPath, user_name)[1]
        comment_length = []
        for issue_id in comments["comments_on_issues"].keys():
            for comment_id in comments["comments_on_issues"][issue_id].keys():
                body = comments["comments_on_issues"][issue_id][comment_id]["body"]
                length = len(body)
                comment_length.append(length)
        
        for issue_id in comments["commnents_on_committs"].keys():
            for comment_id in comments["commnents_on_committs"][issue_id].keys():
            
                body = comments["commnents_on_committs"][issue_id][comment_id]["body"]
                length = len(body)
                comment_length.append(length)

        return comment_length


    def number_of_comment_answers(self, dataFolderPath,user_name):
        comments = self.read_comment_jsons_from_folder(dataFolderPath+"/"+ user_name + "/issue_comments")
        answers_count_list = []
        
        for issue_id in comments.keys():
            for item in range(len(comments[issue_id])):
                if comments[issue_id][item]["user"]["login"]== user_name:
                    date = datetime.datetime.strptime(comments[issue_id][item]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                    counter = 0
                    for item in range(len(comments[issue_id])):
                        comment_dates = datetime.datetime.strptime(comments[issue_id][item]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                        if comment_dates>date:
                            counter = counter + 1
                    answers_count_list.append(counter)
                
        return  answers_count_list

    def comment_reactions(self, dataFolderPath, user_name):

        '''
        This functions returns a dictionary with keys the comment urls and as items the detailed reactions.
        It also returns a dictionary with keys the comment urls and as items the reactions count.
        '''
        #remember it needs special header
        ghd = GithubDownloader(GitHubAuthToken)
        list_url = self.user_comments(dataFolderPath, user_name)[0]
        reactions_detailed = {}
        reactions_count = {}
        headers = {}
        headers["Accept"]="application/vnd.github.squirrel-girl-preview+json"
        headers['Authorization'] = 'token ' + GitHubAuthToken
        for item in list_url:
            url = item +"/reactions"
            r = requests.get(url, headers=headers)
            ghd.set_request_number(r.headers['x-ratelimit-remaining'], r.headers['x-ratelimit-reset'])
            r_dict = json.loads(r.text)
            reactions_detailed[item]= {}
            reactions_detailed[item]=r_dict
        
        for item in list_url:
            r = requests.get(url, headers=headers)
            ghd.set_request_number(r.headers['x-ratelimit-remaining'], r.headers['x-ratelimit-reset'])
            r_dict = json.loads(r.text)
            print(r_dict)
            try:
                reactions_count[item] = {}
                reactions_count[item] = r_dict["reactions"]
            except:
                continue
        
        return reactions_detailed, reactions_count

'''
user_name = 'nbriz'
cm = Communication()
fm = FileManager()
test = cm.user_comments(dataFolderPath,user_name)[0]
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/comment_url_list.json", test) 
'''        
