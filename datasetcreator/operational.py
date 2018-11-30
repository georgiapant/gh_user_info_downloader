import sys
from properties import (GitHubAuthToken, dataFolderPath,  packageFolderPath)
sys.path.insert(0, packageFolderPath)
#from datamanager.filemanager import FileManager
from datasetcreator.dbs import Databases
from collections import Counter
from datasetcreator.communication import Communication

'''
- commit files with .md or .txt ending (Licence)
- comments include words like "document", "documentation" etc
- commmit licence
'''
#user_name = 'nbriz'
#dataFolderPath = '/Users/georgia/Desktop'
# = FileManager()

class Operational(Databases):
    
    def documentation_commit(self, commit_authored):
        #commit_authored=fm.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha")
        fin_dict = {}
        
        doc_list = []
        for key in commit_authored.keys():
            for item in range(len(commit_authored[key]["files"])):
                
                language = commit_authored[key]["files"][item]["filename"].split('.')[-1]
                
                if language in self.keywords_db()[4]:
                    doc_list.append(language)
                    try:
                        try:
                            fin_dict[language]["additions"].append(commit_authored[key]["files"][item]["additions"])
                            fin_dict[language]["deletions"].append(commit_authored[key]["files"][item]["deletions"])
                        except:
                            fin_dict[language]["additions"] = []
                            fin_dict[language]["deletions"] = []
                    except:
                        fin_dict[language] = {}
        document_occurances = Counter(doc_list)
        
        return fin_dict, document_occurances

    def documentation_comments(self, user_name, issue_comments, commit_authored_comments):
        '''
        This function returns the amount of comments of the user that include words related to documentation
        '''
        cm = Communication()
        comments = cm.user_comments(user_name, issue_comments, commit_authored_comments)[1]
        documentation_comments_count = 0
        
        for issue_id in comments["comments_on_issues"].keys():
            for comment_id in comments["comments_on_issues"][issue_id].keys():
                if any(word in comments["comments_on_issues"][issue_id][comment_id]["body"] for word in self.keywords_db()[4]):
                    documentation_comments_count += 1
        
        for issue_id in comments["commnents_on_committs"].keys():
            for comment_id in comments["commnents_on_committs"][issue_id].keys():
                if any(word in comments["commnents_on_committs"][issue_id][comment_id]["body"] for word in self.keywords_db()[4]):
                    documentation_comments_count += 1
        return documentation_comments_count

'''
x = documentation_comments(dataFolderPath, user_name)
fm.write_json_to_file(dataFolderPath + "/" + user_name +"/operational.json", x)
print(x)
'''