# SKELETON CODE FOR SERVER STUB HW4
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

import time, Memory, pickle , InodeOps, config, DiskLayout

filesystem = Memory.Operations()


# FUNCTION DEFINITIONS 
def Initialize():
    print("Client request received - Initialize.")
    retVal = Memory.Initialize()
    retVal = pickle.dumps(retVal)
    print("Memory Initialized!")
    return retVal


#FETCH THE INODE FROM INODE NUMBER
def inode_number_to_inode(inode_number):
    print("Client request received - inode_number_to_inode.")
    try:
        inode_number = pickle.loads(inode_number)
    except Exception:
        print("Unable to unmarshal data from client.")
        return pickle.dumps(-1)
    retVal = filesystem.inode_number_to_inode(inode_number)
    retVal = pickle.dumps(retVal)
    return retVal


#REQUEST THE DATA
def get_data_block(block_number):
    print("Client request received - get_data_block")
    try:
        block_number = pickle.loads(block_number)
    except Exception:
        print("Unable to unmarshal data from client.")
        return pickle.dumps(-1)
    retVal = ''.join(filesystem.get_data_block(block_number))
    retVal = pickle.dumps(retVal)
    return retVal


#REQUESTS THE VALID BLOCK NUMBER 
def get_valid_data_block():
    print("Client request received - get_valid_data_block")
    retVal = ( filesystem.get_valid_data_block() )
    retVal = pickle.dumps(retVal)
    return retVal


#REQUEST TO MAKE BLOCKS RESUABLE AGAIN
def free_data_block(block_number):
    print("Client request received - free_data_block")
    try:
        block_number = pickle.loads(block_number)
    except Exception:
        print("Unable to unmarshal data from client.")
        return pickle.dumps(-1)
    retVal = filesystem.free_data_block((block_number))
    retVal = pickle.dumps(retVal)
    return retVal


#REQUEST TO WRITE DATA
def update_data_block(block_number, block_data):
    print("Client request received - update_data_block")
    try:
        block_number = pickle.loads(block_number)
        block_data = pickle.loads(block_data)
    except Exception:
        print("Unable to unmarshal data from client.")
        return pickle.dumps(-1)
    retVal = filesystem.update_data_block(block_number, block_data)
    retVal = pickle.dumps(retVal)
    return retVal


#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE
def update_inode_table(inode, inode_number):
    print("Client request received - update_inode_table")
    try:
        inode = pickle.loads(inode)
        inode_number = pickle.loads(inode_number)
    except Exception:
        print("Unable to unmarshal data from client.")
        return pickle.dumps(-1)
    retVal = filesystem.update_inode_table(inode, inode_number)
    retVal = pickle.dumps(retVal)
    return retVal


#REQUEST FOR THE STATUS OF FILE SYSTEM
def status():
    print("Client request received - status")
    retVal = filesystem.status()
    retVal = pickle.dumps(retVal)
    return retVal


server = SimpleXMLRPCServer(("",8000))
print ("Listening on port 8000...")


# REGISTER FUNCTIONS
server.register_function(Initialize, "Initialize")
server.register_function(inode_number_to_inode, "inode_number_to_inode")
server.register_function(get_data_block, "get_data_block")
server.register_function(get_valid_data_block, "get_valid_data_block")
server.register_function(free_data_block, "free_data_block")
server.register_function(update_data_block, "update_data_block")
server.register_function(update_inode_table, "update_inode_table")
server.register_function(status, "status")


# run the server
server.serve_forever()