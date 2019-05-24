# Created by pren1 at 5/24/2019

import os
import pdb

# Go over all the files with in the folders, and generate paths to every txt files
class File_scan:
	def __init__(self, input_path):
		# Initialize with the input path to dataset
		self.path = input_path

	def folder_names_in_directory(self):
		# Obtain all the folders within the dataset
		root, dirs, files = os.walk(self.path).__next__()
		# For all the dirs, only return the directory whose name is numeric
		numeric_dirs = []
		for dir_ in dirs:
			if dir_.isdigit():
				numeric_dirs.append(os.path.join(self.path, dir_))
		return numeric_dirs

	def files_in_target_folder(self, path, extension=".txt"):
		# obtain all file paths in the target folder
		res_files=[]
		for file in os.listdir(path):
			if file.endswith(extension):
				target_path=os.path.join(path, file)
				res_files.append(target_path)
		return res_files

	def path_gen(self):
		First_level_folders = self.folder_names_in_directory()
		File_path_list = []
		for folder_path in First_level_folders:
			File_lists_under_folder = self.files_in_target_folder(folder_path)
			File_path_list.extend(File_lists_under_folder)
		return File_path_list



