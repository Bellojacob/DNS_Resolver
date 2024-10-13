

# Open the query and save current iteration as currentDomain, this is the domain we are looking for
file = open("my-sample-query.txt", "r", encoding="utf-8")
for query in file:
    serverList = []
    currentDomain = query
    print("We are looking for " + currentDomain + "\n")

    # let's check the cache first
    print("Checking the cache...")
    cache = open("cache-entries.txt", "r", encoding="utf-8-sig")

    # get all the info from the cache and make it look presentable and easier to look through
    info = None
    for line in cache:
        info = line.strip("\n").split(";")
        print("This is the info: " + str(info))

    cache.close()

    # now iterate through the cache, check the domain we are looking for is exactly the same as any domains in the cache
    for x in info:
        if currentDomain == info[0]:
            print("Found domain!!!")
            print(currentDomain + ";" + info[1])
            break
        else:
            print("Not in cache")
            break
    
    # so if we got to this point, it was not in the cache
    # go to Root server now
    root = open("servers/1-0-0-0.txt", "r", encoding="utf-8")
    serverList.append("1-0-0-0")
    print("\nRoots Servers:")
    for line in root:
        print(line)
    

    # Find correct TLD Server
    tldServer = 0
    domainInfo = currentDomain.split(".")
    print(domainInfo)
    if domainInfo[2] == "edu":
        tldServer = "1-0-0-1"
        serverList.append("1-0-0-1")
    elif domainInfo[2] == "com":
        tldServer = "15-25-72-200"
        serverList.append("15-25-72-200")
    elif domainInfo[2] == "gov":
        tldServer = "100-50-27-1"
        serverList.append("100-50-27-1")
    
    domainName = domainInfo[1]
    print("We are looking for " + domainName)
    
    print("The TLD Server we are going to is " + tldServer +".txt because it is an .edu\n" + tldServer + " info:")
    
    specifiedTLDServer = open("servers/"+tldServer+".txt", "r", encoding="utf-8")

    TLDInfo = None
    
    # loop through all the servers in the current TLD section, split each line by ; to separate domain and ip

    authServerNum = 0;
    for line in specifiedTLDServer:
        line = line.strip("\n").split(";")
        newLine = line[0].split(".")
        # print(line)
        newLine.append(line[1])
        print(newLine)
        if domainName == newLine[0]:
            print("We Found " + domainName)
            print("This is the Server number we need to return " + newLine[2] )
            authServerNum = newLine[2]
            serverList.append(authServerNum)
            break
    
    authServer = open("servers/"+authServerNum+".txt", "r", encoding="utf-8")
    for line in authServer:
        line = line.strip("\n").split(";")
        # print(line)
        if currentDomain == line[0]:
            IPAddressToReturn = line[1]
            
            print(*serverList, sep='; ')
            # used chatGpt to figure out how to print an array without a newLine
            # print("We found the IP Address for " + currentDomain + " and it is " + IPAddressToReturn)
            print(currentDomain+";"+IPAddressToReturn)
            break
        