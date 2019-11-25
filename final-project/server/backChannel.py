import xmlrpclib, config, pickle, os, sys, subprocess, time

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
    serverNum = int(raw_input("Select Server to Corrupt..."))
    try :
        if 0 <= serverNum and serverNum < numServers:
            retVal = proxy[serverNum].corruptData()
            print(serverNum)
            print(pickle.loads(retVal))
        else:
            print('server number out of bounds')
    except Exception as err :
        print('connection error')
