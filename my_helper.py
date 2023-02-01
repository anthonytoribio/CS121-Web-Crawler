
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

def computeWordFrequencies(token_list):
    token_dict = {}
    for token in token_list:
        if token.lower() in token_dict: # Adding tokens into a map
            token_dict[token.lower()] += 1
        else:
            token_dict[token.lower()] = 1
    return token_dict