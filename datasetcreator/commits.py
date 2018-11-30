import sys
from properties import (GitHubAuthToken, dataFolderPath,  packageFolderPath)
sys.path.insert(0, packageFolderPath)
#from datamanager.filemanager import FileManager
from datasetcreator.dbs import Databases

'''
- number of files in a single commit
- number of addition/deletions of a commit per language
- numver of commits with empty body
- number of commits that include bug related words in the commit message (shows bug contribution)
'''
#user_name = 'nbriz'
#dataFolderPath = '/Users/georgia/Desktop'
#fm = FileManager()
#dbs = Databases()

class Commits(Databases):

    def files_in_commits(self, commit_authored):
        '''
        If the real changed files are more than 300 it just returns 300. Usually this many files means copying of somewhere
        '''
        #commit_authored=fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
        commit_files_count = []

        for key in commit_authored.keys():
            commit_files_count.append(len(commit_authored[key]["files"]))
            
        return commit_files_count #doesnt show more than 300 files 

    def commit_changes(self, commit_authored):
        '''
        This function returns the additions, deletions per language done by the user
        '''
        #commit_authored=fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
        fin_dict = {}
        language_commits = {}

        for key in commit_authored.keys():
            for item in range(len(commit_authored[key]["files"])):
                
                language = commit_authored[key]["files"][item]["filename"].split('.')[-1]
                
                try:
                    try:
                        fin_dict[language]["additions"].append(commit_authored[key]["files"][item]["additions"])
                        fin_dict[language]["deletions"].append(commit_authored[key]["files"][item]["deletions"])
                    except:
                        fin_dict[language]["additions"] = []
                        fin_dict[language]["deletions"] = []
                except:
                    fin_dict[language] = {}
        
        for item in fin_dict.keys():        
            try:
                language_commits[self.languages_db(item)] = fin_dict[item]
            except KeyError:
                continue
            
        return language_commits

    def empty_commit_message(self, commit_committed):
        #commit_committed = fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_committed","sha")
        empty_commit = 0

        for key in commit_committed.keys():
            if not bool(commit_committed[key]["commit"]["message"]):
                empty_commit += 1
        return empty_commit

    def bug_fixing_contribution(self, commit_authored):
        '''
        Returns the amount of commits that have a bug related word in the commit message
        '''
        #commit_authored=fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
        bug_contribution_count = 0

        for key in commit_authored.keys():
            if any(word in commit_authored[key]["commit"]["message"] for word in self.keywords_db()[1]):
                bug_contribution_count += 1

        return bug_contribution_count 

'''
x = bug_fixing_contribution(dataFolderPath, user_name)

fm.write_json_to_file(dataFolderPath + "/" + user_name +"/commit_changes.json", x) 
print(x)
'''