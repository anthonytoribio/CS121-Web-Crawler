
def write_to_end(file_name, url):   
    file = open(file_name, 'a+')
    file.write(url + "\n")
    file.close()
    

def copy_page(file_name : str, lines : list):
    file = open(file_name, "w")
    for line in lines:
        file.write(line)
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