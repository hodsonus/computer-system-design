import config
from InodeLayer import InodeLayer
import BlockLayer
interface = BlockLayer.BlockLayer()

def repeat_to_length(string_to_expand, length):
    return (string_to_expand * ((length/len(string_to_expand))+1))[:length]


def evaluate_result(expected_read_data, read_data):
    import difflib
    diff = [li for li in difflib.ndiff(expected_read_data, read_data) if li[0] != ' ']
    if (diff == []):
        print("Expected result!")
    else:
        print("Unexpected result...")
        print(diff)


def test_case_1():
    print("Test case 1 - data 1 block long with an offset of 0 blocks.")
    uut = InodeLayer()

    inode = uut.new_inode(0)
    offset = 0
    # data is the size of one block
    write_data = repeat_to_length("This is a test!", config.BLOCK_SIZE)

    inode = uut.write(inode, offset, write_data)
    inode, read_data = uut.read(inode, offset, len(write_data))

    evaluate_result(write_data, read_data)


def test_case_2():
    print("Test case 2 - data 1.5 blocks long with an offset of 0 blocks.")
    uut = InodeLayer()

    inode = uut.new_inode(0)
    offset = 0
    # data is the size of 1.5 blocks
    write_data = repeat_to_length("This is a test!", (int)(config.BLOCK_SIZE*1.5))

    inode = uut.write(inode, offset, write_data)
    inode, read_data = uut.read(inode, offset, len(write_data))

    evaluate_result(write_data, read_data)


def test_case_3():
    print("Test case 3 - data 1.5 blocks long with an offset of .5 blocks.")
    uut = InodeLayer()

    inode = uut.new_inode(0)
    offset = (int)(config.BLOCK_SIZE*0.5)
    # data is the size of 1.5 blocks
    write_data = repeat_to_length("This is a test!", (int)(config.BLOCK_SIZE*1.5))

    inode = uut.write(inode, offset, write_data)
    inode, read_data = uut.read(inode, offset, len(write_data))

    evaluate_result(write_data, read_data)


def test_case_4():
    print("Test case 4 - data 1.5 blocks long with an offset of .5 blocks. Reading from 0 blocks")
    uut = InodeLayer()

    inode = uut.new_inode(0)
    offset = (int)(config.BLOCK_SIZE*0.5)
    # data is the size of 1.5 blocks
    write_data = repeat_to_length("This is a test!", (int)(config.BLOCK_SIZE*1.5))
    expected_read_data = write_data[:len(write_data)-offset]

    inode = uut.write(inode, offset, write_data)
    inode, read_data = uut.read(inode, 0, len(write_data))

    print(expected_read_data == read_data.strip("\x00"))

    print("Done!")


def test_inode_equivalency(inode, new_inode):
    for i in range(0,len(inode.blk_numbers)):
        inode_blk_num = inode.blk_numbers[i]
        new_inode_blk_num = new_inode.blk_numbers[i]

        if (inode_blk_num == -1 and new_inode_blk_num == -1):
            continue
        if (inode_blk_num == -1 or new_inode_blk_num == -1):
            print("Allocated blocks are not equivalent.")
            break

        inode_data = interface.BLOCK_NUMBER_TO_DATA_BLOCK(inode_blk_num)
        new_inode_data = interface.BLOCK_NUMBER_TO_DATA_BLOCK(new_inode_blk_num)

        if (new_inode_data != inode_data):
            print("Inode data is not equivalent.")
            break


def test_case_5():
    message = "Test case 5 - testing the copy functionality."
    print(message)

    uut = InodeLayer()

    inode = uut.new_inode(0)
    write_data = repeat_to_length(message, (int)(config.BLOCK_SIZE*12))
    offset = 0
    inode = uut.write(inode, offset, write_data)
    inode.name = message

    new_inode = uut.copy(inode)

    test_inode_equivalency(inode, new_inode)

    print("Done!")


def test_case_6():
    message = "Test case 6 - overwrite functionality."
    print(message)
    uut = InodeLayer()

    inode = uut.new_inode(0)
    offset = 0
    # data is the size of 1.5 blocks
    write_data = repeat_to_length(message, (int)(config.BLOCK_SIZE*10))
    overwrite_data = "This is the data that I am using to overwrite the old data with."
    overwrite_offset = 256

    expected_read_data_list = list(write_data)
    for i in range(len(overwrite_data)):
        expected_read_data_list[overwrite_offset+i] = overwrite_data[i]
    expected_read_data = "".join(expected_read_data_list)

    inode = uut.write(inode, offset, write_data)
    inode = uut.write(inode, overwrite_offset, overwrite_data)
    inode, read_data = uut.read(inode, offset, len(write_data))

    print(expected_read_data == read_data.strip("\x00"))

    print("Done!")


if __name__ == "__main__":
    test_case_6()