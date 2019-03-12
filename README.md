
# 2018_Georgia_Pantalona_Symeonidis

 Αναγνώριση Προφίλ Μηχανικών Λογισμικού από Δεδομένα Συστημάτων Ελέγχου Εκδόσεων


## Download_information function

- With this function can download data for a desired user. The data that can be downloaded are:

    * download_user_repos #includes the forked ones
    * download_commits_authored 
    * download_commits_committed
    * download_issues_assigned 
    * download_issues_authored 
    * download_issues_mentions 
    * download_issues_commented
    * download_issues_owened 
    * download_repositories_owned #doesn't include the forked ones

- Along with a file with information about the user and another one with the statistics of the user. The statistics included are:
    * number of commits authored by the user
    * number of commits committed by the user
    * number of events 
    * number of followers the user has
    * number of users the user is following
    * number of issues that are assigned to the user
    * number of issues authored by the user
    * number of issues commented by the user
    * number of issues that mention the user
    * number of issues that are owned by the user
    * number of organisations the user belongs
    * number of events the user received
    * number of repos the user has, with the forked ones
    * number of repositories the user owns without the forked ones
    * number of starred repositories

## datasetcreator folder

This folder contains functions that can download raw data about the user. The different data that can be dowloaded are:
- about the activeness of the user
    * The time the user is active in years, months, days.
- About the communication skills of the user
    * All the comments he made in all issues and committs
    * The length of the comments
    * The number of comment answers
    * The reactions of the comments (both detailed and just the count)
- Languages
    * The amount of files committed in each programming language
- List of URLs of the repos the user has contributed. Its all repos that the user has committed an issue, a committ or he owns.
- Project management
    * Amount of bugs assigned by the user and the list of the issue ids of those bugs
    * Time difference between the assignement of the bug and its closure (in amount of months, days, minutes and seconds) and the amount of not closed bugs
    * Amount of labels assigned in issues
    * Amount of milestones assigned in total and amount assigned by the user
    * Amount of comments that contain keywords related to project and the total count of comments
- Productivity of the user
    * when he mostly works (days of the week) 
    * Frequency of activities (committs/day - issues/day)
    * Time between creation and closure of an issue by the user (both) 
    * Time between the assignment of an issue to the user and the closure of the issue 
    * Time between two committs of the same developer
    * Time between pull request and merge 
    * Deploy rate 
    * Number of projects per day 
    * Duration a repository is active
- Project preference
    * Project popularity stats (amount of subscribers, stargazers and forks of the repo)
    * Project scale stats (amount of committs, releases and contributors of the repo)
