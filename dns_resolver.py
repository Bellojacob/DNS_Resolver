import sys
from collections import deque

def main(filename, cacheFile):
    queue = deque()
    
    # load the cache entries into the queue
    # used chatgpt to find out to use encoding="utf-8-sig" because I was getting hex code in the txt files
    with open(cacheFile, "r", encoding="utf-8-sig") as cache:
        for line in cache:
            line = line.strip("\n")  # remove newline
            queue.append(line)

    # for this project, we are going to assume we are never going to start with more than 3 cache entries
    # use a dictionary to hold cache entries
    cache_dict = {}
    for line in queue:
        domain, ip = line.split(";")
        cache_dict[domain.strip()] = ip.strip()

    # open the query file and loop through each query
    with open(filename, "r", encoding="utf-8-sig") as file:
        for query in file:
            # open the query file and save current iteration as currentDomain; this is the domain we are looking for
            print("resolving query: " + query.strip(), end='\n')
            serverList = []
            currentDomain = query.strip()
            cacheBoolean = False

            # check if the current query is in the cache dictionary
            if currentDomain in cache_dict:
                # print the result from the cache if true
                print("cache")
                print(f"{currentDomain}; {cache_dict[currentDomain]}\n")
                cacheBoolean = True
            else:
                # if not in the cache, proceed with dns iteration starting at the root
                root = open("servers/1-0-0-0.txt", "r", encoding="utf-8-sig")
                serverList.append("1-0-0-0")
                
                rootInfo = [line.strip("\n").split(";") for line in root]
                
                # find correct tld server based on the query domain
                domainInfo = currentDomain.split(".") 
                newDomainList = []
                
                for x in domainInfo:
                    newDomainList.extend(x.split(";"))
                
                tldServer = None 
                for x in rootInfo:
                    if newDomainList[-1] == x[0]: 
                        tldServer = x[1]
                        serverList.append(tldServer)
                        break

                if not tldServer:
                    print("unresolved\n")
                    continue
                
                # open the corresponding tld server file
                specifiedTLDServer = open(f"servers/{tldServer}.txt", "r", encoding="utf-8")
                authServerNum = None
                
                # loop through the tld server to find the authoritative server
                for line in specifiedTLDServer:
                    domain, serverNum = line.strip().split(";")
                    if domainInfo[-2] == domain.split(".")[0]:
                        authServerNum = serverNum 
                        serverList.append(authServerNum)
                        break
                        
                if not authServerNum:
                    print("unresolved\n")
                    continue 

                # open the authoritative server file
                authServer = open(f"servers/{authServerNum}.txt", "r", encoding="utf-8")
                resolved = False  # initialize as not resolved
                
                for line in authServer:
                    domain, ip = line.strip().split(";")
                    if currentDomain == domain:  
                        # if the current query matches this domain
                        # print the path of the dns iteration
                        print(*serverList, sep='; ')    # used chatgpt to figure out how to print an array without a newline
                        domainPlusIp = f"{currentDomain};{ip}"
                        print(f"{domainPlusIp}\n")
                        
                        # update the cache
                        queue.appendleft(domainPlusIp)
                        if len(queue) > 3:
                            queue.pop()
                        resolved = True
                        break
                        
                if not resolved:
                    print("unresolved\n")

    # after processing all queries, write the updated cache to the file
    with open(cacheFile, "w", encoding="utf-8-sig") as cacheWrite:
        for entry in queue:
            cacheWrite.write(entry + "\n")


if len(sys.argv) != 3:
    print("must enter 3 files, dns_resolver.py, some query file, and a cache file")
else:
    # pass the command-line arguments to the main function
    query_file = sys.argv[1]
    cache_file = sys.argv[2]
    main(query_file, cache_file)
