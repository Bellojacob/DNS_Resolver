from collections import deque






def main(filename, cacheFile):
# Open the query and save current iteration as currentDomain, this is the domain we are looking for
    # chatGpt recommended I use this type of queue
    queue = deque()
    file = open(filename, "r", encoding="utf-8-sig")
    cache = open(cacheFile, "r", encoding="utf-8-sig")
    # for this project, we are going to assume we are never going to start with more than 3 cache entries
    for line in cache:
        line = line.strip("\n")
        queue.append(line)

    cache.close()
    queueLength = str(len(queue))
    print(queue)
    print("Queue length " + queueLength)


    for query in file:
        print("Resolving Query: " + query)
        serverList = []
        currentDomain = query.strip()
        cacheBoolean = False
        # print("We are looking for " + currentDomain + "\n")

        # let's check the cache first
        # print("Checking the cache...")
        cache = open(cacheFile, "r", encoding="utf-8-sig")

        # get all the info from the cache and make it look presentable and easier to look through
        info = []
        for line in cache:
            info = line.strip("\n").split(";")
            # print("This is the info: " + str(info))

        cache.close()

        # now iterate through the cache, check the domain we are looking for is exactly the same as any domains in the cache
        for x in info:
            if currentDomain == info[0]:
                # print("Found domain!!!")
                # print(currentDomain + ";" + info[1])
                print("Cache")
                cache = True
                break
            else:
                # print("Not in cache")
                pass
        
        # so if we got to this point, it was not in the cache
        # go to Root server now
        root = open("servers/1-0-0-0.txt", "r", encoding="utf-8-sig")
        serverList.append("1-0-0-0")
        # print("\nRoots Servers:")
        # for line in root:
            # print(line)
        
        rootInfo = []
        
        for line in root:
            rootInfo.append(line.strip("\n").split(";")) 
            
        # print("LINES IN ROOT")
        # for x in rootInfo:
        #     print(x)
        
        # Find correct TLD Server
        tldServer = ""
        domainInfo = currentDomain.split(".")
        newDomainList = []

        for x in domainInfo:
            newDomainList.extend(x.split(";"))  # Extending the list with all split parts

        # for y in newDomainList:
        #     print(y)
        
        for x in rootInfo:
            if newDomainList[2] == "edu":
                if x[0] == newDomainList[2]:
                    tldServer = x[1]
                    serverList.append(tldServer)
            elif newDomainList[2] == "com":
                if x[0] == newDomainList[2]:
                    tldServer = x[1]
                    serverList.append(tldServer)
            elif newDomainList[2] == "gov":
                if x[0] == newDomainList[2]:
                    tldServer = x[1]
                    serverList.append(tldServer)
                    # print(tldServer)
        
        domainName = domainInfo[1]
        # print("We are looking for " + domainName)
        
        # print("The TLD Server we are going to is " + tldServer + ".txt because it is an ." + domainInfo[2] + "\n" + tldServer + " info:")
        
        specifiedTLDServer = open("servers/" + tldServer + ".txt", "r", encoding="utf-8")

        TLDInfo = None
        
        # loop through all the servers in the current TLD section, split each line by ; to separate domain and ip

        authServerNum = ""
        for line in specifiedTLDServer:
            line = line.strip("\n").split(";")
            newLine = line[0].split(".")
            # print(line)
            newLine.append(line[1])
            # print(newLine)
            if domainName == newLine[0]:
                # print("We Found " + domainName)
                # print("This is the Server number we need to return " + newLine[2] )
                authServerNum = newLine[2]
                serverList.append(authServerNum)
                break
        
        authServer = open("servers/" + authServerNum + ".txt", "r", encoding="utf-8")
        for line in authServer:
            line = line.strip("\n").split(";")
            # print(line)
            if currentDomain == line[0]:
                IPAddressToReturn = line[1]
                
                if cacheBoolean == False:
                    print(*serverList, sep='; ')
                # used chatGpt to figure out how to print an array without a newLine
                
                # print("We found the IP Address for " + currentDomain + " and it is " + IPAddressToReturn)
                domainPlusIp = currentDomain + ";" + IPAddressToReturn;
                print(domainPlusIp+ "\n")
                queue.appendleft(domainPlusIp)
                
                if len(queue) > 3:
                    queue.pop()
                break
            
    #let's check the cache queue
    print(queue)
    queueLength = str(len(queue))
    print("Queue length " + queueLength)
    
    
main("my-sample-query.txt","cache-entries.txt")