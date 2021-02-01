import re
from urllib.parse import urlparse, urldefrag
from urllib.request import *
from bs4 import BeautifulSoup
from Tokenizer import *
import hashlib
from bitstring import BitArray
import numpy as np
import os


def scraper(url, resp):
	links = extract_next_links(url, resp)
	return[link for link in links if is_valid(link)]

# ==================================================
#
#	list extract_next_links(url, Response obj)
# 
# ==================================================

def extract_next_links(url, resp):

    # get list of urls found after tokenizening the project
    temp = []


    # HARDCODED AVOID URLS
    avoid = open("data/Avoids.txt", 'r')
    traps = avoid.read()
    avoid.close()



    if url in traps:
        return temp

    # RESP STATUS CHECKING
    if resp.status <200 or resp.status > 399:
        return temp


    # DATA ANALYSIS 1) unique urls
    #f = open("data/Unique.txt", 'w+') #should it be w+ or r+?
    
    #this makes it so that there's only one number (the number of unique pages by the end of running the program)
    
    #This might get tricky because if you restart your crawler, you have to clear Unique.txt beforehand or else you'll be counting incorrectly
    
    f = open("data/Unique.txt","r")
    currentNum = f.read()

    if currentNum == "":
        #this means file is empty,
        f.close()
        f = open("data/Unique.txt", "w+")
        f.write("1")
        f.close()
    else:
        f.close()
        newNum = int(currentNum) + 1
        f = open("data/Unique.txt", "w+")
        f.write(str(newNum))
        f.close()      


    # END DA 1)
    
    '''
    num = int(next(f).split())
	print("this is the value from unique.txt: ")
	print(num)
	num += 1
	f.write(str(num))
	f.write('\n')
	print(num)
	f.close()

	lock.release()
    '''
	

    # Assumption is that the page is a safe object to look at
    # BeautifulSoup takes the page object and converts it into readable HTML
    # 'a' is speficially a tag in HTML that refers to a new link
    # link.get('href') returns the value associated with the key
    page = resp.raw_response.content

    # PARSING HTML FILE & CHECKING SIZE
    length = 0
    soup = BeautifulSoup(page, 'html.parser')
    length = len(soup.getText(strip = True).split())
    '''
    for line in soup.find_all('p').getText():
        length += len(line)
    if length < 100:
        return temp
    '''



    
    # SIMHASH CHECKING
    simValue, wordList = getSimhashVal(soup.get_text())
    threshHold = open("data/thresh.txt", 'r+')
    if os.stat("data/thresh.txt").st_size != 0:
        currLine = int(threshHold.readline())
        while currLine:
            comparison = compareSimhash(int(currLine), simValue)
            if comparison > .95:
                threshHold.close()
                print("too similar")
                return temp
            currLine = threshHold.readline()

    threshHold.write(str(simValue))
    threshHold.write('\n')
    threshHold.close()
    # END SIMHASH

    
    # DATA ANALYSIS 3) top 50 words overall

    f = open("data/Tokens.txt", 'a')
    for word in wordList:
    	f.write(word)
    	f.write(' ')
    f.write('\n')
    f.close()

    # END DA 3)
	
	# DATA ANALYSIS 2) largest page

    f = open("data/Large.txt","r")
    currentNum = f.read()

    if currentNum == "":
        #this means file is empty,
        f.close()
        f = open("data/Large.txt", "w+")
        f.write(str(length))
        f.write(', ')
        f.write(url)
        f.close()
    else:
        f.close()
        currNum = currentNum.split(',')
        if length > int(currNum[0]):
        	f = open("data/Large.txt", "w+")
        	f.write(str(length))
        	f.write(', ')
        	f.write(url)
        	f.close()

    # END DA 2)    

    # LINK SCRAPING + DEFRAG
    for link in soup.find_all('a'):
        temp.append(urldefrag(link.get('href'))[0])


    return temp

# ==================================================
#
#	bool is_valid(str)
# 
# ==================================================

def is_valid(url):
    try:
        # defragObj = urldefrag(url)
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        valids = set([".ics.uci.edu"
                     ,".cs.uci.edu"
                             ,".informatics.uci.edu"
                             ,".stat.uci.edu"
                             ,"today.uci.edu"
                             ])
        present = False

        for domain in valids:
            if domain in parsed.netloc:
                present = True
                break

        if not present:
            return False

        if (parsed.netloc == "today.uci.edu") and ("/department/information_computer_sciences/" not in parsed.path):
            return False

        # DATA ANALYSIS 4) domain page
        if ".ics.uci.edu" in parsed.netloc:
            f = open("data/Domain.txt", 'a')
            f.write(url)
            f.write('\n')
            f.close()

        # Needs to add more possibilities?
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise



# HELPER FUNCTIONS

def getSimhashVal(text):
    wordList = Tokenize(text)
    freq = computeWordFrequencies(wordList)
    hasher = SimHash(freq)
    return hasher.value, wordList

def compareSimhash(val1, val2):
    # val1 = bin(val1)[2:]
    # val2 = bin(val2)[2:]
    xor = val1^val2
    xor = ~xor
    bits = [(xor >> bit) & 1 for bit in range(126 - 1, -1, -1)]
    sameVal = 0
    for bit in bits:
        sameVal += bit

    return sameVal/126

class SimHash:
    def __init__(self, features):
        self.hashVal = dict()
        for key in features.keys():
            bytstr = hashlib.md5(key.encode()).hexdigest()
            value = BitArray(hex=bytstr)
            self.hashVal[key] = value.bin[2:]

        self.vector = np.zeros(126) # note that hashlib is 16 bytes, or 126 bits
        for i in range(0, len(self.vector) - 1):
            for key, number in self.hashVal.items():
                # num_bits = 128
                # bits = [(number >> bit) & 1 for bit in range(num_bits - 1, -1, -1)]
                if number[i] == '1':
                    self.vector[i] += features[key]
                else:
                    self.vector[i] -= features[key]

        for i in range(len(self.vector)):
            if self.vector[i] > 0:
                self.vector[i] = 1
            else:
                self.vector[i] = 0

        # https://stackoverflow.com/questions/41069825/convert-binary-01-numpy-to-integer-or-binary-string
        self.value = int(self.vector.dot(2**np.arange(self.vector.size)[::-1]))
