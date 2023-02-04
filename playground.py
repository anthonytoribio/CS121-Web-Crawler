from my_helper import *
from simhash import Simhash, SimhashIndex
from urllib.parse import urlparse
import re


# calculate_given_quantile("Logs/page_length.txt", 25)

def get_features(s):

    # I think width adjusts the relaxness of the algorithm
    # Lower weight makes it easier to find similarities between urls
    # Higher weight makes it harder
    width = 1
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

# data = {
#     1: u'https://www.stat.uci.edu',
# }

objs = []

# Initializes empty index
index = SimhashIndex(objs, k=0)

f = open('Logs/urls.txt', 'r')
counter = 0



# going through every line in urls.txt to test simhash
for i, line in enumerate(f):

    line = line.strip()
    parsed = urlparse(line)

    if parsed.netloc != "swiki.ics.uci.edu":
        continue

    # This gets the weight of our current url
    s = Simhash(get_features(line))

    # If there are any near or exact duplicates in the index
    if index.get_near_dups(s):
        print("======== Near or exact duplicate url found ======")

        # This shows which line number in the urls.txt is the url that our current url was revealed to be similar to
        print(index.get_near_dups(s))

        # Debug to print out our current url
        print(line)
        counter += 1

    # Otherwise, add url to the index
    else:
        index.add(str(i+1), s)


print(f'There were {counter} near or exact duplicate urls found')
    
