from os import listdir
from folders import steam_libraries

for library in steam_libraries:
    files_list = listdir(library)
    
    for file in files_list:
        if file.startswith("appmanifest"):
            path = library + "\\" + file
            f = open(path, "r")
            line = f.readlines()
            if len(line) > 10:
                line[19] = '\t"AutoUpdateBehavior"\t\t"2"\n'
                with open(file, "w") as file:
                    file.writelines(line)