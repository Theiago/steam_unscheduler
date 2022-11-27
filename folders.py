import winreg

install_path = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam"), "InstallPath")[0] + "\config\libraryfolders.vdf"

f = open(install_path, "r")
steam_config = f.readlines()
steam_libraries = []

for line in steam_config:
    if line.startswith("\t\t\"path\""):
        directory = line.split("\"")[3] + "\steamapps"
        steam_libraries.append(directory)
