import FileSystem, sys
from FileSystem import FileSystemOperations
import time, config

def file_system_repl():
    print("Hello, this is a demo for our RAID 5 file system. We are able to \
           tolerate a fail-stop of one server/disk and recover all data.\n")

    print("Please input the number of servers, between 4 and 16, that you would \
           like to test this with. Ensure that this number of servers \
           reflects the number of servers instantiated with backChannel.py")
    FileSystem.Initialize_My_FileSystem(int(input()))

    invalid_command = "That was not a recognized command, please follow the \
                   formatting seen in the menu choices."
    menu = "" #TODO
    print(menu)
    print("Choose from the above commands in the following terminal:")

    fsop = FileSystemOperations()
    while True:
        print("$ ", end="")
        try:
            command = input().strip().split(" ")
        except:
            print(invlaid_command)
            continue
        if len(command) == 0:
            print(invalid_command)
            continue
        elif command[0] == "mkdir":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.mkdir(path)
        elif command[0] == "create":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.create(path)
        elif command[0] == "mv":
            if (len(command) < 3):
                print(invlaid_command)
                continue
            old_path = command[1]
            new_path = command[2]
            fsop.mv(old_path, new_path)
        elif command[0] == "read":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            offset = 0
            size = -1
            if (len(command) >= 3):
                offset = int(command[2])
            if (len(command) >= 4):
                size = int(command(3))
            fsop.read(path, offset, size)
        elif command[0] == "write":
            if (len(command) < 3):
                print(invlaid_command)
                continue
            path = command[1]
            data = command[2]
            offset = 0
            delay_sec = 0
            if (len(command) >= 4):
                offset = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.write(ptah, data, offset, delay_sec)
        elif command[0] == "status":
            print("Implementation of this method was deemed unecessary by Cody.")
            continue
        elif command[0] == "rm":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.rm(path)
        elif command[0] == "exit":
            print("Exiting demo...")
            quit()
        else:
            print(invlaid_command)
            continue
                print(invlaid_command)
                continue
            path = command[1]
            offset = 0
            size = -1
            if (len(command) >= 3):
                offset = int(command[2])
            if (len(command) >= 4):
                size = int(command(3))
            fsop.read(path, offset, size)
        elif command[0] == "write":
            if (len(command) < 3):
                print(invlaid_command)
                continue
            path = command[1]
            data = command[2]
            offset = 0
            delay_sec = 0
            if (len(command) >= 4):
                offset = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.write(ptah, data, offset, delay_sec)
        elif command[0] == "status":
            print("Implementation of this method was deemed unecessary by Cody.")
            continue
        elif command[0] == "rm":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.rm(path)
        elif command[0] == "exit":
            print("Exiting demo...")
            quit()
        else:
            print(invlaid_command)
            continue
                print(invlaid_command)
                continue
            path = command[1]
            offset = 0
            size = -1
            if (len(command) >= 3):
                offset = int(command[2])
            if (len(command) >= 4):
                size = int(command(3))
            fsop.read(path, offset, size)
        elif command[0] == "write":
            if (len(command) < 3):
                print(invlaid_command)
                continue
            path = command[1]
            data = command[2]
            offset = 0
            delay_sec = 0
            if (len(command) >= 4):
                offset = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.write(ptah, data, offset, delay_sec)
        elif command[0] == "status":
            print("Implementation of this method was deemed unecessary by Cody.")
            continue
        elif command[0] == "rm":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.rm(path)
        elif command[0] == "exit":
            print("Exiting demo...")
            quit()
        else:
            print(invlaid_command)
            continue
                print(invlaid_command)
                continue
            path = command[1]
            offset = 0
            size = -1
            if (len(command) >= 3):
                offset = int(command[2])
            if (len(command) >= 4):
                size = int(command(3))
            fsop.read(path, offset, size)
        elif command[0] == "write":
            if (len(command) < 3):
                print(invlaid_command)
                continue
            path = command[1]
            data = command[2]
            offset = 0
            delay_sec = 0
            if (len(command) >= 4):
                offset = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.write(ptah, data, offset, delay_sec)
        elif command[0] == "status":
            print("Implementation of this method was deemed unecessary by Cody.")
            continue
        elif command[0] == "rm":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.rm(path)
        elif command[0] == "exit":
            print("Exiting demo...")
            quit()
        else:
            print(invlaid_command)
            continue
                print(invlaid_command)
                continue
            path = command[1]
            offset = 0
            size = -1
            if (len(command) >= 3):
                offset = int(command[2])
            if (len(command) >= 4):
                size = int(command(3))
            fsop.read(path, offset, size)
        elif command[0] == "write":
            if (len(command) < 3):
                print(invlaid_command)
                continue
            path = command[1]
            data = command[2]
            offset = 0
            delay_sec = 0
            if (len(command) >= 4):
                offset = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.write(ptah, data, offset, delay_sec)
        elif command[0] == "status":
            print("Implementation of this method was deemed unecessary by Cody.")
            continue
        elif command[0] == "rm":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.rm(path)
        elif command[0] == "exit":
            print("Exiting demo...")
            quit()
        else:
            print(invlaid_command)
            continue
                print(invlaid_command)
                continue
            path = command[1]
            offset = 0
            size = -1
            if (len(command) >= 3):
                offset = int(command[2])
            if (len(command) >= 4):
                size = int(command(3))
            fsop.read(path, offset, size)
        elif command[0] == "write":
            if (len(command) < 3):
                print(invlaid_command)
                continue
            path = command[1]
            data = command[2]
            offset = 0
            delay_sec = 0
            if (len(command) >= 4):
                offset = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.write(ptah, data, offset, delay_sec)
        elif command[0] == "status":
            print("Implementation of this method was deemed unecessary by Cody.")
            continue
        elif command[0] == "rm":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.rm(path)
        elif command[0] == "exit":
            print("Exiting demo...")
            quit()
        else:
            print(invlaid_command)
            continue
                print(invlaid_command)
                continue
            path = command[1]
            offset = 0
            size = -1
            if (len(command) >= 3):
                offset = int(command[2])
            if (len(command) >= 4):
                size = int(command(3))
            fsop.read(path, offset, size)
        elif command[0] == "write":
            if (len(command) < 3):
                print(invlaid_command)
                continue
            path = command[1]
            data = command[2]
            offset = 0
            delay_sec = 0
            if (len(command) >= 4):
                offset = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.write(ptah, data, offset, delay_sec)
        elif command[0] == "status":
            print("Implementation of this method was deemed unecessary by Cody.")
            continue
        elif command[0] == "rm":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.rm(path)
        elif command[0] == "exit":
            print("Exiting demo...")
            quit()
        else:
            print(invlaid_command)
            continue
                print(invlaid_command)
                continue
            path = command[1]
            offset = 0
            size = -1
            if (len(command) >= 3):
                offset = int(command[2])
            if (len(command) >= 4):
                size = int(command(3))
            fsop.read(path, offset, size)
        elif command[0] == "write":
            if (len(command) < 3):
                print(invlaid_command)
                continue
            path = command[1]
            data = command[2]
            offset = 0
            delay_sec = 0
            if (len(command) >= 4):
                offset = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.write(ptah, data, offset, delay_sec)
        elif command[0] == "status":
            print("Implementation of this method was deemed unecessary by Cody.")
            continue
        elif command[0] == "rm":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.rm(path)
        elif command[0] == "exit":
            print("Exiting demo...")
            quit()
        else:
            print(invlaid_command)
            continue
                print(invlaid_command)
                continue
            path = command[1]
            offset = 0
            size = -1
            if (len(command) >= 3):
                offset = int(command[2])
            if (len(command) >= 4):
                size = int(command(3))
            fsop.read(path, offset, size)
        elif command[0] == "write":
            if (len(command) < 3):
                print(invlaid_command)
                continue
            path = command[1]
            data = command[2]
            offset = 0
            delay_sec = 0
            if (len(command) >= 4):
                offset = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.write(ptah, data, offset, delay_sec)
        elif command[0] == "status":
            print("Implementation of this method was deemed unecessary by Cody.")
            continue
        elif command[0] == "rm":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.rm(path)
        elif command[0] == "exit":
            print("Exiting demo...")
            quit()
        else:
            print(invlaid_command)
            continue
                print(invlaid_command)
                continue
            path = command[1]
            offset = 0
            size = -1
            if (len(command) >= 3):
                offset = int(command[2])
            if (len(command) >= 4):
                size = int(command(3))
            fsop.read(path, offset, size)
        elif command[0] == "write":
            if (len(command) < 3):
                print(invlaid_command)
                continue
            path = command[1]
            data = command[2]
            offset = 0
            delay_sec = 0
            if (len(command) >= 4):
                offset = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.write(ptah, data, offset, delay_sec)
        elif command[0] == "status":
            print("Implementation of this method was deemed unecessary by Cody.")
            continue
        elif command[0] == "rm":
            if (len(command) < 2):
                print(invlaid_command)
                continue
            path = command[1]
            fsop.rm(path)
        elif command[0] == "exit":
            print("Exiting demo...")
            quit()
        else:
            print(invlaid_command)
            continue
        
if __name__ == "__main__":
    file_system_repl()