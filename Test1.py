import re
from utils import response
from urllib.parse import urlparse, urljoin, urldefrag
from urllib.request import *
from scraper import is_valid
from bs4 import BeautifulSoup


if __name__ == '__main__':
	
	url = 'https://www.stat.uci.edu'
	page = urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')

	temp =[]
	for link in soup.find_all('a'):
		foundLink = str(urldefrag(link.get('href'))[0])
		print(foundLink)
		if "http" not in foundLink:
			foundLink = urljoin(url, foundLink)
		if foundLink not in temp:
			temp.append(foundLink)

	# for link in soup.find_all('a'):
	# 	foundLink = str(urldefrag(link.get('href'))[0])
	# 	if "http" not in foundLink:
	# 		newLink = urljoin(url, foundLink)
	# 		if newLink not in temp:
	# 			temp.append(newLink)

	print(temp)
	print("\n\n")

	valids = []
	for link in temp:
		if is_valid(link):
			valids.append(link)

	print(valids)

	# parsed = urlparse("//www.ics.uci.edu/community/news/view_news?id=1906")

	# print(parsed)

	# result = urljoin("https://www.ics.uci.edu/community", "//stats/news/view_news?id=1906")
	# print(result)

	# page = urlopen('https://www.stat.uci.edu/minor-in-statistics')
	
	# soup = BeautifulSoup(page,'html.parser')
	# l = len(soup.getText(strip = True).split())
	# print(l)
	
	# val = getSimhashVal("Hello there my name is conner and i like to code")
	# print(val)
	# val1 = getSimhashVal("Hello there my name is meryl and i like to program")
	# print(val1)
	# ratio = compareSimhash(val, val1)
	# print(ratio)
		# url = "https://www.ics.uci.edu/"
	
		# page = urlopen(url)
		# soup = BeautifulSoup(page, 'html.parser')
	
		#extract_next_links(url, None)

		#url1 = "http://www.informatics.uci.edu/files/pdf/InformaticsBrochure-March2018"
		#extract_next_links(url1, None)
	
		