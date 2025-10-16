import os
import re

TEMPLATE_PATH = "templ.py"
CONFIG_START = "# --- Configuration ---"
CONFIG_END = "# ---------------------"

# Read template
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template = f.read()

# Extract template before/after config
pre_config = template.split(CONFIG_START)[0]
post_config = template.split(CONFIG_END)[-1]

# Find all check_update.py in subfolders
base_dir = os.path.dirname(os.path.abspath(__file__))
for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)
    script_path = os.path.join(folder_path, "check_update.py")
    if os.path.isdir(folder_path) and os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Extract config block
        config_match = re.search(f"{CONFIG_START}(.*?){CONFIG_END}", content, re.DOTALL)
        if config_match:
            config_block = config_match.group(0)
            # Build new file
            new_content = pre_config + config_block + post_config
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated: {script_path}")
        else:
            print(f"Skipped (no config block): {script_path}")
print("All done.")
