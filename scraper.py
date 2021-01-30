import re
from urllib.parse import urlparse, urldefrag
from urllib.request import *
from bs4 import BeautifulSoup
from Tokenizer import *
import hashlib 


def scraper(url, resp):
	links = extract_next_links(url, resp)
	return[link for link in links if is_valid(link)]

# ==================================================
#
#	list extract_next_links(url, Response obj)
# 
# ==================================================

def extract_next_links(url, resp):
	
	# TODO:
	# Determine if it is worth scraping



	# get list of urls found after tokenizening the project
	temp = []
	avoid = open("Avoids.txt", 'r')
	traps = avoid.read()

	
	if url in traps:
		return temp

	# Basically we do not want to look at any pages where there are breaking errors
	if resp is not None:
		if resp.status <200 or resp.status > 399:
			return temp

	# This is in case of the resp being 200 but contains no data. 
	try:
		# NOTE: for when the server is back up, I think this urlopen functionis useless	
		# rather use the raw_response
		# if it is, then replace 
		page = urlopen(url)
		print(resp.raw_response)
	except:
		return temp
	else:
	
	

	# Assumption is that the page is a safe object to look at
	# BeautifulSoup takes the page object and converts it into readable HTML
	# 'a' is speficially a tag in HTML that refers to a new link
	# link.get('href') returns the value associated with the key
		soup = BeautifulSoup(page, 'html.parser')
		if len(soup.get_text()) < 100:
			return temp

		for link in soup.find_all('a'):
			temp.append(link.get('href'))

		return temp


# ==================================================
#
#	bool is_valid(str)
# 
# ==================================================

def is_valid(url):
	try:
		url = urldefrag(url)
		parsed = urlparse(url[0])
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

def getSimhashVal(text):
	wordList = Tokenizer.Tokenize(text)
	freq = Tokenizer.computeWordFrequencies(wordList)
	hasher = SimHash(freq)
	return hasher.value

class SimHash:
	def __init__(self, features):
		self.hashVal = dict()
		for key, value in features.items():
			self.hashVal[key] = hashlib.md5(value)

		self.vector = [0]*128 # note that hashlib is 16 bytes, or 128 bits
		for i in range(len(self.vector)):
			for key, number in self.hashVal.items():
				num_bits = 128
				bits = [(number >> bit) & 1 for bit in range(num_bits - 1, -1, -1)]
				if bits[i] == 1:
					vector[i] += features[key]
				else:
					vector[i] -= features[key]

		for i in range(len(self.vector)):
			if self.vector[i] > 0:
				self.vector[i] = 1
			else:
				self.vector[i] = 0

		self.value = self.vector.dot(2**np.arange(self.vector.size)[::-1])