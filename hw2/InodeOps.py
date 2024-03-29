'''
THIS MODULE PERFORMS HAS INODE STRUCTURE DEFINITIONS.
'''

import datetime, config

#TABLE INODE STRUCTURE FOR LOCAL USE OF OPERATIONS
class Table_Inode():
	def __init__(self, _type): 
		# 0 -> file, 1 -> directory
		self.type = _type
		# blk_numbers is the same as (self.map in HW1) mapping table between actual block numbers in memory vs relative block numbers 
		self.blk_numbers = [-1 for _ in range(((config.INODE_SIZE - 63 - config.MAX_FILE_NAME_SIZE) / 2))]
		self.directory = dict() # for storing directory inodes
		self.time_created = str(datetime.datetime.now())[:19]
		self.time_accessed = str(datetime.datetime.now())[:19]
		self.time_modified = str(datetime.datetime.now())[:19]
		self.size = 0 if self.type == 0 else len(self.directory)
		self.links = 2 if self.type == 1 else 1
		self.name = ""

# 63 = (19bytes)time accessed + (19bytes)time created + (19bytes)time modified  + (2 bytes)InodeType + (2 bytes)Size of file