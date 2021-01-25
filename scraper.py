import re
from urllib.parse import urlparse, urldefrag

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

# TODO:
#   1) edit is_valid such that domains not included in accepted list is 
#   rejected - Low Priority
#   2) 
#
#
#
#


def extract_next_links(url, resp):
    # get list of urls found after tokenizening the project
    # 






    return list()

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