import requests
import os
import sys
import tempfile
import webbrowser
from PySide6.QtWidgets import QMessageBox
import subprocess
import shutil
from version import __version__ as APP_VERSION



# Replace with your actual GitHub username and repo
GITHUB_USERNAME = "kunalnaidu0"
GITHUB_REPO = "document-management"

# GitHub URLs
VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/main/version.txt"
DOWNLOAD_URL = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}/releases/latest/download/DocumentManager.exe"

def check_for_update(): 
    """
    Check if a new version is available on GitHub.
    Returns:
        bool: True if an update is available, False otherwise.
        str: The latest version if available, None otherwise.
    """

    try:
        response = requests.get(VERSION_URL, timeout=5)
        # Check if the request was successful
        if response.status_code == 200:
            latest_version = response.text.strip()
            if latest_version != APP_VERSION:
                return True, latest_version
    except Exception as e:
        print("Error checking for update:", e)
    return False, None


def download_update():
    """
    Download the latest update from GitHub.
    Returns:
        str: The path to the downloaded update file, or None if the download failed.
    """

    try:
        print("Downloading update...")
        response = requests.get(DOWNLOAD_URL, stream=True, timeout=10)
        # Check if the request was successful
        if response.status_code == 200:
            # Create a temp folder to store the downloaded file
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, "myapp_update.exe")
            with open(file_path, "wb") as f:
                # Write the content of the response to a file in chunks so whole file is not loaded into memory
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Update downloaded to: {file_path}")
            return file_path
        else:
            print("Failed to download update.")
    except Exception as e:
        print("Error downloading update:", e)
    return None

def launch_update(downloaded_file):
    """
    Launch a separate Python updater to replace the current executable.
    """
    current_exe = sys.argv[0]
    update_script = os.path.join(os.path.dirname(current_exe), "update_runner.py")

    subprocess.Popen([
        sys.executable, update_script, current_exe, downloaded_file
    ])
    sys.exit()

# test function
def prompt_and_update():
    """
    Prompt the user to check for updates and handle the update process.
    """
    should_update, new_version = check_for_update()
    if should_update:
        print(f"New version {new_version} available.")
        user_input = input("Do you want to download and install it now? (y/n): ").strip().lower()
        if user_input == "y":
            file_path = download_update()
            if file_path:
                print("Launching updater...")
                launch_update(file_path)
            else:
                print("Update failed.")
        else:
            print("Update skipped.")
    else:
        print("You have the latest version.")

if __name__ == "__main__":
    prompt_and_update()
