'''
THIS MODULE INTERACTS WITH THE MEMORY
''' 
import time, client_stub

#HANDLE FOR MEMORY OPERATIONS
client_stub = client_stub.client_stub()


#REQUEST TO BOOT THE FILE SYSTEM
def Initialize_My_FileSystem(num_servers, raid_mode):
    print("File System Initializing......")
    time.sleep(2)
    client_stub.Initialize(num_servers, raid_mode)
    print("File System Initialized!")


#REQUEST TO FETCH THE INODE FROM INODE NUMBER FROM SERVER
def inode_number_to_inode(inode_number):
    return client_stub.inode_number_to_inode(inode_number)


#REQUEST THE DATA FROM THE SERVER
def get_data_block(block_number, delay_sec):
    return ''.join(client_stub.get_data_block(block_number, delay_sec))


#REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
def get_valid_data_block():
    return ( client_stub.get_valid_data_block() )


#REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
def free_data_block(block_number):
    client_stub.free_data_block((block_number))


#REQUEST TO WRITE DATA ON THE THE SERVER
def update_data_block(block_number, block_data, delay_sec):
    client_stub.update_data_block(block_number, block_data, delay_sec)


#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
def update_inode_table(inode, inode_number):
    client_stub.update_inode_table(inode, inode_number)
