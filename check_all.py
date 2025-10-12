import os
import subprocess
import sys
import time
from datetime import datetime

TARGET_SCRIPT_NAME = "check_update.py"

class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GRAY = "\033[90m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

BANNER = f"""{Colors.CYAN}
 ▄█       ▄██   ▄    ▄████████    ▄████████ ███▄▄▄▄        ███    █▄   ▄████████ 
███       ███   ██▄ ███    ███   ███    ███ ███▀▀▀██▄      ███    ███ ███    ███ 
███       ███▄▄▄███ ███    █▀    ███    ███ ███   ███      ███    ███ ███    █▀  
███       ▀▀▀▀▀▀███ ███          ███    ███ ███   ███      ███    ███ ███        
███       ▄██   ███ ███        ▀███████████ ███   ███      ███    ███ ███        
███       ███   ███ ███    █▄    ███    ███ ███   ███      ███    ███ ███    █▄  
███▌    ▄ ███   ███ ███    ███   ███    ███ ███   ███      ███    ███ ███    ███ 
█████▄▄██  ▀█████▀  ████████▀    ███    █▀   ▀█   █▀       ████████▀  ████████▀  
▀                                                                                 
{Colors.RESET}"""

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner_with_bar(progress, total, bar_length=30):
    """Prints the banner with an updating loading bar."""
    clear_console()
    print(BANNER)
    print(f"{Colors.GRAY}Fetching update statuses...{Colors.RESET}\n")
    filled_length = int(bar_length * progress / total)
    filled = "█" * filled_length
    empty = "░" * (bar_length - filled_length)
    percent = int((progress / total) * 100)
    print(f"{Colors.CYAN}[{filled}{empty}] {percent}%{Colors.RESET}\n")

def run_update_scripts():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results = []

    # Get all subdirectories with at least one .py script and check_update.py file
    folders = [
        f for f in sorted(os.listdir(current_dir))
        if os.path.isdir(os.path.join(current_dir, f))
        and any(fn.endswith(".py") for fn in os.listdir(os.path.join(current_dir, f)))
        and os.path.exists(os.path.join(current_dir, f, TARGET_SCRIPT_NAME))
    ]

    total = len(folders)
    total_latest = total_outdated = total_errors = 0

    # --- Live loading while checking ---
    for i, folder in enumerate(folders, start=1):
        print_banner_with_bar(i - 1, total if total else 1)
        print(f"{Colors.GRAY}Checking:{Colors.RESET} {folder}")
        sys.stdout.flush()

        path = os.path.join(current_dir, folder)
        try:
            result = subprocess.run(
                [sys.executable, TARGET_SCRIPT_NAME],
                cwd=path,
                text=True,
                capture_output=True,
                encoding="utf-8"
            )

            output = result.stdout.strip() or "LATEST"

            if "OUTDATED" in output.upper():
                color = Colors.YELLOW
                total_outdated += 1
            elif "ERROR" in output.upper() or result.returncode != 0:
                color = Colors.RED
                total_errors += 1
            elif "LATEST" in output.upper():
                color = Colors.GREEN
                total_latest += 1
            else:
                color = Colors.GRAY

            results.append(f"{folder} |{color}{output}{Colors.RESET}|")

        except Exception as e:
            results.append(f"{folder} |{Colors.RED}ERROR: {e}{Colors.RESET}|")
            total_errors += 1

        # Small delay for smoother visuals
        time.sleep(0.1)

    # Final 100% bar
    print_banner_with_bar(total, total if total else 1)
    time.sleep(0.3)

    # --- Display final result ---
    clear_console()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(BANNER)
    print(f"{Colors.GRAY}Check Time:{Colors.RESET} {Colors.CYAN}{now}{Colors.RESET}")
    print(f"{Colors.GRAY}Python Version:{Colors.RESET} {sys.version.split()[0]}")
    print(f"{Colors.GRAY}Checked:{Colors.RESET} {total} mod(s)\n")

    for line in results:
        print(line)

    print("\n" + "-" * 60)
    print(f"{Colors.GREEN}Latest:{Colors.RESET} {total_latest}  |  "
          f"{Colors.YELLOW}Outdated:{Colors.RESET} {total_outdated}  |  "
          f"{Colors.RED}Errors:{Colors.RESET} {total_errors}")
    print("-" * 60)
    print(f"\n{Colors.GRAY}Press Enter to exit...{Colors.RESET}")

    try:
        input()
    except EOFError:
        pass

if __name__ == "__main__":
    run_update_scripts()
