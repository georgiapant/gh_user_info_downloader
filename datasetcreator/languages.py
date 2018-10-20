import json
import os
from collections import Counter
from datamanager.filemanager import FileManager

class Languages(FileManager):

    def count_languages(self, dataFolderPath, user_name):
        '''
        This function returns a dictionary with as keys programming languages and as values the amount of committs the user has
        made with that language.

        :dataFolderPath: The main folder that the json files that need to be iterated are
        :user_name: The username of the user that we are processing
        '''
        commit_authored=self.read_jsons_from_folder(dataFolderPath + "/" + user_name + "/commit_authored","sha") #returns big dict
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
                languages_dict[self.languages_db(item)]= language_occurance[item]
            except KeyError:
                continue
        return languages_dict

    def languages_db(self,file_endings):
        '''
        This function acts like a database of file extensions and the programming language they correspond

        :file_endings: The file ending we want to find the corresponding language
        The output is a string of the corresponding language
        '''

        db = [("js", "JavaScript"), ("py", "Python"), ("css", "CSS"), ("json", "JSON"), ("md", "Markdown"), \
        ("java", "Java"), ("c","C"),("cpp", "C++"),("m", "Objective-C"), ("glsl", "GLSL"), ("lua", "Lua"),("sh","Shell"),\
        ("php","PHP"),("awk","Awk"),("rb","Ruby"),("coffee","CoffeeScript"),("mm","Objective-C++"),("py","Python"),("tpl","Smarty"),\
        ("PSM1","PowerShell"),("qml","QML") ,("cs","C#"),("r","R"),("vim","VimL"),("go","Go"),("pl","Perl"),("tex","Tex"),
        ("swift","Swift"),("scala","Scala"),("lisp","Emacs Lisp"),("hs","Haskell"),("clj","Clojure"), ("pde","Arduino"),
        ("mk","Makefile"),("groovy","Groovy"),("pp","Puppet"), ("rs","Rust"),("ts","TypeScript"),("ipynb","Jupyter Notebook"),\
        ("kt","Kotlin"),("xml","XML"), ("yml","YML")]    
        db = dict(db)
        full_name = db[file_endings]
        return full_name
