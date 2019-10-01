'''
THIS MODULE ACTS AS A INODE NUMBER LAYER. NOT ONLY IT SHARES DATA WITH INODE LAYER, BUT ALSO IT CONNECTS WITH MEMORY INTERFACE FOR INODE TABLE 
UPDATES. THE INODE TABLE AND INODE NUMBER IS UPDATED IN THE FILE SYSTEM USING THIS LAYER
'''
import InodeLayer, config, MemoryInterface, datetime, InodeOps, MemoryInterface

#HANDLE OF INODE LAYER
interface = InodeLayer.InodeLayer()

class InodeNumberLayer():

	#PLEASE DO NOT MODIFY
	#ASKS FOR INODE FROM INODE NUMBER FROM MemoryInterface.(BLOCK LAYER HAS NOTHING TO DO WITH INODES SO SEPERTAE HANDLE)
	def INODE_NUMBER_TO_INODE(self, inode_number):
		array_inode = MemoryInterface.inode_number_to_inode(inode_number)
		inode = InodeOps.InodeOperations().convert_array_to_table(array_inode)
		if inode: inode.time_accessed = datetime.datetime.now()   #TIME OF ACCESS
		return inode


	#PLEASE DO NOT MODIFY
	#RETURNS DATA BLOCK FROM INODE NUMBER
	def INODE_NUMBER_TO_BLOCK(self, inode_number, offset, length):
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if not inode:
			print("Error InodeNumberLayer: Wrong Inode Number! \n")
			return -1
		return interface.read(inode, offset, length)


	#PLEASE DO NOT MODIFY
	#UPDATES THE INODE TO THE INODE TABLE
	def update_inode_table(self, table_inode, inode_number):
		if table_inode: table_inode.time_modified = datetime.datetime.now()  #TIME OF MODIFICATION 
		array_inode = InodeOps.InodeOperations().convert_table_to_array(table_inode)
		MemoryInterface.update_inode_table(array_inode, inode_number)


	#PLEASE DO NOT MODIFY
	#FINDS NEW INODE INODE NUMBER FROM FILESYSTEM
	def new_inode_number(self, type, parent_inode_number, name):
		if parent_inode_number != -1:
			parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
			if not parent_inode:
				print("Error InodeNumberLayer: Incorrect Parent Inode")
				return -1
			entry_size = config.MAX_FILE_NAME_SIZE + len(str(config.MAX_NUM_INODES))
			max_entries = (config.INODE_SIZE - 79 ) / entry_size
			if len(parent_inode.directory) == max_entries:
				print("Error InodeNumberLayer: Maximum inodes allowed per directory reached!")
				return -1
		for i in range(0, config.MAX_NUM_INODES):
			if self.INODE_NUMBER_TO_INODE(i) == False: #FALSE INDICTES UNOCCUPIED INODE ENTRY HENCE, FREEUMBER
				inode = interface.new_inode(type)
				inode.name = name
				self.update_inode_table(inode, i)
				return i
		print("Error InodeNumberLayer: All inode Numbers are occupied!\n")


	# LINKS THE INODE
	# creates a hard link with name "new_path" to the object resolved by "old_path"
	def link(self, file_inode_number, hardlink_name, hardlink_parent_inode_number):
		file_inode = self.INODE_NUMBER_TO_INODE(file_inode_number)
		hardlink_parent_inode = self.INODE_NUMBER_TO_INODE(hardlink_parent_inode_number)
		# check for None types
		if not file_inode or not hardlink_parent_inode:
			return -1
		# 0 -> file, 1 -> directory
		if file_inode.type != 0 or hardlink_parent_inode.type != 1:
			return -1

		if hardlink_name == "" or len(hardlink_name) > config.MAX_FILE_NAME_SIZE:
			return -1

		hardlink_parent_inode.directory[hardlink_name] = file_inode_number
		file_inode.links += 1

		self.update_inode_table(hardlink_parent_inode, hardlink_parent_inode_number	)
		self.update_inode_table(file_inode, file_inode_number)

		return True


	# REMOVES THE INODE ENTRY FROM INODE TABLE
	# removes a link in the file system; if it is the last link to be removed for the inode_number, free all blocks associated with the
	# inode (if it is a file inode), and free the inode. Note: an inode for a non-empty directory cannot be removed.
	def unlink(self, inode_number, parent_inode_number, filename):
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
		# check for None types
		if not inode or not parent_inode:
			return -1
		# 0 -> file, 1 -> directory
		if inode.type != 0 or parent_inode.type != 1:
			return -1

		if filename in parent_inode.directory:
			del parent_inode.directory[filename]
		else:
			return -1

		inode.links -= 1

		if inode.links == 0:
			interface.free_data_block(inode, 0)
			del inode
	
		self.update_inode_table(inode, inode_number)
		self.update_inode_table(parent_inode, parent_inode_number)

		return True


	# IMPLEMENTS WRITE FUNCTIONALITY
	# writes "data" to a file, starting at "offset".
	def write(self, inode_number, offset, data, parent_inode_number):
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)

		# check for None types
		if not inode or not parent_inode:
			return -1
		# 0 -> file, 1 -> directory
		if inode.type != 0 or parent_inode.type != 1:
			return -1

		inode = interface.write(inode, offset, data)
		# an error occured if the write_res was -1
		if inode == -1: return -1

		self.update_inode_table(inode, inode_number)
		self.update_inode_table(parent_inode, parent_inode_number)

		return True


	# IMPLEMENTS READ FUNCTIONALITY
	# reads "length" bytes from a file, starting at offset
	def read(self, inode_number, offset, length, parent_inode_number):
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)

		# check for None types
		if not inode or not parent_inode:
			return -1
		# 0 -> file, 1 -> directory
		if inode.type != 0 or parent_inode.type != 1:
			return -1
			
		read_res = interface.read(inode, offset, length)
		# an error occured if the read_res was -1
		if (read_res == -1): return -1

		inode, read_data = read_res

		self.update_inode_table(inode, inode_number)
		self.update_inode_table(parent_inode, parent_inode_number)

		return read_data