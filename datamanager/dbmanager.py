import os
from datamanager.project import Project
from datamanager.filemanager import FileManager
from properties import dataFolderPath, always_write_to_disk

class DBManager(FileManager):
	"""
	Class that implements a DB manager. To use this class, you must first call the method
	initialize_write_to_disk, then optionally call any other method for writing data to
	disk, and finally call the method finalize_write_to_disk.
	"""
	def __init__(self):
		"""
		Initializes this DB manager.
		"""
		self.create_folder_if_it_does_not_exist(dataFolderPath)

	def initialize_write_to_disk(self, user_name):
		"""
		Initializes the writing of a project to disk. Creates all the necessary directories.

		:param user_name: the name of the repository to be written to disk.
		"""
		rootfolder = os.path.join(dataFolderPath, user_name)
		self.create_folder_if_it_does_not_exist(rootfolder)
		#self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "user_repo"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "commit_authored"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "commit_committed"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issues_assigned"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issues_authored"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issues_mentions"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issues_commented"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issues_owned"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "repositories_owned"))


	def read_project_from_disk(self, user_name):
		"""
		Reads a project from disk given the name of the user that is also the folder
		of the project.

		:param user_name: the name of the user to be read from disk.
		:returns: an object of type Project.
		"""
		project = Project()
		rootfolder = os.path.join(dataFolderPath, user_name)
		project["user_info"] = self.read_json_from_file_if_it_exists(os.path.join(rootfolder, "user_info.json"))
		project["user_stats"] = self.read_json_from_file_if_it_exists(os.path.join(rootfolder, "user_stats.json"))
		#project["user_repo"] = self.read_jsons_from_folder(os.path.join(rootfolder, "user_repo"), "id")
		project["commit_authored"] = self.read_jsons_from_folder(os.path.join(rootfolder, "commit_authored"), "sha")
		project["commit_committed"] = self.read_jsons_from_folder(os.path.join(rootfolder, "commit_committed"), "sha")
		project["issues_assigned"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issues_assigned"), "id")
		project["issues_authored"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issues_authored"), "id")
		project["issues_mentions"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issues_mentions"), "id")
		project["issues_commented"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issues_commented"), "id")
		project["issues_owned"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issues_owned"), "id")
		project["repositories_owned"] = self.read_jsons_from_folder(os.path.join(rootfolder, "repositories_owned"), "id")
		return project

	def finalize_write_to_disk(self, user_name, project):
		"""
		Finalizes the writing of a project to disk. Closes any open buffers.

		:param user_name: the name of the repository to be written to disk.
		:param project: the repository data to be written to disk.
		"""
		if not always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, user_name)
			self.write_json_to_file(os.path.join(rootfolder, "use_info.json"), project["user_info"])
			self.write_json_to_file(os.path.join(rootfolder, "user_stats.json"), project["user_stats"])
			
			'''
			for user_repo in project["user_repo"].values():
				self.write_json_to_file(os.path.join(rootfolder, "user_repo", str(user_repo["id"]) + ".json"), user_repo)
			'''
			for commits_authored in project["commit_authored"].values():
				self.write_json_to_file(os.path.join(rootfolder, "commit_authored", str(commit_authored["sha"]) + ".json"), commit_authored)

			for commits_committed in project["commit_committed"].values():
				self.write_json_to_file(os.path.join(rootfolder, "commit_committed", str(commit_committed["sha"]) + ".json"), commit_committed)
			
			for issues_assigned in project["issues_assigned"].values():
				self.write_json_to_file(os.path.join(rootfolder, "issues_assigned", str(issues_assigned["id"]) + ".json"), issues_assigned)
			
			for issues_authored in project["issues_authored"].values():
				self.write_json_to_file(os.path.join(rootfolder, "issues_authored", str(issues_authored["id"]) + ".json"), issues_authored)
			
			for issues_mentioned in project["issues_mentions"].values():
				self.write_json_to_file(os.path.join(rootfolder, "issues_mentions", str(issues_mentions["id"]) + ".json"), issues_mentions)
			
			for issues_commented in project["issues_commented"].values():
				self.write_json_to_file(os.path.join(rootfolder, "issues_commented", str(issues_commented["id"]) + ".json"), issues_commented)
			
			for issues_owned in project["issues_owned"].values():
				self.write_json_to_file(os.path.join(rootfolder, "issues_owned", str(issues_owned["id"]) + ".json"), issues_owned)
			
			for repositories_owned in project["repositories_owned"].values():
				self.write_json_to_file(os.path.join(rootfolder, "repositories_owned", str(repositories_owned["id"]) + ".json"), repositories_owned)


	def write_project_user_info_to_disk(self, user_name, user_info):
		"""
		Writes the info of a repository to disk.

		:param repo_name: the name of the repository.
		:param info: the info to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, user_name)
			self.write_json_to_file(os.path.join(rootfolder, "user_info.json"), user_info)

	def write_project_user_stats_to_disk(self, user_name, user_stats):
		"""
		Writes the stats of a repository to disk.

		:param repo_name: the name of the repository.
		:param stats: the stats to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, user_name)
			self.write_json_to_file(os.path.join(rootfolder, "user_stats.json"), user_stats)

	def write_project_user_repo_to_disk(self, user_name, user_repo):
		"""
		Writes an issue of a repository to disk.

		:param repo_name: the name of the repository.
		:param issue: the issue to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, user_name)
			self.write_json_to_file(os.path.join(rootfolder, "user_repo", str(user_repo["id"]) + ".json"), user_repo)
#----------

	def write_project_commit_authored_to_disk(self, user_name, commit_authored):
		"""
		Writes an issue of a repository to disk.

		:param repo_name: the name of the repository.
		:param issue: the issue to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, user_name)
			self.write_json_to_file(os.path.join(rootfolder, "commit_authored", str(commit_authored["sha"]) + ".json"), commit_authored)


	def write_project_commit_committed_to_disk(self, user_name, commit_committed):
			"""
			Writes an issue of a repository to disk.

			:param repo_name: the name of the repository.
			:param issue: the issue to be written to disk.
			"""
			if always_write_to_disk:
				rootfolder = os.path.join(dataFolderPath, user_name)
				self.write_json_to_file(os.path.join(rootfolder, "commit_committed", str(commit_committed["sha"]) + ".json"), commit_committed)

	def write_project_issue_assigned_to_disk(self, user_name, issues_assigned):
			"""
			Writes an issue of a repository to disk.

			:param repo_name: the name of the repository.
			:param issue: the issue to be written to disk.
			"""
			if always_write_to_disk:
				rootfolder = os.path.join(dataFolderPath, user_name)
				self.write_json_to_file(os.path.join(rootfolder, "issues_assigned", str(issues_assigned["id"]) + ".json"), issues_assigned)

	def write_project_issue_authored_to_disk(self, user_name, issues_authored):
			"""
			Writes an issue of a repository to disk.

			:param repo_name: the name of the repository.
			:param issue: the issue to be written to disk.
			"""
			if always_write_to_disk:
				rootfolder = os.path.join(dataFolderPath, user_name)
				self.write_json_to_file(os.path.join(rootfolder, "issues_authored", str(issues_authored["id"]) + ".json"), issues_authored)


	def write_project_issue_mentions_to_disk(self, user_name, issues_mentions):
			"""
			Writes an issue of a repository to disk.

			:param repo_name: the name of the repository.
			:param issue: the issue to be written to disk.
			"""
			if always_write_to_disk:
				rootfolder = os.path.join(dataFolderPath, user_name)
				self.write_json_to_file(os.path.join(rootfolder, "issues_mentions", str(issues_mentions["id"]) + ".json"), issues_mentions)


	def write_project_issue_commented_to_disk(self, user_name, issues_commented):
			"""
			Writes an issue of a repository to disk.

			:param repo_name: the name of the repository.
			:param issue: the issue to be written to disk.
			"""
			if always_write_to_disk:
				rootfolder = os.path.join(dataFolderPath, user_name)
				self.write_json_to_file(os.path.join(rootfolder, "issues_commented", str(issues_commented["id"]) + ".json"), issues_commented)


	def write_project_issue_owned_to_disk(self, user_name, issues_owned):
			"""
			Writes an issue of a repository to disk.

			:param repo_name: the name of the repository.
			:param issue: the issue to be written to disk.
			"""
			if always_write_to_disk:
				rootfolder = os.path.join(dataFolderPath, user_name)
				self.write_json_to_file(os.path.join(rootfolder, "issues_owned", str(issues_owned["id"]) + ".json"), issues_owned)


	def write_project_repos_owned_to_disk(self, user_name, repositories_owned):
			"""
			Writes an issue of a repository to disk.

			:param repo_name: the name of the repository.
			:param issue: the issue to be written to disk.
			"""
			if always_write_to_disk:
				rootfolder = os.path.join(dataFolderPath, user_name)
				self.write_json_to_file(os.path.join(rootfolder, "repositories_owned", str(repositories_owned["id"]) + ".json"), repositories_owned)




