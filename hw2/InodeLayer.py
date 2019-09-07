import datetime, config, BlockLayer, InodeOps, MemoryInterface


MemoryInterface.Initialize_My_FileSystem()
#HANDLE OF BLOCK LAYER
interface = BlockLayer.BlockLayer()

class InodeLayer():

    #PLEASE DO NOT MODIFY THIS
    #RETURNS ACTUAL BLOCK NUMBER FROM RESPECTIVE MAPPING  
    def INDEX_TO_BLOCK_NUMBER(self, inode, index):
        if index == len(inode.blk_numbers): return -1
        return inode.blk_numbers[index]


    #PLEASE DO NOT MODIFY THIS
    #RETURNS BLOCK DATA FROM INODE and OFFSET
    def INODE_TO_BLOCK(self, inode, offset):
        index = offset / config.BLOCK_SIZE
        block_number = self.INDEX_TO_BLOCK_NUMBER(inode, index)
        if block_number == -1: return ''
        else: return interface.BLOCK_NUMBER_TO_DATA_BLOCK(block_number)


    #PLEASE DO NOT MODIFY THIS
    #MAKES NEW INODE OBJECT
    def new_inode(self, _type):
        return InodeOps.Table_Inode(_type)


    #PLEASE DO NOT MODIFY THIS
    #FLUSHES ALL THE BLOCKS OF INODES FROM GIVEN INDEX OF MAPPING ARRAY  
    def free_data_block(self, inode, index):
        for i in range(index, len(inode.blk_numbers)):
            interface.free_data_block(inode.blk_numbers[i])
            inode.blk_numbers[i] = -1


    #IMPLEMENTS WRITE FUNCTIONALITY
    # takes as an input an “inode” object
    # writes “data”, starting from “offset”, to the blocks indexed by the inode object.
    # Returns the updated “inode” object
    def write(self, inode, offset, data):
        '''WRITE YOUR CODE HERE '''
        if (type(inode) == Table_Inode):
            1+1

    # IMPLEMENTS THE READ FUNCTION 
    # takes as an input an “inode” object (you can create using new_inode)
    # reads up to “length” bytes, starting from “offset”, from the blocks indexed by the inode object
    # returns the updated “inode” object, and the data read
    def read(self, inode, offset, length): 
        '''WRITE YOUR CODE HERE '''

    # IMPLEMENTS COPY FUNCTIONALITY
    # takes as an input an “inode” object
    # copies the entire contents associated with the input inode to a new “inode” object
    # Returns the new “inode” object
    def copy(self, inode):
        new_inode = new_inode();

    def status(self):
        print(MemoryInterface.status())



