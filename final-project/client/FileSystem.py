import MemoryInterface, AbsolutePathNameLayer, sys, FileSystemUI

def Initialize_My_FileSystem(num_servers):
    MemoryInterface.Initialize_My_FileSystem(num_servers)
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
    if len(sys.argv) != 2:
        print("Must (only) specify number of servers.")
        quit()
    num_servers = int(sys.argv[1])
    if num_servers < 4 or num_servers > 16:
        print("Must use between 4 and 16 servers - terminating program.")
        quit()
    Initialize_My_FileSystem(num_servers)
    FileSystemUI.file_system_repl()
