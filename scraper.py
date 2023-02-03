import re
from urllib.parse import urlparse
from urllib import robotparser
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
from my_helper import *
import os



#Create a global robotparser that is used in is_valid
robotParser = robotparser.RobotFileParser()

VALID_DOMAINS = {"ics.uci.edu", "cs.uci.edu", "informatics.uci.edu",
    "stat.uci.edu"}
PAGE_COPY_PATH = r"./text_copy.txt"


wordFreq = Counter()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    validLinks = [link for link in links if is_valid(link)]
    defraggedLinks = [link.split('#', 1)[0] for link in validLinks]
    finalLinks = []

    # IMPORTANT : Delete subDomains.json when starting a new crawl if you want accurate subdomain counts
    for url in defraggedLinks:
        parsed = urlparse(url)
        netlocList = parsed.netloc.split(".")

        #loop through the path and check if any is a date. If it is then dont add to finalLinks
        hasDate = False
        urlPath = parsed.path.split("/")
        for pathSplit in urlPath:
            if (isDate(pathSplit)):
                hasDate = True
                break
        if (not hasDate):
            finalLinks.append(url)


        domain = netlocList[-3] + "." + netlocList[-2] + "." + netlocList[-1]
        trueDomain = parsed.scheme+"://"+parsed.netloc
        
        # Subdomain is of ics.uci.edu but it isn't the base url of ics.uci.edu
        if domain == 'ics.uci.edu' and trueDomain not in {'https://www.ics.uci.edu','http://www.ics.uci.edu'}:

            # Debug prints
            print("======== Valid Subdomain Found ========")
            print(url)
            print()

            if os.path.exists('subDomains.json'):
                
                domainDict = load_file('subDomains.json')

                if parsed.netloc in domainDict:
                    if url not in domainDict[parsed.netloc]['urls']:
                        domainDict[parsed.netloc]['urls'].append(url)
                        domainDict[parsed.netloc]['count'] += 1
                else:
                    domainDict[parsed.netloc] = {'count': 1, 'urls': [url]}
                
                save_file('subDomains.json', domainDict)

            else:
                domainDict = dict()
                domainDict[parsed.netloc] = {'count': 1, 'urls': [url]}    
                save_file('subDomains.json', domainDict)
            
            # Debug prints
            print("=========== Dictionary Updated ==============")
            for k,v in domainDict.items():
                print(k, v)
            print()

    return finalLinks

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

        page_length = sum([len(string.split()) for string in soup.stripped_strings if string not in punctuation])
        write_to_end( os.path.dirname(__file__) + "/Logs/page_length.txt", str(page_length) + " "+ url )
        #print(page_length)

        if not high_info(soup, resp) and page_length < 200:
            return []


        prev = get_lines(PAGE_COPY_PATH)
        curr = [string for string in soup.stripped_strings]

        if prev == curr:
            print("DUPLICATE FOUND")
            return scrapped_urls

        # Copying current webpage to local txt and tokenize/update wordFreq
        copy_page(PAGE_COPY_PATH, [string for string in soup.stripped_strings])

        anchors = soup.find_all('a')
        #parse the url to get the scheme and domain for later use
        parse = urlparse(url)
        #for each anchor check if its a relative url and if so change to absolute
        for a in anchors:
            hrefLink = a.get('href')

            if hrefLink != None and len(hrefLink) > 2:
                if (hrefLink[:2] == "//"):
                    scrapped_urls.append("https:" + hrefLink)
                elif (hrefLink[0] == "/"):
                    scrapped_urls.append(parse.scheme + "://" + parse.netloc + hrefLink)
            else:
                scrapped_urls.append(a.get('href'))

        file = open(PAGE_COPY_PATH, "rb")
        #token_list = [token[1] for token in tokenize(file.readline) if (token[0] == 1 or token[0] == 2)]
        token_list = tokenize(PAGE_COPY_PATH)

        # IMPORTANT: Delete wordFreq.json when starting from the beginning for accurate tracking
        global wordFreq
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

        if parsed.scheme not in set(["http", "https"]):
            return False

        #CHECKS if the domain is valid
        netlocList = parsed.netloc.split(".")
        if (len(netlocList) < 3):
            return False

        domain = netlocList[-3] + "." + netlocList[-2] + "." + netlocList[-1]
        
        if (not domain in VALID_DOMAINS):
            return False

        #Checks the url is legal to be parsed by the robots.txt
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
