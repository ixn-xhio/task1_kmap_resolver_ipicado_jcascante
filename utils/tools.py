import os

#lambda limpia pantalla
clear = lambda: os.system('cls')

#lee texto de archivo
def readTextFile(path_to_file): 
    with open(path_to_file, "r") as f:
        contents = f.readlines()
        return contents[0]
        