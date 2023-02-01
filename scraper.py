import re
from urllib.parse import urlparse
from urllib import robotparser
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
from my_helper import *
import os
import json
#from tokenize import tokenize


#Create a global robotparser that is used in is_valid
robotParser = robotparser.RobotFileParser()

VALID_DOMAINS = {"ics.uci.edu", "cs.uci.edu", "informatics.uci.edu",
    "stat.uci.edu"}
PAGE_COPY_PATH = r"./text_copy.txt"

domainDicto = dict()
wordFreq = Counter()

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
    #Only read the page if it has content and it is less than .001 gb
    if resp.status == 200 and resp.raw_response != None and len(resp.raw_response.content) < 1000000:
        print(f"\n!-------The page: {url} is size: {len(resp.raw_response.content)} bytes----------!\n")
        soup = BeautifulSoup(resp.raw_response.content)
        anchors = soup.find_all('a')
        for a in anchors:
            scrapped_urls.append(a.get('href'))

        page_length = sum([len(string.split()) for string in soup.stripped_strings if string not in punctuation])
        write_to_end( os.path.dirname(__file__) + "/Logs/page_length.txt", str(page_length))
        #print(page_length)

        # Copying current webpage to local txt and tokenize/update wordFreq
        copy_page(PAGE_COPY_PATH, [string for string in soup.stripped_strings])
        file = open(PAGE_COPY_PATH, "rb")
        #token_list = [token[1] for token in tokenize(file.readline) if (token[0] == 1 or token[0] == 2)]
        token_list = tokenize(PAGE_COPY_PATH)
        if len(wordFreq) == 0 and os.path.exists('wordFreq.json'):
            wordFreq = load_file('wordFreq.json')
        wordFreq.update(Counter(computeWordFrequencies(token_list)))
        save_file('wordFreq.json', wordFreq)


    else:
        print(resp.error)
    return scrapped_urls
    
def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        #Set the url for the robot parser

        # Our url has a fragment so we don't want to crawl it
        if parsed.fragment:
            return False

        if parsed.scheme not in set(["http", "https"]):
            return False

        #CHECKS if the domain is valid
        netlocList = parsed.netloc.split(".")
        if (len(netlocList) < 3):
            return False

        domain = netlocList[-3] + "." + netlocList[-2] + "." + netlocList[-1]
        
        if (not domain in VALID_DOMAINS):
            print("=========== Invalid Domain ==============")
            print(url)
            return False

        elif domain == 'ics.uci.edu': # Domain is of type ics.uci.edu and is a valid domain
            trueDomain = parsed.scheme+"://"+parsed.netloc
            if trueDomain not in {'https://www.ics.uci.edu','http://www.ics.uci.edu'}: # Domain is subdomain of ics.uci.edu 
                if len(domainDicto) == 0 and os.path.exists('domain_count.json'):
                    domainDicto = load_file('domain_count.json')
                domainDicto[parsed.netloc] = domainDicto.get(parsed.netloc, 0) + 1

                print("============ Dictionary Updated ============")
                print(domainDicto)
                save_file('domain_count.json', domainDicto)


        #Checks the url is legal to be parsed by the robots.txt
        #possible error: parsed is not the correct url
        #set the url of the robots.txt and then read 
        robotParser.set_url(parsed.scheme+"://"+domain+"/robots.txt")
        robotParser.read()
        
        if (not robotParser.can_fetch("*", url)):
            print("UNABLE to parse because of robots.txt")
            print("URL AT:", url)
            return False
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
