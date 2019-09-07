import BlockLayer, sys, math, config, MemoryInterface

MemoryInterface.Initialize_My_FileSystem()
interface = BlockLayer.BlockLayer()

class Operations():
	def __init__(self):
		self.map = []
		self.base_block = interface.get_valid_data_block()
		interface.free_data_block(self.base_block)

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
		base_addr = self.base_block*config.BLOCK_SIZE-1

		first_block = self.base_block + offset/config.BLOCK_SIZE
		last_block = first_block + len(string)/config.BLOCK_SIZE

		if (first_block not in self.map):
			raise Exception("Attempted to offset write to an unallocated block.")

		addrs_to_overwrite = range(base_addr+offset,base_addr+offset+len(string))
		curr_addr = first_block*config.BLOCK_SIZE-1
		string_pointer = 0

		for current_block in range(first_block, last_block+1):
			# add memory blocks to pad offset if we have not allocated enough blocks yet
			while (current_block not in self.map):
				self.map.append(interface.get_valid_data_block())

			# read data block at valid_block_number
			old_data = interface.BLOCK_NUMBER_TO_DATA_BLOCK(current_block)
			new_data = ""

			# choose data from either the old data or the new string, dependent on the curr_addr
			for old_data_char in old_data:
				if (curr_addr in addrs_to_overwrite):
					new_data+=string[string_pointer]
					string_pointer+=1
				else:
					new_data += old_data_char
				curr_addr+=1

			interface.update_data_block(current_block, new_data)

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