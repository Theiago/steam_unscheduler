import re
import winreg
from pathlib import Path

STEAM_REGISTRY_KEYS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam", "SteamPath"),
]

# Matches lines like: "path"		"E:\\SteamLibrary"
LIBRARY_PATH_PATTERN = re.compile(r'^\s*"path"\s+"(?P<path>[^"]+)"', re.MULTILINE)


def get_steam_install_path() -> Path:
    """Get the Steam install path from the Windows Registry."""
    for hive, key_path, value_name in STEAM_REGISTRY_KEYS:
        try:
            with winreg.OpenKey(hive, key_path) as key:
                return Path(winreg.QueryValueEx(key, value_name)[0])
        except OSError:
            continue

    raise FileNotFoundError("Steam installation not found in the Windows Registry.")


def get_steam_libraries() -> list[Path]:
    """Return the "steamapps" folder of every existing Steam library."""
    library_folders = get_steam_install_path() / "config" / "libraryfolders.vdf"
    content = library_folders.read_text(encoding="utf-8")

    libraries = []
    for match in LIBRARY_PATH_PATTERN.finditer(content):
        # The vdf file escapes backslashes ("E:\\SteamLibrary")
        directory = match["path"].replace("\\\\", "\\")
        library = Path(directory) / "steamapps"

        # Skip libraries that no longer exist (removed drive/folder)
        if library.is_dir():
            libraries.append(library)

    return libraries
