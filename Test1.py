import re
import requests
from utils import response
from urllib.parse import urlparse
from scraper import *
from bs4 import BeautifulSoup


if __name__ == '__main__':
    
    page = urlopen('https://www.stat.uci.edu/minor-in-statistics')
    
    soup = BeautifulSoup(page,'html.parser')
    l = len(soup.getText(strip = True).split())
    print(l)
    '''

	val = getSimhashVal("Hello there my name is conner and i like to code")
	print(val)
	val1 = getSimhashVal("Hello there my name is meryl and i like to program")
	print(val1)
	ratio = compareSimhash(val, val1)
	print(ratio)
		# url = "https://www.ics.uci.edu/"
	
		# page = urlopen(url)
		# soup = BeautifulSoup(page, 'html.parser')
	
		#extract_next_links(url, None)

		#url1 = "http://www.informatics.uci.edu/files/pdf/InformaticsBrochure-March2018"
		#extract_next_links(url1, None)
	'''
		