import re
import requests
import cbor
from utils import response
from urllib.parse import urlparse
from scraper import is_valid, extract_next_links

if __name__ == '__main__':	
    
        extract_next_links
    
        url = "https://www.ics.uci.edu/"
    
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
    
        #extract_next_links(url, None)

        #url1 = "http://www.informatics.uci.edu/files/pdf/InformaticsBrochure-March2018"
        #extract_next_links(url1, None)
    
        tList = Tokenize(soup.get_text())
        
        print(tList)
        
        print()
        
        print(len(tList))