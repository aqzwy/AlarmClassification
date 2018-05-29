def list_to_txt(list,file_name):
    file = open(file_name, 'w+')
    for keyword in list:
        file.write(keyword + " ")
    file.close()