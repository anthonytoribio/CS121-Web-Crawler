from bs4 import BeautifulSoup

with open("index.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")
    print(soup.text)
    textList = soup.text.replace("\n", " ").split()
    print(textList)
    print(len(textList))
