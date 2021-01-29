import re
import requests
import cbor
from utils import response
from urllib.parse import urlparse
from scraper import is_valid, extract_next_links

if __name__ == '__main__':	
	url = "https://www.ics.uci.edu/"
	extract_next_links(url, None)