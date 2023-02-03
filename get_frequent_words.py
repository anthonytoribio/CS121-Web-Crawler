import json
from my_helper import load_file

wordFreq = load_file('wordFreq.json')

sortedWordFreq = sorted(wordFreq.items(), key=lambda x: x[1], reverse=True)
f = open("Deliverable3.txt", "w")
f.write("The 50 most common words in the entire set of crawled pages were:\n\n")
for word, freq in sortedWordFreq[:50]:
    f.write(f'{word}\n')
f.close()