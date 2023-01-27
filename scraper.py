import re
from urllib.parse import urlparse
from urllib import robotparser
from bs4 import BeautifulSoup

#Create a global robotparser that is used in is_valid
robotParser = robotparser.RobotFileParser()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    validLinks = [link for link in links if is_valid(link)]
    #print(validLinks)
    return validLinks

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    scrapped_urls = []
    if resp.status == 200:
        soup = BeautifulSoup(resp.raw_response.content)
        anchors = soup.find_all('a')
        for a in anchors:
            scrapped_urls.append(a.get('href'))
    else:
        print(resp.error)
    return scrapped_urls
    
def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    VALID_DOMAINS = {"www.ics.uci.edu", "www.cs.uci.edu", "www.informatics.uci.edu",
        "www.stat.uci.edu"}
    try:
        parsed = urlparse(url)
        #Set the url for the robot parser
        robotParser.set_url(parsed.scheme+"://"+parsed.netloc+"/robots.txt")
        if parsed.scheme not in set(["http", "https"]):
            return False
        #CHECKS if the domain is valid
        elif (not parsed.netloc in VALID_DOMAINS):
            return False
        #Checks the url is legal to be parsed by the robots.txt
        #possible error: parsed is not the correct url
        elif (not robotParser.can_fetch("*", parsed)):
            return False
        #TODO: ADD another check if the url is accessbile via the robots.txt file
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
