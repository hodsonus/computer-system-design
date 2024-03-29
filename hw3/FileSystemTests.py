import FileSystem, sys
from FileSystem import FileSystemOperations


def happy_path():
    my_object = FileSystemOperations()
    my_object.status()
    offset = 0
    my_object.mkdir("/A")
    my_object.status()
    my_object.mkdir("/B")
    my_object.status()
    '''as A is already there we can create file in A'''
    my_object.create("/A/1.txt")
    my_object.status()
    '''as 1.txt is already created now, we can write to it.'''
    my_object.write("/A/1.txt", "POCSD", offset)
    my_object.read("/A/1.txt", offset, len("POCSD"))
    my_object.status()
    my_object.mv("/A/1.txt", "/B/1.txt")
    my_object.status()
    my_object.status()
    my_object.rm("/B/1.txt")
    my_object.rm("/B")


def test_case_1():
    """ mv """
    my_object = FileSystemOperations()
    my_object.mkdir("/A")
    my_object.mkdir("/A/B")
    my_object.create("/A/1.txt")
    my_object.mv("/A/1.txt", "/A/B/1.txt")
    my_object.mv("/A/B/1.txt", "/1.txt")
    my_object.mv("/1.txt", "/A/2.txt")
    my_object.status()
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

    my_object.read("/A/2.txt")
    my_object.read("/A/B/1.txt")
    my_object.read("/A/B/1.txt", len(message2)*499)

    my_object.mkdir("/A/B/C")
    my_object.mv("/A/B/1.txt", "/A/B/C/3.txt")
    my_object.read("/A/B/C/3.txt")

    # should fail
    my_object.read("/A/B/1.txt")
    
    return my_object


def test_case_3():
    """ rm for directories (both empty and with files) and files """
    my_object = FileSystemOperations()

    my_object.mkdir("/A")
    my_object.mkdir("/A/B")
    my_object.create("/A/1.txt")
    my_object.status()

    my_object.mkdir("/A/B/C")
    my_object.mkdir("/A/B/C/D")
    my_object.mkdir("/A/B/C/D/E")
    my_object.mv("/A/B/C/D/E", "/A/B/C/E")
    my_object.status()

    my_object.rm("/A/B/C/E")
    my_object.rm("/A/B/C/D")
    my_object.rm("/A/B/C")

    my_object.rm("/A/B")

    message = "PoCSD"
    my_object.write("/A/1.txt", message)

    # should silently fail
    my_object.rm("/A")
    my_object.status()

    my_object.rm("/A/1.txt")
    my_object.status()

    my_object.rm("/A")
    my_object.status()

    # should not be able to remove root
    my_object.rm("/")
    my_object.status()

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

    my_object.read("/A/test.txt")
    my_object.status()


def test_case_5():
    """ """


def test_case_6():
    """  """


if __name__ == '__main__':
    FileSystem.Initialize_My_FileSystem()
    if (len(sys.argv) < 2):
        print("invalid usage")
        exit(0)
    test_case = sys.argv[1]
    if (test_case == "happy_path"):
        happy_path()
    elif (test_case == "1"):
        test_case_1()
    elif (test_case == "2"):
        test_case_2()
    elif (test_case == "3"):
        test_case_3()
    elif (test_case == "4"):
        test_case_4()
    elif (test_case == "5"):
        test_case_5()
    elif (test_case == "6"):
        test_case_6()
    exit(0)