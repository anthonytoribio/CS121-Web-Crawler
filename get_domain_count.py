import json
from my_helper import *

domainCounts = load_file('subDomains.json')

sortedDicto = {key: val for key, val in sorted(domainCounts.items())}

f = open("Deliverable4.txt", "w")
f.write(f'There were {len(sortedDicto.keys())} subdomains found in the ics.uci.edu domain\n')
for k, v in sortedDicto.items():
    f.write(f'{k}, {v["count"]}\n')
f.close()