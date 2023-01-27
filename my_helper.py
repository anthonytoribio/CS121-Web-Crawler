def write_to_end(file_name, url):
    file = open(file_name, 'a')
    file.write(url + "\n")
    file.close()