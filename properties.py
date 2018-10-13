
# Set this to folder where data are downloaded
dataFolderPath = '/Users/georgia/Desktop'
# Set this to your GitHub auth token
GitHubAuthToken = '293082ef9f1fc1408a19acc44640ec0ac0f76c11'

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
download_commits_authored  = False
download_commits_committed = False
download_issues_assigned = False
download_issues_authored = False
download_issues_mentions = False
download_issues_commented = False
download_issues_owened = False
download_repositories_owned = False #doesn't include the forked ones


# Select whether the downloaded issues and commits information will be full
"""
download_issues_full = True
download_commits_full = True
"""
