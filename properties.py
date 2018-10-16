
# Set this to folder where data are downloaded
dataFolderPath = '/Users/georgia/Desktop'
# Set this to your GitHub auth token
GitHubAuthToken = 'ae38ec3b1f1efe31eae0d2b9ef34c6912febd6fa'

# Set this to the path of the git executable
gitExecutablePath = '/usr/local/bin'

# Set to 0 for no messages, 1 for simple messages, and 2 for progress bars
verbose = 1

# Select how to write to disk
always_write_to_disk = True

# Select what to download
"""
download_issues = True
download_issue_comments = True
download_issue_events = True
download_commits = True
download_commit_comments = True
download_contributors = True
download_source_code = False
"""

download_user_repos = False #includes the forked ones
download_commits_authored  = True
download_commits_committed = True
download_issues_assigned = True
download_issues_authored = True
download_issues_mentions = True
download_issues_commented = True
download_issues_owened = True
download_repositories_owned = True #doesn't include the forked ones


# Select whether the downloaded issues and commits information will be full
"""
download_issues_full = True
download_commits_full = True
"""
download_issues_owened_full = True
download_issues_commented_full = True
download_issues_mentions_full = True
download_issues_authored_full = True
download_issues_assigned_full = True
download_commits_committed_full = True
download_commits_authored_full = True



