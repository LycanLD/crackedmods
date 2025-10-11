import os
import subprocess
import sys

# The name of the script we are looking for in each subdirectory
TARGET_SCRIPT_NAME = "check_update.py"

def run_update_scripts():
    """
    Checks all immediate subdirectories for the target script and runs it.
    """
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Iterate through all items in the current directory
    for item in os.listdir(current_dir):
        # Construct the full path to the item
        path = os.path.join(current_dir, item)
        
        # 1. Check if the item is a directory
        if os.path.isdir(path):
            print("-" * 50)
            print(f"Checking directory: {item}")
            
            # Construct the full path to the target script inside the subdirectory
            target_script_path = os.path.join(path, TARGET_SCRIPT_NAME)
            
            # 2. Check if the target script exists in that directory
            if os.path.exists(target_script_path):
                print(f"Found {TARGET_SCRIPT_NAME}. Running update check...")
                
                # --- Execution Command ---
                # We use 'subprocess.run' to execute the script in the terminal.
                # 'cwd=path' ensures the script runs from its own directory,
                # which is crucial for it to find 'lib123.so' locally.
                # 'capture_output=False' lets the output print directly to the console.
                try:
                    # The command to run: python <script_path>
                    command = [sys.executable, target_script_path]
                    
                    # Execute the command
                    result = subprocess.run(
                        command, 
                        cwd=path, 
                        check=True,  # Raise an exception for non-zero exit codes
                        text=True,
                        encoding='utf-8'
                    )
                    print(f"Script finished successfully in {item}")
                
                except subprocess.CalledProcessError as e:
                    print(f"ERROR: Script failed in {item} with code {e.returncode}")
                    # You could print e.stderr here if you captured output
                except FileNotFoundError:
                    print(f"ERROR: Python executable not found to run script in {item}.")
                
            else:
                print(f"'{TARGET_SCRIPT_NAME}' not found in {item}. Skipping.")
    
    print("-" * 50)
    print("All directories checked.")


if __name__ == "__main__":
    run_update_scripts()
    
    # Pause at the end
    print("\nPress Enter to exit the main runner script...")
    input()