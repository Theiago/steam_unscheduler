f = open("C:\Program Files (x86)\Steam\config\libraryfolders.vdf", "r")
steam_config = f.readlines()
steam_libraries = []

for line in steam_config:
    if line.startswith("\t\t\"path\""):
        directory = line.split("\"")[3] + "\steamapps"
        steam_libraries.append(directory)