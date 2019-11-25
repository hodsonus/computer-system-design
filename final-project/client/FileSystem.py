import MemoryInterface, AbsolutePathNameLayer, sys

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
    #DO NOT MODIFY THIS
    Initialize_My_FileSystem(int(sys.argv[1]))
    my_object = FileSystemOperations()
    #YOU MAY WRITE YOUR CODE AFTER HERE