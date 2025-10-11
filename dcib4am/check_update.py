import requests
import os

# --- Configuration ---
REMOTE_URL = "http://panelofdcibx4am911.x10.mx/DCIBX4AM/libdcibx4amVIP.so"
LOCAL_FILE = "lib123.so"
# ---------------------

def get_remote_file_size(url):
    """Gets the Content-Length of a file using a HEAD request."""
    try:
        # Send a HEAD request to get just the header information
        response = requests.head(url, allow_redirects=True, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes

        # Get the size from the 'Content-Length' header
        content_length = response.headers.get('content-length')
        if content_length:
            return int(content_length)
        
        print("Warning: Remote server did not provide a Content-Length header. Cannot compare size.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error accessing remote file: {e}")
        return None

def get_local_file_size(filepath):
    """Gets the size of a local file in bytes."""
    if os.path.exists(filepath):
        return os.path.getsize(filepath)
    return None

def download_file(url, filepath):
    """Downloads a file from a URL and saves it to a path."""
    print(f"Downloading latest update to {filepath}...")
    try:
        # Stream the download
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error during download: {e}")
        return False

def check_for_update():
    """Main function to check and download the update."""
    local_size = get_local_file_size(LOCAL_FILE)
    remote_size = get_remote_file_size(REMOTE_URL)

    if remote_size is None:
        print("Update check failed due to remote file error.")
        return

    print(f"Current local size of '{LOCAL_FILE}': {local_size if local_size is not None else 'N/A'} bytes")
    print(f"Latest remote size: {remote_size} bytes")

    if local_size is None or local_size != remote_size:
        print("\nThere's a new update!")
        download_file(REMOTE_URL, LOCAL_FILE)
    else:
        print("\nFile sizes match. No update needed.")

if __name__ == "__main__":
    check_for_update()
    
    # --- PAUSE AT THE END ---
    print("\nPress Enter to exit...")
    input()