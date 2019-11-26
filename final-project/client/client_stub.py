# SKELETON CODE FOR CLIENT STUB HW4
import xmlrpclib, config, pickle, sys, traceback
from time import sleep

class client_stub():

    def __init__(self):
        self.proxy = []
        self.portNum = 8000
        self.num_servers = -1

    def inode_number_to_inode(self, inode_number):
        inode_number = pickle.dumps(inode_number)
        try: # try server 0 for inode data
            respVal = self.proxy[0].inode_number_to_inode(inode_number)
            inode, state = pickle.loads(respVal)
            if state == False: raise Exception()
        except Exception:
            try: # try server 1 for inode data
                respVal = self.proxy[1].inode_number_to_inode(inode_number)
                inode, state = pickle.loads(respVal)
                if state == False: raise Exception()
            except:
                print("Server error [inode_number_to_inode] - terminating program.") # s in servers #0 and #1
                traceback.print_exc()
                quit()
        return inode

    def get_data_block(self, virtual_block_number, delay_sec):
        data_server_number = virtual_block_number & 0b1111
        local_block_number = virtual_block_number >> 4
        respVal = 0
        try: # direct read from target server
            print("Reading data from the data server (" + str(data_server_number) + ").")
            sleep(delay_sec)
            respVal, state = pickle.loads(\
                self.proxy[data_server_number].get_data_block(\
                    pickle.dumps(local_block_number)))
            if (state == False): raise Exception()
        except: # target server down or corrupt
            try: # read all other servers same local block
                print("Target server down, reconstructing data from other servers.")
                sibling_blocks = []
                for i in range(self.num_servers):
                    if i == data_server_number: continue
                    print("Reading data from the data server (" + str(i) + ").")
                    data, state = pickle.loads(\
                        self.proxy[i].get_data_block(\
                            pickle.dumps(local_block_number)))
                    if (state == False): raise Exception()
                    sibling_blocks.append(data)

                respVal = list(sibling_blocks[0])
                for sibling_index in range(1,len(sibling_blocks)):
                    sibling = sibling_blocks[sibling_index]
                    for i in range(len(sibling)):
                        respVal[i] = chr(ord(respVal[i]) ^ ord(sibling[i]))    

                # TODO: write to fix corrupted value and correct state?
            except: # multiple servers down or corrupt
                print("Server Error [get_data_block] - terminating program.")
                traceback.print_exc()
                quit()
        return respVal

    def get_valid_data_block(self):
        # returns a valid virtual block number
        # make sure we never return a parity block here, and for a row number,
        # ensure that the parity of that row is allocated as well
        try:
            # determine the candidate blocks
            v_candidate_blocks = []
            server_down = False
            for server_num in range(self.num_servers):
                try:
                    local_candidate, state = pickle.loads(self.proxy[server_num].get_valid_data_block())
                    if state == False:
                        raise Exception()
                except: 
                    if not server_down:
                        server_down = True
                        continue
                    else: raise Exception()
                v_candidate = local_candidate << 4 | server_num
                # if the server number is not the parity server for that block row
                if server_num != local_candidate % self.num_servers:
                    v_candidate_blocks.append(v_candidate)

            # take the minimum value from the virtual candidates
            v_selected = min(v_candidate_blocks)

            server_down = False
            # free unused temporarily reserved blocks
            for v_candidate in v_candidate_blocks:
                if v_candidate == v_selected: continue
                try: self.proxy[v_candidate & 0b1111].free_data_block(pickle.dumps(v_candidate>>4))
                except: 
                    if not server_down:
                        server_down = True
                        continue
                    else: raise Exception()

        except Exception:
            print("Server Error [get_valid_data_block] - terminating program.")
            traceback.print_exc()
            quit()

        return v_selected

    def free_data_block(self, virtual_block_number):
        if virtual_block_number == -1: return
        local_block_number = virtual_block_number >> 4
        server_number = virtual_block_number & 0b1111
        try:
            self.proxy[server_number].free_data_block(\
                            pickle.dumps(local_block_number))
        except Exception:
            print("Error in server #" + str(server_number) + " [free_data_block].")
            traceback.print_exc()

    def _update_data(self, data_server_number, local_block_number, block_data, delay_sec):
        print("Writing data to server (" + str(data_server_number) + ")...")
        sleep(delay_sec)
        self.proxy[data_server_number].update_data_block(\
            pickle.dumps(local_block_number), pickle.dumps(block_data))
    
    def _update_parity(self, parity_server_number, local_block_number, old_parity_value, \
        old_data_value, block_data, delay_sec):
        new_parity_value = list(old_parity_value)
        for i in range(len(old_data_value)):
            new_parity_value[i] = chr(ord(new_parity_value[i]) ^ ord(old_data_value[i]))
        for i in range(len(block_data)):
            new_parity_value[i] = chr(ord(new_parity_value[i]) ^ ord(block_data[i]))
        
        print("Writing parity to server (" + str(parity_server_number) + ")...")
        sleep(delay_sec)
        self.proxy[parity_server_number].update_data_block(\
            pickle.dumps(local_block_number), pickle.dumps(new_parity_value))

    def update_data_block(self, virtual_block_number, block_data, delay_sec):
        local_block_number = virtual_block_number >> 4
        data_server_number = virtual_block_number & 0b1111
        parity_server_number = local_block_number % self.num_servers

        data_down, parity_down = False, False
        try:
            old_parity_value, state = pickle.loads(self.proxy[parity_server_number].get_data_block(pickle.dumps(local_block_number)))
            if state == False:
                raise Exception()
        except:
            print("Parity server (" + str(parity_server_number) + ") is down.")
            parity_down = True
        try:
            old_data_value, state = pickle.loads(self.proxy[data_server_number].get_data_block(pickle.dumps(local_block_number)))
            if state == False:
                raise Exception()
        except:
            print("Data server (" + str(data_server_number) + ") is down.")
            data_down = True

        if parity_down and data_down:
            print("Multiple server errors [update_data_block], terminating.")
            traceback.print_exc()
            quit()

        if parity_down and not data_down:
            # update data, skip parity update
            print("Skipping parity update to server (" + str(parity_server_number) + ").")
            try: self._update_data(data_server_number, local_block_number, block_data, delay_sec)
            except:
                print("Multiple server errors [update_data_block], terminating.")
                traceback.print_exc()
                quit()

        if not parity_down and data_down:
            # skip data update, update parity
            print("Skipping data update to server (" + str(data_server_number) + ").")
            # rely on get_data_block for good data and perform update
            old_data_value = self.get_data_block(virtual_block_number, delay_sec=0)
            try: self._update_parity(parity_server_number, local_block_number, old_parity_value, \
                     old_data_value, block_data, delay_sec)
            except:
                print("Multiple server errors [update_data_block], terminating.")
                traceback.print_exc()
                quit()

        if not parity_down and not data_down:
            # update data and parity
            try: self._update_data(data_server_number, local_block_number, block_data, delay_sec)
            except:
                print("Data server (" + str(data_server_number) + ") is down.")
                data_down = True
            try: self._update_parity(parity_server_number, local_block_number, old_parity_value, \
                     old_data_value, block_data, delay_sec)
            except:
                print("Parity server (" + str(parity_server_number) + ") is down.")
                parity_down = True
            
            if (parity_down and data_down):
                print("Multiple server errors [update_data_block], terminating.")
                traceback.print_exc()
                quit()

        return

    def update_inode_table(self, inode, inode_number):
        inode = pickle.dumps(inode)
        inode_number = pickle.dumps(inode_number)
        server_down = False

        try:
            for s in range(self.num_servers):
                try: self.proxy[s].update_inode_table(inode, inode_number)
                except:
                    if not server_down: server_down = True
                    else: raise Exception()
        except Exception:
            print("Server Error [update_inode_table] - terminating program.")
            traceback.print_exc()
            quit()

    # example provided for initialize
    def Initialize(self, num_servers):
        if num_servers < 4 or num_servers > 16:
            print("Must use between 4 and 16 servers - terminating program.")
            quit()
        
        for i in range(num_servers):
            try:
                self.proxy.append(xmlrpclib.ServerProxy("http://localhost:" + str(self.portNum + i) + "/"))
                self.proxy[i].Initialize()
            except Exception: pass
        self.num_servers = len(self.proxy)

        diff = num_servers - self.num_servers
        if diff > 0: print("Failed to connect to " + str(diff) + " servers.")
        if self.num_servers < 4:
            print("Insufficient servers connected to run client - terminating program.")
            quit()
        print("Running client with " + str(self.num_servers) + " servers up.")
