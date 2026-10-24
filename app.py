import os
import re
from pathlib import Path

from folders import get_steam_libraries

HIGH_PRIORITY = "2"
UPDATE_BEHAVIORS = {
    "0": "Always keep updated",
    "1": "Only update on launch",
    "2": "High priority",
}

AUTO_UPDATE_PATTERN = re.compile(r'^(\s*"AutoUpdateBehavior"\s+)"(?P<value>\d+)"', re.MULTILINE)
NAME_PATTERN = re.compile(r'^\s*"name"\s+"(?P<name>[^"]*)"', re.MULTILINE)

# ANSI colors
GREEN, YELLOW, RED, DIM, BOLD, RESET = "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"


def set_high_priority_update_behavior(appmanifest: Path) -> str | None:
    """Set "AutoUpdateBehavior" to high priority. Return the previous value if the file changed."""
    content = appmanifest.read_text(encoding="utf-8")
    match = AUTO_UPDATE_PATTERN.search(content)

    if not match or match["value"] == HIGH_PRIORITY:
        return None

    new_content = AUTO_UPDATE_PATTERN.sub(rf'\1"{HIGH_PRIORITY}"', content, count=1)
    appmanifest.write_text(new_content, encoding="utf-8")
    return match["value"]


def get_game_name(appmanifest: Path) -> str:
    match = NAME_PATTERN.search(appmanifest.read_text(encoding="utf-8"))
    return match["name"] if match else appmanifest.name


def describe_behavior(value: str) -> str:
    return UPDATE_BEHAVIORS.get(value, f"Unknown ({value})")


def main() -> None:
    print(f"{BOLD}Steam Unscheduler{RESET}")
    print("=" * 40)

    libraries = get_steam_libraries()
    updated, unchanged, failed = 0, 0, 0

    for library in libraries:
        manifests = sorted(library.glob("appmanifest_*.acf"))
        print(f"\n{BOLD}{library}{RESET} {DIM}({len(manifests)} games){RESET}")

        for manifest in manifests:
            try:
                name = get_game_name(manifest)
                previous = set_high_priority_update_behavior(manifest)
            except OSError as error:
                failed += 1
                print(f"  {RED}✘ {manifest.name}: {error}{RESET}")
                continue

            if previous is None:
                unchanged += 1
                print(f"  {DIM}· {name}{RESET}")
            else:
                updated += 1
                print(
                    f"  {GREEN}✔ {name}{RESET} "
                    f"{YELLOW}{describe_behavior(previous)}{RESET} → {GREEN}{describe_behavior(HIGH_PRIORITY)}{RESET}"
                )

    print("\n" + "=" * 40)
    print(f"{GREEN}{updated} updated{RESET}, {DIM}{unchanged} already high priority{RESET}", end="")
    print(f", {RED}{failed} failed{RESET}" if failed else "")
    print(f"{len(libraries)} libraries scanned")


if __name__ == "__main__":
    os.system("")  # Enable ANSI colors on the Windows console

    try:
        main()
    except Exception as error:
        print(f"\n{RED}Error: {error}{RESET}")

    input("\nPress Enter to exit...")
