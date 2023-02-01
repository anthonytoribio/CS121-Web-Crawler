import json
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

# def computeWordFrequencies(token_list):
#     token_dict = {}
#     for token in token_list:
#         if token.lower() in token_dict: # Adding tokens into a map
#             token_dict[token.lower()] += 1
#         else:
#             token_dict[token.lower()] = 1
#     return token_dict


import sys

ALPHANUMERIC = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1",
    "2", "3", "4", "5", "6", "7", "8", "9", "0"}

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
        if token in counts:
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