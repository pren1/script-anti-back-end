# Created by pren1 at 5/24/2019
# Notice that the python3 should be used
# Run this file to obtain the fashion danmaku lists

import pdb
import time
import numpy as np
import sys
from File_scan import File_scan
from txt_processor import txt_processor


def print_output_to_file(file_name, data):
	# write data into files
	with open(file_name, "a") as file:
		for single_data in data:
			file.write(str(single_data) + '\n')

def print_output_to_file_spec(file_name, data):
	# For this, we would like to output in a list fashion...
	# write data into files
	with open(file_name, "a") as file:
		file.write('[')
		for single_data in data:
			file.write(str(single_data) + ',')
		file.write(']')

def Merge_similar_things(Message_list):
	# For example, merge 888888 and 888 together
	new_message_list = []
	for message in Message_list:
		if message[:3] == '233':
			message = "233333"
		elif message[:3] == '666':
			message = "666666"
		elif message[:3] == '888':
			message = "888888"
		elif message[:3] == '哈哈哈':
			message = "哈哈哈"
		elif message[:3] == 'nee':
			message = "neeeee"
		elif message[:1] == '？':
			message = "？？？？？"
		new_message_list.append(message)
	return new_message_list

def Get_unique_fassion_message(output_path, Fassion_message_path):
	# Remove duplicate messages in the "Fashion_message_total.txt" file
	processor = txt_processor(output_path)
	Message_list = processor.read_target_txt()
	# Last dim of message_list
	Message_list = Message_list[:, 2]
	# Merge similar things together
	New_Message_list = Merge_similar_things(Message_list)
	# Unique!
	unique_message_list, count = np.unique(New_Message_list, return_counts = True)
	count_sort_ind = np.argsort(-count)
	unique_message_list = unique_message_list[count_sort_ind]
	print_output_to_file(Fassion_message_path, unique_message_list)
	return unique_message_list

if __name__ == '__main__':
	assert len(sys.argv)==2, "wrong input parameter length, require 1, input {}".format(len(sys.argv))
	Run_Fashion = sys.argv[1]
	input_path = "bilibili-vtuber-danmaku-master/"
	output_path = "Fashion_message_total.txt"
	Fassion_message_path = "Fashion_message.txt"
	suspect_UID_path = "UID.txt"
	file_scan = File_scan(input_path)
	all_file_paths = file_scan.path_gen()
	Fashion_message_list = []
	if Run_Fashion == 'True':
		# Scan and figure out the Fashion_message
		# The results are saved on the Fashion_message.txt, so you do not need to run the following
		# for loop again :D
		for (process_index, single_file_path) in zip(range(len(all_file_paths)), all_file_paths):
			start_time = time.time()
			# process_index = 7
			# single_file_path = all_file_paths[process_index]
			processor = txt_processor(single_file_path)
			processor.read_target_txt()
			Fashion_message = processor.Find_Fashion_message()

			if len(Fashion_message) > 0:
				Fashion_message_list.append(Fashion_message)
				print_output_to_file(output_path, Fashion_message)
			print("{}th data processed within {}".format(process_index, "--- %s seconds ---" % (time.time() - start_time)))
		# Obtain the Fashion_message.txt
		Get_unique_fassion_message(output_path, Fassion_message_path)
	else:
		# Here is the harmful message I obtained from the Fashion_message_list:
		suspect_UIDs = []
		target_danmaku_list = ["我宫内莲华来呼吸夏哥了！",
			"我是“774ガチ恋勢”，我前来DD了！",
			"俺のID「774ガチ恋勢」ですよろしく",
			"来DD了，我是宫内莲华Official", 
			"宫内莲华Official，前来DD了！",
			"俺の名は774ガチ恋勢です，よろしく！",
			"俺のID「774ガチ恋勢」です",
			"僕の名は774ガチ恋勢です，よろしく"]
		for (process_index, single_file_path) in zip(range(len(all_file_paths)), all_file_paths):
			start_time = time.time()
			processor = txt_processor(single_file_path, target_danmaku_list)
			processor.read_target_txt()
			UID_list = processor.Uid_scanner()
			if len(UID_list) > 0:
				suspect_UIDs.extend(UID_list)
			print("{}th data processed within {}".format(process_index, "--- %s seconds ---" % (time.time() - start_time)))
		# Finally, select the unique UID
		final_UIDs = []
		for UIDs in suspect_UIDs:
			if UIDs not in final_UIDs:
				final_UIDs.append(UIDs)
		print_output_to_file_spec(suspect_UID_path, final_UIDs)
		pdb.set_trace()











