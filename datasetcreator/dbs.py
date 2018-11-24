


class Databases():

    def keywords_db(self):
        project_words = ["plan","timeline","project", "sprint", "risk", "resources", "agile" , "progress", "cost", "planning", "budget", "analysis", \
        "business model" , "value", "communication", "task", "task manager", "complete", "constraint", "stakeholders", "customer", "critical success factor", \
        "KPI", "effort", "impact", "XP", "goal setting", "goal" , "HR"]
        bug_words = ["bug", "error","defect","debug", "faulty", "problem", "trial", "try", "tried","solve", "solution", "fix", "fixed", "issue", \
        "wrong", "mistake", "issues", "debugging"]
        test_words = ["test", "defect", "test case", "testing", "expected result", "fat", "fault injection", "maintenance"\
        "quality", "QA", "quality assurance", "re-testing", "risk", "scenario", "tpi"]
        test_filenames = ["/test/", "/tests/"]
        operational = ["md", "txt", "LICENSE", "pdf", "doc", "docx", "license", "document", "documentation"]

        return project_words, bug_words, test_words, test_filenames, operational

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
'''
dbs = Databases()
kw = dbs.languages_db("js")
print(kw)
'''