import BlockLayer, sys, config, MemoryInterface

MemoryInterface.Initialize_My_FileSystem()
interface = BlockLayer.BlockLayer()

class Operations():
	def __init__(self):
		self.map = []

	#WRITES STRING1
	def write(self, string):
		data_array = []
		# verify that string is of type string
		for i in range(0, len(string), config.BLOCK_SIZE):
			# divide up the string into chunks of length BLOCK_SIZE
			data_array.append(string[i : i + config.BLOCK_SIZE])
		self.__write_to_filesystem(data_array)

	#READS THE STRING
	def read(self):
		data = []
		for i in range(len(self.map)):
			# index through block numbers in map to get data blocks
			data.append(interface.BLOCK_NUMBER_TO_DATA_BLOCK(self.map[i]))
		print( "".join(data))
		return "".join(data)

	#WRITE TO FILESYSTEM
	def __write_to_filesystem(self, data_array):
		for i in range(len(data_array)):
			valid_block_number = interface.get_valid_data_block()
			interface.update_data_block(valid_block_number, data_array[i])
			self.map.append(valid_block_number)

	#STATUS FUNCTION TO CHECK THE STATUS OF THE DATA BLOCKS IN THE MEMORY
	def status(self):
		print(MemoryInterface.status())

	# WRITE TO OFFSET (refer to assignment doc)
	def write_to_offset(self,offset,string):
		# range from blocks offset/4 -> offset/4+len(string)/4
		first_map_index = offset/config.BLOCK_SIZE
		last_map_index = first_map_index + len(string)/config.BLOCK_SIZE
		if (first_map_index >= len(self.map)):
			raise Exception("Attempted to offset write to an unallocated block.")

		char_numbers_to_overwrite = range(offset,offset+len(string))
		curr_char_num = first_map_index*config.BLOCK_SIZE
		curr_string_pointer = 0

		for map_index in range(first_map_index, last_map_index+1):
			# add memory blocks to pad offset if we have not allocated enough blocks yet
			while (map_index >= len(self.map)):
				self.map.append(interface.get_valid_data_block())

			# get the valid block number to update from the map_index
			valid_block_number = self.map[map_index]

			# read data block at valid_block_number
			old_data = interface.BLOCK_NUMBER_TO_DATA_BLOCK(valid_block_number)
			new_data = ""

			# choose data from either the old data or the new string, dependent on the curr_char_num
			for old_data_char in old_data:
				if (curr_char_num in char_numbers_to_overwrite):
					new_data+=string[curr_string_pointer]
					curr_string_pointer+=1
				else:
					new_data += old_data_char
				curr_char_num+=1

			interface.update_data_block(valid_block_number, new_data)

if __name__ == "__main__":
	if len(sys.argv) < 4: 
		print("Usage: python HW1.py <string1> <string2> <string3>")
		exit(0)
	test = Operations()
	test.write(sys.argv[1])
	test.read()
	test.status()
	test.write_to_offset(int(sys.argv[3]),sys.argv[2])
	test.read()
	# last call 
	test.status()