import winreg
import os


def get_steam_libraries():
    # Get the Steam install path in the Windows Registers
    steam_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
    install_path = os.path.join(winreg.QueryValueEx(steam_key, "InstallPath")[0], "config", "libraryfolders.vdf")

    with open(install_path, "r") as f:
        steam_config = f.readlines()

    steam_libraries = []

    # Change the priority to high
    for line in steam_config:
        if line.startswith("\t\t\"path\""):
            directory = line.split("\"")[3]
            steam_libraries.append(os.path.join(directory, "steamapps"))

    return steam_libraries

steam_libraries = get_steam_libraries()