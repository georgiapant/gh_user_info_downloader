import datetime
from dateutil.relativedelta import relativedelta

def time_active(commit_committed):
    '''
    This funtion returns the years, months and days between the first commit committed and the last by the user in the form of a tuple
    It needs to have downloaded the full version of the committs_committed 
    '''
    first_commit = datetime.datetime.combine(datetime.datetime.now().date(), datetime.datetime.now().time())
    last_commit = datetime.datetime.combine(datetime.date.min,  datetime.time.min)

    for element_id in commit_committed.keys():
        date_str = commit_committed[element_id]["commit"]["committer"]["date"]
        date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ') 

        if date<first_commit:
            first_commit = date 
        elif date>last_commit:
            last_commit = date
        else:
            continue

    return relativedelta(last_commit, first_commit).years, relativedelta(last_commit, first_commit).months, relativedelta(last_commit, first_commit).days


