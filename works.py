#This is my code that worked

import requests
import os
import json
import codecs


url = 'https://api.github.com/search/commits'
headers = {'Accept':'application/vnd.github.cloak-preview', 'Authorization':'token 293082ef9f1fc1408a19acc44640ec0ac0f76c11'}
user_name = 'nbriz'
params = {'q':'committer:'+user_name} # 'per_page':'100'
dataFolderPath = '/Users/georgia/Desktop/'



def create_folder_if_it_does_not_exist(foldername):
	"""
	Creates a folder in the filesystem if it does not already exist.

	:param foldername: the path to the folder to be created.
	"""
	if not os.path.exists(foldername):
		os.makedirs(foldername)


def initialize_write_to_disk(user_name):
	"""
	Initializes the writing of a project to disk. Creates all the necessary directories.

	:param user_name: the name of the repository to be written to disk.
	"""
	rootfolder = os.path.join(dataFolderPath, user_name)
	create_folder_if_it_does_not_exist(os.path.join(rootfolder, "committs_committed2"))
	return rootfolder

def write_json_to_file(data, filename):
	'''
	Function that writes json format to a file
	input
	data: any data in string format 
	filename: the name of the file for the data to be saved to
	'''
	#data_dict= json.loads(data.text)
	with  codecs.open(filename +'.json', 'w', encoding = 'utf-8') as file:
		file.write(json.dumps(data, indent=4, sort_keys = True, ensure_ascii = False))

def get_request(url, params, headers):
	
	if params:
		parameters='?' + '&'.join('{}={}'.format(key, val) for key, val in params.items())
	else: 
		parameters= ""

	r = requests.get(url+parameters,  headers=headers)
	return r


def download_paginated_object(url, params, headers):
	
	if not 'per_page' in params:
		params['per_page']=100

	r = get_request(url,  params,  headers)
	
	if(r.ok):
		data_dict= json.loads(r.text)
		for i in data_dict["items"]:
			name_file = os.path.join(rootfolder, "committs_committed2",str(i["sha"]))
			write_json_to_file(i, name_file)

	while True:
		try:
			#print(r.headers['Authorization'])
			links = {}
			for link in r.headers['Link'].split(", "):
				linkaddress, linktype = link.split("; ")
				linkaddress = linkaddress[1:-1]
				linktype = linktype.split("\"")[1]
				links[linktype] = linkaddress

			if "next" in links:
				relnext = links["next"]
				is_relnext = True
			else:
				is_relnext = False
				
		except (KeyError, ValueError):
			break
		

		if is_relnext:
			r = get_request(relnext, {},headers= headers)
			print(r.url)
			#print(r.headers)
		else:
			break
		
		if(r.ok):
			r_dict = json.loads(r.text)
			#print("it enters here")
			for obj in r_dict["items"]:
				#yield obj
				name_file = os.path.join(rootfolder, "committs_committed2",str(obj["sha"]))
				write_json_to_file(obj, name_file)
				#print("it gets in here2")



rootfolder = initialize_write_to_disk(user_name)
download_paginated_object(url, params=params, headers=headers)




