# Created by pren1 at 5/24/2019
# Notice that the python3 should be used
# Run this file to obtain the fashion danmaku lists

import pdb
import time
from File_scan import File_scan
from txt_processor import txt_processor

def print_output_to_file(file_name, data):
	# write data into files
	with open(file_name, "a") as file:
		for single_data in data:
			file.write(str(single_data) + '\n')

if __name__ == '__main__':
	input_path = "bilibili-vtuber-danmaku-master/"
	output_path = "Fashion_message.txt"
	file_scan = File_scan(input_path)
	all_file_paths = file_scan.path_gen()
	Fashion_message_list = []
	for (process_index, single_file_path) in zip(range(len(all_file_paths)), all_file_paths):
		start_time = time.time()
		# process_index = 7
		# single_file_path = all_file_paths[process_index]
		processor = txt_processor(single_file_path)
		Fashion_message = processor.read_target_txt()
		if len(Fashion_message) > 0:
			Fashion_message_list.append(Fashion_message)
			print_output_to_file(output_path, Fashion_message)
		print("{}th data processed within {}".format(process_index, "--- %s seconds ---" % (time.time() - start_time)))
