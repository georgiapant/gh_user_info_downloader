
class Project(dict):
	"""
	Class that includes the data of a GitHub project. This class is implemented as a dict
	and includes also several helper functions for adding data and checking for data.
	"""

	def user_info_exists(self):
		""" 
		Checks if the user exists in the project.

		:param user: the user to be checked.
		:returns: True if the given user exists in the project, or False otherwise.
		"""
		return bool(self["user_info"])

	def add_user_info(self, user_info):
		"""
		Adds a user to the repository.

		:param user: the user to be added to the repository.
		"""
		self["user_info"] = user_info

	def user_stats_exists(self):
		"""
		Checks if the stats of the project exist.

		:returns: True if the project stats exist, or False otherwise.
		"""
		return bool(self["user_stats"])

	def add_user_stats(self, user_stats):
		"""
		Adds the stats of the repository.

		:param stats: the stats to be added to the repository.
		"""
		self["user_stats"] = user_stats
	
	def user_dataset_exists(self):
		"""
		Checks if the stats of the project exist.

		:returns: True if the project stats exist, or False otherwise.
		"""
		return bool(self["user_dataset"])

	def add_user_dataset(self, user_dataset):
		"""
		Adds the stats of the repository.

		:param stats: the stats to be added to the repository.
		"""
		self["user_dataset"] = user_dataset

	def user_repo_exists(self, user_repo):
		"""
		Checks if the given user repository exists in the project.

		:param user_repo: the user_repo to be checked.
		:returns: True if the given user repo exists in the project, or False otherwise.
		"""
		return user_repo["id"] in self["user_repo"]


	def add_user_repo(self, user_repo):
		"""
		Adds a user repo to the user.

		:param user repo: the user repo to be added.
		"""
		self["user_repo"][user_repo["id"]] = user_repo
	#----------

	def commit_authored_exists(self, commit_authored):
		#print(commit_authored["sha"])
		#print(bool(commit_authored["sha"] in self["commit_authored"]))
		return commit_authored["sha"] in self["commit_authored"]


	def add_commit_authored(self, commit_authored):
		self["commit_authored"][commit_authored["sha"]] = commit_authored


	def commit_committed_exists(self, commit_committed):
		return commit_committed["sha"] in self["commit_committed"]

	def add_commit_committed(self, commit_committed):
		self["commit_committed"][commit_committed["sha"]] = commit_committed

	
	def issue_assigned_exists(self, issues_assigned):
		return issues_assigned["id"] in self["issues_assigned"]

	def add_issue_assigned(self, issues_assigned):
		self["issues_assigned"][issues_assigned["id"]] = issues_assigned

	
	def issue_authored_exists(self, issues_authored):
		return issues_authored["id"] in self["issues_authored"]

	def add_issue_authored(self, issues_authored):
		self["issues_authored"][issues_authored["id"]] = issues_authored


	def issue_mentions_exists(self, issues_mentions):
		return issues_mentions["id"] in self["issues_mentions"]

	def add_issue_mentions(self, issues_mentions):
		self["issues_mentions"][issues_mentions["id"]] = issues_mentions


	def issue_commented_exists(self, issues_commented):
		return issues_commented["id"] in self["issues_commented"]

	def add_issue_commented(self, issues_commented):
		self["issues_commented"][issues_commented["id"]] = issues_commented


	def issue_owned_exists(self, issues_owned):
		return issues_owned["id"] in self["issues_owned"]

	def add_issue_owned(self, issues_owned):
		self["issues_owned"][issues_owned["id"]] = issues_owned


	def repositories_owned_exists(self, repositories_owned):
		return repositories_owned["id"] in self["repositories_owned"]

	def add_repositories_owned(self, repositories_owned):
		self["repositories_owned"][repositories_owned["id"]] = repositories_owned

#--------

	def issue_comment_exists(self, comment):
		'''
		This function checks if the list of comments of an issue with a specific id exists in the project
		'''
		for key in comment.keys():
			return key in self["issue_comments"]

	def add_issue_comment(self, comment):
		self["issue_comments"] = comment
	
	def commit_comment_exists(self, comment):
		'''
		This function checks if the list of comments of an issue with a specific id exists in the project
		'''
		for key in comment.keys():
			return key in self["commit_comments"]

	def add_commit_comment(self, comment):
		self["commit_comments"] = comment



