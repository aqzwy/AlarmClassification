def string_to_txt(string,file_name):
    file = open(file_name , 'w+')
    file.write(string)
    file.close()
    print("write:",file_name,string)