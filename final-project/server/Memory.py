'''
THIS IS A MEMORY MODULE ON THE SREVER WHICH ACTS LIKE MEMORY OF FILE SYSTEM. ALL THE OPERATIONS REGARDING THE FILE SYSTEM OPERATES IN 
THIS MODULE. THE MODULE HAS POINTER TO DISK AND HAS EXACT SAME LAYOUT AS UNIX TYPE FILE SYSTEM.
'''  
import config, DiskLayout


#POINTER TO DISK
sblock = DiskLayout.SuperBlock()			 


#BOOTS THE FILE SYSTEM
class Initialize():
    def __init__(self):
        #ALLOCATING BITMAP BLOCKS 0 AND 1 BLOCKS ARE RESERVED FOR BOOT BLOCK AND SUPERBLOCK
        sblock.BITMAP_BLOCKS_OFFSET, count = 2, 2 
        for i in range(0, sblock.TOTAL_NO_OF_BLOCKS / sblock.BLOCK_SIZE):  	
            sblock.ADDR_BITMAP_BLOCKS.append(DiskLayout.Bitmap_Block(sblock.BLOCK_SIZE))
            count += 1
        #ALLOCATING INODE BLOCKS
        sblock.INODE_BLOCKS_OFFSET = count
        for i in range(0, (sblock.MAX_NUM_INODES * sblock.INODE_SIZE) / sblock.BLOCK_SIZE):		#for Inode blocks
            sblock.ADDR_INODE_BLOCKS.append(DiskLayout.Inode_Block(sblock.INODES_PER_BLOCK))
            count  += 1
        #ALLOCATING DATA BLOCKS
        sblock.DATA_BLOCKS_OFFSET = count
        for i in range(sblock.DATA_BLOCKS_OFFSET, sblock.TOTAL_NO_OF_BLOCKS):
            sblock.ADDR_DATA_BLOCKS.append(DiskLayout.Data_Block(sblock.BLOCK_SIZE))
        #MAKING BLOCKS BEFORE DATA BLOCKS UNAVAILABLE FOR USE SINCE OCCUPIED BY SUPERBLOCK, BOOTBLOCK, BITMAP AND INODE TABLE
        for i in range(0, sblock.DATA_BLOCKS_OFFSET): 
            sblock.ADDR_BITMAP_BLOCKS[i / sblock.BLOCK_SIZE].block[i % sblock.BLOCK_SIZE] = -1


#OPERATIONS ON FILE SYSTEM
class Operations():

    #GIVES ADDRESS OF INODE TABLE
    def addr_inode_table(self):				
        return sblock.ADDR_INODE_BLOCKS


    #RETURNS THE DATA OF THE BLOCK
    def get_data_block(self, block_number):	
        if block_number == 0: print("Memory: Reserved for Boot Block")
        elif block_number == 1: print("Memory: Reserved for Super Block")
        elif block_number >= sblock.BITMAP_BLOCKS_OFFSET and block_number < sblock.INODE_BLOCKS_OFFSET:
            return sblock.ADDR_BITMAP_BLOCKS[block_number - sblock.BITMAP_BLOCKS_OFFSET].block
        elif block_number >= sblock.INODE_BLOCKS_OFFSET and block_number < sblock.DATA_BLOCKS_OFFSET:
            return sblock.ADDR_INODE_BLOCKS[block_number - sblock.INODE_BLOCKS_OFFSET].block
        elif block_number >= sblock.DATA_BLOCKS_OFFSET and block_number < sblock.TOTAL_NO_OF_BLOCKS:
            return sblock.ADDR_DATA_BLOCKS[block_number - sblock.DATA_BLOCKS_OFFSET].block
        return -1


    #RETURNS THE BLOCK NUMBER OF AVAIALBLE DATA BLOCK  
    def get_valid_data_block(self):			
        for i in range(0, sblock.TOTAL_NO_OF_BLOCKS):
            if sblock.ADDR_BITMAP_BLOCKS[i / sblock.BLOCK_SIZE].block[i % sblock.BLOCK_SIZE] == 0:
                sblock.ADDR_BITMAP_BLOCKS[i / sblock.BLOCK_SIZE].block[i % sblock.BLOCK_SIZE] = 1
                return i
        print("Memory: No valid blocks available")
        return -1

    #REMOVES THE INVALID DATA BLOCK TO MAKE IT REUSABLE
    def free_data_block(self, block_number):  	
        sblock.ADDR_BITMAP_BLOCKS[block_number / sblock.BLOCK_SIZE].block[block_number % sblock.BLOCK_SIZE] = 0
        b = sblock.ADDR_DATA_BLOCKS[block_number - sblock.DATA_BLOCKS_OFFSET].block
        for i in range(0, sblock.BLOCK_SIZE): b[i] = '\0'


    #WRITES TO THE DATA BLOCK
    def update_data_block(self, block_number, block_data):		
        b = sblock.ADDR_DATA_BLOCKS[block_number - sblock.DATA_BLOCKS_OFFSET].block
        for i in range(0, len(block_data)): b[i] = block_data[i]
        #print("Memory: Data Copy Completes")
    
    
    #UPDATES INODE TABLE WITH UPDATED INODE
    def update_inode_table(self, inode, inode_number):
        sblock.ADDR_INODE_BLOCKS[inode_number / sblock.INODES_PER_BLOCK].block[inode_number % sblock.INODES_PER_BLOCK] = inode

    
    #RETURNS THE INODE FROM INODE NUMBER
    def inode_number_to_inode(self, inode_number):
        return sblock.ADDR_INODE_BLOCKS[inode_number / sblock.INODES_PER_BLOCK].block[inode_number % sblock.INODES_PER_BLOCK]
