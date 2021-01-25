import re
from urllib.parse import urlparse
from scraper import is_valid, extract_next_links

if __name__ == '__main__':	
	extract_next_links("https://www.ics.uci.edu/", None)