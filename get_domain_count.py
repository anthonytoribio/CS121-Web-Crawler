import json

with open('domain_count.txt', 'r') as domainCountTxt:
    data = domainCountTxt.read()

dicto = json.loads(data)

sortedDicto = {key: val for key, val in sorted(dicto.items())}

f = open("Deliverable4.txt", "w")
f.write(f'There were {len(sortedDicto.keys())} subdomains found in the ics.uci.edu domain\n')
for k, v in sortedDicto.items():
    f.write(f'{k}, {v}\n')
f.close()