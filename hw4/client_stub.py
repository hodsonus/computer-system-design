# SKELETON CODE FOR CLIENT STUB HW4
import xmlrpclib, config, pickle

class client_stub():

    def __init__(self):
        self.proxy = xmlrpclib.ServerProxy("http://localhost:8000/")


    def inode_number_to_inode(self, inode_number):
        inode_number = pickle.dumps(inode_number)
        try:
            respVal = self.proxy.inode_number_to_inode(inode_number)
            respVal = pickle.loads(respVal)
        except Exception:
            print("Server Error - terminating program.")
            quit()
        return respVal


    def get_data_block(self, block_number):
        block_number = pickle.dumps(block_number)
        try:
            respVal = self.proxy.get_data_block(block_number)
            respVal = pickle.loads(respVal)
        except Exception:
            print("Server Error - terminating program.")
            quit()
        return respVal


    def get_valid_data_block(self):
        try:
            respVal = self.proxy.get_valid_data_block()
            respVal = pickle.loads(respVal)
        except Exception:
            print("Server Error - terminating program.")
            quit()
        return respVal


    def free_data_block(self, block_number):
        block_number = pickle.dumps(block_number)
        try:
            respVal = self.proxy.free_data_block(block_number)
            respVal = pickle.loads(respVal)
        except Exception:
            print("Server Error - terminating program.")
            quit()
        return respVal


    def update_data_block(self, block_number, block_data):
        block_number = pickle.dumps(block_number)
        block_data = pickle.dumps(block_data)
        try:
            respVal = self.proxy.update_data_block(block_number, block_data)
            respVal = pickle.loads(respVal)
        except Exception:
            print("Server Error - terminating program.")
            quit()
        return respVal


    def update_inode_table(self, inode, inode_number):
        inode = pickle.dumps(inode)
        inode_number = pickle.dumps(inode_number)
        
        try:
            respVal = self.proxy.update_inode_table(inode, inode_number)
            respVal = pickle.loads(respVal) 
        except Exception:
            print("Server Error - terminating program.")
            quit()
        return respVal


    def status(self):
        try:
            respVal = self.proxy.status()
            respVal = pickle.loads(respVal)
        except Exception:
            print("Server Error - terminating program.")
            quit()
        return respVal


    # example provided for initialize
    def Initialize(self):
        try :
            self.proxy.Initialize()
        except Exception:
            print("Server Error - terminating program.")
            quit()