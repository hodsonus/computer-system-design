import FileSystem, sys
from FileSystem import FileSystemOperations
import time, config, traceback


def happy_path():
    start_time = time.time()
    my_object = FileSystemOperations()
    offset = 0
    my_object.mkdir("/A")
    my_object.mkdir("/B")
    '''as A is already there we can create file in A'''
    my_object.create("/A/1.txt")
    '''as 1.txt is already created now, we can write to it.'''
    my_object.write("/A/1.txt", "POCSD", offset)
    my_object.read("/A/1.txt", offset, len("POCSD"), 0)
    my_object.mv("/A/1.txt", "/B/1.txt")
    my_object.rm("/B/1.txt")
    my_object.rm("/B")
    end_time = time.time()
    print("--- %s seconds ---" % (time.time() - start_time))


def test_case_1():
    """ mv """
    my_object = FileSystemOperations()
    my_object.mkdir("/A")
    my_object.mkdir("/A/B")
    my_object.create("/A/1.txt")
    my_object.mv("/A/1.txt", "/A/B/1.txt")
    my_object.mv("/A/B/1.txt", "/1.txt")
    my_object.mv("/1.txt", "/A/2.txt")
    return my_object


def test_case_2():
    """ read and write to file """
    my_object = test_case_1()

    message = "POCSD"
    message2 = "JOHN"
    offset = 0

    my_object.write("/A/2.txt", message*500)
    my_object.create("/A/B/1.txt")
    my_object.write("/A/B/1.txt", message2*500)

    my_object.read("/A/2.txt", 0, -1, 0)
    my_object.read("/A/B/1.txt", 0, -1, 0)
    my_object.read("/A/B/1.txt", len(message2)*499, -1, 0)

    my_object.mkdir("/A/B/C")
    my_object.mv("/A/B/1.txt", "/A/B/C/3.txt")
    my_object.read("/A/B/C/3.txt", 0, -1, 0)

    # should fail
    my_object.read("/A/B/1.txt", 0, -1, 0)
    
    return my_object


def test_case_3():
    """ rm for directories (both empty and with files) and files """
    my_object = FileSystemOperations()

    my_object.mkdir("/A")
    my_object.mkdir("/A/B")
    my_object.create("/A/1.txt")

    my_object.mkdir("/A/B/C")
    my_object.mkdir("/A/B/C/D")
    my_object.mkdir("/A/B/C/D/E")
    my_object.mv("/A/B/C/D/E", "/A/B/C/E")
    

    my_object.rm("/A/B/C/E")
    my_object.rm("/A/B/C/D")
    my_object.rm("/A/B/C")
    my_object.rm("/A/B")
    

    message = "PoCSD"
    my_object.write("/A/1.txt", message)

    # should silently fail
    my_object.rm("/A")
    

    my_object.rm("/A/1.txt")
    

    my_object.rm("/A")
    

    # should not be able to remove root
    my_object.rm("/")
    

    return my_object


def test_case_4():
    """ test replace functionality """
    my_object = FileSystemOperations()

    my_object.mkdir("/A")
    my_object.mkdir("/A/B")
    my_object.create("/A/test.txt")
    my_object.create("/A/B/test.txt")

    messageA = "A"*500
    messageAB = "AB"*250

    my_object.write("/A/B/test.txt", messageAB)
    my_object.write("/A/test.txt", messageA)
    
    my_object.mv("/A/B/test.txt", "/A/test.txt")

    my_object.read("/A/test.txt", 0, -1, 0)

def test_case_5():
    my_object = FileSystemOperations()

    my_object.mkdir("/A")
    my_object.create("/A/test.txt")
    messageA = "A"*500
    my_object.write("/A/test.txt", messageA)
    my_object.read("/A/test.txt", 0, -1, 0)

def test_case_6(my_object):
    print('test case set 1')
    for i in range(12):
        name = '/d'*(i+1)
        my_object.mkdir(name)
    for j in range(1, 8):
        for i in range(12):
            name = '/d'*(i)+'/f'
            msg = chr(ord("a")+i)*config.BLOCK_SIZE*j
            my_object.create(name)
            my_object.write(name, msg)
            assert(msg == my_object.read(name, 0, -1, 0))
        for i in range(12):
            name = '/d'*(i)+'/f'
            my_object.rm(name)

def test_case_7(my_object):
    print('test case set 2')
    for i in range(8):
        name = '/d'*(i)+'/f'
        msg = chr(ord("a")+i)*config.BLOCK_SIZE*(1+(i%2))
        my_object.create(name)
        my_object.write(name, msg)
        assert(msg == my_object.read(name, 0, -1, 0))
    for i in range(8):
        name = '/d'*(i)+'/f'
        my_object.rm(name)

def test_case_8(my_object):
    print('test case set 3')
    for i in range(8):
        name = '/d'*(i)+'/f'
        msg = chr(ord("a")+i)*config.BLOCK_SIZE*(1+((i+1)%2))
        my_object.create(name)
        my_object.write(name, msg)
        assert(msg == my_object.read(name, 0, -1, 0))
    for i in range(8):
        name = '/d'*(i)+'/f'
        my_object.rm(name)

if __name__ == '__main__':

    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Must (only) specify raid mode.")
        quit()
    
    raid_mode = sys.argv[1]
    if raid_mode != '1' and raid_mode != '5':
        print("Must use raid mode 1 or 5 - terminating program.")
        quit()

    FileSystem.Initialize_My_FileSystem(4, raid_mode)
    if (len(sys.argv) < 3):
        my_object = FileSystemOperations()
        print('Delaying 5s to allow termination of a server.')
        print('Server may also be terminated during execution.')
        time.sleep(5)
        test_case_6(my_object)
        test_case_7(my_object)
        test_case_8(my_object)
        my_object.create('/f')
        my_object.mv('/f', '/d/f')
        my_object.rm('/d/f')
        print('\nTests Complete.')
        print('Scroll up server logs to observe GET/SET load counters.')
        exit(0)
    
    test_case = sys.argv[2]

    if (test_case == "happy_path"): happy_path()
    elif (test_case == "1"): test_case_1()
    elif (test_case == "2"): test_case_2()
    elif (test_case == "3"): test_case_3()
    elif (test_case == "4"): test_case_4()
    elif (test_case == "5"): test_case_5()
    elif (test_case == "6"): test_case_6()
    elif (test_case == "7"): test_case_7()
    elif (test_case == "8"): test_case_8()
    elif (test_case == "9"): test_case_9()
    exit(0)
