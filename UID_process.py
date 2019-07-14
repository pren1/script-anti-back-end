# Created by pren1 at 7/13/2019
# Notice that the python3 should be used
# Run this file to get information about all the uids in UID.txt

import pdb
import time
import numpy as np
import sys
from File_scan import File_scan
from txt_processor import txt_processor
import pandas as pd

class UID_process:
	def __init__(self, UID_path, input_path, output_path):
		'initializer'
		self.UID_path = UID_path
		self.input_path = input_path
		self.output_path = output_path

		'obtain all the file paths'
		file_scan = File_scan(input_path)
		self.all_file_paths = file_scan.path_gen()

		'read in uid.txt'
		self.uid_index = self.read_uid()

		'Build dataframe'
		self.dataframe = self.build_dataframe()

	def read_uid(self):
		# Read in target txt into a string list
		if not self.UID_path.endswith('.txt'):
			assert(1==0), file+" extension is not txt"
		with open(self.UID_path, "r") as txtfile:
			data = txtfile.readlines()
		uid_list = self.convert(data[0][1:-2]).split(',')
		return uid_list

	def convert(self, s):
		# initialization of string to ""
		str1 = ""
		# using join function join the list s by
		# separating words by str1
		return (str1.join(s))

	def build_dataframe(self):
		'build a dataframe'
		columns = ['Room_counter', 'danmaku_counter', 'Room', 'Messages']
		df = pd.DataFrame(index=self.uid_index, columns=columns)
		# 'initialize the df at here'
		for uid_index in self.uid_index:
			df['Room'][uid_index] = []
			df['Messages'][uid_index] = {}
		return df

	def reiterate_danmaku_data(self):
		'read in all the txt again, then figure out the information about UIDs'
		for (process_index, single_file_path) in zip(range(len(self.all_file_paths)), self.all_file_paths):
			start_time = time.time()
			processor = txt_processor(single_file_path)
			danmaku_info_list = processor.read_target_txt()
			'obtain room id & date'
			room_id = single_file_path.split('/')[1]
			# date = single_file_path.split('/')[2][:-4]
			'iterate over all the danmaku info'
			for danmaku_info in danmaku_info_list:
				current_uid = danmaku_info[1]
				current_message = danmaku_info[2]
				'First, check if the uid lives in the list'
				if current_uid in self.uid_index:
					'Then, set everything'
					self.dataframe['Room'][current_uid].append(room_id)
					'see if we have already able to save the message'
					if room_id not in self.dataframe['Messages'][current_uid]:
						self.dataframe['Messages'][current_uid][room_id] = []
					self.dataframe['Messages'][current_uid][room_id].append(current_message)
			print("{}th data processed within {}".format(process_index, "--- %s seconds ---" % (time.time() - start_time)))

	def post_process(self):
		'count room number and message number'
		for uid_index in self.uid_index:
			self.dataframe['Room_counter'][uid_index] = len(self.dataframe['Room'][uid_index])
			'iterate over the messages'
			message_counter = 0
			for _, value in self.dataframe['Messages'][uid_index].items():
				message_counter += len(value)
			assert message_counter > 0,'no message obtained, something wrong'
			self.dataframe['danmaku_counter'][uid_index] = message_counter

	def drop_useless_uid(self, minimum_shown_number):
		'remove uid that sent too few messages'
		for uid_index in self.uid_index:
			danmaku_counter = self.dataframe['danmaku_counter'][uid_index]
			if danmaku_counter < minimum_shown_number:
				self.dataframe = self.dataframe.drop(uid_index)

	def save_res_as_csv(self):
		'save the dataframe result as csv'
		self.dataframe.to_csv(self.output_path)

if __name__ == '__main__':
	uid_path = "UID.txt"
	input_path = "bilibili-vtuber-danmaku-master/"
	output_path = "danmaku_info.csv"
	'Remove target uid unless that uid sent more than 20 messages'
	minimum_shown_number = 20
	uid_processor = UID_process(uid_path, input_path, output_path)
	uid_processor.reiterate_danmaku_data()
	uid_processor.post_process()
	uid_processor.drop_useless_uid(minimum_shown_number)
	uid_processor.save_res_as_csv()