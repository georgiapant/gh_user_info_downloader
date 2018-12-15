import datetime

def response_time_to_comments_mentioned(user_name, issues_mentions, issue_comments):
    mention = "@"+user_name
    issue_mentions_ids = []
    response_times = []

    for key in issues_mentions.keys():
        issue_mentions_ids.append(key)
    
    for key in issue_comments.keys():
        if int(key) in issue_mentions_ids:
            counter = len(issue_comments[key])            
            for item in issue_comments[key]:
                if mention in item["body"]:
                    mention_time = datetime.datetime.strptime(item["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                    for comment_item in range(counter):
                        if issue_comments[key][comment_item]["user"]["login"]==user_name:                            
                            response_time = datetime.datetime.strptime(issue_comments[key][comment_item]["created_at"],'%Y-%m-%dT%H:%M:%SZ')
                            if mention_time < response_time:
                                a = (response_time-mention_time).total_seconds()
                                response_times.append(a)
                                break

    return  response_times

