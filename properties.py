
from paths import PathDataFolderPath, PathPackageFolderPath , PathGitHubAuthToken, PathGitExecutablePath

# Set this to folder where data are downloaded
dataFolderPath = PathDataFolderPath

# Set this to folder where the package is stored 
packageFolderPath = PathPackageFolderPath

# Set this to your GitHub auth token
GitHubAuthToken = PathGitHubAuthToken

# Set this to the path of the git executable
gitExecutablePath = PathGitExecutablePath

# Set to 0 for no messages, 1 for simple messages, and 2 for progress bars
verbose = 1

# Select how to write to disk
always_write_to_disk = True


download_user_repos = False #includes the forked ones
download_commits_authored  = True
download_commits_committed = True
download_issues_assigned = True
download_issues_authored = True
download_issues_mentions = True
download_issues_commented = True
download_issues_owened = True
download_repositories_owned = True #doesn't include the forked ones


download_issues_owened_full = True
download_issues_commented_full = True
download_issues_mentions_full = True
download_issues_authored_full = True
download_issues_assigned_full = True
download_commits_committed_full = True
download_commits_authored_full = True



