# SKELETON CODE FOR CLIENT STUB HW4
import xmlrpclib, config, pickle, sys, traceback

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
        except Exception:
            try: # try server 1 for inode data
                respVal = self.proxy[1].inode_number_to_inode(inode_number)
                inode, state
            except:
                print("Server error [inode_number_to_inode] - terminating program.") # s in servers #0 and #1
                traceback.print_exc()
                quit()
        return inode

    def get_data_block(self, virtual_block_number):
        data_server_number = virtual_block_number & 0b1111
        local_block_number = virtual_block_number >> 4
        respVal = 0
        try: # direct read from target server 
            respVal, state = pickle.loads(\
                self.proxy[data_server_number].get_data_block(\
                    pickle.dumps(local_block_number)))
            if (state == False): raise Exception()
        except: # target server down or corrupt
            try: # read all other servers same local block
                sibling_blocks = []
                for i in range(self.num_servers):
                    if i == data_server_number: continue
                    data, state = pickle.loads(\
                        self.proxy[i].get_data_block(\
                            pickle.dumps(local_block_number)))
                    if (state == False): raise Exception()
                    sibling_blocks.append(data)
                respVal = sibling_blocks[0]
                for i in range(1, len(sibling_blocks)):
                    respval = respval ^ sibling_blocks[i]
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
                try: local_candidate, state = pickle.loads(\
                    self.proxy[server_num].get_valid_data_block())
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
        local_block_number = virtual_block_number >> 4
        server_number = virtual_block_number & 0b1111
        try:
            self.proxy[server_number].free_data_block(\
                            pickle.dumps(local_block_number))
        except Exception:
            print("Error in server #" + server_number + " [free_data_block].")

    def update_data_block(self, virtual_block_number, block_data):
        local_block_number = virtual_block_number >> 4
        data_server_number = virtual_block_number & 0b1111
        parity_server_number = local_block_number % self.num_servers

        # TODO - we need logic here to decide what to do when we fail. This is more complicated
        # then first glance.
        old_parity_value, state = pickle.loads(\
            self.proxy[parity_server_number].get_data_block(pickle.dumps(local_block_number)))
        old_data_value, state = pickle.loads(\
            self.proxy[data_server_number].get_data_block(pickle.dumps(local_block_number)))

        new_parity_value = []
        for i in range(max(len(old_parity_value), max(len(old_data_value), len(block_data)))):
            new_parity_value += old_parity_value[i] ^ old_data_value[i] ^ block_data[i]

        firstFailed = False
        try: self.proxy[data_server_number].update_data_block(\
            pickle.dumps(local_block_number), pickle.dumps(block_data))
        except Exception: firstFailed = True
        try: self.proxy[parity_server_number].update_data_block(\
            pickle.dumps(local_block_number), pickle.dumps(new_parity_value))
        except Exception:
            if firstFailed:
                print("Server error [update_data_block] - terminating program.")
                #  occured in servers #" + data_server_number + " and #" + parity_server_number + "
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
        try :
            self.num_servers = num_servers
            for i in range(num_servers) :
                self.proxy.append(xmlrpclib.ServerProxy("http://localhost:" + str(self.portNum + i) + "/"))
                self.proxy[i].Initialize()
        except Exception:
            print("Server Error [Initialize] - terminating program.")
            traceback.print_exc()
            quit()