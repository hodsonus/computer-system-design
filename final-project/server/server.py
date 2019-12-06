import xmlrpclib, time, Memory, pickle , InodeOps, config, DiskLayout, sys, hashlib, config, traceback, random
from SimpleXMLRPCServer import SimpleXMLRPCServer

global portNumber
filesystem = Memory.Operations()
RAID_REQ_COUNT_GET = 0
RAID_REQ_COUNT_SET = 0
BASE_DATA_BLOCK = 0

def configure():
    configuration = [config.TOTAL_NO_OF_BLOCKS, config.BLOCK_SIZE, config.MAX_NUM_INODES, config.INODE_SIZE, config.MAX_FILE_NAME_SIZE]
    return pickle.dumps(configuration)

def Initialize():
    global BASE_DATA_BLOCK
    retVal = Memory.Initialize()
    BASE_DATA_BLOCK = filesystem.get_valid_data_block()
    filesystem.free_data_block(BASE_DATA_BLOCK)
    return pickle.dumps(retVal)

def addr_inode_table():
    return pickle.dumps(filesystem.addr_inode_table())

def get_data_block(block_number):
    global RAID_REQ_COUNT_GET
    RAID_REQ_COUNT_GET += 1
    print("GET:" + str(RAID_REQ_COUNT_GET))
    block_number = pickle.loads(block_number)
    try:
        res = filesystem.get_data_block(block_number)
        block_data, chksum_read = ''.join(res[:-16]), ''.join(res[-16:])
    except: return pickle.dumps(('ErrCode1', True)) # invalid blk access
    block_data, chksum_calc = _data_and_chksum(block_data)
    if (chksum_read != chksum_calc): return pickle.dumps(('ErrCode2', True)) # corruption
    return pickle.dumps((block_data, False))

def get_valid_data_block():	
    return pickle.dumps(filesystem.get_valid_data_block())

def free_data_block(block_number):
    block_number = pickle.loads(block_number)
    return pickle.dumps(filesystem.free_data_block(block_number))

def update_data_block(block_number, block_data):	
    global RAID_REQ_COUNT_SET
    RAID_REQ_COUNT_SET += 1
    print("SET:" + str(RAID_REQ_COUNT_SET))
    block_number, block_data = pickle.loads(block_number), pickle.loads(block_data)
    block_data, chksum = _data_and_chksum(block_data)
    return pickle.dumps(filesystem.update_data_block(block_number, block_data+chksum))

def update_inode_table(inode, inode_number):
    inode, inode_number = pickle.loads(inode), pickle.loads(inode_number)
    return pickle.dumps(filesystem.update_inode_table(inode, inode_number))

def inode_number_to_inode(inode_number):
    inode_number = pickle.loads(inode_number)
    return pickle.dumps(filesystem.inode_number_to_inode(inode_number))

def corruptData(mode):
    mode = pickle.loads(mode)
    retVal = 'Failed to corrupt server.'
    if(mode == '1'):
        # 0th
        filesystem.corrupt_data_block(BASE_DATA_BLOCK)
        retVal = 'Data corrupted in server ' + str(portNumber) + ' block ' + str(BASE_DATA_BLOCK)
    if(mode == '2'):
        # random
        max_b = filesystem.get_valid_data_block()
        filesystem.free_data_block(max_b)
        b = random.randint(BASE_DATA_BLOCK, max_b-1)
        filesystem.corrupt_data_block(b)
        retVal = 'Data corrupted in server on port ' + str(portNumber) + ' block ' + str(b)
    print(retVal)
    return pickle.dumps(retVal)

def _data_and_chksum(block_data):
    block_data = ''.join(block_data)
    checksum = hashlib.md5(block_data).digest()
    checksum = ''.join(checksum)
    return block_data, checksum

portNumber = int(sys.argv[1])
server = SimpleXMLRPCServer(("localhost",portNumber))
print ("Listening on port " + str(portNumber) + "...")

server.register_function(corruptData, "corruptData")
server.register_function(configure, "configure")
server.register_function(Initialize, "Initialize")
server.register_function(addr_inode_table, "addr_inode_table")
server.register_function(get_data_block, "get_data_block")
server.register_function(get_valid_data_block, "get_valid_data_block")
server.register_function(free_data_block, "free_data_block")
server.register_function(update_data_block, "update_data_block")
server.register_function(update_inode_table, "update_inode_table")
server.register_function(inode_number_to_inode, "inode_number_to_inode")
server.serve_forever()
