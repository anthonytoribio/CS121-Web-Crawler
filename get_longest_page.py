longest_page_count = 0
longest_page_url = ''
f = open('Logs/page_length.txt', 'r')
for line in f:
    line = line.strip().split(' ')
    if int(line[0]) > longest_page_count:
        longest_page_count = int(line[0])
        longest_page_url = line[1]
f.close()

f2 = open('Deliverable2.txt', 'w')
f2.write(f"The longest page is {longest_page_url}, with {longest_page_count} words!")
f2.close()