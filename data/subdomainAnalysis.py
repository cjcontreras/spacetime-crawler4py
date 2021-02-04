from collections import defaultdict

# script that analyzes Domain.txt and returns unique subdomains with the number of unique pages in each subdomain
subdomains = defaultdict(lambda: 0)

with open("Domain.txt", "r") as input:
    for line in input:
        start = line.find("://") + 3
        subdomains[line [start:line.find("ics.uci.edu") + 11] ] += 1
        
sortedSubdomains = sorted(subdomains.items(),key = lambda item: item[0])
    
with open("subdomains.txt", "a") as output:
    for item in sortedSubdomains:
        l = str(item[0]) + ", " + str(item[1])
        output.write(l)
        output.write("\n")
