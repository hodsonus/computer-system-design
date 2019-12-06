import MemoryInterface, AbsolutePathNameLayer, sys, FileSystemUI

def Initialize_My_FileSystem(num_servers, raid_mode):
    MemoryInterface.Initialize_My_FileSystem(num_servers, raid_mode)
    AbsolutePathNameLayer.AbsolutePathNameLayer().new_entry('/', 1)

#HANDLE TO ABSOLUTE PATH NAME LAYER
interface = AbsolutePathNameLayer.AbsolutePathNameLayer()

class FileSystemOperations():

    #MAKES NEW DIRECTORY
    def mkdir(self, path):
        interface.new_entry(path, 1)

    #CREATE FILE
    def create(self, path):
        interface.new_entry(path, 0)
        

    #WRITE TO FILE
    def write(self, path, data, offset=0, delay_sec=0):
        interface.write(path, offset, data, delay_sec)
      

    #READ
    def read(self, path, offset=0, size=-1, delay_sec=5):
        read_buffer = interface.read(path, offset, size, delay_sec)
        if read_buffer != -1: print(path + " : " + read_buffer)
        return read_buffer

    
    #DELETE
    def rm(self, path):
        interface.unlink(path)


    #MOVING FILE
    def mv(self, old_path, new_path):
        interface.mv(old_path, new_path)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Must (only) specify number of servers and raid mode.")
        quit()
    
    try:
        num_servers = int(sys.argv[1])
        if num_servers < 4 or num_servers > 16: raise Exception()
    except:
        print("Must use between 4 and 16 servers - terminating program.")
        quit()
    
    raid_mode = sys.argv[2]
    if raid_mode != '1' and raid_mode != '5':
        print("Must use raid mode 1 or 5 - terminating program.")
        quit()

    Initialize_My_FileSystem(num_servers, raid_mode)
    FileSystemUI.file_system_repl()
