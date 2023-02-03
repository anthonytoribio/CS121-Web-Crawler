import json
import datetime as dt
from string import punctuation
import os
import statistics
import numpy as np



stop_words = {'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
              'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being',
              'below', 'between', 'both', 'but', 'by', 'can', "can't", 'cannot', 'com', 'could',
              "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during',
              'each', 'else', 'ever', 'few', 'for', 'from', 'further', 'get', 'had', "hadn't", 'has',
              "hasn't", 'have', "haven't", 'having', 'he', 'her', 'here', "here's", 'hers', 'herself',
              'him', 'himself', 'his', 'how', "how's", 'i', "i'm", 'if', 'in', 'into', 'is', "isn't",
              'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself',
              'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our',
              'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll",
              "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the',
              'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they',
              "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under',
              'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were',
              "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while',
              'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you',
              "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'}

ALPHANUMERIC = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1",
    "2", "3", "4", "5", "6", "7", "8", "9", "0"}

#formats for dates that we want to avoid
FMTS = ("%Y-%m-%d", "%Y-%m")


def write_to_end(file_name, url):   
    file = open(file_name, 'a+')
    file.write(url + "\n")
    file.close()
    

def copy_page(file_name : str, lines : list):
    file = open(file_name, "w", encoding="utf-8")
    for line in lines:
        for char in line:
            if char.isalnum():
                file.write(char)
            elif char.isspace():
                file.write(char)
        file.write("\n")
    file.close()


#BELOW LET n = the total amount of any characters inside a file. 

#Time Complexity = O(n) + O(n) + O(n) + O(n) = O(4n) = O(n)
def tokenize(textFilePath: str) -> '[str]':
    """
    The function returns a list of strings (tokens) from the original file
    that are seperated by non alphanumeric characters. If an error occured
    then the function will return -1.
    """
    try:
        with open(textFilePath) as f:  #opens the file and returns resources once done reading (O(1))
            done = False
            tokens = []
            leftOver = ""

            while not done:   #Reads the file until reaching the end (O(n)) where n is the total characters in the file.
                data = f.read(1024)
                if not data:
                    done = True
                else:
                    # change to lowercase O(d); where d = the size of data read
                    # By the end of the loop total data read and change to lowercase is O(n)
                    data = data.lower()  
                    start = 0
                    #Check if the first char is non alpha numeric and if leftOver is not an empty string
                    #if so then we can add leftOver to tokens O(1)
                    if not data[start] in ALPHANUMERIC and leftOver:
                        tokens.append(leftOver)
                        leftOver = ""
                    # Loop through the data and use sliding window algorithm
                    # By the time we return from the function this loop will have looped through all n characters
                    # so O(n)
                    for index in range(len(data)):
                        #DEBUG print(f"data char is: {data[index]}")
                        #DEBUG print(f"start data is: {data[start]}")
                        if not (data[start] in ALPHANUMERIC) and data[index] in ALPHANUMERIC:
                            #DEBUG print("Setting start")
                            start = index
                        elif data[start] in ALPHANUMERIC and not data[index] in ALPHANUMERIC:
                            #DEBUG print("Adding token\n")
                            #Checking if there was leftOver chars that are continous
                            #Appending is O(1), but creating the substring/token to append is O(s)
                            # where s = the size of the substring/token.
                            #In the worst case scenario we may have a token that is n chars long so
                            # this is O(n).
                            if leftOver:
                                tokens.append(leftOver + data[start:index])
                                leftOver = ""
                            else:
                                tokens.append(data[start:index])
                            start = index
                    #Checks if index == start (if not then we have a word that may continue)
                    if data[index] in ALPHANUMERIC:
                        leftOver += data[start: index+1]
    except UnicodeDecodeError:
        print("ERROR: Program can only tokenize a text file (.txt).")
        return -1
    except FileNotFoundError:
        print("ERROR: Program was unable to find the file:", textFilePath)
        return -1
    if leftOver:
        tokens.append(leftOver)
    #DEBUG print(tokens)
    return tokens


#Time Complexity = O(t)
def computeWordFrequencies(tokens: '[str]') -> "dict(str, int)":
    """
    The function takes in a list of strings (tokens) and returns a 
    dictioanry where keys= tokens and vals = the number of occurances of that token
    in the list.
    """
    #Initalize Dictionary to store tokens and their counts O(1)
    counts = {}

    #loop through the tokens list and increment their count in the dictionary O(t)
    # where t = the number of tokens in the list; When function is used in conjuction with tokenizer function,
    # t < n.
    # To illustrate the point above, if we wanted t = n that would there are n tokens, which is impossible.
    # Imagine we had a file with only the following string inside of it: "a a a a a".
    # From this example n = 9 and we could at most have 5 tokens, following our definition of a token.
    for token in tokens:
        if token in stop_words:
            continue
        elif token in counts:
            counts[token] += 1
        else:
            counts[token] = 1
    
    return counts

def save_file(file_name : str , object):
    with open(file_name, 'w') as file:
        file.write(json.dumps(object))

def load_file(file_name : str):
    with open(file_name, 'r') as file:
        return json.loads(file.read())

def get_lines(file_name : str):
    l = []
    with open('text_copy.txt', 'r') as f:
        for line in f:
            l.append(line.strip())
    return l

def isDate(date: str) -> bool:
    #check each format in FMTS if it 'fits' the given date
    for fmt in FMTS:
        try:
            dt.datetime.strptime(date, fmt)
            return True
        except ValueError:
            pass
    return False



def calculate_longest_page(filepath):
    longest_length = 0
    with open(filepath, "r") as file:
        for line in file:
            content = line.split(" ")
            longest_length = max(longest_length, int(content[0]))
    return longest_length
            
            
def calcualte_median_page_length(filepath):
    urls_length = []
    with open(filepath, "r") as file:
        for line in file:
            content = line.split(" ")
            urls_length.append(int(content[0]))
    print(statistics.median(urls_length))

def calculate_given_quantile(filepath, quantile):
    urls_length = []
    with open(filepath, "r") as file:
        for line in file:
            content = line.split(" ")
            urls_length.append(int(content[0]))
    percentile = np.percentile(urls_length, quantile)
    print(percentile)
    
    
def high_info(soup, resp) -> bool: # checks if page has high info or not
    page_size = len(soup.prettify())
    body = soup.body
    body = ''.join([string for string in body.stripped_strings])
    ratio = (len(body) / page_size) * 100
    print(ratio)
    return ratio > 7