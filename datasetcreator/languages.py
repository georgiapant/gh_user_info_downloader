import sys
from properties import (dataFolderPath, packageFolderPath)
sys.path.insert(0, packageFolderPath) 
import json
import os
from collections import Counter
from datamanager.filemanager import FileManager
from datasetcreator.dbs import Databases

class Languages(FileManager):

    def count_languages(self, commit_authored):
        '''
        This function returns a dictionary with as keys programming languages and as values the amount of files 
        the user has committed written in that language.

        :dataFolderPath: The main folder that the json files that need to be iterated are
        :user_name: The username of the user that we are processing
        '''
        dbs = Databases()
        #commit_authored=self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha") #returns big dict
        list_of_languages = []
        final_list = []
        languages_dict = {}
        
        for element_id in commit_authored.keys():
            files = commit_authored[element_id]["files"]
            list_of_languages.append(files)

        for item in range(len(list_of_languages)):
            for file in range(len(list_of_languages[item])):
                file_ending = list_of_languages[item][file]["filename"].split('.')[-1]
                final_list.append(file_ending)

        language_occurance = Counter(final_list)
        for item in language_occurance.keys():
            try:
                languages_dict[dbs.languages_db(item)]= language_occurance[item]
            except KeyError:
                continue
        return languages_dict

   
