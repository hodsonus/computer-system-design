# SKELETON CODE FOR CLIENT STUB HW4
import config
import xmlrpclib, pickle, sys, traceback, random
from time import sleep

class client_stub():

    def __init__(self):
        self.proxy = []
        self.portNum = 8000
        self.num_servers = -1
        self.raid_mode = '5'

    def Initialize(self, num_servers, raid_mode):
        if num_servers < 4 or num_servers > 16:
            print("Must use between 4 and 16 servers - terminating program.")
            quit()
        
        if raid_mode != '1' and raid_mode != '5':
            print('Invalid raid mode - terminating program.')
            quit()
        
        self.raid_mode = raid_mode

        for i in range(num_servers):
            try:
                self.proxy.append(xmlrpclib.ServerProxy("http://localhost:" + str(self.portNum + i) + "/"))
                self.proxy[-1].Initialize()
            except Exception: pass
        self.num_servers = len(self.proxy)

        diff = num_servers - self.num_servers
        if diff > 0: print("Failed to connect to " + str(diff) + " server(s).")
        if self.num_servers < 4 or self.num_servers < num_servers-1:
            print("Insufficient servers for " + str(num_servers) + "-server configuratuion - terminating program.")
            quit()
        print("Running client with " + str(self.num_servers) + " servers up.")

        self.GET = [0]*self.num_servers
        self.SET = [0]*self.num_servers

    def inode_number_to_inode(self, inode_number):
        if self.raid_mode == '1': return self.raid1_inode_number_to_inode(inode_number)
        if self.raid_mode == '5': return self.raid5_inode_number_to_inode(inode_number)

    def get_data_block(self, virtual_block_number, delay_sec):
        if self.raid_mode == '1': return self.raid1_get_data_block(virtual_block_number, delay_sec)
        if self.raid_mode == '5': return self.raid5_get_data_block(virtual_block_number, delay_sec)

    def get_valid_data_block(self):
        if self.raid_mode == '1': return self.raid1_get_valid_data_block()
        if self.raid_mode == '5': return self.raid5_get_valid_data_block()

    def free_data_block(self, virtual_block_number):
        if self.raid_mode == '1': return self.raid1_free_data_block(virtual_block_number)
        if self.raid_mode == '5': return self.raid5_free_data_block(virtual_block_number)

    def update_data_block(self, virtual_block_number, block_data, delay_sec):
        if self.raid_mode == '1': return self.raid1_update_data_block(virtual_block_number, block_data, delay_sec)
        if self.raid_mode == '5': return self.raid5_update_data_block(virtual_block_number, block_data, delay_sec)

    def update_inode_table(self, inode, inode_number):
        if self.raid_mode == '1': return self.raid1_update_inode_table(inode, inode_number)
        if self.raid_mode == '5': return self.raid5_update_inode_table(inode, inode_number)

    
    ### RAID 5 ###
    
    
    def raid5_inode_number_to_inode(self, inode_number):
        inode_number = pickle.dumps(inode_number)
        rand1 = random.randint(0, len(self.proxy)-1)
        rand2 = random.randint(0, len(self.proxy)-1)
        while rand1 == rand2:
            rand2 = random.randint(0, len(self.proxy)-1)
        try: # try server 0 for inode data
            respVal = self.proxy[rand1].inode_number_to_inode(inode_number)
            inode = pickle.loads(respVal) # inode table never corrupted
        except Exception:
            try: # try server 1 for inode data
                respVal = self.proxy[rand2].inode_number_to_inode(inode_number)
                inode = pickle.loads(respVal) # inode table never corrupted
            except: # at least two servers are down
                print("Server error [inode_number_to_inode]. Two or more down, terminating program.")
                #traceback.print_exc()
                quit()
        return inode

    def raid5_get_data_block(self, virtual_block_number, delay_sec):
        data_server_number = virtual_block_number & 0b1111
        local_block_number = virtual_block_number >> 4
        try: # direct read from target server
            print("Reading data local block (" + str(local_block_number) + ") from server (" + str(data_server_number) + "). - GET " + str(self.GET))
            sleep(delay_sec)
            data1, err1 = pickle.loads(self.proxy[data_server_number].get_data_block(pickle.dumps(local_block_number)))
            if err1: raise Exception()
            self.GET[data_server_number] += 1
        except: # target server down/corrupt
            try: # read all other servers same local block
                print("Data server down/corrupt, reconstructing data from other servers.")
                sleep(delay_sec)
                sibling_blocks = []
                print("Reading data local block (" + str(local_block_number) + ") from all servers...")
                for i in range(self.num_servers):
                    if i == data_server_number: continue
                    print("Reading data local block (" + str(local_block_number) + ") from server (" + str(data_server_number) + "). - GET " + str(self.GET))
                    data2, err2 = pickle.loads(self.proxy[i].get_data_block(pickle.dumps(local_block_number)))
                    if err2: raise Exception()
                    self.GET[data_server_number] += 1
                    sibling_blocks.append(data2)
                data1 = list(sibling_blocks[0])
                for sibling_index in range(1,len(sibling_blocks)):
                    sibling = sibling_blocks[sibling_index]
                    for i in range(len(sibling)):
                        data1[i] = chr(ord(data1[i]) ^ ord(sibling[i]))
            except: # multiple servers down/corrupt
                print("Server Error [get_data_block]. Two or more down/corrupt, terminating program.")
                #traceback.print_exc()
                quit()
        return data1

    def raid5_get_valid_data_block(self):
        # returns a valid virtual block number
        # make sure we never return a parity block here, and for a row number,
        # ensure that the parity of that row is allocated as well
        try:
            # determine the candidate blocks
            v_candidate_blocks = []
            server_down = False
            for server_num in range(self.num_servers):
                try: local_candidate = pickle.loads(self.proxy[server_num].get_valid_data_block())
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
            print("Server Error [get_valid_data_block]. Two or more down/corrupt, terminating program.")
            #traceback.print_exc()
            quit()

        return v_selected

    def raid5_free_data_block(self, virtual_block_number):
        if virtual_block_number == -1: return
        local_block_number = virtual_block_number >> 4
        server_number = virtual_block_number & 0b1111
        try:
            self.proxy[server_number].free_data_block(\
                            pickle.dumps(local_block_number))
        except Exception: pass

    def raid5_update_data_block(self, virtual_block_number, block_data, delay_sec):
        local_block_number = virtual_block_number >> 4
        data_server_number = virtual_block_number & 0b1111
        parity_server_number = local_block_number % self.num_servers

        data_down, parity_down = False, False
        try:
            # print("Reading data local block (" + str(local_block_number) + ") from server (" + str(data_server_number) + ").)
            # check if alive and avoid passing as param previously GET'ed data from higher-level layer
            old_data_value, d_err = pickle.loads(self.proxy[data_server_number].get_data_block(pickle.dumps(local_block_number)))
            if d_err: raise Exception(d_err)
        except:
            print("Data server (" + str(data_server_number) + ") is down.")
            data_down = True
        try:
            print("Reading parity local block (" + str(local_block_number) + ") from server (" + str(parity_server_number) + "). - GET " + str(self.GET))
            old_parity_value, p_err = pickle.loads(self.proxy[parity_server_number].get_data_block(pickle.dumps(local_block_number)))
            if p_err: raise Exception()
            self.GET[parity_server_number] += 1
        except:
            print("Parity server (" + str(parity_server_number) + ") is down.")
            parity_down = True

        if parity_down and data_down:
            print("Server error [update_data_block]. Two or more down, terminating program.")
            #traceback.print_exc()
            quit()

        if parity_down and not data_down:
            # update data, skip parity update
            print("Skipping parity update to server (" + str(parity_server_number) + ").")
            try:
                print("Writing data local block (" + str(local_block_number) + ") to server (" + str(data_server_number) + ") - SET " + str(self.SET))
                sleep(delay_sec)
                self.proxy[data_server_number].update_data_block(\
                    pickle.dumps(local_block_number), pickle.dumps(block_data))
                self.SET[data_server_number] += 1
            except:
                print("Server error [update_data_block]. Two or more down, terminating program.")
                #traceback.print_exc()
                quit()

        if not parity_down and data_down:
            # skip data update, update parity
            print("Skipping data update to server (" + str(data_server_number) + ").")
            # rely on get_data_block for good data and perform update
            old_data_value = self.get_data_block(virtual_block_number, delay_sec=0)
            try:
                new_parity_value = list(old_parity_value)
                for i in range(len(old_data_value)):
                    new_parity_value[i] = chr(ord(new_parity_value[i]) ^ ord(old_data_value[i]))
                for i in range(len(block_data)):
                    new_parity_value[i] = chr(ord(new_parity_value[i]) ^ ord(block_data[i]))
                print("Writing parity local block (" + str(local_block_number) + ") to server (" + str(parity_server_number) + "). - SET " + str(self.SET))
                sleep(delay_sec)
                self.proxy[parity_server_number].update_data_block(\
                    pickle.dumps(local_block_number), pickle.dumps(new_parity_value))
                self.SET[parity_server_number] += 1
            except:
                print("Server error [update_data_block]. Two or more down, terminating program.")
                #traceback.print_exc()
                quit()

        if not parity_down and not data_down:
            # update data and parity
            try:
                print("Writing data local block (" + str(local_block_number) + ") to server (" + str(data_server_number) + "). - SET " + str(self.SET))
                sleep(delay_sec)
                self.proxy[data_server_number].update_data_block(\
                    pickle.dumps(local_block_number), pickle.dumps(block_data))
                self.SET[data_server_number] += 1
            except:
                #traceback.print_exc()
                print("Data server (" + str(data_server_number) + ") is down.")
                data_down = True
            try:
                new_parity_value = list(old_parity_value)
                for i in range(len(old_data_value)):
                    new_parity_value[i] = chr(ord(new_parity_value[i]) ^ ord(old_data_value[i]))
                for i in range(len(block_data)):
                    new_parity_value[i] = chr(ord(new_parity_value[i]) ^ ord(block_data[i]))
                print("Writing parity local block (" + str(local_block_number) + ") to server (" + str(parity_server_number) + "). - SET " + str(self.SET))
                sleep(delay_sec)
                self.proxy[parity_server_number].update_data_block(\
                    pickle.dumps(local_block_number), pickle.dumps(new_parity_value))
                self.SET[parity_server_number] += 1
            except:
                print("Parity server (" + str(parity_server_number) + ") is down.")
                parity_down = True
            
            if (parity_down and data_down):
                print("Server error [update_data_block]. Two or more down, terminating program.")
                #traceback.print_exc()
                quit()

        return

    def raid5_update_inode_table(self, inode, inode_number):
        inode = pickle.dumps(inode)
        inode_number = pickle.dumps(inode_number)
        server_down = False

        try:
            for s in range(self.num_servers):
                try: self.proxy[s].update_inode_table(inode, inode_number)
                except:
                    if not server_down:
                        server_down = True
                        continue
                    else: raise Exception()
        except Exception:
            print("Server Error [update_inode_table]. Two or more down, terminating program.")
            #traceback.print_exc()
            quit()


    ### RAID 1 ###
    
    
    def raid1_inode_number_to_inode(self, inode_number):
        inode_number = pickle.dumps(inode_number)
        rand = random.randint(0, len(self.proxy)-1)
        for i in range(self.num_servers):
            try: # try server 0 for inode data
                inode = self.proxy[(rand+i)%self.num_servers].inode_number_to_inode(inode_number)
                return pickle.loads(inode) # inode table never corrupted
            except Exception: pass
        print("Server error [inode_number_to_inode]. No server reachable, terminating program.")
        #traceback.print_exc()
        quit()

    def raid1_get_data_block(self, virtual_block_number, delay_sec):
        rand = random.randint(0, len(self.proxy)-1)
        for i in range(self.num_servers):
            try:
                x = (rand+i)%self.num_servers
                print("Reading data local block (" + str(virtual_block_number) + ") from server (" + str(x) + "). - GET " + str(self.GET))
                sleep(delay_sec)
                ret = self.proxy[x].get_data_block(pickle.dumps(virtual_block_number))
                data, err = pickle.loads(ret)
                if not err:
                    self.GET[x] += 1
                    return data
                if data == 'ErrCode1':
                    print('Invalid data access, terminating program.')
                    quit()
                if data == 'ErrCode2': print('Data corrupted, trying another server.')
            except Exception: print('Data not reachable, trying another server.')
        print("Server error [get_data_block]. No server reachable, terminating program.")
        #traceback.print_exc()
        quit()

    def raid1_get_valid_data_block(self):
        blk = -1
        for i in range(self.num_servers):
            try:
                tmp_blk = pickle.loads(self.proxy[i].get_valid_data_block())
                if blk == -1: blk = tmp_blk
                elif tmp_blk != blk:
                    print("Server error [get_valid_data_block]. Block state misaligned, terminating program.")
                    #traceback.print_exc()
                    quit()
            except Exception: pass
        if blk != -1: return blk
        print("Server error [get_valid_data_block]. No server reachable, terminating program.")
        #traceback.print_exc()
        quit()

    def raid1_free_data_block(self, virtual_block_number):
        if virtual_block_number == -1: return
        at_least_one = False
        for i in range(self.num_servers):
            try:
                self.proxy[i].free_data_block(pickle.dumps(virtual_block_number))
                at_least_one = True
            except Exception: pass
        if not at_least_one:
            print("Server error [free_data_block]. No server reachable, terminating program.")
            #traceback.print_exc()
            quit()

    def raid1_update_data_block(self, virtual_block_number, block_data, delay_sec):
        print("Writing data local block (" + str(virtual_block_number) + ") to all servers...")
        sleep(delay_sec)
        at_least_one = False
        for i in range(self.num_servers):
            try:
                print("Writing data local block (" + str(virtual_block_number) + ") to server (" + str(i) + "). - SET " + str(self.SET))
                self.proxy[i].update_data_block(pickle.dumps(virtual_block_number), pickle.dumps(block_data))
                at_least_one = True
                self.SET[i] += 1
            except Exception: pass
        if not at_least_one:
            print("Server error [update_data_block]. No server reachable, terminating program.")
            #traceback.print_exc()
            quit()

    def raid1_update_inode_table(self, inode, inode_number):
        inode = pickle.dumps(inode)
        inode_number = pickle.dumps(inode_number)
        at_least_one = False
        for i in range(self.num_servers):
            try:
                self.proxy[i].update_inode_table(inode, inode_number)
                at_least_one = True
            except Exception: pass
        if not at_least_one:
            print("Server error [update_inode_table]. No server reachable, terminating program.")
            #traceback.print_exc()
            quit()
