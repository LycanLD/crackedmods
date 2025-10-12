import requests
import os
import sys

# --- Configuration ---
REMOTE_URL = "https://pidrumodz.x10.mx/OnlineLibZek/libpidru.so"
LOCAL_FILE = "lib123.so"
# ---------------------

def get_remote_file_size(url):
    """Gets the Content-Length of a file using a HEAD request."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        response.raise_for_status()
        content_length = response.headers.get('content-length')
        return int(content_length) if content_length else None
    except requests.exceptions.RequestException:
        return None

def get_local_file_size(filepath):
    """Gets the size of a local file in bytes."""
    if os.path.exists(filepath):
        return os.path.getsize(filepath)
    return None

def download_file(url, filepath):
    """Downloads a file from a URL and saves it to a path."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.exceptions.RequestException:
        return False

def check_for_update():
    """Main function to check and download the update."""
    local_size = get_local_file_size(LOCAL_FILE)
    remote_size = get_remote_file_size(REMOTE_URL)

    if remote_size is None:
        print("ERROR - Remote file inaccessible")
        sys.exit(1)

    if local_size is None or local_size != remote_size:
        # Update needed
        if download_file(REMOTE_URL, LOCAL_FILE):
            print("OUTDATED - Lib Downloaded")
        else:
            print("ERROR - Download Failed")
            sys.exit(1)
    else:
        print("LATEST")

if __name__ == "__main__":
    check_for_update()
