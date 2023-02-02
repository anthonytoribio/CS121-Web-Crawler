seen = set()

f = open('Logs/urls.txt', 'r')
for line in f:
    line = line.strip().split('#', 1)[0]
    if line not in seen:
        seen.add(line)
f.close()

f = open('Deliverable1.txt', 'w')
f.write(f'There were {len(seen)} unique pages found after web crawling')
f.close()