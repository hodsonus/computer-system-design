from __future__ import print_function
import FileSystem, sys, time, config, traceback

def file_system_repl():
    fsop = FileSystem.FileSystemOperations()

    invalid_command = "That was not a recognized command, please follow the formatting seen in the menu choices."
    menu = """
    mkdir  <path>
    create <path>
    mv     <old_path> <new_path>
    read   <path> <offset>=0 <size>=-1 <delay>=0
    write  <path> <data> <offset>=0 <delay>=0
    rm     <path>
    status
    exit
    """
    print(menu)
    print("Choose from the above commands in the following terminal:\n(Optional parameters must be specified in order if desired.)")

    while True:
        print("$ ", end="")
        input = raw_input().strip()
        if input == "": continue
        try: command = input.split(" ")
        except:
            print(invalid_command)
            continue
        if len(command) == 0: continue
        elif command[0] == "mkdir":
            if (len(command) != 2):
                print(invalid_command)
                continue
            path = command[1]
            fsop.mkdir(path)
        elif command[0] == "create":
            if (len(command) != 2):
                print(invalid_command)
                continue
            path = command[1]
            if (path == '/'):
                print("Invalid path. Root exists.")
                continue
            fsop.create(path)
        elif command[0] == "mv":
            if (len(command) != 3):
                print(invalid_command)
                continue
            old_path = command[1]
            new_path = command[2]
            fsop.mv(old_path, new_path)
        elif command[0] == "read":
            if (len(command) < 2 or len(command) > 5):
                print(invalid_command)
                continue
            path = command[1]
            offset = 0
            size = -1
            delay_sec = 5
            if (len(command) >= 3):
                offset = int(command[2])
            if (len(command) >= 4):
                size = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.read(path, offset, size, delay_sec)
        elif command[0] == "write":
            if (len(command) < 3 or len(command) > 5):
                print(invalid_command)
                continue
            path = command[1]
            data = command[2]
            offset = 0
            delay_sec = 0
            if (len(command) >= 4):
                offset = int(command[3])
            if (len(command) >= 5):
                delay_sec = int(command[4])
            fsop.write(path, data, offset, delay_sec)
        elif command[0] == "status":
            if (len(command) > 1):
                print(invalid_command)
                continue
            print("Implementation of this method was deemed unecessary by Cody.")
            continue
        elif command[0] == "rm":
            if (len(command) != 2):
                print(invalid_command)
                continue
            path = command[1]
            fsop.rm(path)
        elif command[0] == "exit":
            if (len(command) > 1):
                print(invalid_command)
                continue
            print("Exiting demo...")
            quit()
        else:
            print(invalid_command)
            continue
        
if __name__ == "__main__":
    print("Hello, this is a demo for our RAID 5 file system. We are able to tolerate a fail-stop of one server/disk and recover all data.\n")
    
    print("Please input the number of servers, between 4 and 16, that you would like to test this with.")
    print("Ensure that this number of servers reflects the number of servers instantiated with backChannel.py")
    num_servers = int(input())
    while num_servers < 4 or num_servers > 16:
        print('Please enter a number of servers between 4 and 16.')
        num_servers = int(input())
    
    print("Please input the raid mode, 1 or 5, that you would like to test this with.")
    print("Ensure that this raid mode reflects the raid mode instantiated with backChannel.py")
    raid_mode = input()
    while raid_mode != '1' and raid_mode != '5':
        print('Please enter a raid mode 1 or 5.')
        raid_mode = input()
    
    FileSystem.Initialize_My_FileSystem(num_servers, raid_mode)
    file_system_repl()
