'''
THIS MODULE IS INODE LAYER OF THE FILE SYSTEM. IT INCLUDES THE INODE DEFINITION DECLARATION AND GLOBAL HANDLE OF BLOCK LAYER OF API.
THIS MODULE IS RESPONSIBLE FOR PROVIDING ACTUAL BLOCK NUMBERS SAVED IN INODE ARRAY OF BLOCK NUMBERS TO FETCH DATA FROM BLOCK LAYER.
'''
import datetime, config, BlockLayer, InodeOps

#HANDLE OF BLOCK LAYER
interface = BlockLayer.BlockLayer()

class InodeLayer():

    #RETURNS BLOCK NUMBER FROM RESPECTIVE INODE DIRECTORY
    def INDEX_TO_BLOCK_NUMBER(self, inode, index):
        if index == len(inode.blk_numbers): return -1
        return inode.blk_numbers[index]


    #RETURNS BLOCK DATA FROM INODE
    def INODE_TO_BLOCK(self, inode, offset):
        index = offset / config.BLOCK_SIZE
        block_number = self.INDEX_TO_BLOCK_NUMBER(inode, index)
        if block_number == -1: return ''
        else: return interface.BLOCK_NUMBER_TO_DATA_BLOCK(block_number, delay_sec=0)


    #MAKES NEW INODE OBJECT
    def new_inode(self, type):
        return InodeOps.Table_Inode(type)


    #FLUSHES ALL THE BLOCKS OF INODES FROM GIVEN INDEX OF MAPPING ARRAY  
    def free_data_block(self, inode, index):
        for i in range(index, len(inode.blk_numbers)):
            interface.free_data_block(inode.blk_numbers[i])
            inode.blk_numbers[i] = -1


    def validate_inode_as_file(self, inode):
        # 0 -> file
        if (inode.type != 0):
            raise Exception('Inode type is not that of a file.')


    def calculate_blk_range(self, offset, length):
        # ex1
        # abcX XXXX Xjkl mnop
        # offset = 3, len(data) = 6
        # first_block = 3/4 = 0
        # last_block = (6 + 3 - 1)/4 - 0 = 2

        # ex2
        # abXX XXXX ijkl mnop
        # offset = 2, len(data) = 6
        # first_block = 2/4 = 0
        # last_block = (6 + 2 - 1)/4 - 0 = 1

        # ex3
        # XXXX XXXX ijkl mnop
        # offset = 0, len(data) = 8
        # first_block = 0/4 = 0
        # last_block = (8 + 0 - 1)/4 - 0 = 1

        first_blk_index = offset/config.BLOCK_SIZE
        last_blk_index = (length + offset - 1)/config.BLOCK_SIZE - first_blk_index;

        return first_blk_index, last_blk_index


    #IMPLEMENTS WRITE FUNCTIONALITY
    def write(self, inode, offset, data, delay_sec):
        # return an error if the inode type is not a file
        self.validate_inode_as_file(inode)

        first_blk_index, last_blk_index = self.calculate_blk_range(offset, len(data))

        # return an error if writing from an offset larger than the file size
        if (first_blk_index >= len(inode.blk_numbers)):
            return -1

        byte_nums_to_overwrite = range(offset, offset+len(data))
        curr_byte_num = first_blk_index*config.BLOCK_SIZE
        next_data_byte = 0

        # range over the blocks that we have to update
        for curr_blk_index in range(first_blk_index, last_blk_index+1):

            # truncate data if attempting to write beyond the maximum size of a file
            if (curr_blk_index >= len(inode.blk_numbers)):
                break

            blk_num = inode.blk_numbers[curr_blk_index]
            if blk_num == -1:
                blk_num = interface.get_valid_data_block()
                inode.blk_numbers[curr_blk_index] = blk_num

            # read data at blk_num
            old_data = interface.BLOCK_NUMBER_TO_DATA_BLOCK(blk_num, delay_sec=0)
            data_to_write = ""

            # builds data_to_write from either the old_data or data, dependent on the curr_byte_num
            for old_data_byte in old_data:
                if (curr_byte_num in byte_nums_to_overwrite):
                    data_to_write += data[next_data_byte]
                    next_data_byte += 1
                else:
                    data_to_write += old_data_byte
                curr_byte_num += 1

            interface.update_data_block(blk_num, data_to_write, delay_sec)

        # update "accessed" and "modified" times in the inode
        inode.time_modified = str(datetime.datetime.now())[:19]
        inode.time_accessed = str(datetime.datetime.now())[:19]

        # Returns the updated "inode" object
        return inode

    #IMPLEMENTS THE READ FUNCTION 
    def read(self, inode, offset, length, delay_sec): 
        # validate that we are operating on a file
        self.validate_inode_as_file(inode)

        if (length == -1):
            first_blk_index, last_blk_index = 0, len(inode.blk_numbers)-1
            byte_nums_to_read = range(offset, (last_blk_index+1)*config.BLOCK_SIZE)
        else:
            first_blk_index, last_blk_index = self.calculate_blk_range(offset, length)
            byte_nums_to_read = range(offset, offset+length)

        # return an error if writing from an offset larger than the file size
        if (first_blk_index >= len(inode.blk_numbers)):
            return -1

        curr_byte_num = first_blk_index*config.BLOCK_SIZE
        read_data = ""

        # range over the blocks that we have to read from
        for curr_blk_index in range(first_blk_index, last_blk_index+1):

            # break if there is no data block defined at this index to read from or if attempting to
            # read beyond the maximum size of a file
            curr_blk_num = self.INDEX_TO_BLOCK_NUMBER(inode, curr_blk_index)
            if curr_blk_num == -1:
                break

            # read data at blk_num
            curr_blk_data = interface.BLOCK_NUMBER_TO_DATA_BLOCK(curr_blk_num, delay_sec)

            # choose data from either the old data or the new string, dependent on the curr_byte_num
            for curr_data_byte in curr_blk_data:
                if (curr_byte_num in byte_nums_to_read):
                    read_data += curr_data_byte
                curr_byte_num += 1

        # update "accessed" time in the inode
        inode.time_accessed = str(datetime.datetime.now())[:19]

        return inode, read_data


    def copy(self, old_inode):
        # validate that we are operating on a file
        self.validate_inode_as_file(old_inode)
        
        # sets the type of the new inode
        new_inode = self.new_inode(old_inode.type)
        
        # perform a deep copy on all of the old_inode blocks
        for i in range(0,len(old_inode.blk_numbers)):
            old_blk_num = old_inode.blk_numbers[i]
            # if the old index was never assigned, continue
            if (old_blk_num == -1):
                continue
            # retrieve the old data and set the new data to be the old data
            old_blk_data = interface.BLOCK_NUMBER_TO_DATA_BLOCK(old_blk_num, delay_sec=0)
            new_blk_num = interface.get_valid_data_block()
            interface.update_data_block(new_blk_num, old_blk_data, delay_sec=0)

            # persist the new block number that was allocated in the blk_numbers list of the new_inode
            new_inode.blk_numbers[i] = new_blk_num

        # copy the old directory contents (should be empty because we are operating on a file)
        new_inode.directory = old_inode.directory

        # new_inode.time_created set in the constructor

        # new_inode.time_accessed set in the constructor
        
        # new_inode.time_modified set in the constructor

        # new_inode.size set in the constructor

        # new_inode.links set in the constructor

        new_inode.name = old_inode.name

        old_inode.time_accessed  = str(datetime.datetime.now())[:19]
        return new_inode
