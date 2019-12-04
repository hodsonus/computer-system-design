import xmlrpclib, config, pickle, os, sys, subprocess, time, traceback

numServers = int(sys.argv[1])
basePortNum = 8000
proxy = []

for i in range(numServers) :
    # append to the list of client proxies
    print('running server #' + str(basePortNum+i))
    proxy.append(xmlrpclib.ServerProxy("http://localhost:" + str(basePortNum + i) + "/"))
    #os.system('gnome-terminal -e \"python server.py ' + str(basePortNum + i) + '\"') # Ubuntu 16
    os.system('gnome-terminal -- python server.py ' + str(basePortNum + i)) # Ubuntu 18
    time.sleep(1)

while True:
    try:
        serverNum = int(raw_input("Select Server to Corrupt: "))
        if 0 <= serverNum and serverNum < numServers:
            modeNum = raw_input("Select mode [1] 0th blk [2] random blk: ")
            if modeNum == '1' or modeNum == '2':
                try:
                    retVal = proxy[serverNum].corruptData(pickle.dumps(modeNum))
                    print(pickle.loads(retVal))
                except: print("server down, cannot corrupt")
            else:
                print('option number out of bounds')
                continue
        else:
            print('server number out of bounds')
    except Exception as err :
        traceback.print_exc()
        print('connection error')
