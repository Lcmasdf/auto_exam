import codecs

#read data from utf8 file , detect BOM and ignore it
def read_from_utf8(path):
    with open(path,'r',encoding='UTF-8') as file:
        data = file.read()
        if codecs.BOM_UTF8.decode('utf-8') == data[0]:
            data = data[1:]
        file.close()
    return data