def list_to_txt(list,file_name):
    file = open(file_name, 'w+')
    for keywords in list:
        file.write(keywords + " ")
    file.close()