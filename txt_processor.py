# Created by pren1 at 5/24/2019

import pdb
import numpy as np

# Deal with the strings within txt, count the string frequency

class txt_processor:
	def __init__(self, path_to_txt, target_danmaku_list = []):
		self.path = path_to_txt
		self.target_danmaku_list = target_danmaku_list
		self.txt_list = []

	def read_target_txt(self):
		# Read in target txt into a string list
		if not self.path.endswith('.txt'):
			assert(1==0), file+" extension is not txt"
		with open(self.path, "r") as txtfile:
			data = txtfile.readlines()
		# Remove '\n'
		self.txt_list = [string.rstrip('\n') for string in data]
		# process the readin list with format: [Time, UID, Message]
		self.txt_list = self.preprocess_readin_list()
		# Turn to numpy array...
		self.txt_list = np.asarray(self.txt_list)
		return self.txt_list
	
	def Find_Fashion_message(self):
		if len(self.txt_list) == 0:
			return []
		# Process the data, and figure out the message that occurs frequently within a small time-interval
		Message_detected = self.Slide_time_interval_window()
		# remove the duplicate messages in Message_detected
		unique_message_found = np.unique(Message_detected)
		return unique_message_found

	def Uid_scanner(self):
		# Scan all the danmaku, and find all the UIDs that sends those danmakus(?)
		if len(self.txt_list) == 0:
			return []
		assert len(self.target_danmaku_list) > 0
		UID_suspector = []
		for single_ in self.txt_list:
			if single_[2] in self.target_danmaku_list:
				UID_suspector.append(single_[1])
		return UID_suspector

	def preprocess_readin_list(self):
		# Remove the SPEAKERNUM, and append Time stamp to each message
		new_list = []
		# Avoid bug
		current_time_stamp = 0
		for single_string in self.txt_list:
			if single_string[:4] == 'TIME':
				current_time_stamp = self.Time_to_stamp_number(single_string)
			elif single_string[:10] == 'SPEAKERNUM':
				continue
			else:
				# Find the first occurance of ':'
				sign_pos = single_string.find(':')
				if sign_pos == -1:
					# Assign a fake UID
					UID = 114514
					message = single_string
				else:
					# assert single_string[:sign_pos].isdigit() == True
					if single_string[:sign_pos].isdigit() != True:
						# Assign a fake UID, in this condition, the string itself contains ':', and no UID is provided here
						UID = 114514
						message = single_string
					else:
						UID = int(single_string[:sign_pos])
						message = single_string[sign_pos + 1:]
				new_list.append([current_time_stamp, UID, message])
		return new_list

	def Time_to_stamp_number(self, time_string):
		assert time_string[:4] == 'TIME'
		# First, remove the first four characters: 'TIME'
		time_string = time_string[4:]
		# Then, find the position of the string 'ONLINE'
		end_pos = time_string.find('ONLINE')
		# After that, get the time string we need:
		time_string = time_string[:end_pos].split(':')
		assert len(time_string) == 2
		hour = int(time_string[0])
		minute = int(time_string[1])
		fin_time = hour * 60 + minute
		return fin_time

	def Slide_time_interval_window(self):
		# Window_size, which means that we are considering an time interval of 2 minutes
		Window_size = 2
		# Calculate_threshold, if a message occurs more than Calculate_threshold times within a time interval record it
		Calculate_threshold = 5
		# Ok, let's slide over the total self.txt_list!
		Time_seq = self.txt_list[:, 0].astype(np.int32)
		UID_seq = self.txt_list[:, 1].astype(np.int32)
		Message = self.txt_list[:, 2]
		# Skip if the time interval is too small
		if len(Time_seq) < 2:
			return []
		Detected_message = []
		for time_index in range(Time_seq[-1] - Window_size + 1):
			# Find all the array index within the time interval time_index:time_index + 1
			index_list = []
			for index, time in zip(range(len(Time_seq)), Time_seq):
				if time >= time_index and time <= time_index + 1:
					index_list.append(index)
			# Skip if no message occur within such an interval
			if len(index_list) == 0:
				continue
			# Then, obtain the corresponding message lists
			Message_list = Message[index_list]
			# Process the unique message:
			Message_unique, index_unique, count_unique = np.unique(Message_list, return_index = True, return_counts=True)
			for count_index in range(len(count_unique)):
				if count_unique[count_index] > Calculate_threshold:
					Detected_message.append(Message_unique[count_index])
		return Detected_message










